import os
import sys
import random
import pygame

# Изображение не получится загрузить
# без предварительной инициализации pygame
pygame.init()
GRAVITY = 0.1
size = width, height = 500, 500
screen = pygame.display.set_mode(size)


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


# class AnimatedSprite(pygame.sprite.Sprite):
#     def __init__(self, sheet, columns, rows, x, y, delta=1):
#         super().__init__(all_sprites)
#         self.frames = []
#         self.cut_sheet(sheet, columns, rows)
#         self.cur_frame = 0
#         self.image = self.frames[self.cur_frame]
#         self.rect = self.rect.move(x, y)
#         self.delta = delta
#         self.time = 0
#
#     def cut_sheet(self, sheet, columns, rows):
#         self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
#                                 sheet.get_height() // rows)
#         for j in range(rows):
#             for i in range(columns):
#                 frame_location = (self.rect.w * i, self.rect.h * j)
#                 self.frames.append(sheet.subsurface(pygame.Rect(
#                     frame_location, self.rect.size)))
#
#     def update(self):
#         self.time += 1
#         if self.time == self.delta:
#             self.time = 0
#             self.cur_frame = (self.cur_frame + 1) % len(self.frames)
#             self.image = self.frames[self.cur_frame]


# class Dino(AnimatedSprite):
#     def __init__(self, x, y):
#         super(Dino, self).__init__(load_image("pygame-8-1.png"), 8, 1, x, y)


# class Hero(AnimatedSprite):
#     def __init__(self, x, y, delta):
#         super(Hero, self).__init__(load_image("hero.png", 400, 200, colorkey=-1), 6, 1, x, y, delta)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)


screen_rect = (0, 0, width, height)


# class Particle(pygame.sprite.Sprite):
#     # сгенерируем частицы разного размера
#     fire = [load_image("star.png")]
#     for scale in (5, 10, 20):
#         fire.append(pygame.transform.scale(fire[0], (scale, scale)))
#
#     def __init__(self, pos, dx, dy):
#         super().__init__(all_sprites)
#         # гравитация будет одинаковой (значение константы)
#         self.gravity = GRAVITY
#         self.start_velocity = [dx, dy]
#         self.pos = pos
#         self.start()
#
#     def start(self):
#         self.image = random.choice(self.fire)
#         self.rect = self.image.get_rect()
#         self.rect.x, self.rect.y = self.pos
#         self.velocity = self.start_velocity.copy()
#
#     def update(self):
#         # применяем гравитационный эффект:
#         # движение с ускорением под действием гравитации
#         self.velocity[1] += self.gravity
#         # перемещаем частицу
#         self.rect.x += self.velocity[0]
#         self.rect.y += self.velocity[1]
#         # убиваем, если частица ушла за экран
#         if not self.rect.colliderect(screen_rect):
#             self.start()


# def create_particles(position):
#     # количество создаваемых частиц
#     particle_count = 20
#     # возможные скорости
#     numbers_x = range(-5, 6)
#     numbers_y = range(-5, 0)
#     numbers = range(-5, 6)
#     for _ in range(particle_count):
#         Particle(position, random.choice(numbers_x), random.choice(numbers_y))


clock = pygame.time.Clock()
running = True
all_sprites = pygame.sprite.Group()
# c = Dino(10, 10)
h = Hero(200, 200, 5)
create_particles((50, 50))
fps = 100
pygame.display.set_caption("Герой двигается!")
# pygame.mouse.set_visible(False)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))
    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(fps)