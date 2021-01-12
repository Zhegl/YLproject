import os
import sys
import pygame
from random import randint, choice
import random

pygame.init()
clock = pygame.time.Clock()
start_ticks = pygame.time.get_ticks()
fps = 60
player = None
screen_rect = (0, 0, 500, 500)
# группы спрайтов
all_sprites = pygame.sprite.Group()
particle_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
alive_tanks = 0
sound1 = pygame.mixer.Sound('sound/kill.wav')
sound2 = pygame.mixer.Sound('sound/shoot.wav')
points = [(190, 250, 'Играть', (255, 255, 255), (255, 100, 50), 0),
          (190, 300, 'Выход', (255, 255, 255), (255, 100, 50), 1)]
points_level = [(50, 50, '1', (255, 255, 255), (255, 100, 50), 0),
                (100, 50, '2', (255, 255, 255), (255, 100, 50), 1),
                (150, 50, '3', (255, 255, 255), (255, 100, 50), 2),
                (200, 50, '4', (255, 255, 255), (255, 100, 50), 3),
                (250, 50, '5', (255, 255, 255), (255, 100, 50), 4)]


class Menu():
    def __init__(self, points):
        self.points = points

    def render(self, screen, number_points):
        font_name = pygame.font.Font(None, 80)
        screen.blit(font_name.render(
            'Battle Tank', True, (255, 100, 50)), (98, 100))
        font = pygame.font.Font(None, 50)
        for i in self.points:
            if number_points == i[5]:
                screen.blit(font.render(i[2], True, i[4]), (i[0], i[1]))
            else:
                screen.blit(font.render(i[2], True, i[3]), (i[0], i[1]))

    def menu(self, screen):
        point = 0
        done = True
        while done:
            screen.fill((0, 0, 0))
            mp = pygame.mouse.get_pos()
            for i in self.points:
                if mp[0] > i[0] and mp[0] < i[0] + 155 and \
                        mp[1] > i[1] and mp[1] < i[1] + 50:
                    point = i[5]
            self.render(screen, point)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        sys.exit()
                    if e.key == pygame.K_UP:
                        if point > 0:
                            point -= 1
                    if e.key == pygame.K_DOWN:
                        if point < len(self.points) - 1:
                            point += 1
                    if e.key == pygame.K_RETURN:
                        if point == 0:
                            done = False
                        else:
                            sys.exit()

                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if point == 0:
                        done = False
                    elif point == 1:
                        sys.exit()

            screen.blit(screen, (0, 0))
            pygame.display.flip()


class Select_level():
    def __init__(self, points_level):
        self.points = points_level

    def render(self, screen, number_points):
        font = pygame.font.Font(None, 50)
        for i in self.points:
            if number_points == i[5]:
                screen.blit(font.render(i[2], True, i[4]), (i[0], i[1]))
            else:
                screen.blit(font.render(i[2], True, i[3]), (i[0], i[1]))

    def sel_level(self, screen):
        point = 0
        done = True
        while done:
            screen.fill((0, 0, 0))

            mp = pygame.mouse.get_pos()
            for i in self.points:
                if mp[0] > i[0] and mp[0] < i[0] + 50 and \
                        mp[1] > i[1] and mp[1] < i[1] + 50:
                    point = i[5]
            self.render(screen, point)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        sys.exit()
                    if e.key == pygame.K_LEFT:
                        if point > 0:
                            point -= 1
                    if e.key == pygame.K_RIGHT:
                        if point < len(self.points) - 1:
                            point += 1
                    if e.key == pygame.K_RETURN:
                        if point <= 0:
                            done = False
                            return '2_lvl.map'
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if point <= 0:
                        done = False
                        return '1_lvl.map'
                    elif point == 1:
                        done = False
                        return '2_lvl.map'
                    elif point == 2:
                        done = False
                        return '3_lvl.map'
                    elif point == 3:
                        done = False
                        return '4_lvl.map'
                    elif point == 4:
                        done = False
                        return '5_lvl.map'
            screen.blit(screen, (0, 0))
            pygame.display.flip()


def gameover(screen):
    screen.fill((0, 0, 0))
    load_sound('dead_music.mp3')
    pygame.mixer.music.play()
    image = load_image('game_over.png')
    image_rect = image.get_rect()
    screen.blit(image, image_rect)
    pygame.display.flip()
    pygame.time.wait(3000)
    start()


def win(screen):
    # global screen
    size = 500, 500
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 100)
    text = font.render('You Win!', True, (255, 100, 50))
    text_x = size[0] // 2 - text.get_width() // 2
    text_y = size[1] // 2 - text.get_height() // 2
    screen.blit(text, (text_x, text_y))
    pygame.display.flip()
    pygame.time.wait(3000)
    start()


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


def create_particles(position):
    # количество создаваемых частиц
    particle_count = 20
    # возможные скорости
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    fire = [load_image("explosion.png")]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(particle_group)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой (значение константы)
        self.gravity = 1

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(screen_rect):
            self.kill()


def generate_level(level):
    global enemys
    enemys = []
    global collisions
    collisions = []
    global all_sprites
    all_sprites = pygame.sprite.Group()
    global particle_group
    particle_group = pygame.sprite.Group()
    global tiles_group
    tiles_group = pygame.sprite.Group()
    global player_group
    player_group = pygame.sprite.Group()
    global player_bullets
    player_bullets = 0
    global pl_xp
    pl_xp = 5
    global turn
    turn = 1100
    global bullets
    bullets = []
    global alive_tanks
    alive_tanks = 0
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

            if level[y][x] == '*':
                Tile('empty', x, y)
                enemys.append(Enemy(x, y, 3))
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
    load_sound('music.mp3')
    pygame.mixer.music.play()
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
        global bullets, pl_x, pl_y

    def update(self):
        if pygame.sprite.spritecollideany(self, all_sprites):
            return False
        else:
            return True

    def check(self, screen):
        for i in range(len(bullets) - 1, -1, -1):

            el = bullets[i]
            if pl_x < el.x < pl_x + 50 and \
                    pl_y < el.y < pl_y + 50 and not (el.isplayer):
                del bullets[i]
                global pl_xp
                pl_xp -= 1
                create_particles((pl_x, pl_y))
            if pl_xp <= 0:
                gameover(screen)


class CollisionBullet():
    def __init__(self, pos_x=None, pos_y=None):
        global bullets
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


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x=None, pos_y=None, type=3):
        super().__init__(player_group)
        # global previous_time
        self.hp = type
        self.type = str(type)

        self.image = load_image('enemy_tank_0_' + self.type + '.png')
        self.pos_x = pos_x * 50
        self.pos_y = pos_y * 50

        self.alivee = True
        self.last_der = -1
        global bullets, pl_x, pl_y

    def shoot(self):
        sound2.play()
        bullets.append(Snaryad(round(self.pos_x + 50 // 2),
                               round(self.pos_y + 50 // 2), 3, (0, 0, 0),
                               self.last_der, False))

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
                create_particles((self.pos_x, self.pos_y))
        if self.hp <= 0:
            self.pos_y = 1000
            self.pos_x = 1000
            if self.alivee:
                alive_tanks -= 1
                sound1.play()
            self.alivee = False

    def move(self):
        previous_time2 = 0
        current_time2 = pygame.time.get_ticks()
        if current_time2 - previous_time2 > 500:
            if randint(0, 1000) > 900:
                if self.last_der == -2 and self.pos_y > pl_y and \
                        abs(self.pos_x - pl_x) <= 50:
                    self.shoot()
                    previous_time = pygame.time.get_ticks()
                if self.last_der == 2 and self.pos_y < pl_y and \
                        abs(self.pos_x - pl_x) <= 50:
                    self.shoot()
                    previous_time = pygame.time.get_ticks()
                if self.last_der == -1 and self.pos_x > pl_x and \
                        abs(self.pos_y - pl_y) <= 50:
                    self.shoot()
                    previous_time = pygame.time.get_ticks()
                if self.last_der == 1 and self.pos_x < pl_x and \
                        abs(self.pos_y - pl_y) <= 50:
                    self.shoot()
                    previous_time = pygame.time.get_ticks()

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

    def draw(self, screen):
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

    def draw(self, screen):
        screen.blit(self.image, (self.x - 25, self.y - 25))


bullets = []
pl_x, pl_y = 200, 400


def start():
    global pl_xp
    global alive_tanks
    global start_ticks
    global pl_x, pl_y
    global lastMove
    pl_xp = 5
    size = 500, 500
    screen = pygame.display.set_mode(size)
    pl_x, pl_y = 200, 400
    wind = Menu(points)
    wind.menu(screen)
    sel_lvl = Select_level(points_level)
    lvl_map = sel_lvl.sel_level(screen)
    level_map = load_level(lvl_map)
    hero, max_x, max_y = generate_level(level_map)
    speed = 1
    running = True
    player_image = load_image('test_tank_0.png')
    font = pygame.font.Font(None, 30)
    while running:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                running = False
        if alive_tanks == 0:
            win(screen)
        proverka = Player(pl_x, pl_y)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            sound2.play()
            if lastMove == 'up':
                direction = -2
            elif lastMove == 'down':
                direction = +2
            elif lastMove == 'right':
                direction = 1
            elif lastMove == 'left':
                direction = -1

            if (pygame.time.get_ticks() - start_ticks) / 1000 > 0.5:
                bullets.append(Snaryad(round(pl_x + 50 // 2),
                                       round(pl_y + 50 // 2), 3, (0, 0, 0),
                                       direction, True))
                start_ticks = pygame.time.get_ticks()

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
        if proverka.update():
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
        screen.fill((0, 0, 0))
        proverka.check(screen)
        for i in range(len(collisions)):
            collisions[i].check()
        tiles_group.draw(screen)
        for i in range(len(enemys)):
            enemys[i].draw(screen)
        screen.blit(player_image, (pl_x, pl_y))
        for bullet in bullets:
            bullet.draw(screen)
        particle_group.update()
        particle_group.draw(screen)
        screen.blit(font.render(f'Здоровье: {str(pl_xp)}', True, (0, 0, 0)), (375, 5))
        clock.tick(fps)
        pygame.display.update()


pygame.quit()

if __name__ == '__main__':
    pygame.init()
    start()
