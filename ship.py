from settings import *
from sounds import *


class Ship:
    def __init__(self, game, label) -> None:
        self.label = label
        self.game = game
        self.width, self.height = ships_settings[label]['width'], ships_settings[label]['height']
        self.__x, self.__y = random.randint(10, 400), -32
        self.__energy = ships_settings[label]['energy']
        self.speed = ships_settings[label]['speed']
        self.images = self.__load_images(label)
        self.current_frame = 0
        self.explosion_images = self.__load_explosion_images()
        self.explosion_sound = Sound('explode')
        self.rect = pg.Surface.get_rect(self.images[0])
        self.shoot_sound = Sound('shoot')
        self.__bullets = []
        self.last_shoot_time = 0
        self.can_collide = True
        self.dead = False
        self.max_bullets = ships_settings[label]['max_bullets']
        self.time_to_shoot = ships_settings[label]['time_to_shoot']

    def __load_images(self, label):
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

    def __load_explosion_images(self):
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

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def pos(self):
        return (self.__x, self.__y)

    @property
    def energy(self):
        return self.__energy

    @property
    def bullets(self):
        return self.__bullets

    def set_x(self, x):
        self.__x = x

    def set_y(self, y):
        self.__y = y

    def set_pos(self, x, y):
        self.__x = x
        self.__y = y

    def set_energy(self, energy):
        self.__energy = energy

    def swap_images(self):
        self.current_frame = 0
        aux = self.images
        self.images = self.explosion_images
        self.explosion_images = aux

    def got_shot(self, bullets):
        if self.can_collide and not self.dead:
            for bullet in bullets:
                if self.rect.colliderect(bullet.rect):
                    return bullet

        return False

    def collides_with(self, ships):
        if not isinstance(ships, list):
            ships = [ships]

        for ship in ships:
            if self.can_collide and ship.can_collide:
                if not self.dead and not ship.dead:
                    return self.rect.colliderect(ship.rect)

        return False

    def add_bullet(self, bullet):
        self.__bullets.append(bullet)

    def kill_bullet(self, bullet):
        self.__bullets.remove(bullet)

    def get_hit(self):
        self.__energy = self.__energy - 1

    def draw(self):
        self.game.screen.blit(
            self.images[self.current_frame], (self.__x, self.__y))

        for bullet in self.__bullets:
            bullet.draw()
