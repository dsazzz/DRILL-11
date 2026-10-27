from pico2d import load_image
from transitions import Machine
import math
import time


class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.face_dir = 1
        self.pressed_directions = set()
        self.image = load_image('animation_sheet.png')
        self.last_input_time = time.time()
        self.machine = Machine(
            model=self,
            states=['IDLE', 'RUN', 'SLEEP'],
            initial='IDLE',
            auto_transitions=False,
        )
        self.machine.add_transition('start_run', ['IDLE', 'SLEEP'], 'RUN')
        self.machine.add_transition('stop_run', 'RUN', 'IDLE')
        self.machine.add_transition('sleep', 'IDLE', 'SLEEP')
        self.machine.add_transition('wake_up', 'SLEEP', 'IDLE')

    def handle_input(self, key, pressed=True):
        self.last_input_time = time.time()
        if key in ('LEFT', 'RIGHT'):
            if pressed:
                self.pressed_directions.add(key)
                self.face_dir = -1 if key == 'LEFT' else 1
                if self.state == 'SLEEP':
                    self.wake_up()
                if self.state != 'RUN':
                    self.start_run()
            else:
                self.pressed_directions.discard(key)
                if self.pressed_directions:
                    direction = next(iter(self.pressed_directions))
                    self.face_dir = -1 if direction == 'LEFT' else 1
                elif self.state == 'RUN':
                    self.stop_run()
        elif key == 'SPACE' and pressed and self.state == 'SLEEP':
            self.wake_up()

    def update(self):
        if self.state == 'IDLE' and time.time() - self.last_input_time >= 3:
            self.sleep()
        elif self.state == 'IDLE':
            self.frame = (self.frame + 1) % 8
        elif self.state == 'RUN':
            self.x += self.face_dir * 5
            self.x = max(50, min(750, self.x))
            self.frame = (self.frame + 1) % 8
        elif self.state == 'SLEEP':
            self.frame = 0

    def draw(self):
        if self.state == 'SLEEP':
            self.image.clip_composite_draw(
                0, 300, 100, 100, math.pi / 2, '', self.x, self.y - 30, 100, 100
            )
            return

        if self.state == 'RUN':
            bottom = 100 if self.face_dir == 1 else 0
            self.image.clip_draw(self.frame * 100, bottom, 100, 100, self.x, self.y)
        elif self.face_dir == 1:
            self.image.clip_draw(self.frame * 100, 300, 100, 100, self.x, self.y)
        else:
            self.image.clip_draw(self.frame * 100, 200, 100, 100, self.x, self.y)