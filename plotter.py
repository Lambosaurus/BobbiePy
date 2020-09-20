import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import threading


class Plotter(threading.Thread):
    def __init__(self, length, limits = (0,1)):
        super().__init__()
        self.length = length
        self.value = None
        self.limits = limits
        self.y = [0] * self.length
        self.x = list(range(0, self.length))
        self.interval = 50

    def run(self):
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        ax.set_ylim(self.limits)
        self.line, = ax.plot(self.x, self.y)

        # Set up plot to call animate() function periodically
        ani = animation.FuncAnimation(fig,
            self.__animate,
            interval=self.interval,
            blit=True)
        plt.show()

    def __pop(self):
        while self.value == None:
            time.sleep(0.01)
        v = self.value
        self.value = None
        return v

    def __animate(self, _):
        y = self.__pop()
        self.y.append(y)
        self.y = self.y[-self.length:]
        self.line.set_ydata(self.y)
        return self.line,

    def update(self, value):
        self.value = value

