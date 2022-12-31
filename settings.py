import random

import pygame as pg

FPS = 0
FIELD_COLOR = (200, 200, 200)

TILE_SIZE = 50
FIELD_SIZE = FIELD_W, FIELD_H = 10, 20
FIELD_RES = FIELD_W * TILE_SIZE, FIELD_H * TILE_SIZE
frame_duration = 50
explosion_settings = {
    'width': 32,
    'height': 32
}

enemies = {
    1: 'enemy1',
    2: 'enemy2',
    3: 'enemy3',
}

stages = [
    {
        'background': {
            'image': './assets/space_bg.png',
            'image_count': 3,
            'speed': 0.5
        },
        'menu': {
            'backgeound': ''
        }
    }
]

ships_settings = {
    'player': {
        'image_x': 0,
        'image_y': 0,
        'width': 32,
        'height': 32,
        'lives': 5,
        'energy': 10,
        'speed': 0.3,
        'images': 4,
        'image_path': './assets/spritesheet.png'
    },

    'enemy1': {
        'image_x': 0,
        'image_y': 160,
        'width': 32,
        'height': 32,
        'energy': 1,
        'speed': 0.3,
        'images': 4,
        'image_path': './assets/spritesheet.png',
        'can_shoot': True,
    },

    'enemy2': {
        'image_x': 0,
        'image_y': 128,
        'width': 16,
        'height': 25,
        'energy': 3,
        'speed': 0.1,
        'images': 4,
        'image_path': './assets/spritesheet.png',
        'energy': 1,
        'can_shoot': True,
    },

    'enemy3': {
        'image_x': 64,
        'image_y': 128,
        'width': 32,
        'height': 30,
        'energy': 5,
        'speed': 0.1,
        'images': 3,
        'image_path': './assets/spritesheet.png',
        'can_shoot': True,
    },


}
