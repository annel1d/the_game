import os
import random
import sys

import pygame
import pygame_gui
import sqlite3
from sqlite3 import Error
import datetime


def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
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
    return image


def load_level(filename):
    filename = "data/" + filename
    if not os.path.isfile(filename):
        print(f"Карта '{filename}' не найдена")
        sys.exit()
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


tile_images = {
    'wall': load_image('block.png'),
    'empty': load_image('dirt.png'),
    'grass': load_image('grass1.png'),
    'wood': load_image('wood1.png'),
    'list': load_image('list1.png'),
    'kust': load_image('kust.png'),
    'trovo': load_image('trovo.png'),
    'trovo1': load_image('trovo1.png'),
    'stair': load_image('stair.png'),
    'exit': load_image('exit.png'),
}
player_image = load_image('main_guy.png')


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = load_image('exit.png')
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(20 * x, 20 * y)
        self.add(exit_group, all_sprites)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.Go_pause = False
        self.Animation_fram_L = [load_image('main_guy_left_stand.png'), load_image('main_guy_left_going.png'),
                                 load_image('main_guy_left_going1.png')]
        self.Animation_fram_R = [load_image('main_guy_right_stand.png'), load_image('main_guy_right_going.png'),
                                 load_image('main_guy_right_going1.png')]

    def xodit(self, turn, counter):
        x = player.rect.x
        y = player.rect.y
        X1 = [' ', '%', '@', '&', '}', '{', '-', '|', '?', 'z', 'x', 'c', '1', '2', '3']
        Y1 = ['%', '&', '|']
        Z1 = ['?']
        if not self.Go_pause:
            if turn == 'Вправо':
                self.image = self.Animation_fram_R[int(counter)]
                if ((level_map[y // 20][(x + 18) // 20] in X1) and
                        (level_map[(y + 20) // 20][(x + 18) // 20] in X1) and
                        ((level_map[(y + 40) // 20][(x + 18) // 20] != " ") or (
                                level_map[(y + 20) // 20][(x + 18) // 20] == "&"))):
                    if level_map[(y + 20) // 20][(x + 18) // 20] == "1":
                        if door1.check():
                            player.rect.x += 2
                    elif level_map[(y + 20) // 20][(x + 18) // 20] == "2":
                        if door2.check():
                            player.rect.x += 2
                    elif level_map[(y + 20) // 20][(x + 18) // 20] == "3":
                        if door3.check():
                            player.rect.x += 2
                    else:
                        player.rect.x += 2
            if turn == 'Влево':
                self.image = self.Animation_fram_L[int(counter)]
                if x - 2 >= 0:
                    if ((level_map[y // 20][(x + 2) // 20] in X1) and
                            (level_map[(y + 20) // 20][(x + 2) // 20] in X1) and
                            ((level_map[(y + 40) // 20][(x + 2) // 20] != " ") or (
                                    level_map[(y + 20) // 20][(x + 2) // 20] == "&"))):
                        if level_map[(y + 20) // 20][(x + 2) // 20] == "1":
                            if door1.check():
                                player.rect.x -= 2
                        elif level_map[(y + 20) // 20][(x + 2) // 20] == "2":
                            if door2.check():
                                player.rect.x -= 2
                        elif level_map[(y + 20) // 20][(x + 2) // 20] == "3":
                            if door3.check():
                                player.rect.x -= 2
                        else:
                            player.rect.x -= 2
            if turn == 'Вверх':
                if level_map[(y + 38) // 20][(x + 9) // 20] in Y1:
                    player.rect.y -= 2
            if turn == 'Вниз':
                if level_map[(y + 40) // 20][(x + 9) // 20] in Y1:
                    player.rect.y += 2

    def stoit(self, turn):
        if not self.Go_pause:
            if turn == "Вправо":
                self.image = load_image('main_guy_right_stand.png')
            if turn == "Влево":
                self.image = load_image('main_guy_left_stand.png')
            if turn == "Вверх" or turn == "Вниз":
                self.image = load_image('main_guy.png')
            if turn == "ВправоИ":
                self.image = load_image('main_guy_right_going.png')
            if turn == "ВлевоИ":
                self.image = load_image('main_guy_left_going.png')

    def pause(self):
        self.Go_pause = not self.Go_pause

    def is_paused(self):
        return self.Go_pause


class Buttonz(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.pressed = False
        self.image = load_image('button.png')
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def click(self):
        if not self.pressed:
            self.image = load_image('button_pressed.png')
            music("button", player.is_paused())
        else:
            self.image = load_image('button.png')

    def up(self):
        self.image = load_image('button.png')


class Buttonx(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.pressed = False
        self.image = load_image('button.png')
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def click(self):
        if not self.pressed:
            self.image = load_image('button_pressed.png')
            music("button", player.is_paused())
        else:
            self.image = load_image('button.png')

    def up(self):
        self.image = load_image('button.png')


class Buttonc(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.pressed = False
        self.image = load_image('button.png')
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def click(self):
        if not self.pressed:
            self.image = load_image('button_pressed.png')
            music("button", player.is_paused())

    def up(self):
        self.image = load_image('button.png')


class Doorz(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.opened = False
        self.image = load_image('door.png')
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def open(self):
        self.image = load_image('door_opened.png')
        self.opened = True

    def close(self):
        self.image = load_image('door.png')
        self.opened = False

    def check(self):
        return self.opened


class Doorx(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.opened = False
        self.image = load_image('door.png')
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def open(self):
        self.image = load_image('door_opened.png')
        self.opened = True

    def close(self):
        self.image = load_image('door.png')
        self.opened = False

    def check(self):
        return self.opened


class Doorc(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.opened = False
        self.image = load_image('door.png')
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def open(self):
        self.image = load_image('door_opened.png')
        self.opened = True

    def close(self):
        self.image = load_image('door.png')
        self.opened = False

    def check(self):
        return self.opened


pygame.init()
size = width, height = 1200, 700
screen = pygame.display.set_mode(size)
tile_width = tile_height = 20
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
pygame.display.set_caption('digital rescue')
manager = pygame_gui.UIManager((1200, 700))
clock = pygame.time.Clock()


def timing(screen):
    clockh = pygame.time.get_ticks() // 1000
    font = pygame.font.Font(None, 25)
    if clockh >= 60:
        clockh = f'{clockh // 60}:{clockh % 60}'
    times = font.render(f'Время: {clockh}', True, (255, 255, 255))
    screen.blit(times, (20, 20))


def generate_level(level):
    new_player, x, y, exit1, n1_button, n2_button, n3_button, n1_door, n2_door, n3_door = None, None, None, None, \
        None, None, None, None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '*':
                Tile('grass', x, y)
            elif level[y][x] == '%':
                Tile('wood', x, y)
            elif level[y][x] == '&':
                Tile('list', x, y)
            elif level[y][x] == '}':
                Tile('kust', x, y)
            elif level[y][x] == '{':
                Tile('trovo', x, y)
            elif level[y][x] == '-':
                Tile('trovo1', x, y)
            elif level[y][x] == '|':
                Tile('stair', x, y)
            elif level[y][x] == '?':
                Tile('exit', x, y)
                exit1 = Exit(x, y)
            elif level[y][x] == '@':
                new_player = Player(x, y - 1)
            elif level[y][x] == 'z':
                n1_button = Buttonz(x, y)
            elif level[y][x] == 'x':
                n2_button = Buttonx(x, y)
            elif level[y][x] == 'c':
                n3_button = Buttonc(x, y)
            elif level[y][x] == '1':
                n1_door = Doorz(x, y - 1)
            elif level[y][x] == '2':
                n2_door = Doorx(x, y - 1)
            elif level[y][x] == '3':
                n3_door = Doorc(x, y - 1)
    return new_player, x, y, exit1, n1_button, n2_button, n3_button, n1_door, n2_door, n3_door


def music(how, is_paused):
    if not is_paused:
        if how == "stop":
            pygame.mixer.stop()
        if how == "Трава":
            s = pygame.mixer.Sound("sounds/xodba.mp3")
            s.play()
        elif how == "Main":
            pygame.mixer.stop()
            s = pygame.mixer.Sound("sounds/Main.mp3")
            s.set_volume(0.2)
            s.play()
        elif how == "button":
            s = pygame.mixer.Sound("sounds/button.mp3")
            s.set_volume(0.5)
            s.play()
    else:
        pygame.mixer.stop()


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    count = 0
    connection = create_connection("main.db")
    cursor = connection.cursor()
    otv = cursor.execute(f"""SELECT * FROM records""").fetchall()
    intro_text = ["                               Цифровое спасение", "",
                  "Кусочек истории: Вы с другом пошли в игровой центр поиграть",
                  "  Но поломка в игровом автомате заточила вас в нём!", "",
                  "       Ваша цель: выбраться из игрового автомата", "Жёлтые квадратики - выход из 8-бит мира",
                  "",
                  "                    Нажмите ENTER для продолжения",
                  "                                И наслаждайтесь!",
                  "", "", "стрелка влево - управление", 'стрелка вниз - рекорды',
                  "R - рестарт музыки", "S - остановить музыку"]
    upr_text = ["  Управление: ESC - пауза ",
                "  wasd или стрелочки - движение",
                "На кнопки в игре нужно нажимать мышкой - тогда что то произойдёт",
                "", "", "",
                "(ПАУЗА ОСТАНАВЛИВАЕТ ИГРУ НО НЕ ВРЕМЯ)",
                "(так сделано по причине того что можно обманывать игру паузой)",
                "", "", "", "", "", "", "стрелка вправо - вступление", 'стрелка вниз - рекорды']
    rec_text = ["Результаты ваших игр в секундах!", "", "стрелка вправо - вступление",
                "стрелка влево - управление", "", "Номер. Дата - Время", "", ]
    for i in otv:
        i = str(i)
        i = i.replace("(", "")
        i = i.replace(")", "")
        i = i.replace("'", "")
        i = i.replace(",", "")
        if int(i[:1]) == 11 and count == 0:
            count += 1
            rec_text.append("Много вы сыграли... Остальные рекорды есть в базе :0")
            break
        else:
            i = i[:1] + ". " + i[1:12] + " - " + i[12:]
            rec_text.append(str(i))
    number = str(random.randint(1, 30))
    fon = pygame.transform.scale(load_image(f'fons/{number}.png'), (1200, 700))
    screen.blit(fon, (0, 0))
    music("Main", player.is_paused())
    pygame.font.init()
    font = pygame.font.Font("data/font/Pixel_Times.ttf", 22)
    text_coord = 10
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color((0, 0, 0)))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 300
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    fon = pygame.transform.scale(load_image(f'fons/{number}.png'), (1200, 700))
                    screen.blit(fon, (0, 0))
                    pygame.font.init()
                    font = pygame.font.Font("data/font/Pixel_Times.ttf", 22)
                    text_coord = 10
                    for line in upr_text:
                        string_rendered = font.render(line, True, pygame.Color((0, 0, 0)))
                        intro_rect = string_rendered.get_rect()
                        text_coord += 10
                        intro_rect.top = text_coord
                        intro_rect.x = 300
                        text_coord += intro_rect.height
                        screen.blit(string_rendered, intro_rect)
                if event.key == pygame.K_RIGHT:
                    fon = pygame.transform.scale(load_image(f'fons/{number}.png'), (1200, 700))
                    screen.blit(fon, (0, 0))
                    pygame.font.init()
                    font = pygame.font.Font("data/font/Pixel_Times.ttf", 22)
                    text_coord = 10
                    for line in intro_text:
                        string_rendered = font.render(line, True, pygame.Color((0, 0, 0)))
                        intro_rect = string_rendered.get_rect()
                        text_coord += 10
                        intro_rect.top = text_coord
                        intro_rect.x = 300
                        text_coord += intro_rect.height
                        screen.blit(string_rendered, intro_rect)
                if event.key == pygame.K_DOWN:
                    fon = pygame.transform.scale(load_image(f'fons/{number}.png'), (1200, 700))
                    screen.blit(fon, (0, 0))
                    pygame.font.init()
                    font = pygame.font.Font("data/font/Pixel_Times.ttf", 22)
                    text_coord = 10
                    for line in rec_text:
                        string_rendered = font.render(line, True, pygame.Color((0, 0, 0)))
                        intro_rect = string_rendered.get_rect()
                        text_coord += 10
                        intro_rect.top = text_coord
                        intro_rect.x = 300
                        text_coord += intro_rect.height
                        screen.blit(string_rendered, intro_rect)
                if event.key == pygame.K_r:
                    music("Main", player.is_paused())
                if event.key == pygame.K_s:
                    music("stop", player.is_paused())
                if event.key == pygame.K_RETURN:
                    pygame.mixer.stop()
                    return
        pygame.display.flip()


def finish_screen():
    count = 0
    connection = create_connection("main.db")
    cursor = connection.cursor()
    otv = cursor.execute(f"""SELECT * FROM records""").fetchall()
    clockh = pygame.time.get_ticks() // 1000
    if clockh >= 60:
        clockh = f'{clockh // 60}:{clockh % 60}'
    daaa = datetime.datetime.now().strftime("%d-%m-%Y")
    final_text = ["THANKS FOR PLAYING!", "Ваше время: ", str(clockh), "", "Нажмите ENTER для продолжения",
                  "", "", "Стрелка вниз - рекорды"]
    cursor.execute(f"""INSERT INTO records (date, time) VALUES (?, ?);""", (daaa, clockh))
    connection.commit()
    rec_text = ["Результаты ваших игр в секундах!", "", "стрелка вправо - заключение",
                "", "Номер. Дата - Время", "", ]
    for i in otv:
        i = str(i)
        i = i.replace("(", "")
        i = i.replace(")", "")
        i = i.replace("'", "")
        i = i.replace(",", "")
        if int(i[:1]) == 11 and count == 0:
            count += 1
            rec_text.append("Много вы сыграли... Остальные рекорды есть в базе :0")
            break
        else:
            i = i[:1] + ". " + i[1:12] + " - " + i[12:]
            rec_text.append(str(i))
    fon = pygame.transform.scale(load_image('fons/Final.png'), (1200, 700))
    screen.blit(fon, (0, 0))
    music("Main", player.is_paused())
    pygame.font.init()
    font = pygame.font.Font("data/font/Pixel_Times.ttf", 22)
    text_coord = 10

    for line in final_text:
        string_rendered = font.render(line, True, pygame.Color((0, 0, 0)))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 300
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            manager.process_events(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    fon = pygame.transform.scale(load_image(f'fons/Final.png'), (1200, 700))
                    screen.blit(fon, (0, 0))
                    pygame.font.init()
                    font = pygame.font.Font("data/font/Pixel_Times.ttf", 22)
                    text_coord = 10
                    for line in rec_text:
                        string_rendered = font.render(line, True, pygame.Color((0, 0, 0)))
                        intro_rect = string_rendered.get_rect()
                        text_coord += 10
                        intro_rect.top = text_coord
                        intro_rect.x = 300
                        text_coord += intro_rect.height
                        screen.blit(string_rendered, intro_rect)
                if event.key == pygame.K_RIGHT:
                    fon = pygame.transform.scale(load_image(f'fons/Final.png'), (1200, 700))
                    screen.blit(fon, (0, 0))
                    pygame.font.init()
                    font = pygame.font.Font("data/font/Pixel_Times.ttf", 22)
                    text_coord = 10
                    for line in final_text:
                        string_rendered = font.render(line, True, pygame.Color((0, 0, 0)))
                        intro_rect = string_rendered.get_rect()
                        text_coord += 10
                        intro_rect.top = text_coord
                        intro_rect.x = 300
                        text_coord += intro_rect.height
                        screen.blit(string_rendered, intro_rect)
                if event.key == pygame.K_RETURN:
                    pygame.mixer.stop()
                    return
        pygame.display.flip()


level_map = load_level('map/fdf.txt')
player, x, y, exit1, button1, button2, button3, door1, door2, door3 = generate_level(level_map)

start_screen()


def level_1():
    counter = 0.0
    stopl = False
    stopr = False
    to_left = False
    to_right = False
    to_up = False
    to_down = False
    running = True
    b1, b2, b3 = 0, 0, 0

    while running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            manager.process_events(event)
            if event.type == pygame.QUIT:
                conf_dialog = pygame_gui.windows.UIConfirmationDialog(
                    rect=pygame.Rect((450, 250), (300, 200)),
                    manager=manager,
                    window_title="Подтверждение",
                    action_long_desc="Вы уверены, что хотите выйти?",
                    action_short_name="OK",
                    blocking=True
                )
            if event.type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if (pos[0] >= button1.rect.x and pos[0] <= button1.rect.x + 20) and \
                        (pos[1] > button1.rect.y and pos[1] <= button1.rect.y + 20):
                    if not player.is_paused():
                        button1.click()
                        b1 = 1
                        if door1 != None:
                            if not door1.check():
                                door1.open()
                            else:
                                door1.close()
                if (pos[0] >= button2.rect.x and pos[0] <= button2.rect.x + 20) and \
                        (pos[1] > button2.rect.y and pos[1] <= button2.rect.y + 20):
                    if not player.is_paused():
                        button2.click()
                        b2 = 1
                        if door2 != None:
                            if not door2.check():
                                door2.open()
                            else:
                                door2.close()
                if (pos[0] >= button3.rect.x and pos[0] <= button3.rect.x + 20) and \
                        (pos[1] > button3.rect.y and pos[1] <= button3.rect.y + 20):
                    if not player.is_paused():
                        button3.click()
                        b3 = 1
                        if door3 != None:
                            if not door3.check():
                                door3.open()
                            else:
                                door3.close()
            if event.type == pygame.MOUSEBUTTONUP:
                if not player.is_paused():
                    if b1 == 1:
                        button1.up()
                        b1 = 0
                    if b2 == 1:
                        button2.up()
                        b2 = 0
                    if b3 == 1:
                        button3.up()
                        b3 = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    to_up = True
                    stopl = False
                    stopr = False
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    to_down = True
                    stopl = False
                    stopr = False
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    to_right = True
                    stopl = False
                    stopr = False
                    music("Трава", player.is_paused())
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    to_left = True
                    stopl = False
                    stopr = False
                    music("Трава", player.is_paused())
                if event.key == pygame.K_ESCAPE:
                    player.pause()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    to_left = False
                    stopl = True
                    stopr = False
                    pygame.mixer.stop()
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    to_right = False
                    stopl = False
                    stopr = True
                    pygame.mixer.stop()
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    to_down = False
                    stopl = False
                    stopr = False
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    to_up = False
                    stopl = False
                    stopr = False
        if to_up:
            player.stoit("Вверх")
            player.xodit("Вверх", counter)
        if to_down:
            player.stoit("Вниз")
            player.xodit("Вниз", counter)
        if to_right:
            counter = (counter + 0.1) % 3
            player.xodit('Вправо', counter)
        elif stopr and not to_left:
            player.stoit('Вправо')
        if to_left:
            counter = (counter + 0.1) % 3
            player.xodit('Влево', counter)
        elif stopl and not to_right:
            player.stoit('Влево')
        if to_left and to_right:
            player.stoit("Вверх")
            pygame.mixer.stop()
        if not pygame.sprite.collide_rect(player, exit1):
            screen.fill((135, 206, 235))
            tiles_group.draw(screen)
            all_sprites.draw(screen)
            player_group.draw(screen)
            timing(screen)
            manager.update(time_delta)
            manager.draw_ui(screen)
        else:
            tiles_group.empty()
            all_sprites.empty()
            player_group.empty()
            return

        pygame.display.flip()


def level_2():
    counter = 0.0
    stopl = False
    stopr = False
    to_left = False
    to_right = False
    to_up = False
    to_down = False
    running = True
    b1, b2, b3 = 0, 0, 0

    while running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            manager.process_events(event)
            if event.type == pygame.QUIT:
                conf_dialog = pygame_gui.windows.UIConfirmationDialog(
                    rect=pygame.Rect((450, 250), (300, 200)),
                    manager=manager,
                    window_title="Подтверждение",
                    action_long_desc="Вы уверены, что хотите выйти?",
                    action_short_name="OK",
                    blocking=True
                )
            if event.type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if (pos[0] >= button1.rect.x and pos[0] <= button1.rect.x + 20) and \
                        (pos[1] > button1.rect.y and pos[1] <= button1.rect.y + 20):
                    if not player.is_paused():
                        button1.click()
                        b1 = 1
                        if door1 != None:
                            if not door1.check():
                                door1.open()
                            else:
                                door1.close()
                if (pos[0] >= button2.rect.x and pos[0] <= button2.rect.x + 20) and \
                        (pos[1] > button2.rect.y and pos[1] <= button2.rect.y + 20):
                    if not player.is_paused():
                        button2.click()
                        b2 = 1
                        if door2 != None:
                            if not door2.check():
                                door2.open()
                            else:
                                door2.close()
                if (pos[0] >= button3.rect.x and pos[0] <= button3.rect.x + 20) and \
                        (pos[1] > button3.rect.y and pos[1] <= button3.rect.y + 20):
                    if not player.is_paused():
                        button3.click()
                        b3 = 1
                        if door3 != None:
                            if not door3.check():
                                door3.open()
                            else:
                                door3.close()
            if event.type == pygame.MOUSEBUTTONUP:
                if not player.is_paused():
                    if b1 == 1:
                        button1.up()
                        b1 = 0
                    if b2 == 1:
                        button2.up()
                        b2 = 0
                    if b3 == 1:
                        button3.up()
                        b3 = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    to_up = True
                    stopl = False
                    stopr = False
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    to_down = True
                    stopl = False
                    stopr = False
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    to_right = True
                    stopl = False
                    stopr = False
                    music("Трава", player.is_paused())
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    to_left = True
                    stopl = False
                    stopr = False
                    music("Трава", player.is_paused())
                if event.key == pygame.K_ESCAPE:
                    player.pause()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    to_left = False
                    stopl = True
                    stopr = False
                    pygame.mixer.stop()
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    to_right = False
                    stopl = False
                    stopr = True
                    pygame.mixer.stop()
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    to_down = False
                    stopl = False
                    stopr = False
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    to_up = False
                    stopl = False
                    stopr = False
        if to_up:
            player.stoit("Вверх")
            player.xodit("Вверх", counter)
        if to_down:
            player.stoit("Вниз")
            player.xodit("Вниз", counter)
        if to_right:
            counter = (counter + 0.1) % 3
            player.xodit('Вправо', counter)
        elif stopr and not to_left:
            player.stoit('Вправо')
        if to_left:
            counter = (counter + 0.1) % 3
            player.xodit('Влево', counter)
        elif stopl and not to_right:
            player.stoit('Влево')
        if to_left and to_right:
            player.stoit("Вверх")
            pygame.mixer.stop()
        if not pygame.sprite.collide_rect(player, exit1):
            screen.fill((5, 5, 120))
            tiles_group.draw(screen)
            all_sprites.draw(screen)
            player_group.draw(screen)
            timing(screen)
            manager.update(time_delta)
            manager.draw_ui(screen)
        else:
            tiles_group.empty()
            all_sprites.empty()
            player_group.empty()
            return

        pygame.display.flip()


level_1()
level_map = load_level('map/123.txt')
player, x, y, exit1, button1, button2, button3, door1, door2, door3 = generate_level(level_map)
level_2()
finish_screen()
pygame.quit()
