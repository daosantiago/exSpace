import pygame as pg


def blink(obj):
    current_time = pg.time.get_ticks()
    elapsed_time = current_time - obj.last_blink_time

    # Se o tempo transcorrido for maior que o tempo de exibição do quadro atual, atualize o quadro atual
    if elapsed_time > obj.blink_time:
        obj.last_blink_time = pg.time.get_ticks()
        obj.toggle = not obj.toggle

    if obj.toggle:
        for i in obj.images:
            i.image.set_alpha(100)
    else:
        for i in obj.images:
            i.image.set_alpha(255)

    return obj
