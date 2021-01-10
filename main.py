import os
import sys
import pygame
from random import randint, choice

clock = pygame.time.Clock()

fps = 60
player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
alive_tanks = 0


def gameover():
    screen.fill((0, 0, 0))
    load_sound('dead_music.mp3')
    pygame.mixer.music.play()
    # global screen
    # size = 650, 500
    image = load_image('game_over.png')
    image_rect = image.get_rect()
    # screen = pygame.display.set_mode(image, size)
    screen.blit(image, image_rect)
    pygame.display.flip()
    pygame.time.wait(5000)
    sys.quit()
    # screen.fill(0, 0, 0)
    # pygame.display.update()


def win():
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 100)
    text = font.render('You Win!', True, (255, 255, 255))
    text_x = size[0] // 2 - text.get_width() // 2
    text_y = size[1] // 2 - text.get_height() // 2
    screen.blit(text, (text_x, text_y))
    pygame.display.flip()
    pygame.time.wait(5000)


def load_sound(name, colorkey=None):
    fullname = os.path.join('sound', name)
    if not os.path.isfile(fullname):
        print(f"Файл со звуком '{fullname}' не найден")
        sys.exit()
    sound = pygame.mixer.music.load(fullname)
    return sound


def load_image(name, colorkey=None):
    fullname = os.path.join('textures', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            if level[y][x] == '#':
                Tile('brick', x, y)
            elif level[y][x] == '!':
                Tile('metal', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
            elif level[y][x] == '*':
                Tile('empty', x, y)
                enemys.append(Enemy(x, y, 3))
                global alive_tanks
                alive_tanks += 1
            elif level[y][x] == '/':
                Tile('empty', x, y)
                enemys.append(Enemy(x, y, 10))
                alive_tanks += 1
            elif level[y][x] == '&':
                Tile('empty', x, y)
                enemys.append(Enemy(x, y, 5))
                alive_tanks += 1
                # вернем игрока, а также размер поля в клетках
    return new_player, x, y


tile_images = {
    'brick': load_image('brick.png'),
    'empty': load_image('grass.png'),
    'metal': load_image('metal.png')
}
player_image = load_image('test_tank_0.png')


bullet_image = load_image('bullet.png')
tile_width = tile_height = 50
enemys = []
collisions = []
player_bullets = 0
pl_xp = 5
turn = 1100


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type=None, pos_x=None, pos_y=None):
        if tile_type is not None:
            if tile_type == 'empty':
                super().__init__(tiles_group)
                self.image = tile_images[tile_type]
                self.rect = self.image.get_rect().move(
                    tile_width * pos_x, tile_height * pos_y)
            else:
                super().__init__(tiles_group, all_sprites)
                collisions.append(CollisionBullet(pos_x, pos_y))
                self.image = tile_images[tile_type]
                self.rect = self.image.get_rect().move(
                    tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x=None, pos_y=None):
        super().__init__(player_group)
        self.image = player_image
        self.rect = self.image.get_rect().move(pos_x, pos_y)

    def update(self):
        if pygame.sprite.spritecollideany(self, all_sprites):
            return False
        else:
            return True

    def check(self):

        for i in range(len(bullets) - 1, -1, -1):

            el = bullets[i]
            if pl_x < el.x < pl_x + 50 and \
                    pl_y < el.y < pl_y + 50 and not (el.isplayer):
                del bullets[i]
                global pl_xp
                pl_xp -= 1
            if pl_xp <= 0:
                gameover()


class CollisionBullet:
    def __init__(self, pos_x=None, pos_y=None):
        self.pos_x = pos_x * 50
        self.pos_y = pos_y * 50

    def check(self):
        for i in range(len(bullets) - 1, -1, -1):
            el = bullets[i]
            if self.pos_x < el.x < self.pos_x + 50 and \
                    self.pos_y < el.y < self.pos_y + 50:
                if el.isplayer:
                    global player_bullets
                    player_bullets = 0
                del bullets[i]


previous_time = 0


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x=None, pos_y=None, type=3):
        super().__init__(player_group)
        self.hp = type
        self.type = str(type)

        self.image = load_image('enemy_tank_0_' + self.type + '.png')
        self.pos_x = pos_x * 50
        self.pos_y = pos_y * 50

        self.alivee = True
        self.last_der = -1

    def shoot(self):
        bullets.append(Snaryad(round(self.pos_x + 50 // 2),
                               round(self.pos_y + 50 // 2), 3, (0, 0, 0),
                               self.last_der, False))
        previous_time = pygame.time.get_ticks()

    def check(self):
        global alive_tanks
        for i in range(len(bullets) - 1, -1, -1):
            el = bullets[i]
            if self.pos_x < el.x < self.pos_x + 50 and \
                    self.pos_y < el.y < self.pos_y + 50 and el.isplayer:
                self.hp -= 1
                del bullets[i]
                global player_bullets
                player_bullets = 0
        if self.hp <= 0:
            print(self.hp <= 0 and 0 < alive_tanks < 4)
            self.alivee = False
            self.pos_y = 1000
            self.pos_x = 1000
            alive_tanks -= 1

    def move(self):
        global previous_time
        current_time = pygame.time.get_ticks()
        if randint(0, 1000) > 900:
            if current_time - previous_time > 500:
                if self.last_der == -2 and self.pos_y > pl_y and \
                        abs(self.pos_x - pl_x) <= 50:
                    self.shoot()
                if self.last_der == 2 and self.pos_y < pl_y and \
                        abs(self.pos_x - pl_x) <= 50:
                    self.shoot()
                if self.last_der == -1 and self.pos_x > pl_x and \
                        abs(self.pos_y - pl_y) <= 50:
                    self.shoot()
                if self.last_der == 1 and self.pos_x < pl_x and \
                        abs(self.pos_y - pl_y) <= 50:
                    self.shoot()

        if self.update() and randint(0, 1000) < turn:
            if self.last_der == -2:
                self.pos_y -= 1
            if self.last_der == 2:
                self.pos_y += 1
            if self.last_der == -1:
                self.pos_x -= 1
            if self.last_der == 1:
                self.pos_x += 1

        else:
            if self.last_der == -2:
                self.last_der = 2
            elif self.last_der == 2:
                self.last_der = -2
            elif self.last_der == -1:
                self.last_der = 1
            elif self.last_der == 1:
                self.last_der = -1
            if self.last_der == -2:
                self.pos_y -= 1
            if self.last_der == 2:
                self.pos_y += 1
            if self.last_der == -1:
                self.pos_x -= 1
            if self.last_der == 1:
                self.pos_x += 1
        if randint(0, 1000) > 995:
            self.last_der = choice([1, -1, -2, 2])

    def update(self):
        self.rect = self.image.get_rect().move(self.pos_x, self.pos_y)
        if pygame.sprite.spritecollideany(self, all_sprites):
            return False
        else:
            return True

    def draw(self):
        self.move()
        if self.last_der == -2:
            self.image = load_image('enemy_tank_0_' + self.type + '.png')
        elif self.last_der == 1:
            self.image = load_image('enemy_tank_90_' + self.type + '.png')
        elif self.last_der == 2:
            self.image = load_image('enemy_tank_180_' + self.type + '.png')
        elif self.last_der == -1:
            self.image = load_image('enemy_tank_270_' + self.type + '.png')

        self.check()
        if self.alivee:
            screen.blit(self.image, (self.pos_x, self.pos_y))


def load_level(filename):
    filename = filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


lastMove = 'up'


class Snaryad():

    def __init__(self, x, y, radius, color, direction, isplayer):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.direction = direction
        self.vel = 5 * direction
        self.image = bullet_image
        self.rect = self.image.get_rect().move(x, y)
        self.isplayer = isplayer

    # def draw(self, win):
    # pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
    def draw(self, wind):
        screen.blit(self.image, (self.x - 25, self.y - 25))


if __name__ == '__main__':
    pygame.init()
    size = 650, 500
    screen = pygame.display.set_mode(size)
    level_map = load_level("map.map")
    pl_x = 200
    pl_y = 400
    hero, max_x, max_y = generate_level(level_map)
    speed = 1
    running = True
    bullets = []
    while running:
        print(alive_tanks)
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                running = False
        if alive_tanks == 0:
            win()
        proverka = Player(pl_x, pl_y)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            if lastMove == 'up':
                direction = -2
            elif lastMove == 'down':
                direction = +2
            elif lastMove == 'right':
                direction = 1
            elif lastMove == 'left':
                direction = -1

            if player_bullets < 1:
                bullets.append(Snaryad(round(pl_x + 50 // 2),
                                       round(pl_y + 50 // 2), 3, (0, 0, 0),
                                       direction, True))
                player_bullets += 1

        for bullet in bullets:
            if bullet.direction == 1 or bullet.direction == -1:
                if bullet.x < 450 and bullet.x > 50:
                    bullet.x += bullet.vel
                else:
                    bullets.pop(bullets.index(bullet))
            elif bullet.direction == 2:
                if bullet.y < 450 and bullet.y > 50:
                    bullet.y += bullet.vel - 5
                else:
                    bullets.pop(bullets.index(bullet))
            elif bullet.direction == -2:
                if bullet.y < 450 and bullet.y > 50:
                    bullet.y += bullet.vel + 5
                else:
                    bullets.pop(bullets.index(bullet))
        # pygame.mixer.music.load('/home/alpha/Документы/project_tank/YLproject/sound/ride_tank.mp3')
        if proverka.update():
            # pygame.mixer.music.play()
            if keys[pygame.K_LEFT] and pl_x > 0:
                pl_x -= speed
                lastMove = 'left'
                player_image = load_image('test_tank_270.png')
            elif keys[pygame.K_RIGHT] and pl_x < 450:
                pl_x += speed
                lastMove = 'right'
                player_image = load_image('test_tank_90.png')
            elif keys[pygame.K_UP] and pl_y > 0:
                pl_y -= speed
                lastMove = 'up'
                player_image = load_image('test_tank_0.png')
            elif keys[pygame.K_DOWN] and pl_y < 450:
                pl_y += speed
                lastMove = 'down'
                player_image = load_image('test_tank_180.png')

        elif lastMove == 'up':
            pl_y += 1
            if keys[pygame.K_LEFT] and pl_x > 0:
                pl_x -= speed
                lastMove = 'left'
                player_image = load_image('test_tank_270.png')
            elif keys[pygame.K_RIGHT] and pl_x < 450:
                pl_x += speed
                lastMove = 'right'
                player_image = load_image('test_tank_90.png')
            elif keys[pygame.K_DOWN] and pl_y < 450:
                pl_y += speed
                lastMove = 'down'
                player_image = load_image('test_tank_180.png')
        elif lastMove == 'left':
            pl_x += 1
            if keys[pygame.K_RIGHT] and pl_x < 450:
                pl_x += speed
                lastMove = 'right'
                player_image = load_image('test_tank_90.png')
            elif keys[pygame.K_UP] and pl_y > 0:
                pl_y -= speed
                lastMove = 'up'
                player_image = load_image('test_tank_0.png')
            elif keys[pygame.K_DOWN] and pl_y < 450:
                pl_y += speed
                lastMove = 'down'
                player_image = load_image('test_tank_180.png')
        elif lastMove == 'right':
            pl_x -= 1
            if keys[pygame.K_LEFT] and pl_x > 0:
                pl_x -= speed
                lastMove = 'left'
                player_image = load_image('test_tank_270.png')
            elif keys[pygame.K_UP] and pl_y > 0:
                pl_y -= speed
                lastMove = 'up'
                player_image = load_image('test_tank_0.png')
            elif keys[pygame.K_DOWN] and pl_y < 450:
                pl_y += speed
                lastMove = 'down'
                player_image = load_image('test_tank_180.png')
        elif lastMove == 'down':
            pl_y -= 1
            if keys[pygame.K_LEFT] and pl_x > 0:
                pl_x -= speed
                lastMove = 'left'
                player_image = load_image('test_tank_270.png')
            elif keys[pygame.K_RIGHT] and pl_x < 450:
                pl_x += speed
                lastMove = 'right'
                player_image = load_image('test_tank_90.png')
            elif keys[pygame.K_UP] and pl_y > 0:
                pl_y -= speed
                lastMove = 'up'
                player_image = load_image('test_tank_0.png')
        proverka.check()
        for i in range(len(collisions)):
            collisions[i].check()
        tiles_group.draw(screen)
        for i in range(len(enemys)):
            enemys[i].draw()
        screen.blit(player_image, (pl_x, pl_y))

        for bullet in bullets:
            bullet.draw(screen)

        clock.tick(fps)
        pygame.display.update()
pygame.quit()
