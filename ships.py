import time

from main import GameObject
from settings import *
from utils import blink


class Ship:
    def __init__(self, game, label) -> None:
        self.label = label
        self.game = game
        self.width, self.height = ships_settings[label]['width'], ships_settings[label]['height']
        self.x, self.y = random.randint(10, 400), -32
        self.energy = ships_settings[label]['energy']
        self.speed = ships_settings[label]['speed']
        self.images = self.load_images(label)
        self.current_frame = 0
        self.explosion_images = self.load_explosion_images()
        self.rect = pg.Surface.get_rect(self.images[0])

    def load_images(self, label):
        num_images = ships_settings[label]['images']
        images_list = []
        image = pg.image.load(ships_settings[label]['image_path'])
        image_x = ships_settings[label]['image_x']
        image_y = ships_settings[label]['image_y']

        for i in range(num_images):
            sprite_rect = pg.Rect((self.width*i) + image_x, image_y,
                                  self.width, self.height)
            sub_image = image.subsurface(sprite_rect)
            images_list.append(sub_image)

        return images_list

    def load_explosion_images(self):
        image = pg.image.load("./assets/explode.png")
        images_list = []
        width = explosion_settings['width']
        height = explosion_settings['height']

        for i in range(25):
            sprite_rect = pg.Rect(
                width * (i % 5), height * (i // 5), width, height)
            sub_image = image.subsurface(sprite_rect)
            images_list.append(sub_image)
        return images_list

    def swap_images(self):
        self.current_frame = 0
        aux = self.images
        self.images = self.explosion_images
        self.explosion_images = aux

    def draw(self):
        self.game.screen.blit(
            self.images[self.current_frame], (self.x, self.y))


class Enemy(Ship):
    def __init__(self, game, label) -> None:
        super().__init__(game, label)
        self.width, self.height = ships_settings[label]['width'], ships_settings[label]['height']
        self.bullets = []
        self.dead = False
        self.last_update_time = 0

    def update(self):
        if self.energy > 0:
            self.y += self.speed
            self.rect.topleft = self.x, self.y

        current_time = pg.time.get_ticks()
        elapsed_time = current_time - self.last_update_time

        if self.energy == 0 and self.dead == False:
            self.dead = True
            self.images = self.explosion_images
            self.rect = pg.Surface.get_rect(self.images[0])
            self.current_frame = 0

            if self.width != self.rect.width or self.height != self.rect.height:
                diff_x = self.rect.width - self.width
                diff_y = self.rect.height - self.height
                self.x = self.x - (diff_x / 2)
                self.y = self.y - (diff_y / 2)

        # Se o tempo transcorrido for maior que o tempo de exibição do quadro atual, atualize o quadro atual
        if elapsed_time > frame_duration:
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.last_update_time = pg.time.get_ticks()

        if self.current_frame == 24:
            self.game.ships.remove(self)


class Player(Ship):
    def __init__(self, game, label) -> None:
        super().__init__(game, label)
        self.x = (self.game.width / 2) - (self.width / 2)
        self.y = 400
        self.points = 0
        self.bullets = []
        self.rect = pg.Surface.get_rect(self.images[0])
        self.last_shoot_time = 0
        self.last_update_time = 0
        self.lives = ships_settings[label]['lives']
        self.dead = False
        self.just_born = False
        self.born_time = 0
        self.born_duration = 3
        self.blink_time = 200
        self.last_blink_time = 0
        self.toggle = False
        self.update()

    def update(self) -> None:
        keys = pg.key.get_pressed()
        self.fire(keys)
        self.move(keys)
        self.rect.topleft = self.x, self.y

        if self.energy == 0 and not self.dead:
            self.die()

        if self.current_frame == 24:
            self.born()

        current_time = pg.time.get_ticks()
        elapsed_time = current_time - self.last_update_time

        # Se o tempo transcorrido for maior que o tempo de exibição do quadro atual, atualize o quadro atual
        if elapsed_time > frame_duration:
            if self.just_born:
                self.blink()

            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.last_update_time = pg.time.get_ticks()

        for bullet in self.bullets:
            if bullet.y < -10:
                self.bullets.remove(bullet)
            else:
                bullet.update()

    def to_alpha(self):
        if self.just_born:
            if self.toggle:
                a = 100
            else:
                a = 255
        else:
            a = 255

        for i in self.images:
            i.set_alpha(a)

        self.toggle = not self.toggle

    def die(self):
        current_time = pg.time.get_ticks()
        elapsed_time = current_time - self.last_update_time

        self.swap_images()
        self.dead = True
        if elapsed_time > frame_duration:
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.last_update_time = pg.time.get_ticks()

    def born(self):
        self.x = (self.game.width / 2) - (self.width / 2)
        self.y = 400
        self.bullets = []
        self.rect = pg.Surface.get_rect(self.images[0])
        self.last_shoot_time = 0
        self.last_update_time = 0
        self.current_frame = 0
        self.energy = 10
        self.dead = False
        self.just_born = True
        self.born_time = time.time()
        self.swap_images()

    def blink(self):
        elapsed_time = time.time() - self.born_time
        if elapsed_time > self.born_duration:
            self.just_born = False

        self.to_alpha()

    def draw(self) -> None:
        super().draw()
        for bullet in self.bullets:
            bullet.draw()

    def fire(self, keys):
        elapsed_time = time.time() - self.last_shoot_time
        if keys[pg.K_SPACE]:
            if len(self.bullets) < 30 and elapsed_time >= 0.05:
                self.bullets.append(GameObject(self))
                self.last_shoot_time = time.time()

    def move(self, keys) -> None:
        speed = round(self.speed * self.game.delta_time)
        if keys[pg.K_UP]:
            if self.y > (self.game.height * 0.6):
                self.y -= speed
        if keys[pg.K_LEFT]:
            if self.x > 1:
                self.x -= speed
        if keys[pg.K_RIGHT]:
            if self.x < self.game.width - 32:
                self.x += speed
        if keys[pg.K_DOWN]:
            if self.y < (self.game.height - 50):
                self.y += speed
