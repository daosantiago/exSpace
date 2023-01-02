import time

from settings import *
from ship import *
from sounds import *


class Bullet():
    def __init__(self, p=None) -> None:
        self.game = p.game
        self.width, self.height = 0, 0
        self.x = p.x + (p.width / 2) - 4
        self.y = p.y
        self.speed = 3 if p.label == 'player' else -1
        self.image = self.load_image('bullet')
        self.rect = pg.Surface.get_rect(self.image)
        self.visible = True

    def load_image(self, label):
        if label == 'bullet':
            self.width, self.height = 8, 8
            posx, posy = 56, 80

        sprite_rect = pg.Rect(posx, posy, self.width, self.height)
        image = pg.image.load("./assets/spritesheet.png")
        image = image.subsurface(sprite_rect)
        return image

    def update(self):
        self.y -= self.speed
        self.rect.topleft = self.x, self.y

    def draw(self):
        self.game.screen.blit(self.image, (self.x, self.y))


class Enemy(Ship):
    def __init__(self, game, label) -> None:
        super().__init__(game, label)
        self.width, self.height = ships_settings[label]['width'], ships_settings[label]['height']
        self.last_update_time = 0
        self.can_shoot = ships_settings[label]['can_shoot']
        self.last_shoot_time = time.time() + 0.001

    def shoot(self):
        if self.can_shoot:
            elapsed_time = time.time() - self.last_shoot_time
            if not self.dead and len(self.bullets) < self.max_bullets and elapsed_time >= self.time_to_shoot:
                self.add_bullet(Bullet(self))
                self.last_shoot_time = time.time()
                self.shoot_sound.play()

    def update(self):
        current_time = pg.time.get_ticks()
        elapsed_time = current_time - self.last_update_time

        if not self.dead:
            self.set_y(self.y + self.speed)
            self.rect.topleft = self.pos

        self.shoot()
        for bullet in self.bullets:
            if bullet.y > 480:
                self.__bullets.remove(bullet)
            else:
                bullet.update()

        if self.energy == 0 and self.dead == False:
            self.die()

        # Se o tempo transcorrido for maior que o tempo de exibição do quadro atual, atualize o quadro atual
        if elapsed_time > frame_duration and self.current_frame != 24:
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.last_update_time = pg.time.get_ticks()

        if self.current_frame == 24:
            if len(self.bullets) == 0:
                self.game.ships.remove(self)

    def die(self):
        self.set_energy(0)
        self.explosion_sound.play()
        self.dead = True
        self.images = self.explosion_images
        self.rect = pg.Surface.get_rect(self.images[0])
        self.current_frame = 0
        self.can_collide = False

        if self.width != self.rect.width or self.height != self.rect.height:
            diff_x = self.rect.width - self.width
            diff_y = self.rect.height - self.height
            x = self.x - (diff_x / 2)
            y = self.y - (diff_y / 2)
            self.set_pos(x, y)


class Player(Ship):
    def __init__(self, game, label) -> None:
        super().__init__(game, label)
        self.set_pos((self.game.width / 2) - (self.width / 2), 400)
        self.points = 0
        self.rect = pg.Surface.get_rect(self.images[0])
        self.last_shoot_time = 0
        self.last_update_time = 0
        self.lives = ships_settings[label]['lives']
        self.just_born = False
        self.born_time = 0
        self.born_duration = 3
        self.blink_time = 200
        self.last_blink_time = 0
        self.toggle = False
        self.update()

    def make_point(self) -> None:
        self.points += 1

    def update(self) -> None:
        keys = pg.key.get_pressed()
        self.fire(keys)
        self.move(keys)
        self.rect.topleft = self.pos

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
        self.set_energy(0)
        self.explosion_sound.play()
        self.lives -= 1
        self.dead = True
        self.can_collide = False

        self.swap_images()

        if elapsed_time > frame_duration:
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.last_update_time = pg.time.get_ticks()

    def born(self):
        x = (self.game.width / 2) - (self.width / 2)
        y = 400
        self.set_pos(x, y)
        self.bullets = []
        self.rect = pg.Surface.get_rect(self.images[0])
        self.last_shoot_time = 0
        self.last_update_time = 0
        self.current_frame = 0
        self.set_energy(10)
        self.dead = False
        self.just_born = True
        self.born_time = time.time()
        self.swap_images()

    def blink(self):
        elapsed_time = time.time() - self.born_time
        if elapsed_time > self.born_duration:
            self.just_born = False
            self.can_collide = True

        self.to_alpha()

    def fire(self, keys):
        elapsed_time = time.time() - self.last_shoot_time
        if not self.dead:
            if keys[pg.K_SPACE]:
                if len(self.bullets) < self.max_bullets and elapsed_time >= self.time_to_shoot:
                    self.bullets.append(Bullet(self))
                    self.last_shoot_time = time.time()
                    self.shoot_sound.play()

    def move(self, keys) -> None:
        if self.dead:
            return

        speed = round(self.speed * self.game.delta_time)
        if keys[pg.K_UP]:
            if self.y > (self.game.height * 0.6):
                self.set_y(self.y - speed)
        if keys[pg.K_LEFT]:
            if self.x > 1:
                self.set_x(self.x - speed)
        if keys[pg.K_RIGHT]:
            if self.x < self.game.width - 32:
                self.set_x(self.x + speed)
        if keys[pg.K_DOWN]:
            if self.y < (self.game.height - 50):
                self.set_y(self.y + speed)
