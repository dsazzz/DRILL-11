from pico2d import *
import random
import transitions
from grass import Grass
from boy import Boy


# Game object class here



def handle_events():
    global running

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_SPACE:
                boy.handle_input('SPACE', True)
            elif event.key == SDLK_a:
                boy.handle_input('A', True)
            elif event.key == SDLK_LEFT:
                boy.handle_input('LEFT', True)
            elif event.key == SDLK_RIGHT:
                boy.handle_input('RIGHT', True)
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_LEFT:
                boy.handle_input('LEFT', False)
            elif event.key == SDLK_RIGHT:
                boy.handle_input('RIGHT', False)


def reset_world():
    global world
    global boy

    world = []

    grass = Grass()
    world.append(grass)

    boy = Boy()
    world.append(boy)



def update_world():
    for o in world:
        o.update()
    pass


def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()


running = True

open_canvas()
reset_world()
# game loop
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)
# finalization code
close_canvas()
