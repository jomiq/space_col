from multiprocessing.shared_memory import SharedMemory 
from multiprocessing import Process, Pipe, Lock, cpu_count
from .Worker import Horse
from .util import *

import numpy as np

import logging
import sys
from time import time
log = logging.getLogger('SCA')
out_hdlr = logging.StreamHandler(sys.stdout)
out_hdlr.setFormatter(logging.Formatter('%(name)s:%(levelname)s:: %(message)s'))
out_hdlr.setLevel(logging.DEBUG)
log.addHandler(out_hdlr)
log.setLevel(logging.DEBUG)

class SpaceColony:
    def __init__(self,  points, roots=np.zeros((1,3)), 
                        r=0.04, iD=0.5, kD=0.2, bias=np.zeros(3), 
                        trunk_lim=1, min_activation=5, yeet_condition=5, 
                        maxsize=100000,  ncpu=cpu_count(),
                        log_stats=True, compute_mode=1):

        # Static information
        self.r = r
        self.iD = iD
        self.kD = kD
        self.bias = bias

        self.trunk_lim = trunk_lim
        self.min_activation = min_activation
        self.yeet_condition = yeet_condition
        
        self.maxsize = maxsize
        self.ncpu = ncpu

        self.nroots = len(roots)
        self.log_stats = log_stats
        self.compute_mode = compute_mode

        # Dynamic information
        self.age = 0
        self.start = 0
        self.end = len(roots)
        self.done = False
        self.trunk_mode = True
        self.yeet_count = 0

        self.activation = 0
        self.reached_points = 0
        self.stats = []

        self.dirty = True
        
        # Local dynamics
        self.edges = []
        self.children = [[] for _ in range(maxsize)]
        self.w = []
        
        # This array is sliced at start:
        self.points = points
        
        # Multiprocess parameters
        self.lock = Lock()
        A = np.zeros((self.maxsize, 3), dtype=roots.dtype)
        
        self.vectors_sm = SharedMemory(create=True, size=A.nbytes)
        self.tree_sm = SharedMemory(create=True, size=A.nbytes)
        
        self.vectors = as_numpy_arr(A.shape, shared_obj=self.vectors_sm)
        self.vectors[:] = A[:]
        
        self.nodes = as_numpy_arr(A.shape, self.tree_sm)
        self.nodes[:] = A[:]
        for i in range(len(roots)):
            self.nodes[i] = roots[i]

        # 'Pool'
        point_slices = np.array_split(self.points, self.ncpu)
        self.workers = []
        self.pipes = []
        for i in range(self.ncpu):
            parent_pipe, child_pipe = Pipe()
            self.pipes.append(parent_pipe)
            args = self.pack(point_slices[i], child_pipe)
            self.workers.append(Horse(*args))
            self.workers[i].start()

        self.running = True


    def iterate(self, N):
        self.dirty = True
        log.info(f'START: {time()}\n{self.__str__()}')
        for i in range(N):
            self.update_stats()
            if self.done:
                break
                
            for pipe in self.pipes:
                pipe.send(Batch(True, self.compute_mode, (self.start, self.end, self.trunk_mode)))

            result_list = [pipe.recv() for pipe in self.pipes]           
            res = self.collect(result_list)
            self.grow(res)
            self.age += 1
            self.done_yet()

        log.info(f'DONE: {time()}\n{self.__str__()}')

    def stop(self):
        if not self.running:
            return

        log.info('Horse shutdown.')
        for pipe in self.pipes:
            pipe.send(Batch(False, 1, (None,)))
            pipe.close()
        
        for w in self.workers:
            w.join(1)
            w.terminate()
        self.pipes = []
        self.workers = []
        self.running = False

    def collect(self, result_list):
        self.activation = 0
        self.reached_points = 0
        result = []
        for res in result_list:
            self.activation += res[0]
            self.reached_points += res[1]
            for i in res[2]:
                if i not in result:
                    result.append(i)
        return result

    def grow(self, res):
        self.start = self.end
        for i in res:
            if self.end >= self.maxsize:
                log.info(f'{self.age} Halt condition: node vector full.')
                self.done = True
                return
            self.nodes[self.end] = self.nodes[i] + (normalize(self.vectors[i]) + self.bias)*self.r
            self.children[i].append(self.end)
            self.vectors[i] = np.zeros(3)
            self.end += 1
        

    def done_yet(self):
        if self.done:
            return True

        if self.trunk_mode:
            self.trunk_mode = self.activation <= self.trunk_lim
            if self.trunk_mode:
                return False
            else:
                log.info(f'Trunk mode disabled at {self.age} iterations.')

        if self.activation < self.min_activation:
            log.info(f'{self.age} Halt condition: activation < {self.min_activation}.')
            self.done = True
            return True

        if self.age > self.yeet_condition:
            if np.abs(self.activation - self.stats[self.age-1].act) < 3:
                self.yeet_count += 1
                if self.yeet_count >= self.yeet_condition:
                    self.end = self.stats[self.age-self.yeet_count].sz
                    
                    for i in range(self.end):
                        self.children[i] = [c for c in self.children[i] if c <= self.end-1] 

                    self.age -= self.yeet_count
                    if self.log_stats:
                        self.stats = self.stats[:self.age]
                    
                    log.info(f'{self.age} Halt condition: yeet count {self.yeet_count}.')
                    self.done = True
                    return True
            else:
                self.yeet_count = 0
                return False
        
        return False
    
    def walk(self):
        self.w = np.ones(self.maxsize)
        self.edges = []

        for i in range(self.nroots):
            self._walk(i)

        self.dirty = False
            
    def _walk(self, i):
        w = self.w[i]
        for j in self.children[i]:
            self.edges.append((i,j))
            w += self._walk(j)**2
        
        w = np.sqrt(w)
        self.w[i] = w
        return w
            

    def pack(self, points, pipe):
        iD2 = self.iD**2
        kD2 = self.kD**2
        return  (points, iD2, kD2, 
                self.vectors_sm.name, 
                self.tree_sm.name, 
                self.maxsize, 
                pipe, 
                self.lock)
    
    def update_stats(self):
        if self.log_stats:
            self.stats.append(Stats(self.end, self.activation, self.reached_points))
    
    def get_stats(self):
        return self.stats

    def __str__(self):
        nproc = 0
        for w in self.workers:
            nproc += 1 if w.is_alive() else 0

        leaves = 0
        for i in range(self.end):
            if len(self.children[i]) == 0:
                leaves += 1

        return f'{self.end} nodes, {self.age} iterations \n{self.activation}/{len(self.points) - self.reached_points} active points \nTotal {len(self.points)} points on {nproc}/{self.ncpu} processes \n{self.nroots} trees. Avg. branching: {self.nroots*leaves/(self.end+1)} \nr={self.r}, iD={self.iD}, kD={self.kD}, bias={self.bias}'

    def __del__(self):
        log.debug('Delete SpaceColony')
        self.stop()
        self.vectors_sm.close()
        self.vectors_sm.unlink()
        self.tree_sm.close()
        self.tree_sm.unlink()
        
        


