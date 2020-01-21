from multiprocessing.shared_memory import SharedMemory 
from multiprocessing import Process, Pipe, Lock, cpu_count
from .Worker import Horse
from .util import *

import numpy as np

class SpaceColony:
    def __init__(self,  points, roots=np.zeros((1,3)), 
                        parameters=Param(r=0.04, iD=0.5, kD=0.2, bias=np.zeros(3)), 
                        trunk_lim=1, min_activation=5, maxsize=100000,  ncpu=cpu_count()):

        # Static information
        self.par = parameters
        self.ncpu = ncpu
        self.min_activation = min_activation
        self.trunk_lim = trunk_lim
        self.maxsize = maxsize

        self.nroots = len(roots)

        # Dynamic information
        self.age = 0
        self.start = 0
        self.end = 1
        self.done = False
        self.trunk_mode = True

        self.activation = 0
        self.reached_points = 0
        self.stats = []

        
        # Local dynamics
        self.edges = []
        self.children = [[] for _ in range(maxsize)]
        self.w = []
        
        # This array is sliced at start:
        self.points = points
        
        # This is sparta.
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


    def iterate(self, N):
        for i in range(N):
            self.update_stats()
            if self.done:
                break
                
            for pipe in self.pipes:
                pipe.send(Batch(True, 1, (self.start, self.end, self.trunk_mode)))

            result_list = [pipe.recv() for pipe in self.pipes]           
            res = self.collect(result_list)
            self.grow(res)
            self.done_yet()

    def stop(self):
        for pipe in self.pipes:
            pipe.send(Batch(False, 1, (None,)))
        for w in self.workers:
            w.join()

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
                self.done = True
                return
            self.nodes[self.end] = self.nodes[i] + normalize(self.vectors[i] + self.par.bias)*self.par.r
            self.children[i].append(self.end)
            self.vectors[i] = np.zeros(3)
            self.end += 1
        self.age += 1

    def done_yet(self):
        if self.done:
            return True

        if self.trunk_mode:
            self.trunk_mode = self.activation <= self.min_activation + self.trunk_lim
            if self.trunk_mode:
                return False

        if self.activation < self.min_activation:
            self.done = True
            return True
        return False
    
    def walk(self):
        self.w = np.ones(self.maxsize)
        self.edges = []
        for i in range(self.nroots):
            self._walk(i)
            
    def _walk(self, i):
        w = self.w[i]
        for j in self.children[i]:
            self.edges.append((i,j))
            w += self._walk(j)**2
        
        w = np.sqrt(w)
        self.w[i] = w
        return w
            

    def pack(self, points, pipe):
        return points, self.par.iD, self.par.kD, self.vectors_sm.name, self.tree_sm.name, self.maxsize, pipe, self.lock
    
    def update_stats(self):
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

        return f'{self.end} nodes, {self.age} iterations \n\
                {self.activation}/{len(self.points) - self.reached_points} active points \n\
                {len(self.points)} points on {nproc}/{self.ncpu} processes \n\
                avg. branching: {leaves/(len(self.edges)+1)} \n\
                {self.par}'

    def __del__(self):
        self.stop()
        self.vectors_sm.close()
        self.vectors_sm.unlink()
        self.tree_sm.close()
        self.tree_sm.unlink()
        
        


