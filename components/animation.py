from time import time


class Animation:
    def __init__(self, func, t=1, on_finished=None):
        self.going_up = False
        self.going_down = False
        self.elapsed = 0
        self.t = t
        self.func = func
        self.last_call = None
        self.on_finished = on_finished

    def reset(self):
        self.last_call = None
        self.going_up = False
        self.going_down = False
        self.elapsed = 0

    @property
    def value(self):
        if self.last_call is None:
            self.last_call = time()

        if self.going_up:
            self.elapsed += time() - self.last_call
            if self.elapsed >= self.t:
                self.elapsed = self.t
                self.going_up = False
                if self.on_finished:
                    self.on_finished(self)
            self.last_call = time()

        if self.going_down:
            self.elapsed -= time() - self.last_call
            if self.elapsed <= 0:
                self.elapsed = 0
                self.going_down = False
            self.last_call = time()

        return self.func(self.elapsed)
