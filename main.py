import os
import sys
import pygame

pygame.init()
pygame.key.set_repeat(200, 70)

FPS = 100
WIDTH = 600
HEIGHT = 600
STEP = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

player = None
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()


def load_image(name, width=None, height=None, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    if width is not None and height is not None:
        image = pygame.transform.scale(image, (width, height))
    return image


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, new_enemie_goblin, x, y = None, None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            # Floors
            if level[y][x] == '.':
                Tile('floor1', x, y)
            if level[y][x] == ',':
                Tile('floor2', x, y)
            # Walls
            elif level[y][x] == '#':
                Tile('wall', x, y)
            # Doors
            elif level[y][x] == '*':
                Tile('door', x, y)
            # Hero
            elif level[y][x] == '@':
                Tile('floor1', x, y)
                new_player = Player(x, y)
            # Enemies
            elif level[y][x] == '!':
                Tile('floor1', x, y)
                Enemie_Goblin('enemie_goblin', x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('full tilemap.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    pygame.display.set_caption('Dark Lifes')
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


tile_images = {'wall': load_image('tiles/wall/wall_1.png', 50, 50),
               'floor1': load_image('tiles/floor/floor_1.png', 50, 50),
               'floor2': load_image('tiles/floor/floor_9.png', 50, 50),
               'door': load_image('tiles/wall/door_anim_opening_f0.png', 50, 50)}

player_image = load_image('heroes/knight/knight_idle_anim_f0.png', 50, 50)

enemies = {'enemie_goblin': load_image('enemies/goblin/goblin_idle_anim_f0.png', 50, 50)}

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)


class Enemie_Goblin(pygame.sprite.Sprite):
    def __init__(self, name_enemie, pos_x, pos_y):
        super().__init__(enemies_group, all_sprites)
        self.image = enemies[name_enemie]
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)


# class Camera:
#     # зададим начальный сдвиг камеры и размер поля для возможности реализации циклического сдвига
#     def __init__(self, field_size):
#         self.dx = 0
#         self.dy = 0
#         self.field_size = field_size
#
#     # сдвинуть объект obj на смещение камеры
#     def apply(self, obj):
#         obj.rect.x += self.dx
#         # вычислим координату клитки, если она уехала влево за границу экрана
#         if obj.rect.x < -obj.rect.width:
#             obj.rect.x += (self.field_size[0] + 1) * obj.rect.width
#         # вычислим координату клитки, если она уехала вправо за границу экрана
#         if obj.rect.x >= (self.field_size[0]) * obj.rect.width:
#             obj.rect.x += -obj.rect.width * (1 + self.field_size[0])
#         obj.rect.y += self.dy
#         # вычислим координату клитки, если она уехала вверх за границу экрана
#         if obj.rect.y < -obj.rect.height:
#             obj.rect.y += (self.field_size[1] + 1) * obj.rect.height
#         # вычислим координату клитки, если она уехала вниз за границу экрана
#         if obj.rect.y >= (self.field_size[1]) * obj.rect.height:
#             obj.rect.y += -obj.rect.height * (1 + self.field_size[1])
#
#     # позиционировать камеру на объекте target
#     def update(self, target):
#         self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
#         self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


start_screen()
level = load_level("level_1.txt")
player, level_x, level_y = generate_level(level)
# camera = Camera((level_x, level_y))
pygame.display.set_caption('Dark Lifes')
running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and player.rect.x >= tile_width:
                player.rect.x -= STEP
            if event.key == pygame.K_RIGHT and player.rect.x <= tile_width * (len(level[0]) - 2):
                player.rect.x += STEP
            if event.key == pygame.K_UP and player.rect.y >= tile_height - player.rect.y // 2:
                player.rect.y -= STEP
            if event.key == pygame.K_DOWN and player.rect.y <= tile_height * (len(level) - 2):
                player.rect.y += STEP

    # camera.update(player)

    # for sprite in all_sprites:
    # camera.apply(sprite)

    screen.fill(pygame.Color(0, 0, 0))
    tiles_group.draw(screen)
    player_group.draw(screen)
    enemies_group.draw(screen)

    pygame.display.flip()

    clock.tick(FPS)

terminate()
