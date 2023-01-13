import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import Rectangle, Color, Ellipse
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
import numpy as np

import threading
import queue

from uart_source import serial_receive


q = queue.Queue()
PORT = "/dev/ttyACM0"

SPACE_SIZE_X = 4.5
SPACE_SIZE_Y = 5.0

class MyLayout(BoxLayout):
    def __init__(self, data_source=None, **kwargs):
        super().__init__(**kwargs)

    def update(self, *args):
        self.update_view()

    def update_view(self):
        pass


class Agent(Widget):
    def __init__(self, pos, size, **kwargs):
        super().__init__(**kwargs)
        self.width = size[0]
        self.height = size[1]
        x = pos[0] - self.width/2
        y = pos[1] - self.height/2
        self.circle = Ellipse(pos=(x, y), size=(self.width, self.height))

        with self.canvas:
            Color(0.9, 0.2, 0.2, 0.7, mode="rgba")
            self.canvas.add(self.circle)

    def move_to(self, pos):
        #print(pos)
        self.circle.pos = (int(pos[0]), int(pos[1]))
        #self.circle.pos = (100, 200)


class CanvasWidget(RelativeLayout):
    global q

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.agent = Agent(pos=self.pos, size=(30, 30))
        self.add_widget(self.agent)

        self.i = 0
        self.samples_count = 24
        self.buf_x = [0] * self.samples_count
        self.buf_y = [0] * self.samples_count

        Clock.schedule_interval(self.update, 1.0/5.0)

    def update(self, *args):
        try:
            while not q.empty():
                data = q.get(block=False)
                if len(data) == 3:
                    self.buf_x[self.i] = data[0]
                    self.buf_y[self.i] = data[1]

                    data_avg = [0] * 2

                    data_avg[0] = sum(self.buf_x) / self.samples_count
                    data_avg[1] = sum(self.buf_y) / self.samples_count
                    x = (data_avg[0] / SPACE_SIZE_X) * self.size[0]
                    y = (data_avg[1] / SPACE_SIZE_Y) * self.size[1]

                    self.agent.move_to((x, y))

                    self.i += 1
                    if self.i >= self.samples_count:
                        self.i = 0
        except queue.Empty:
            pass


class MainApp(App):
    global q
    
    def build(self):
        return MyLayout(q)

    def update(self, *args):
        pass


thr_recv = threading.Thread(target=serial_receive, args=(PORT, q,), daemon=True)
thr_recv.start()

MainApp().run()
