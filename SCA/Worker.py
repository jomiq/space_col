from multiprocessing.shared_memory import SharedMemory
from multiprocessing import Process #, Pipe, Lock

from .util import *

# Implements iterations on a subset of the attractor.
class Horse(Process):
    def __init__(
        self,
        points,
        iD,
        kD,
        vectors_UID,
        tree_UID,
        maxsize,
        pipe,
        lock,
        distance_function=(lambda v: np.sum(v ** 2)),
        vector_function=(lambda p, n: p - n),
        square_distances=True,
    ):
        super(Horse, self).__init__()

        self.distance_function = distance_function
        self.vector_function = vector_function

        self.points = points

        if square_distances:
            self.iD = iD ** 2
            self.kD = kD ** 2
        else:
            self.iD = iD
            self.kD = kD

        self.maxsize = maxsize

        self.reached_bool = np.zeros(len(points), dtype=bool)
        self.reached_points = 0

        self.closest = np.ones(len(points), dtype=np.int)
        self.L = np.ones(len(points)) * np.inf
        self.dv = np.zeros((len(points), 3))

        self.vectors_sm = SharedMemory(name=vectors_UID)
        self.tree_sm = SharedMemory(name=tree_UID)

        self.nodes = as_numpy_arr((self.maxsize, 3), self.tree_sm)
        self.vectors = as_numpy_arr((self.maxsize, 3), self.vectors_sm)

        self.pipe = pipe
        self.lock = lock
        self.batch = None

    def run(self):
        if self.batch is None:
            self.batch = self.pipe.recv()

        while self.batch.run:
            res = self.compute(*self.batch.args)
            self.pipe.send(res)
            self.batch = self.pipe.recv()

        self.vectors_sm.close()
        self.tree_sm.close()

    def compute(self, start, end, trunk_mode):
        active_points = 0
        result = []
        for i, p in enumerate(self.points):
            if self.reached_bool[i]:
                pass
            else:
                for j in range(start, end):
                    n = self.nodes[j]
                    dv = self.vector_function(p, n)
                    L = self.distance_function(dv)

                    if L < self.kD:
                        self.reached_points += 1
                        self.reached_bool[i] = True
                        break

                    if L < self.L[i]:
                        self.closest[i] = j
                        self.L[i] = L
                        self.dv[i] = dv

                if not self.reached_bool[i]:
                    if self.L[i] < self.iD:
                        active_points += 1
                        result.append(self.closest[i])
                        self.protected_add(self.closest[i], self.dv[i], self.L[i])

                    elif trunk_mode:
                        result.append(self.closest[i])
                        self.protected_add(self.closest[i], self.dv[i], self.L[i])

        return active_points, self.reached_points, result

    def protected_add(self, node_idx, value, length):
        self.lock.acquire()
        if length < self.distance_function(self.vectors[node_idx]):
            self.vectors[node_idx] = value
        self.lock.release()