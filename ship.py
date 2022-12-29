from settings import *


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
