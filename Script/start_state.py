import my_framework

from my_engine import *
from data import *

name = "StartState"


def enter():
    global data
    open_canvas(1024, 768)
    hide_lattice()
    data = Data()

def exit():
    global data
    del(data)

    pass

def update():
    data.update()
    pass
    #delay(0.015)

def draw():
    global data
    clear_canvas()

    data.draw()

    update_canvas()


def pause(): pass


def resume(): pass

def handle_events():
    events = get_events()
    for event in events:
        if (event.type == SDL_QUIT) or (event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE):
            my_framework.quit()

        # elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE) or (event.type, event.key) == (SDL_KEYDOWN, SDLK_RETURN) :
        #     my_framework.change_state(main_state)


