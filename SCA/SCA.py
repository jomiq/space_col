from multiprocessing import Process, Array, Lock, cpu_count

class SCA:

    def __init__(self, maxsize=10000, ncpu=cpu_count(), log_stats=True):

        self.age = 0
        self.start = 0
        self.end = 0
        self.done = False
        self.trunk_mode = True
        self.yeet_count = 0

        self.activation = 0
        self.reached_points = 0
        self.stats = []

        self.dirty = True

        self.nodes = np.zeros((maxsize, 3), dtype='float64')

        
              