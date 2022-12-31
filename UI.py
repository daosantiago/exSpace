import pygame as pg

from sounds import *


class Menu:
    def __init__(self):
        self.texts = [('Start Game', 'play'), ("Quit", 'quit')]
        self.options = self.createOptions()
        self.background = pg.image.load('./assets/menu_bg.jpg')
        self.bg_sound = Sound('menu')
        self.bg_sound.play()

    def update(self):
        pass

    def select(self, opt):
        return opt.command

    def hover(self, pos):
        for opt in self.options:
            if opt.rect.collidepoint(pos):
                opt.highlight()
                return opt
            else:
                opt.downlight()

    def draw(self, game):
        game.screen.blit(self.background, (0, 0))
        for opt in self.options:
            opt.draw(game)

    def createOptions(self):
        options = []
        for i, opt in enumerate(self.texts):
            options.append(MenuOption(opt, i))

        return options


class MenuOption():
    def __init__(self, opt, i):
        self.text = opt[0]
        self.command = opt[1]
        self.selected = False
        self.color = 'white'
        self.image = pg.Surface((100, 100))
        self.rect = pg.Surface.get_rect(self.image)
        self.x = 0
        self.y = 0
        self.index = i
        self.font = pg.font.Font(None, 36)
        self.rect = pg.Surface.get_rect(self.image)

    def highlight(self):
        self.color = 'orange'

    def downlight(self):
        self.color = 'white'

    def update(self):
        pass

    def set_selected(self, color):
        self.selected = True
        self.color = 'orange'

    def draw(self, game):
        self.image = self.font.render(self.text, True, self.color)
        self.rect = pg.Surface.get_rect(self.image)
        self.x = game.width/2 - self.rect.center[0]
        self.y = game.height/2 + (self.index * self.rect.height +
                                  (self.index*4)) - self.rect.center[1]
        self.rect.x, self.rect.y = self.x, self.y
        # Desenhe a surface do texto na tela, centralizando-a
        game.screen.blit(self.image, (self.x, self.y))


class LifeBar():
    def __init__(self, game, p):
        self.game = game
        self.player = p
        self.energy = p.energy
        self.max_energy = 100
        self.x = 0
        self.y = 0
        self.width = 100
        self.height = 10
        self.rect = None
        self.color = 'green'
        self.image = self.create_bar()
        self.last_blink_time = 1
        self.blink_time = 200
        self.toggle = False

    def update(self):
        if self.energy < 5:
            self.color = 'red'
        elif self.energy < 7:
            self.color = 'orange'
        elif self.energy < 9:
            self.color = 'yellow'
        else:
            self.color = 'green'

        if self.energy != self.player.energy:
            self.energy = self.player.energy
            self.width = self.energy * 10
            self.image.fill((self.color))
            if self.width > 0 and self.height > 0:
                self.image = pg.transform.scale(
                    self.image, (self.width, self.height))

        if self.energy < 3:
            self.blink()
        elif self.toggle:
            self.image.set_alpha(255)

    def blink(self):
        current_time = pg.time.get_ticks()
        elapsed_time = current_time - self.last_blink_time

        # Se o tempo transcorrido for maior que o tempo de exibição do quadro atual, atualize o quadro atual
        if elapsed_time > self.blink_time:
            self.last_blink_time = pg.time.get_ticks()
            self.toggle = not self.toggle

        if self.toggle:
            self.image.set_alpha(100)
        else:
            self.image.set_alpha(255)

    def create_bar(self):
        img = pg.Surface((self.width, self.height))
        img.fill(self.color)

        return img

    def draw(self):
        self.image.fill((self.color))
        self.game.screen.blit(self.image, (self.x, self.y))


class Gameover():
    def __init__(self, game) -> None:
        self.game = game
        self.x = 0
        self.y = 0
        self.font = pg.font.Font(None, 36)
        self.image = pg.Surface((100, 100))
        self.rect = pg.Surface.get_rect(self.image)

    def draw(self):
        self.game.screen.fill('black')
        self.image = self.font.render(f'GAME OVER', True, 'white')
        self.rect = pg.Surface.get_rect(self.image)
        self.x = self.game.width/2 - self.rect.center[0]
        self.y = self.game.height/2 - self.rect.center[1]
        # Desenhe a surface do texto na tela, centralizando-a
        self.game.screen.blit(self.image, (self.x, self.y))


class PointsDisplay:
    def __init__(self, game, p) -> None:
        self.game = game
        self.player = p
        self.x = 0
        self.y = 0
        self.width = 100
        self.height = 10
        self.points = 0
        self.font = pg.font.Font(None, 20)
        self.image = pg.Surface((self.width, self.height))

    def update(self):
        pass

    def draw(self):
        self.image = self.font.render(
            f'Points: {self.player.points} - Lives: {self.player.lives}', True, 'white')
        # Desenhe a surface do texto na tela, centralizando-a
        self.game.screen.blit(self.image, (self.x, self.y))

    def create_display(self):
        # Renderize o texto como uma surface
        text_surface = self.font.render(
            f'Points: {self.player.points}', True, (255, 255, 255))

        return text_surface


class Panel():
    def __init__(self, game, p):
        self.game = game
        self.player = p
        self.width = 120
        self.height = 50
        self.x = game.width - self.width - 20
        self.y = 20
        self.items = self.loadItems()

    def update(self):
        if self.items:
            for i in self.items:
                i.update()

    def draw(self):
        if self.items:
            for i in self.items:
                i.draw()

    def loadItems(self):
        items = []

        item = LifeBar(self.game, self.player)
        item.x = self.x + 2
        item.y = self.y + 2
        items.append(item)

        item = PointsDisplay(self.game, self.player)
        item.x = items[0].x
        item.y = items[0].y + items[0].height + 4
        items.append(item)
        return items
