import os
import sys

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
exit_group = pygame.sprite.Group()


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


def load_level():
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
            elif level[y][x] == '%':
                Exit(x, y)
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
            elif level[y][x] == '$':
                Tile('floor_1', x, y)
                new_enemies.append(Enemie_Big_Ogre(x, y))
            elif level[y][x] == 'o':
                Tile('floor_1', x, y)
                new_enemies.append(Enemie_Masked_Orc(x, y))

    # вернем игрока, а также размер поля в клетках
    return new_player, new_enemies, x, y


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('ui (new)/start_screen.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    pygame.display.set_caption('Dark Lifes')
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('black'))
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

               'exit_dungeon': pygame.transform.flip(load_image('tiles/floor/stair_nextlevel.png', 60, 60), True,
                                                     False),

               'door': load_image('tiles/wall/door_anim_opening_f0.png', 60, 60)}

player_image_anim_right = load_image('heroes/knight/knight_run_spritesheet.png', 360, 60)
player_image_anim_left = pygame.transform.flip(player_image_anim_right, True, False)

spikes_anim = load_image('tiles/floor/spikes_spritesheet.png', 600, 60)

health_player = {"health_1": load_image('ui (new)/health_ui.png', 250, 50),
                 "health_2": load_image('ui (new)/health_ui_2.png', 250, 50),
                 "health_3": load_image('ui (new)/health_ui_3.png', 250, 50),
                 "health_4": load_image('ui (new)/health_ui_4.png', 250, 50),
                 "health_5": load_image('ui (new)/health_ui_5.png', 250, 50)}

enemies = {'enemie_goblin': load_image('enemies/goblin/goblin_run_spritesheet.png', 360, 60),
           'enemie_slime': load_image('enemies/slime/slime_run_spritesheeet.png', 360, 60),
           'enemie_big_ogre': load_image('enemies/big_ogre/ogre_run_animation.png', 360, 90, -1),
           'enemie_masked_orc': load_image('enemies/masked_orc/masked_orc_run_animation.png', 200, 50, -1),
           }

drop_objects = [load_image('props_itens/key_silver.png', 50, 50), load_image('props_itens/potion_green.png', 50, 50),
                load_image('props_itens/potion_red.png', 50, 50), load_image('props_itens/potion_yellow.png', 50, 50)]

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
            if number_location == 1:
                if len(list_top) == 11:
                    list_right.append(rect)
            else:
                if len(list_top) > 10:
                    if len(list_top) == 12:
                        list_left.append(rect)
                    elif len(list_top) == 13:
                        list_right.append(rect)
        elif tile_type == "wall_left" or tile_type == "wall_top_inner_left_2":
            list_left.append(rect)
        elif tile_type == "wall_bottom" or tile_type == "wall_bottom_left" or tile_type == "wall_bottom_right":
            list_bottom.append(rect)
        elif tile_type == "wall_right" or tile_type == "wall_top_inner_right_2":
            list_right.append(rect)


class Exit(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(exit_group, all_sprites)
        self.image = tile_images['exit_dungeon']
        self.rect = self.image.get_rect().move(LEFT_IND + tile_width * pos_x, TOP_IND + tile_height * pos_y)


class Health_Player(pygame.sprite.Sprite):
    def __init__(self, health_number):
        super().__init__(tiles_group, healths_group)
        self.image = health_player[health_number]
        self.rect = self.image.get_rect().move(10, 10)


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
                    selection = random.choice(["-", "+", "-", "+", "-"])
                    if selection == "+":
                        x, y = target.rect.x, target.rect.y
                        DropableObjects(random.choice(drop_objects), x, y)
                    target.kill()
                    all_enemies.remove(target)
                else:
                    target.kill()
            print(target.hp)
        else:
            print(f'Враг слишком далеко для оружия {self.name}')

    def __str__(self):
        return self.name


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, group_sprites, delta=1):
        super().__init__(group_sprites, all_sprites)
        self.frames = []
        self.cnt = 0
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.delta = delta
        self.time = 0

    def cut_sheet(self, sheet, columns, rows):
        if self.cnt == 0:
            self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                    sheet.get_height() // rows)
            self.cnt += 1
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.time += 1
        if self.time == self.delta:
            self.time = 0
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]


class Spikes(AnimatedSprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(spikes_anim, 10, 1, LEFT_IND + tile_width * pos_x, TOP_IND + tile_height * pos_y, spikes_group)
        self.UP_or_DOWN = False
        self.delta = 1
        for i in range(7):
            self.update()
        if self.rect.x >= 400:
            list_right.append(self.rect)
        else:
            list_left.append(self.rect)


class Player(AnimatedSprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_image_anim_right, 6, 1, LEFT_IND + tile_width * pos_x + 16,
                         TOP_IND + tile_height * pos_y + 5, player_group)
        self.hp = 100
        self.player_weapons = []
        self.eqip_weapon = 0
        self.delta = 2

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


class BaseEnemy(AnimatedSprite):
    def __init__(self, name_enemie, pos_x, pos_y, column=6, row=1):
        super().__init__(enemies[name_enemie], column, row, LEFT_IND + tile_width * pos_x + 15,
                         TOP_IND + tile_height * pos_y + 5, enemies_group)
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
    def __init__(self, pos_x, pos_y):
        super().__init__('enemie_goblin', pos_x, pos_y, column=6, row=1)
        self.enemie_weapons.append(sword_for_goblin)
        self.hp = 50


class Enemie_Slime(BaseEnemy):
    def __init__(self, pos_x, pos_y):
        super().__init__('enemie_slime', pos_x, pos_y, column=6, row=1)
        self.enemie_weapons.append(slize_for_slime)


class Enemie_Masked_Orc(BaseEnemy):
    def __init__(self, pos_x, pos_y):
        super().__init__('enemie_masked_orc', pos_x, pos_y, column=4, row=1)
        self.enemie_weapons.append(sword_for_masked_ork)
        self.hp = 40


class Enemie_Big_Ogre(BaseEnemy):
    def __init__(self, pos_x, pos_y):
        super().__init__('enemie_big_ogre', pos_x, pos_y, column=4, row=1)
        self.enemie_weapons.append(sword_for_big_ogre)
        self.hp = 80


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
sword_for_player = Weapon('Меч игрока', 10, 100)
sword_for_goblin = Weapon('Меч гоблина', 8, 100)
slize_for_slime = Weapon('Слизь', 4, 100)
sword_for_masked_ork = Weapon('Меч маленького орка', 4, 100)
sword_for_big_ogre = Weapon('Меч большого огра', 12, 100)
healths = Health_Player("health_5")
# Таймеры
ENEMIEGOEVENT = pygame.USEREVENT + 1
pygame.time.set_timer(ENEMIEGOEVENT, 300)
MYEVENTTYPE = pygame.USEREVENT + 2
pygame.time.set_timer(MYEVENTTYPE, 1200)

level = load_level()
player, all_enemies, level_x, level_y = generate_level(level)
player.add_weapon(sword_for_player)
camera = Camera((level_x, level_y))

running = True

animations_spikes_cnt = 0
L_or_R_or_S = 'stay'
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                for lt in list_left:
                    if player.rect.collidepoint(lt.bottomright):
                        break
                else:
                    if L_or_R_or_S == 'right' or L_or_R_or_S == 'stay':
                        L_or_R_or_S = 'left'
                        player.frames = []
                        player.cur_frame = 0
                        player.cut_sheet(player_image_anim_left, 6, 1)
                    player_group.update()
                    player.rect.x -= STEP

            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                for r in list_right:
                    if list_right[0] == r:
                        if player.rect.collidepoint(0, r.left) or player.rect.collidepoint(r.topleft):
                            break
                    else:
                        if player.rect.collidepoint(r.bottomleft) or \
                                player.rect.collidepoint(0, r.left) or player.rect.collidepoint(r.topleft):
                            break
                else:
                    if L_or_R_or_S == 'left' or L_or_R_or_S == 'stay':
                        L_or_R_or_S = 'right'
                        player.frames = []
                        player.cur_frame = 0
                        player.cut_sheet(player_image_anim_right, 6, 1)
                    player_group.update()
                    player.rect.x += STEP

            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                for h in list_top:
                    if player.rect.collidepoint(h.center[0], h.center[1] + 10):
                        break
                else:
                    player_group.update()
                    player.rect.y -= STEP

            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                for b in list_bottom:
                    if player.rect.collidepoint(b.top + 30, b.left):
                        break
                else:
                    player_group.update()
                    player.rect.y += STEP
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for enemie in enemies_group:
                    player.hit(enemie)

        if event.type == ENEMIEGOEVENT:
            for enemie in all_enemies:
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
                enemie.update()

        if event.type == MYEVENTTYPE:
            for enemie in all_enemies:
                enemie.hit(player)
                if not player.is_alive():
                    player.hp = 100
                    player = Player(5, 5)
                    player.hp = 100
                    healths.kill()
                    healths = Health_Player("health_5")
                    player.add_weapon(sword_for_player)
                else:
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
                    if not spike.UP_or_DOWN:
                        spike.UP_or_DOWN = True
                        for i in range(4):
                            spike.update()
                    try:
                        list_right.remove(spike)
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
                list_top = []
                list_left = []
                list_bottom = []
                list_right = []
                level = load_level()
                player, all_enemies, level_x, level_y = generate_level(level)
                player.kill()
                player = now_player
                player.rect.x = 275
                player.rect.y = 351
                camera = Camera((level_x, level_y))
                animations_spikes_cnt = 0

    camera.update(player)

    for sprite in all_sprites:
        camera.apply(sprite)

    screen.fill(pygame.Color(181, 83, 83))
    spikes_group.draw(screen)
    exit_group.draw(screen)
    tiles_group.draw(screen)
    enemies_group.draw(screen)
    player_group.draw(screen)
    healths_group.draw(screen)
    pygame.display.flip()

    clock.tick(FPS)

terminate()
