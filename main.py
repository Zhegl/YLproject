import os
import sys
import pygame

clock = pygame.time.Clock()

fps = 60
player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


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
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


tile_images = {
    'wall': load_image('brick.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('test_tank.png')

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


def load_level(filename):
    filename = filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


# left = False
# right = False
lastMove = 'up'


class Snaryad():
    def __init__(self, x, y, radius, color, direction):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.direction = direction
        self.vel = 5 * direction

    def draw(self, win):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)


if __name__ == '__main__':
    pygame.init()
    size = 500, 500
    screen = pygame.display.set_mode(size)
    level_map = load_level("map.map")
    hero, max_x, max_y = generate_level(level_map)
    pl_x = 500 // 2
    pl_y = 500 // 2
    speed = 1
    running = True
    bullets = []
    while running:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                running = False

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

            if len(bullets) < 1:
                bullets.append(Snaryad(round(pl_x + 50 // 2),
                                       round(pl_y + 50 // 2), 3, (0, 0, 0),
                                       direction))

        for bullet in bullets:
            if bullet.direction == 1 or bullet.direction == -1:
                if bullet.x < 500 and bullet.x > 0:
                    bullet.x += bullet.vel
                else:
                    bullets.pop(bullets.index(bullet))
            elif bullet.direction == 2:
                if bullet.y < 500 and bullet.y > 0:
                    bullet.y += bullet.vel - 5
                else:
                    bullets.pop(bullets.index(bullet))
            elif bullet.direction == -2:
                if bullet.y < 500 and bullet.y > 0:
                    bullet.y += bullet.vel + 5
                else:
                    bullets.pop(bullets.index(bullet))

        if keys[pygame.K_LEFT] and pl_x > 0:
            pl_x -= speed
            lastMove = 'left'
        elif keys[pygame.K_RIGHT] and pl_x < 450:
            pl_x += speed
            lastMove = 'right'
        elif keys[pygame.K_UP] and pl_y > 0:
            pl_y -= speed
            lastMove = 'up'
        elif keys[pygame.K_DOWN] and pl_y < 450:
            pl_y += speed
            lastMove = 'down'

        player_group.draw(screen)
        tiles_group.draw(screen)
        screen.blit(player_image, (pl_x, pl_y))
        for bullet in bullets:
            bullet.draw(screen)
        clock.tick(fps)
        pygame.display.update()
pygame.quit()
