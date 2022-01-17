import os
import sys
import time
import datetime

import pygame
import random

pygame.init()
pygame.key.set_repeat(200, 70)

FPS = 100
WIDTH = 700
HEIGHT = 650
STEP = 30
STEPEN = 10
LEFT_IND = 50
TOP_IND = 50
number_dungeon = 1
number_location = 1

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

player = None
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
spikes_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
healths_group = pygame.sprite.Group()
dropable_group = pygame.sprite.Group()


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


def load_level(number_dungeon, number_location):
    filename = "data/dungeons/dungeon_" + str(number_dungeon) + '/location_' + str(number_location) + '.txt'
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # дополняем каждую строку пустыми клетками ('.')
    return level_map


def generate_level(level):
    new_player, new_enemies, x, y = None, [], None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            # Floors
            if level[y][x] == '.':
                Tile('floor_' + str(random.choice([1, 1, 1, 2, 3, 4, 9])), x, y)
            # Walls

            # Doors
            elif level[y][x] == '*':
                Spikes(x, y)

            elif level[y][x] == '[':
                Wall('wall_left', x, y - 1)
            elif level[y][x] == ']':
                Wall('wall_right', x, y - 1)

            elif level[y][x] == '{':
                Tile('wall_side_left_top', x, y - 1)
            elif level[y][x] == '}':
                Tile('wall_side_right_top', x, y - 1)

            elif level[y][x] == '(':
                Tile('wall_side_left_bottom', x, y - 1)
            elif level[y][x] == ')':
                Tile('wall_side_right_bottom', x, y - 1)

            elif level[y][x] == '<':
                Wall('wall_' + random.choice(['1', '1', '2', '3', 'crack']), x, y)
                Wall('wall_top_inner_right_2', x, y - 1)
            elif level[y][x] == '>':
                Wall('wall_' + random.choice(['1', '1', '2', '3', 'crack']), x, y)
                Wall('wall_bottom_left', x, y - 1)

            elif level[y][x] == ';':
                Wall('wall_' + random.choice(['1', '1', '2', '3', 'crack']), x, y)
                Wall('wall_top_inner_left_2', x, y - 1)
            elif level[y][x] == ':':
                Wall('wall_' + random.choice(['1', '1', '2', '3', 'crack']), x, y)
                Wall('wall_bottom_right', x, y - 1)
            elif level[y][x] == '#':
                Wall('wall_' + random.choice(['1', '1', '2', '3', 'crack']), x, y)
                Wall('wall_top', x, y - 1)

            elif level[y][x] == '+':
                Wall('wall_' + random.choice(['1', '1', '2', '3', 'crack']), x, y)
                Wall('wall_bottom', x, y - 1)
            # Hero
            elif level[y][x] == '@':
                Tile('floor_1', x, y)
                new_player = Player(x, y)
            # Enemies
            elif level[y][x] == '!':
                Tile('floor_1', x, y)
                new_enemies.append(Enemie_Goblin(x, y))
            elif level[y][x] == '&':
                Tile('floor_1', x, y)
                new_enemies.append(Enemie_Slime(x, y))


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    fon = pygame.transform.scale(load_image('ui (new)/start_screen.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    pygame.display.set_caption('Dark Lifes')
    font = pygame.font.Font(None, 70)
    text = font.render("  PLAY", True, (255, 62, 61))
    text_x = 480
    text_y = 120
    text_w = text.get_width()
    text_h = text.get_height()
    pygame.draw.rect(screen, (0, 28, 40), (text_x - 10, text_y - 10,
                                           text_w + 50, text_h + 20), 0)
    screen.blit(text, (text_x, text_y))
    text_x_2 = 480
    text_y_2 = 210
    font = pygame.font.Font(None, 70)
    text = font.render("  HELP", True, (255, 62, 61))
    pygame.draw.rect(screen, (0, 28, 40), (text_x_2 - 10, text_y_2 - 10,
                                           text_w + 50, text_h + 20), 0)
    screen.blit(text, (text_x_2, text_y_2))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if text_x - 10 <= event.pos[0] <= (text_x - 10) + (text_w + 50) and \
                            text_y - 10 <= event.pos[1] <= (text_y - 10) + (text_h + 20):
                        if final_flag:
                            file = open("save_data.txt", "r+", encoding='utf-8')
                            file.truncate()
                            file.close()
                        return
                    elif text_x_2 - 10 <= event.pos[0] <= (text_x_2 - 10) + (text_w + 50) and \
                            text_y_2 - 10 <= event.pos[1] <= (text_y_2 - 10) + (text_h + 20):
                        help_screen()
                        return
        pygame.display.flip()
        clock.tick(FPS)


def help_screen():
    fon = pygame.transform.scale(load_image('ui (new)/help_screen.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    pygame.display.set_caption('Dark Lifes')
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start_screen()
                    return
        pygame.display.flip()
        clock.tick(FPS)


def final_screen():
    global final_flag, number_dungeon, number_location, player, healths
    if player.hp > 0:
        final_flag = True
        fon = pygame.transform.scale(load_image('ui (new)/final_screen_win.png'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        pygame.display.set_caption('Dark Lifes')
        font = pygame.font.Font(None, 50)
        font_2 = pygame.font.Font(None, 30)
        text = font.render(f"Количество убийств: {len(murders_numbers)}", True, (255, 62, 61))
        text_2 = font_2.render(f"Количество пройденных подземелий, локаций: {number_dungeon}, {number_location}", True,
                               (255, 62, 61))
        now_date = datetime.datetime.today()
        game_timer_2 = datetime.timedelta(hours=now_date.hour, minutes=now_date.minute,
                                          seconds=now_date.second)
        if delta != 0:
            text_3 = font.render(f"Общее время: {game_timer_2 - game_timer + deltas}", True, (255, 62, 61))
        else:
            text_3 = font.render(f"Общее время: {game_timer_2 - game_timer}", True, (255, 62, 61))
        text_x = 113
        text_y = 236
        text_4 = font.render(f'Нажмите "Enter"', True, (255, 62, 61))
        screen.blit(text, (text_x, text_y))
        screen.blit(text_2, (text_x, text_y + 60))
        screen.blit(text_3, (text_x, text_y + 120))
        screen.blit(text_4, (text_x, text_y + 180))
    else:
        final_flag = True
        fon = pygame.transform.scale(load_image('ui (new)/final_screen_over.png'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        pygame.display.set_caption('Dark Lifes')
        font = pygame.font.Font(None, 50)
        font_2 = pygame.font.Font(None, 30)
        text = font.render(f"Количество убийств: {len(murders_numbers)}", True, (255, 62, 61))
        text_2 = font_2.render(f"Количество пройденных подземелий, локаций: {number_dungeon}, {number_location}", True,
                               (255, 62, 61))
        now_date = datetime.datetime.today()
        game_timer_2 = datetime.timedelta(hours=now_date.hour, minutes=now_date.minute,
                                          seconds=now_date.second)
        if deltas != 0:
            text_3 = font.render(f"Общее время: {game_timer_2 - game_timer + deltas}", True, (255, 62, 61))
        else:
            text_3 = font.render(f"Общее время: {game_timer_2 - game_timer}", True, (255, 62, 61))
        text_x = 113
        text_y = 236
        font_3 = pygame.font.Font(None, 30)
        text_4 = font_3.render(f'Нажмите "Пробел", если хотите выйти в главное меню', True, (255, 62, 61))
        text_5 = font_3.render(f'Нажмите "B", если хотите начать заново', True, (255, 62, 61))
        screen.blit(text, (text_x, text_y))
        screen.blit(text_2, (text_x, text_y + 60))
        screen.blit(text_3, (text_x, text_y + 120))
        screen.blit(text_4, (text_x, text_y + 180))
        screen.blit(text_5, (text_x, text_y + 240))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start_screen()
                    number_dungeon = 1
                    number_location = 1
                    player.hp = 100
                    for sprt in all_sprites:
                        if sprt not in player_group:
                            sprt.kill()
                    level = load_level(number_dungeon, number_location)
                    player, goblins, level_x, level_y = generate_level(level)
                    player.kill()
                    player = now_player
                    player.rect.x = 275
                    player.rect.y = 351
                    for goblin in goblins:
                        goblin.add_weapon(sword_for_goblin)
                    camera = Camera((level_x, level_y))
                    healths.kill()
                    healths = Health_Player("health_5")
                    return
                elif event.key == pygame.K_b:
                    number_dungeon = 1
                    number_location = 1
                    player.hp = 100

        pygame.display.flip()
        clock.tick(FPS)


list_top = []
list_left = []
list_bottom = []
list_right = []

tile_images = {'wall_top': load_image('tiles/wall/wall_top_1.png', 60, 60),
               'wall_left': load_image('tiles/wall/wall_top_left.png', 60, 60),
               'wall_right': load_image('tiles/wall/wall_top_right.png', 60, 60),
               'wall_bottom': load_image('tiles/wall/wall_bottom.png', 60, 60),

               'wall_bottom_left': load_image('tiles/wall/wall_bottom_left.png', 60, 60),
               'wall_bottom_right': load_image('tiles/wall/wall_bottom_right.png', 60, 60),

               'wall_side_left_top': load_image('tiles/wall/wall_top_inner_left.png', 60, 60),
               'wall_side_right_top': load_image('tiles/wall/wall_top_inner_right.png', 60, 60),
               'wall_side_left_bottom': load_image('tiles/wall/wall_bottom_inner_left.png', 60, 60),
               'wall_side_right_bottom': load_image('tiles/wall/wall_bottom_inner_right.png', 60, 60),

               'wall_top_inner_right_2': load_image('tiles/wall/wall_top_inner_right_2.png', 60, 60),
               'wall_top_inner_left_2': load_image('tiles/wall/wall_top_inner_left_2.png', 60, 60),

               'wall_1': load_image('tiles/wall/wall_1.png', 60, 60),
               'wall_2': load_image('tiles/wall/wall_2.png', 60, 60),
               'wall_3': load_image('tiles/wall/wall_3.png', 60, 60),
               'wall_crack': load_image('tiles/wall/wall_crack.png', 60, 60),

               'floor_1': load_image('tiles/floor/floor_1.png', 60, 60),
               'floor_2': load_image('tiles/floor/floor_2.png', 60, 60),
               'floor_3': load_image('tiles/floor/floor_3.png', 60, 60),
               'floor_4': load_image('tiles/floor/floor_4.png', 60, 60),
               'floor_5': load_image('tiles/floor/floor_5.png', 60, 60),
               'floor_6': load_image('tiles/floor/floor_6.png', 60, 60),
               'floor_7': load_image('tiles/floor/floor_7.png', 60, 60),
               'floor_8': load_image('tiles/floor/floor_8.png', 60, 60),
               'floor_9': load_image('tiles/floor/floor_9.png', 60, 60),

               'door': load_image('tiles/wall/door_anim_opening_f0.png', 60, 60)}

player_image_right = load_image('heroes/knight/knight_idle_anim_f0.png', 60, 60)
player_image_left = pygame.transform.flip(player_image_right, True, False)

spikes_up = load_image('tiles/floor/spikes_anim_f9.png', 60, 60)
spikes_down = load_image('tiles/floor/spikes_anim_f0.png', 60, 60)

health_player = {"health_1": load_image('ui (new)/health_ui.png', 250, 50),
                 "health_2": load_image('ui (new)/health_ui_2.png', 250, 50),
                 "health_3": load_image('ui (new)/health_ui_3.png', 250, 50),
                 "health_4": load_image('ui (new)/health_ui_4.png', 250, 50),
                 "health_5": load_image('ui (new)/health_ui_5.png', 250, 50)}

enemies = {'enemie_goblin': load_image('enemies/goblin/goblin_idle_anim_f0.png', 60, 60),
           'enemie_slime': load_image('enemies/slime/slime_idle_anim_f0.png', 60, 60)}

drop_objects = [load_image('props_itens\potion_green.png', 50, 50),
                load_image('props_itens\potion_red.png', 50, 50), load_image('props_itens\potion_yellow.png', 50, 50)]

flag_moves_enemys = True

tile_width = tile_height = 60


class DropableObjects(pygame.sprite.Sprite):
    def __init__(self, drop_ob, pos_x, pos_y):
        super().__init__(dropable_group, all_sprites)
        self.image = drop_ob
        self.rect = self.image.get_rect().move(pos_x, pos_y)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(LEFT_IND + tile_width * pos_x, TOP_IND + tile_height * pos_y)


class Wall(Tile):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tile_type, pos_x, pos_y)
        self.proverka(tile_type, self.rect)

    def proverka(self, tile_type, rect):
        if tile_type in ["wall_1", "wall_2", "wall_3", "wall_crack"]:
            list_top.append(rect)
            list_left.append(rect)
            if len(list_top) == 11:
                list_right.append(rect)
        if tile_type == "wall_left":
            list_left.append(rect)
        if tile_type == "wall_bottom" or tile_type == "wall_bottom_left":
            list_bottom.append(rect)
        if tile_type == "wall_right":
            list_right.append(rect)
        if tile_type == "wall_top_inner_right_2":
            list_right.append(rect)
            list_left.append(rect)
        if tile_type == "wall_top":
            list_left.append(rect)


class Health_Player(pygame.sprite.Sprite):
    def __init__(self, health_number):
        super().__init__(tiles_group, healths_group)
        self.image = health_player[health_number]
        self.rect = self.image.get_rect().move(10, 10)


class Spikes(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(spikes_group, all_sprites)
        self.image = spikes_up
        self.rect = self.image.get_rect().move(LEFT_IND + tile_width * pos_x, TOP_IND + tile_height * pos_y)
        list_right.append(self.rect)
        list_left.append(self.rect)


class Weapon:
    def __init__(self, name, damage, range):
        self.name = name
        self.damage = damage
        self.range = range

    def hit(self, actor, target):
        if (self.range ** 2 >= (target.rect.x - actor.rect.x) ** 2 +
                (target.rect.y - actor.rect.y) ** 2):
            if isinstance(target, BaseEnemy):
                print(f'Врагу нанесен урон оружием {self.name} в размере {self.damage}')
            else:
                print(f'Вам нанесен урон оружием {self.name} в размере {self.damage}')
            target.hp -= self.damage
            if not target.is_alive():
                if isinstance(target, BaseEnemy):
                    if selection == "+":
                        x, y = target.rect.x, target.rect.y
                        drop = DropableObjects(random.choice(drop_objects), x, y)
                        drop_list.append(drop)
                    target.kill()
                   goblins.remove(target)
                else:
                    target.kill()
                    final_screen()
            print(target.hp)
        else:
            print(f'Враг слишком далеко для оружия {self.name}')

    def __str__(self):
        return self.name



class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image_right
        self.rect = self.image.get_rect().move(LEFT_IND + tile_width * pos_x + 16, TOP_IND + tile_height * pos_y + 5)
        self.hp = 100
        self.player_weapons = [sword_for_player]
        self.eqip_weapon = 0

    def hit(self, target):
        self.player_weapons[self.eqip_weapon].hit(self, target)

    def add_weapon(self, weapon):
        if isinstance(weapon, Weapon):
            self.player_weapons.append(weapon)
            print('Подобрал', weapon)
        else:
            print('Это не оружие')

    def next_weapon(self):
        if len(self.player_weapons) == 0:
            print('Я безоружен')
        elif len(self.player_weapons) == 1:
            print('У меня только одно оружие')
        else:
            self.eqip_weapon += 1
            if self.eqip_weapon == len(self.player_weapons):
                self.eqip_weapon = 0
            print(f'Сменил оружие на {self.player_weapons[self.eqip_weapon]}')

    def is_alive(self):
        return self.hp > 0

    def get_damage(self, amount):
        if self.is_alive():
            self.hp -= amount


class BaseEnemy(pygame.sprite.Sprite):
    def __init__(self, name_enemie, pos_x, pos_y):
        super().__init__(enemies_group, all_sprites)
        self.image = enemies[name_enemie]
        self.rect = self.image.get_rect().move(LEFT_IND + tile_width * pos_x + 15, TOP_IND + tile_height * pos_y + 5)
        self.enemie_weapons = []
        self.eqip_weapon = 0
        self.hp = 30

    def is_alive(self):
        return self.hp > 0

    def get_damage(self, amount):
        if self.is_alive():
            self.hp -= amount

    def add_weapon(self, weapon):
        if isinstance(weapon, Weapon):
            self.enemie_weapons.append(weapon)
            print('Подобрал', weapon, "(гоблин)")
        else:
            print('Это не оружие')

    def hit(self, target):
        self.enemie_weapons[self.eqip_weapon].hit(self, target)


class Enemie_Goblin(BaseEnemy):
        super().__init__('enemie_goblin', pos_x, pos_y)
        self.enemie_weapons.append(sword_for_goblin)
        self.hp = 50


class Enemie_Slime(BaseEnemy):
    def __init__(self, pos_x, pos_y):
        super().__init__('enemie_slime', pos_x, pos_y)
        self.enemie_weapons.append(slize_for_slime)


class Camera:
    # зададим начальный сдвиг камеры и размер поля для возможности реализации циклического сдвига
    def __init__(self, field_size):
        self.dx = 0
        self.dy = 0
        self.field_size = field_size

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


start_screen()

pygame.display.set_caption('Dark Lifes')
# Оружия
sword_for_player = Weapon('Меч', 10, 100)
sword_for_goblin = Weapon('Меч', 8, 100)
slize_for_slime = Weapon('Меч', 4, 100)
healths = Health_Player("health_5")
# Таймеры
ENEMIEGOEVENT = pygame.USEREVENT + 1
pygame.time.set_timer(ENEMIEGOEVENT, 100)
MYEVENTTYPE = pygame.USEREVENT + 1
pygame.time.set_timer(MYEVENTTYPE, 1000)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if not final_flag:
                f = open("save_data.txt", "r+", encoding='utf-8')
                f.truncate()
                f.close()
                f = open("save_data.txt", "w+", encoding='utf-8')
                dates = datetime.datetime.today()
                date = datetime.timedelta(hours=dates.hour, minutes=dates.minute, seconds=int(dates.second))
                f.write(
                    f"{str(number_dungeon)}\n{str(number_location)}\n{str(date - game_timer)}\n{str(len(murders_numbers))}\n{str(player.hp)}")
                f.close()
            final_flag = False
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player.image = player_image_left
                for lt in list_left:
                    if player.rect.collidepoint(lt.bottomright):
                        break
                else:
                    player.rect.x -= STEP
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player.image = player_image_right
                for r in list_right:
                    if list_right[0] == r:
                        if player.rect.collidepoint(0, r.left) or player.rect.collidepoint(r.topleft):
                            break
                    else:
                        if player.rect.collidepoint(r.bottomleft) or \
                                player.rect.collidepoint(0, r.left) or player.rect.collidepoint(r.topleft):
                            break
                else:
                    player.rect.x += STEP
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                for h in list_top:
                    if player.rect.collidepoint(h.center[0], h.center[1] + 10):
                        break
                else:
                    player.rect.y -= STEP
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                for b in list_bottom:
                    if player.rect.collidepoint(b.top + 30, b.left):
                        break
                else:
                    player.rect.y += STEP

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for enemie in enemies_group:
                    player.hit(enemie)

        if time_flag and player.eqip_weapon == 1:
            time_flag = False
            pygame.time.set_timer(SUPERSWORD, 10000)

        if player.eqip_weapon == 1 and event.type == SUPERSWORD:
            player.eqip_weapon = 0
            print("Действия зелёного зелья закончилось")

        for drops in drop_list:
            if drops.rect.colliderect(player.rect):
                if drop_objects.index(drops.image) == 0:
                    delta = random.choice([-25, 25])
                    player.hp += delta
                    if delta < 0:
                        print("Вам подобрали отравленное зелье, на -25 жизней")
                    else:
                        print("Вам подобрали полезное зелье, на +25 жизней")
                    if 50 < player.hp <= 75:
                        healths.kill()
                        healths = Health_Player("health_4")
                    elif 25 < player.hp <= 50:
                        healths.kill()
                        healths = Health_Player("health_3")
                    elif 0 < player.hp <= 25:
                        healths.kill()
                        healths = Health_Player("health_2")
                    print("Вы подобрали зелье случайного изменения жизней")
 for drops in drop_list:
            if drops.rect.colliderect(player.rect):
                if drop_objects.index(drops.image) == 2:
                    player.hp = 100
                    healths.kill()
                    healths = Health_Player("health_5")
                    print("Вы подобрали зелье восстановления здоровья")
                elif drop_objects.index(drops.image) == 2:
                    if player.eqip_weapon != 1:
                        sword_for_player_2 = Weapon('Меч', 20, 120)
                        player.add_weapon(sword_for_player_2)
                        player.eqip_weapon = 1
                        print("Вы подобрали зелье, дающее супер меч на некоторое время")
                drops.kill()
                drop_list.remove(drops)
        for enemie in enemies_group:
            if event.type == ENEMIEGOEVENT:
                player_x, player_y = player.rect.x, player.rect.y
                enemie_x, enemie_y = enemie.rect.x, enemie.rect.y
                ans = pygame.sprite.spritecollide(enemie, enemies_group, False)
                if len(ans) == 1:
                    if player_x + STEPEN * 2 - 10 >= enemie_x:
                        enemie.rect.x += STEPEN
                    if player_y + STEPEN * 2 - 10 >= enemie_y:
                        enemie.rect.y += STEPEN
                    if player_x + STEPEN * 2 - 10 <= enemie_x:
                        enemie.rect.x -= STEPEN
                    if player_y + STEPEN * 2 - 10 <= enemie_y:
                        enemie.rect.y -= STEPEN
                else:
                    enemie.rect.x += random.choice([-STEPEN, STEPEN, -STEPEN * 2, STEPEN * 2])
                    enemie.rect.y += random.choice([-STEPEN, STEPEN, -STEPEN * 2, STEPEN * 2])
        if event.type == MYEVENTTYPE:
            for goblin in goblins:
                goblin.hit(player)
                if player.is_alive():
                    if 50 < player.hp <= 75:
                        healths.kill()
                        healths = Health_Player("health_4")
                    elif 25 < player.hp <= 50:
                        healths.kill()
                        healths = Health_Player("health_3")
                    elif 0 < player.hp <= 25:
                        healths.kill()
                        healths = Health_Player("health_2")
        if len(enemies_group) == 0:
            for spike in spikes_group:
                if spike.rect.x >= 400:
                    spike.image = spikes_down
                    try:
                        list_right.remove(spike)
                        list_left.remove(spike)
                    except:
                        pass
            ans = pygame.sprite.spritecollide(player, spikes_group, False)
            if len(ans) >= 4:
                number_location += 1
                if number_location > 10:
                    number_dungeon += 1
                now_player = player
                for sprt in all_sprites:
                    if sprt not in player_group:
                        sprt.kill()
                level = load_level(number_dungeon, number_location)
                player, goblins, level_x, level_y = generate_level(level)
                player.kill()
                player = now_player
                player.rect.x = 275
                player.rect.y = 351
                for goblin in goblins:
                    goblin.add_weapon(sword_for_goblin)
                camera = Camera((level_x, level_y))

    camera.update(player)

    for sprite in all_sprites:
        camera.apply(sprite)

    screen.fill(pygame.Color(124, 72, 36))
    spikes_group.draw(screen)
    tiles_group.draw(screen)
    enemies_group.draw(screen)
    dropable_group.draw(screen)
    player_group.draw(screen)
    healths_group.draw(screen)
    pygame.display.flip()

    clock.tick(FPS)

terminate()
