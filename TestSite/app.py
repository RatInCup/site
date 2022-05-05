from flask import *
import requests
import pygame
import os
import sys
import random
size = width, height = 900, 550
ch = random.randint(1, 2022)

url = f'http://numbersapi.com/{ch}/year?write&fragment'
r = requests.get(url)

with open('Text.txt', 'w') as output_file:
    output_file.write(r.text)

with open('Text.txt') as f:
    st = f.readline()


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
f = open('users.txt', 'a')


@app.route("/runscript")
def ScriptPage():
    global stad
    stad = 1
    screen = pygame.display.set_mode(size)
    running = True

    def load_image(name, colorkey=None):
        fullname = os.path.join('data', name)
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname)
        return image

    def start_screen():  # Класс отвечающий за стартовый экран
        pygame.font.init()
        fon = pygame.transform.scale(load_image('fon.png'), size)
        screen.blit(fon, (0, 0))

        font = pygame.font.Font(None, 30)
        text_coord = 25
        all_group = pygame.sprite.Group()
        fonp = pygame.sprite.Sprite()
        fonp.image = pygame.transform.scale(load_image("fonp.png"), (300, 150))
        all_group.add(fonp)
        fonp.rect = fonp.image.get_rect()
        fonp.rect.x = 300
        fonp.rect.y = 400
        all_group.draw(screen)


    def get_click(mouse_pos):
        global stad
        cell = mouse_pos
        if (cell[0] >= 300 and cell[1] >= 400) and (cell[0] <= 600 and cell[1] <= 550) and stad == 1:
            stad = 2

    class Wall(pygame.sprite.Sprite):  # Класс отвечающий за создание стен
        image = load_image("wall.png")

        def __init__(self, x, y, *group):
            super().__init__(*group)
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            self.rect.x = x
            self.rect.y = y - 50

        def update(self, *cords):  # Обновление кординат объекта
            self.rect = self.rect.move(*cords)

    class Floor(pygame.sprite.Sprite):  # Класс отвечающий за создание пола
        image = load_image("floor.png")

        def __init__(self, x, y, *group):
            super().__init__(*group)
            self.image = Floor.image
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

        def update(self, *cords):  # Обновление кординат объекта
            self.rect = self.rect.move(*cords)

    class Finish(pygame.sprite.Sprite):  # Класс отвечающий за финиш(окончание уровня)
        image = load_image("Finish.png")

        def __init__(self, x, y, *group):
            super().__init__(*group)
            self.image = Finish.image
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            self.rect.x = x
            self.rect.y = y

        def update(self, *cords):  # Обновление кординат объекта
            self.rect = self.rect.move(*cords)

    class Player(pygame.sprite.Sprite):  # Класс отвечающий за игрока
        image = load_image("player.png")
        image_move = load_image("player_move.png")

        def __init__(self, x, y, *group):
            super().__init__(*group)
            self.image = self.image
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            self.rect.x = x
            self.rect.y = y

        def collide(self, object):  # Взаимодействие с объектами
            for i in object:
                if pygame.sprite.collide_mask(self, i):
                    return True
            return False

        def update(self, *cords):  # Обновление кординат объекта
            self.rect = self.rect.move(*cords)

    def maze(screen, map):  # Основной клаас отвечающий за лабиринт
        global size
        back_color = "black"
        form = 50
        layer3_sprites = pygame.sprite.Group()
        layer2_sprites_standing = pygame.sprite.Group()
        layer1_sprites = pygame.sprite.Group()
        layer_for_finish = pygame.sprite.Group()
        screen.fill(pygame.Color(back_color))
        map = open(map, encoding="utf8").readlines()
        start_and_finish = []
        for y in range(len(map)):
            for x in range(len(map[y])):
                if map[y][x] == "W":
                    Wall(x * form, y * form, layer3_sprites)
                if map[y][x] == "f":
                    Floor(x * form, y * form, layer1_sprites)
                elif map[y][x] == "S":
                    Floor(x * form, y * form, layer1_sprites)
                    start_and_finish.append((x, y))
        cord = random.randint(0, len(start_and_finish) - 1)
        start_x, start_y = start_and_finish[cord]
        del start_and_finish[cord]
        finish_x, finish_y = start_and_finish[random.randint(0, len(start_and_finish) - 1)]
        Finish(finish_x * form, finish_y * form, layer_for_finish)
        player = Player(size[0] // 2 - 25, size[1] // 2 - 50, layer2_sprites_standing)
        Player(size[0] // 2 - 25, size[1] // 2 - 50, layer2_sprites_standing)
        layer1_sprites.update(start_x * -form + size[0] // 2, start_y * -form + size[1] // 2)
        layer3_sprites.update(start_x * -form + size[0] // 2, start_y * -form + size[1] // 2)
        layer_for_finish.update(start_x * -form + size[0] // 2, start_y * -form + size[1] // 2)
        run = True
        clock = pygame.time.Clock()
        fps = 60
        v = 25
        pygame.key.set_repeat(1, 5)
        global stad
        while run:
            move = 0, 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    stad = 4
                    run = False
                if event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_UP]:
                    move = 0, int(v / (fps / 30))
                if event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_DOWN]:
                    move = 0, int(-v / (fps / 30))
                if event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_LEFT]:
                    move = int(v / (fps / 30)), 0
                if event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_RIGHT]:
                    move = int(-v / (fps / 30)), 0
                else:
                    pass
            if player.collide(layer_for_finish):
                stad = 3
                run = False
            screen.fill(pygame.Color(back_color))
            if player.collide(layer3_sprites):
                move = -1 * move[0], -1 * move[1]
            layer3_sprites.update(move)
            layer1_sprites.update(move)
            layer_for_finish.update(move)
            if player.collide(layer3_sprites):
                move = int(-1.1 * move[0]), int(-1.1 * move[1])
                layer3_sprites.update(move)
                layer1_sprites.update(move)
                layer_for_finish.update(move)
            layer1_sprites.draw(screen)
            layer3_sprites.draw(screen)
            layer_for_finish.draw(screen)
            layer2_sprites_standing.draw(screen)
            clock.tick(fps)
            pygame.display.flip()

    def end(time):  # Конечный экран
        global size
        back_color = "black"
        screen.fill(pygame.Color(back_color))
        font = pygame.font.Font(None, 50)
        text = font.render(time, True, (100, 255, 100))
        text_x = size[0] // 2 - text.get_width() // 2
        text_y = size[1] // 2 - text.get_height() // 2
        screen.blit(text, (text_x, text_y))
        text = font.render("Заново", True, (100, 255, 100))
        text_x = size[0] - text.get_width()
        text_y = size[1] - text.get_height()
        screen.blit(text, (text_x, text_y))
        pygame.display.flip()
        global stad
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    stad = 4
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if size[0] - text.get_width() < event.pos[0] < size[0] and size[1] - text.get_height() < event.pos[
                        1] < \
                            size[1]:
                        stad = 2
                        run = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                get_click(event.pos)
        if stad == 1:
            start_screen()
        elif stad == 2:
            start_time = pygame.time.get_ticks()
            maze(screen, "data/maps/map4.txt")
            finish_time = pygame.time.get_ticks()
        elif stad == 3:
            end(F"""Время:  {str((finish_time - start_time) // 60000)} минуты {str((finish_time - start_time) // 1000 % 60)} секунд""")
            Time = f'{str((finish_time - start_time) // 60000)} минуты {str((finish_time - start_time) // 1000 % 60)} секунд'
        elif stad == 4:
            running = False
        pygame.display.flip()
    pygame.quit()
    return lk(Time)

@app.route('/greeting/<username>')
def greeting(username, surname):
    return f'''<!doctype html>
                <html lang="en">
                  <head>
                    <meta charset="utf-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                   <link rel="stylesheet"
                   href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                   integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                   crossorigin="anonymous">
                    <title>Привет, {username, surname}</title>
                  </head>
                  <body>
                    <h3 align="center">Привет, {username} {surname}!</h3>
                    <a align="center" href='/runscript'>Играть</a>
                  </body>
                </html>'''


@app.route('/two_params/<username>/<int:number>')
def two_params(username, number):
    return render_template('two_params.html', title='Домашняя страница')


@app.route('/', methods=['POST', 'GET'])
def form_sample():
    if request.method == 'GET':
        return f'''<!doctype html>
                        <html lang="en">
                          <head>
                            <meta charset="utf-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                            <link rel="stylesheet"
                            href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                            integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                            crossorigin="anonymous">
                            <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
                            <title>Пример формы</title>
                          </head>
                          <body>
                            <h3 align="center">Зарегистрируйся прежде чем играть)</h3>
                            <div>
                                <form class="login_form" method="post">
                                    <input type="name" class="form-control" id="name" placeholder="Введите имя" name="name">
                                    <input type="surname" class="form-control" id="surname" placeholder="Введите фамилию" name="surname">
                                    <input type="email" class="form-control" id="email" aria-describedby="emailHelp" placeholder="Введите адрес почты" name="email">
                                    <input type="password" class="form-control" id="password" placeholder="Введите пароль" name="password">
                                    <div class="form-group">
                                        <label for="form-check">Укажите пол</label>
                                        <div class="form-check">
                                          <input class="form-check-input" type="radio" name="sex" id="male" value="male" checked>
                                          <label class="form-check-label" for="male">
                                            Мужской
                                          </label>
                                        </div>
                                        <div class="form-check">
                                          <input class="form-check-input" type="radio" name="sex" id="female" value="female">
                                          <label class="form-check-label" for="female">
                                            Женский
                                          </label>
                                        </div>
                                    </div>
                                    <button type="submit" class="btn btn-primary">Играть</button>
                                </form>
                            </div>
                            <div>
                            <h5 align="center">{ch}y - {st}</h5>
                            </div>
                          </body>
                        </html>'''
    elif request.method == 'POST':
        print(request.form['name'])
        print(request.form['surname'])
        print(request.form['email'])
        print(request.form['password'])
        print(request.form['sex'])
        s = request.form['name'] + "   " + request.form['surname'] + "   " + request.form['email'] + "   " + request.form['password'] + "    " + request.form['sex']
        f.write(s + '\n')
        f.close()
        return greeting(request.form['name'], request.form['surname'])


@app.route('/lk')
def lk(Time):
    return f'''<!doctype html>
                    <html lang="en">
                      <head>
                        <meta charset="utf-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                       <link rel="stylesheet"
                       href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                       integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                       crossorigin="anonymous">
                        <title>LK</title>
                      </head>
                      <body>
                        <h3>Время твоего прохождения - {Time}</h3>
                        <a align="center" href='/runscript'>Играть</a>
                      </body>
                    </html>'''


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')

