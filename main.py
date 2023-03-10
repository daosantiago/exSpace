import random
import sys
import time

from pygame.locals import *

from settings import *
from ships import *
from UI import *


class Background:
    def __init__(self, game) -> None:
        self.game = game
        self.images = self.load_images()
        self.speed = stages[0]['background']['speed']

    def load_images(self) -> list:
        images = []
        for i in range(stages[0]['background']['image_count']):
            image = BackgroundImage()

            image.y = -i * image.rect.height
            images.append(image)

        return images

    def update(self):
        for image in self.images:
            image.y += self.speed

        for i in self.images:
            if i.y >= 480:
                i.y = -i.rect.height * (len(self.images) - 1)

    def draw(self):
        for image in self.images:
            self.game.screen.blit(image.image, (image.x, image.y))


class BackgroundImage():
    def __init__(self) -> None:
        self.image = pg.image.load(stages[0]['background']['image'])
        self.x = 0
        self.y = 0
        self.rect = pg.Surface.get_rect(self.image)


class GameState():
    def __init__(self, game) -> None:
        self.game = game
        self.state = 'play'

    # @property
    # def state(self):
    #     return self.__state

    # def set_state(self, state):
    #     self.__state = state


class Game:
    def __init__(self):
        pg.init()
        pg.display.set_caption('ExSpace')
        self.width, self.height = (640, 480)
        self.screen = pg.display.set_mode((self.width, self.height))
        self.clock = pg.time.Clock()
        self.background = Background(self)
        self.ships = []
        self.player = None
        self.enemies = []
        self.delta_time = 1
        self.enemy_creation_time = 3.0000
        self.last_enemie_creation = 0
        self.panel = None
        self.state = GameState(self)
        self.bg_music = Sound('play')

    def check_hits(self):
        for ship in self.ships:
            if ship.label != 'player':
                if ship.collides_with(self.player):
                    ship.die()
                    self.player.die()
                else:
                    # get a bullet if there's collision, else false
                    bullet = ship.got_shot(self.player.bullets)
                    if bullet:
                        ship.get_hit()
                        self.player.kill_bullet(bullet)
                        if ship.energy == 0:
                            self.player.make_point()

                    bullet = self.player.got_shot(ship.bullets)
                    if bullet:
                        self.player.get_hit()
                        ship.kill_bullet(bullet)

                if ship.y > self.height + ship.height:
                    self.player.get_hit()
                    self.ships.remove(ship)

    def updateShips(self):
        for ship in self.ships:
            ship.update()

    def drawShips(self):
        for ship in self.ships:
            ship.draw()

    def update(self):
        self.background.update()
        self.updateShips()
        self.panel.update()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'ExSpace - {self.clock.get_fps(): .1f}')

    def draw(self):
        self.screen.fill('black')
        self.background.draw()
        self.drawShips()
        self.panel.draw()

        pg.display.flip()

    def check_enemies(self):
        elapsed_time = time.time() - self.last_enemie_creation
        enemy_index = random.randint(1, 3)

        if elapsed_time >= self.enemy_creation_time:
            self.ships.append(Enemy(self, enemies[enemy_index]))
            self.last_enemie_creation = time.time()

            if self.enemy_creation_time > 1:
                self.enemy_creation_time -= 0.1

    def check_events(self):
        self.check_enemies()
        self.check_hits()

        if self.player.energy == 0 and self.player.lives == 0:
            self.state = 'gameover'

        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            # if event.type == pg.KEYDOWN and (event.key == pg.K_UP or event.key == pg.K_DOWN or event.key == pg.K_LEFT or event.key == pg.K_RIGHT):
            if event.type == pg.KEYDOWN and (event.key == pg.K_DELETE):
                self.state = 'gameover'

    def welcome(self):
        menu = Menu()

        while True:
            menu.draw(self)
            pg.display.flip()

            for event in pg.event.get():
                pos = pg.mouse.get_pos()
                hovered = menu.hover(pos)
                if hovered:
                    if (event.type == MOUSEBUTTONDOWN):
                        if event.button == 1:
                            text = menu.select(hovered)
                            menu.bg_sound.stop()
                            return text

                    menu.update()
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN):
                    return False

    def play(self):
        player = Player(self, 'player')
        self.player = player
        self.ships.append(self.player)
        self.panel = Panel(self, self.player)
        self.bg_music.play()

        while self.state == 'play':
            self.check_events()
            self.update()
            self.draw()

        del self.player
        self.ships.clear()
        del self.panel
        self.bg_music.stop()

    def loop(self):
        while self.state != 'quit':
            self.state = self.welcome()

            if self.state == 'play':
                self.play()

            if self.state == 'gameover':
                game.over()

    def over(self):
        over = Gameover(self)
        over.draw()
        pg.display.flip()

        loop = True

        while loop:
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN):
                    loop = False
                    self.state = 'menu'
                    self.bg_music.stop()


if __name__ == '__main__':
    game = Game()
    game.loop()
