
import time

import pygame as pg

pg.init()
pg.mixer.init()  # Inicializa o mixer do Pygame

pg.mixer.music.load('./assets/BlueSpacev0_8.mp3')
pg.mixer.music.play(-1)
time.sleep(2)
pg.mixer.music.stop()

# Reproduz o áudio
soundtrack.play()
