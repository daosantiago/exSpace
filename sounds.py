import pygame

FILES = {
    'menu': './assets/sound/Planetrise_LEO.wav',
    'play': './assets/sound/background.wav',
    'shoot': './assets/sound/tiro.wav',
    'explode': './assets/sound/explosion.wav'
}


class Sound():
    def __init__(self, song) -> None:
        self.__sound = pygame.mixer.Sound(FILES[song])
        self.__sound.set_volume(0.1)
        self.__loop = -1 if song == 'play' else 0

    def play(self):
        self.__sound.play(self.__loop)

    def stop(self):
        self.__sound.stop()
