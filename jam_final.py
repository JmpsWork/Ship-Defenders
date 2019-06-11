# Game jam #1
# make a space themed game of any genre
# Made by Jmp


import pygame
import math  # for angles and stuff
import random  # For random spawnpoints


closed = False

pygame.init()
pygame.display.init()
pygame.mixer.init()

clock = pygame.time.Clock()
size = (1280, 720)
display = pygame.display.set_mode(size)

CENTER = 1280 / 2, 720 / 2
FPS = 60

sprites = []

pygame.font.init()
# font = pygame.font.SysFont('Comic Sans MS', 20)  Meant for debugging player position
score_font = pygame.font.SysFont('System Bold', 30)
wave_font = pygame.font.SysFont('System Bold', 30)
score = 0

missiles = 3
wave_count = 0
wave_text_counter = 0
powerup_count = 20 * FPS  # Anything else multiplied by FPS means that the number multiplied is time, in seconds
powerup_counter = 0

rotate_left = False
rotate_right = False

pygame.display.set_caption('Jam #1')


def within(bbox: tuple, other_bbox: tuple) -> bool:
    # This function is pretty wonky, if anybody could fix it up, that would be great
    # It uses the Axis Aligned Bounding Box method (hence the name, bbox)
    # 0: X, 1: Y, 2: WIDTH, 3: HEIGHT
    t_bbox = bbox[0], bbox[1], bbox[0] - bbox[2], bbox[1] - bbox[3]
    t_other_bbox = other_bbox[0], other_bbox[1], other_bbox[0] - other_bbox[2], other_bbox[1] - other_bbox[3]
    if t_bbox[0] < t_other_bbox[0] + t_other_bbox[2] and t_bbox[0] + t_bbox[2] > t_other_bbox[0] and \
            t_bbox[1] < t_other_bbox[1] + t_other_bbox[3] and t_bbox[1] + t_bbox[3] > t_other_bbox[1]:
        return True
    return False


def spawnpoint() -> tuple:  # If the game opens and crashes afterwards, look here
    x = round(player.x)
    y = round(player.y)
    player_box = range(x - 300, x + 300), range(y - 200, y + 200)
    while True:
        possible = random.randrange(0, size[0]), random.randrange(0, size[1])
        if possible[0] not in player_box[0] and possible[1] not in player_box[1]:
            break
    return possible


def new_wave():
    amount = round(wave_count + 0.5 / 2)  # + 0.5 because the wave counter is always behind
    while amount != 0:
        amount -= 1
        point = spawnpoint()
        if amount % 2 == 0 and amount != 0:
            # Create a missile boat (mb) every third wave. Increases difficulty
            point = spawnpoint()
            sprites.append(Enemy(point, ['images/ship_idle_enemy.png'], (-2, -2), 1, 'enemy_ship', mb=True))
            # sprites.append(Friendly(point, ['images/ship_idle_ally.png'], (-2, -2), 1, 'friendly_ship'))
        if amount % 3 == 0 and amount != 0:
            # Create reinforcements
            print('friendly ship')
            new_point = player.x - 100, player.y - 100
            sprites.append(Friendly(new_point, ['images/ship_idle_ally.png'], (-2, -2), 1, 'friendly_ship'))
        if amount % 6 == 0 and amount != 0:
            print('friendly missile boat')
            new_point = player.x + 100, player.y + 100
            sprites.append(Friendly(new_point, ['images/ship_friendly_mb.png'], (-2, -2), 1, 'friendly_ship', mb=True))
        else:
            sprites.append(Enemy(point, ['images/ship_idle_enemy.png'], (-2, -2), 1, 'enemy_ship'))


def new_powerup():
    point = spawnpoint()
    # For people using pycharm ,
    powerup = AnimSprite(point, ['images/missile_powerup.png'], (0, 0), 1, 'powerup', 0, None)
    powerup.collide = False
    sprites.append(powerup)


class Sprite:
    def __init__(self, coords: tuple, path: str, velocity: tuple, shot: str='bullet', direction: int=0):
        self.x = coords[0]
        self.y = coords[1]
        self.vx = velocity[0]
        self.vy = velocity[1]
        self.facing = direction
        self.image = pygame.image.load(path)
        self.size = self.image.get_rect().size
        self.die = False
        self.shot = shot
        self.collide = True

    @property
    def bbox(self):
        return self.x, self.y, self.x-self.size[0], self.y-self.size[1]

    def draw(self, move: bool=True):
        # screen being display
        # angle being amount
        # W, H are from image.get_size()
        # pos is the pivot point, so self.x + size[0] / 2, self.y + size[1] / 2
        image = pygame.transform.rotate(self.image, self.facing)
        display.blit(image, (self.x - self.size[0], self.y - self.size[1]))
        if move:
            self.move_forward()

    def face(self, other):
        x = other.x - self.x
        y = other.y - self.y
        self.facing = -math.degrees(math.atan2(y, x)) - 90

    def gradual_face(self, other, speed: [int, float]=1.0):
        """Gradually face another Sprite. Speed is degrees per frame"""
        other_x = other.x - self.x
        other_y = other.y - self.y

        if self.x + size[0] / 2 < other.x:
            other_x -= size[0]
        if self.y + size[1] / 2 < other.y:
            other_y -= size[1]
        if self.x - size[0] / 2 > other.x:
            other_x += size[0]
        if self.y - size[1] / 2 > other.y:
            other_y += size[1]

        to_face = -math.degrees(math.atan2(other_y, other_x)) - 90

        if not to_face + speed > self.facing - speed:
            self.facing -= speed
        elif not to_face - speed < self.facing + speed:
            self.facing += speed
        else:
            self.facing = to_face

    def rotate(self, amount: int):
        self.facing += amount
        if self.facing > 180:  # Clamp angles
            self.facing -= 360
        elif self.facing < -180:
            self.facing += 360

    def set_rotation(self, angle: int):
        self.facing = angle

    def set_velocity(self, x: [int, float], y: [int, float]):
        self.vx = x
        self.vy = y

    def move_forward(self):
        self.x += self.vx * math.cos(math.radians(-self.facing + 90))
        self.y += self.vy * math.sin(math.radians(-self.facing + 90))
        if self.x + self.size[0] < 0:  # Account for the size of the object to smooth the transition of teleportation
            self.x += size[0] + self.size[0]
        elif self.x > size[0] + self.size[0]:
            self.x -= size[0] + self.size[0]
        if self.y + self.size[1] < 0:
            self.y += size[1] + self.size[1]
        elif size[1] + self.size[1] < self.y:
            self.y -= size[1] + self.size[1]


class AnimSprite(Sprite):
    def __init__(self, coords: tuple, frames: list, velocity: tuple, delay: int=1, shot: str='bullet', direction: int=0, friendly: bool=True):
        super().__init__(coords, frames[0], velocity, shot, direction)
        self.frames = frames
        self.frame_count = 0
        self.delay = delay
        self.delay_count = 1
        self.friendly = friendly

    def draw(self, move: bool=True):
        image = pygame.image.load(self.frames[self.frame_count])
        image = pygame.transform.rotate(image, self.facing)
        # Debug collision rectangle
        color = (255, 0, 0)
        if self.friendly:
            color = (0, 255, 0)
        # pygame.draw.rect(display, color, pygame.Rect(self.x, self.y, -self.size[0], -self.size[1]))
        # pygame.draw.rect(display, color, pygame.Rect(*self.bbox))
        display.blit(image, (self.x - self.size[0], self.y - self.size[1]))
        if move:
            self.move_forward()

    def loop(self):
        """Loop does the same draw routines as self.draw(), but loops the frames based on the delay.
        The delay is the number of frames before the next frame is chosen to be drawn."""
        if self.delay_count >= self.delay:
            self.frame_count += 1
            if self.frame_count >= len(self.frames):  # Reset frames
                self.frame_count = 0
            image = pygame.image.load(self.frames[self.frame_count])
            image = pygame.transform.rotate(image, self.facing)
            self.image = image
            self.delay_count = 0

        else:
            image = pygame.transform.rotate(pygame.image.load(self.frames[self.frame_count]), self.facing)
            self.image = image
            self.delay_count += 1

        display.blit(image, (self.x, self.y))
        self.move_forward()

    def nearest(self):
        sorted_sprites = sorted(sprites, key=lambda x: math.sqrt((self.x - x.x)**2 + (self.y - x.y)**2))
        try:
            return [near for near in sorted_sprites if near.friendly != self.friendly and near.friendly is not None][0]
        except IndexError:  # If all sprites friendly or no sprites exist
            return sprites[0]

    def set_frame(self, frame: int):
        self.frame_count = frame


class Projectile(AnimSprite):  # Projectile have a
    def __init__(self, coords: tuple, frames: list, velocity: tuple, delay: int=1, shot: str='bullet', direction: int=0, life: int=5, friendly: bool=True):
        super().__init__(coords, frames, velocity, delay, shot, direction)
        self.vx = velocity[0]
        self.vy = velocity[1]
        self.life = life * FPS
        self.life_counter = 0
        self.shot = shot
        self.friendly = friendly

    def face(self, other):
        """We override the face method so that it faces based on relative position, not absolute position
        Essentially, we want to avoid the missile suddenly jumping when the player reaches the top of the screen.
        We do this by checking if the player's position is >< than half the screen"""
        other_x = other.x
        other_y = other.y
        if self.x + size[0] / 2 < other.x:
            other_x -= size[0]
        if self.y + size[1] / 2 < other.y:
            other_y -= size[1]
        if self.x - size[0] / 2 > other.x:
            other_x += size[0]
        if self.y - size[1] / 2 > other.y:
            other_y += size[1]

        x = other_x - self.x
        y = other_y - self.y

        self.facing = -math.degrees(math.atan2(y, x)) - 90

    def draw(self, move: bool=True):
        super().draw(move=move)
        self.life_counter += 1
        if self.life_counter > self.life:
            self.die = True

    def loop(self):
        super().loop()
        self.life_counter += 1
        if self.life_counter > self.life:
            self.die = True


class Enemy(AnimSprite):
    def __init__(self, *args, mb=False):
        super().__init__(*args)
        self.shoot = 3 * FPS
        if mb is True:
            self.shoot *= 2
            self.frames = ['images/ship_enemy_mb.png']
        else:
            self.frames = ['images/ship_idle_enemy.png']
        self.friendly = False
        self.shoot_counter = 0
        self.mb = mb

    def draw(self, move: bool=True):
        self.gradual_face(self.nearest(), 0.8)
        super().draw(move=move)
        if self.shoot_counter >= self.shoot:
            self.shoot_counter = 0
            if self.mb is False:
                self.fire()
            else:
                self.launch()
        self.shoot_counter += 1

    def fire(self):
        new = Projectile((self.x, self.y), ['images/bullet_enemy.png'], (self.vx-4.5, self.vy-4.5), 1, 'bullet', self.facing, 2, False)
        sprites.append(new)

    def launch(self):
        new = Projectile((self.x, self.y), ['images/ship_missile_enemy.png'], (-4.2, -4.2), 1, 'enemy_missile', self.facing, 12, False)
        sprites.append(new)


class Friendly(AnimSprite):
    def __init__(self, *args, mb: bool=False):
        super().__init__(*args)
        self.friendly = True
        self.shoot = 2 * FPS  # + random.randrange(60, 120, 15)
        if mb is True:
            self.shoot *= 2
            self.set_velocity(-1.5, -1.5)
        self.shoot_counter = 0
        self.mb = mb

    def draw(self, move: bool=True):
        nearest = self.nearest()
        self.gradual_face(nearest, 1)
        super().draw(move=move)
        if self.shoot_counter >= self.shoot:
            self.shoot_counter = 0
            if self.mb:
                self.launch()
            else:
                self.fire()
        self.shoot_counter += 1

    def fire(self):
        new = Projectile((self.x, self.y), ['images/bullet.png'], (self.vx-4.5, self.vy-4.5), 1, 'bullet', self.facing, 2, True)
        sprites.append(new)

    def launch(self):
        new = Projectile((self.x, self.y), ['images/ship_missile.png'], (-4.2, -4.2), 1, 'friendly_missile', self.facing, 12, True)
        sprites.append(new)


player = AnimSprite(CENTER, ['images/ship_idle.png'], (0, 0), 1, 'player', 0)
# powerup = AnimSprite((200, 200), ['images/missile_powerup.png'], (0, 0), 1, 'powerup', 0, None)
# None is so it doesn't get targeted by enemies and allies

# enemy = Enemy((200, 200), ['images/ship_idle_enemy.png'], (-2, -2), 1, 'enemy_ship')
# enemy2 = Enemy((400, 400), ['images/ship_idle_enemy.png'], (-2, -2), 1, 'enemy_ship')

missile1 = Sprite((size[0] - 100, 40), 'images/ship_missile.png', (0, 0))
missile2 = Sprite((size[0] - 80, 40), 'images/ship_missile.png', (0, 0))
missile3 = Sprite((size[0] - 60, 40), 'images/ship_missile.png', (0, 0))
missile1.collide = False
missile2.collide = False
missile3.collide = False

# friendly = Friendly((600, 600), ['images/ship_idle_ally.png'], (-2, -2), 1, 'friendly_ship')

# sprites.append(enemy)  # Dummy enemies
# sprites.append(enemy2)
# sprites.append(powerup)
# sprites.append(friendly)


sprites.append(player)

wave_count += 1  # Test
new_wave()
while not closed:

    pygame.display.update()
    pygame.draw.rect(display, (24, 24, 24), pygame.Rect(0, 0, 1280, 720))  # Background colour
    pygame.draw.rect(display, (180, 180, 180), pygame.Rect(0, 500, 1280, 20))

    # Used for debugging
    # text = font.render(f'X:{round(player.x, 2)}, Y:{round(player.y, 2)}, Angle:{player.facing}', True, (200, 200, 200))
    score_text = score_font.render(f'Score: {score}', True, (200, 200, 200))
    wave_text_color = (200, 200 - wave_count * 4, 200 - wave_count * 4)
    if wave_text_color[1] <= 40:
        wave_text_color = (200, 40, 40)
    wave_text = wave_font.render(f'Current Wave: {wave_count}', True, wave_text_color)

    powerup_counter += 1

    if missiles >= 3:  # Missile counter
        missile3.draw(False)
        missile2.draw(False)
        missile1.draw(False)
    elif missiles == 2:
        missile2.draw(False)
        missile1.draw(False)
    elif missiles == 1:
        missile1.draw(False)

    if powerup_counter >= powerup_count:
        new_powerup()
        powerup_counter = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            closed = True
            print('GAME OVER')
            print(f'Your final score is: {score}')
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                rotate_left = True
                player.rotate(1)

            if player.die is False:
                if event.key == pygame.K_d:
                    rotate_right = True
                    player.rotate(-1)

                if event.key == pygame.K_w:
                    # player.set_frame(1)
                    player.set_velocity(-3.5, -3.5)

                if event.key == pygame.K_e and missiles >= 1:
                    shoot_sound = pygame.mixer.Sound('sounds/shoot.wav')
                    shoot_sound.set_volume(0.5)
                    shoot_sound.play()
                    new = Projectile((player.x, player.y), ['images/ship_missile.png'], (-4.2, -4.2), 1, 'missile', player.facing, 12, True)
                    sprites.append(new)
                    missiles -= 1

                if event.key == pygame.K_SPACE:
                    shoot_sound = pygame.mixer.Sound('sounds/shoot.wav')
                    shoot_sound.play()
                    origin = (player.x - player.size[0] / 2, player.y - player.size[1] / 2)
                    new = Projectile(origin, ['images/bullet.png'], (player.vx -5.5, player.vy-5.5), 1, 'bullet', player.facing, 2, True)
                    sprites.append(new)

        if event.type == pygame.KEYUP:
            if player.die is False:
                if event.key == pygame.K_a:
                    rotate_left = False

                if event.key == pygame.K_d:
                    rotate_right = False

                if event.key == pygame.K_w:
                    player.set_velocity(0, 0)

    if rotate_left:
        player.rotate(-2)

    elif rotate_right:
        player.rotate(2)

    if sprites:
        for index, sprite in enumerate(sprites):
            if sprite.collide is True:

                for other_index, other_sprite in enumerate(sprites):  # Other index is for finding the other Sprite collided with
                    if other_index != index:  # Avoid collision with itself
                        if within(other_sprite.bbox, sprite.bbox) and (sprite.friendly is not other_sprite.friendly):
                            if other_sprite.shot == 'powerup' and sprite.shot == 'player':
                                # Prevent player death on pickup
                                powerup_sound = pygame.mixer.Sound('sounds/powerup_pickup.wav')
                                powerup_sound.play()
                                other_sprite.die = True
                                missiles += 1
                            elif sprite.shot == 'powerup' and other_sprite.shot == 'player':
                                powerup_sound = pygame.mixer.Sound('sounds/powerup_pickup.wav')
                                powerup_sound.play()
                                sprite.die = True
                                missiles += 1
                            else:
                                sprite.die = True
                                other_sprite.die = True
                            # print(f'Collision with {sprite.shot} and {other_sprite.shot}')

            sprite.draw()
            if sprite.shot == 'missile':
                sprite.gradual_face(sprite.nearest(), 0.8)
            elif sprite.shot == 'friendly_missile':
                sprite.gradual_face(sprite.nearest(), 0.8)
            elif sprite.shot == 'enemy_missile':
                sprite.gradual_face(sprite.nearest(), 0.8)
            elif sprite.shot == 'powerup':
                sprite.rotate(2)
            if sprite.die is True:
                if sprite.shot == 'enemy_ship':
                    explode = pygame.mixer.Sound(f'sounds/explode{random.randrange(1, 5)}.wav')
                    explode.play()
                    score += 600
                elif sprite.shot == 'enemy_missile':
                    score += 100
                elif sprite.shot == 'friendly_ship':
                    explode = pygame.mixer.Sound(f'sounds/explode{random.randrange(1, 5)}.wav')
                    explode.play()
                sprites.pop(index)

            if [sprite.friendly for sprite in sprites if sprite.friendly is False] == []:
                wave_count += 1
                new_wave()

    if player.die is True:
        death = pygame.mixer.Sound(f'sounds/explode{random.randrange(1, 5)}.wav')
        death.play()
        pygame.display.quit()
        closed = True
        print('GAME OVER')
        print(f'Your final score is: {score}')
        quit()

    # player.draw()
    # display.blit(text, (40, 40))
    display.blit(score_text, (40, 80))
    display.blit(wave_text, (40, 40))

    clock.tick(FPS)
