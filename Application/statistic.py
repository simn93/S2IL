import time


class Statistic:
    t = None
    act_t = None
    start_t = None
    is_start = False

    def __init__(self):
        self.t = 0
        self.act_t = time.time()

    def start_time(self):
        if not self.is_start:
            self.start_t = time.time()
            self.is_start = True

    def stop_time(self):
        if self.is_start:
            self.t += time.time() - self.start_t
        self.is_start = False

    def refresh_time(self):
        self.t = 0

    def get_time_from_activation(self):
        return int(time.time() - self.act_t)

    def get_time(self):
        if self.is_start:
            return int(self.t + time.time() - self.start_t)
        else:
            return int(self.t)
