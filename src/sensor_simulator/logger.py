import matplotlib.pyplot as plt
import time

class Plotter:
    def __init__(self, interval, event, time_diff):
        self.time_axes = []
        self.value_axes = []
        self.interval = interval
        self.event = event
        self.time_diff = time_diff
        self.line = None
        self.text = None

    def update_arrays(self, t, v):
        if len(self.time_axes) > self.interval:
            self.time_axes.pop(0)
            self.value_axes.pop(0)
        self.time_axes.append(t)
        self.value_axes.append(v)

    def update_axes(self):
        if self.text: self.text.remove()
        try:
            self.text = plt.text(self.time_axes[-1], self.value_axes[-1], "{:.2f}".format(self.value_axes[-1]), fontdict=None)
        except:
            pass
        self.line.set_data(self.time_axes, self.value_axes)
        self.line.axes.relim()
        self.line.axes.autoscale_view()

    def start(self, lim, title=None, value_title=None, variables=None):
        plt.show(block=False)
        plt.title(title)
        plt.ylabel(value_title)
        plt.connect('close_event', self.stop)

        axes = plt.gca()
        axes.set_ylim(lim[0]-0.1,lim[1]+0.1)
        axes.legend()
            
        self.line, = axes.plot(self.time_axes, self.value_axes, 'r-')

    def run(self):
        while self.event.is_set():
            self.update_axes()
            plt.draw()
            plt.pause(1e-1)
            time.sleep(self.time_diff)

    def stop(self, evn):
        self.event.clear()