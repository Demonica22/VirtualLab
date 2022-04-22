import pygame
import random
import math
import time

pygame.init()
pygame.display.set_caption("Измерение скорости пули с помощью баллистического маятника")
PISTOL = pygame.image.load('img/pistol.png')
PISTOL_STARTED = pygame.image.load('img/pistol_started.png')
START = pygame.image.load('img/start.png')
RESET = pygame.image.load('img/reset.png')
RULER = pygame.image.load('img/ruler.png')
EMPTY_ALLUMINIUM_BULLET = pygame.image.load("img/empty_alluminium.png")
ALLUMINIUM_BULLET = pygame.image.load("img/alluminium.png")
STEEL_BULLET = pygame.image.load("img/steel.png")
EMPTY_BRASS_BULLET = pygame.image.load("img/empty_brass.png")
BRASS_BULLET = pygame.image.load("img/brass.png")
INFO = pygame.image.load("img/info.png")
ICON = pygame.image.load("img/icon.png")
TICKER = pygame.image.load("img/ticker.png")
bullet_coords = [(700, 2), (810, 2), (920, 2), (1030, 9),
                 (1140, 2)]  # Координаты иконок пуль в формате (x,y) левого верхнего угла иконки
bullet_weights = [5.2, 6.8, 13.6, 13.8, 19.9]  # Веса пуль
bullet_colors = ["grey", "blue", "black", "orange", "red"]  # Цвета шариков (моделей) пуль на экране
bullet_velocities = [240, 250, 300, 305, 330]  # Скорости пуль в пикселях в секунду
bullet_times = [12, 14, 21, 22, 24]  # Время для каждой пули, которое требуется для полного затухания колебаний маятника
deltas = [(1295, 1305, 5), (1275, 1285, 5), (1170, 1190, 5), (1165, 1185, 5),
          (1100, 1120, 5)]  # Промежутки отклонений маятника при разных пулях, полученные экспериментальным путем.
# Записанные в формате (минимальное значение, максимальное значение, шаг), макс. и мин. записаны в сантиметрах * 100.
ticker_coords = (350, 300, 250, 100)  # Начальное положение маятника

FPS = 60  # Частота кадров приложения

pygame.display.set_icon(ICON)  # Иконка кафедры физики для приложения


class Lab:
    def __init__(self):
        self.doing = True  # Работает ли приложение
        self.started = False  # Запущен ли эксперимент
        # Нужно ли отображать сообщения об ошибках
        self.set_warning_message_bullet = False
        self.set_warning_message_ticker = False
        self.bullet_chosen = None  # Индекс выбранной пули
        self.screen = pygame.display.set_mode((1280, 600))  # Размер окна
        self.screen.fill(pygame.Color("White"))  # Задний фон приложения
        self.clock = pygame.time.Clock()
        self.ticker = Ticker(ticker_coords, self.bullet_chosen)  # Создание экземпляра маятника
        self.pistol = Pistol(self.ticker.get_coords())  # Создание экземпляра пистолета
        self.delta_x = 0  # Отклонение по оси X

    def run(self):
        self.render()
        while self.doing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.doing = False
                # Обработка нажатий мыши
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    # Нажатие кнопки Старт
                    if 1180 < pos[0] < 1280 and 550 < pos[1] < 600:
                        if self.started:
                            self.set_warning_message_ticker = True
                        else:
                            self.set_warning_message_ticker = False
                            self.start()
                    # Нажатие кнопки Сброс
                    if 1070 < pos[0] < 1170 and 550 < pos[1] < 600:
                        self.ticker.return_to_start_position()
                        self.started = False
                    # Нажатие на одну из иконок пуль
                    if not self.started:
                        for bullet in bullet_coords:
                            if bullet[0] <= pos[0] <= bullet[0] + 105 and bullet[1] <= pos[1] <= bullet[1] + 100:
                                self.bullet_chosen = bullet_coords.index(bullet)
                                self.set_warning_message_bullet = False
            if self.started:
                # Движение пули
                if not self.pistol.bullet.collide(self.ticker) and self.ticker.velocity > 0:
                    self.pistol.bullet.move()
                else:  # Движение бруска
                    self.ticker.move()
                    # Изменение положения пули, если брусок двигается. (Пуля остается "прикрепленной" к бруску)
                    self.pistol.bullet.coords = [self.ticker.left + self.ticker.width, self.pistol.bullet.coords[1]]
                if self.ticker.reached_most_left_point and self.delta_x == 0:
                    # Генерация максимального отклонения бруска
                    self.delta_x = random.randrange(*deltas[self.bullet_chosen]) / 100
                self.started = not self.ticker.finished
            self.clock.tick(60)
            self.render()
            pygame.display.flip()

    def render(self):
        self.screen.fill(pygame.Color("White"))
        # Линейка
        self.screen.blit(RULER, (-5, ticker_coords[1] + ticker_coords[3]))
        # Подвес и нити
        pygame.draw.line(self.screen, pygame.Color('black'), (250, 120), (695, 120), width=7)
        pygame.draw.line(self.screen, pygame.Color('black'), (550, 120),
                         (self.ticker.left + self.ticker.width - 50, self.ticker.top), width=2)
        pygame.draw.line(self.screen, pygame.Color('black'), (400, 120), (self.ticker.left + 50, self.ticker.top),
                         width=2)
        # Маятник
        self.screen.blit(TICKER, self.ticker.get_coords()[:2])
        # Подставка пистолета
        pygame.draw.line(self.screen, pygame.Color("black"), (800, 394), (899, 394), width=10)
        pygame.draw.rect(self.screen, pygame.Color("black"), pygame.Rect((850, 394), (5, 206)))
        pygame.draw.line(self.screen, pygame.Color("black"), (800, 598), (899, 598), width=10)

        # Кнопки
        self.screen.blit(START, (1180, 550))
        self.screen.blit(RESET, (1070, 550))
        # Иконки пуль
        self.screen.blit(EMPTY_ALLUMINIUM_BULLET, bullet_coords[0])
        self.screen.blit(ALLUMINIUM_BULLET, bullet_coords[1])
        self.screen.blit(STEEL_BULLET, bullet_coords[2])
        self.screen.blit(EMPTY_BRASS_BULLET, bullet_coords[3])
        self.screen.blit(BRASS_BULLET, bullet_coords[4])
        # Отображение рамки у выбранной пули
        if self.bullet_chosen is not None:
            pygame.draw.rect(self.screen, pygame.Color('red'),
                             pygame.Rect((bullet_coords[self.bullet_chosen][0], 0), (100, 100)), width=3)
        # Информация об установке
        self.screen.blit(INFO, (0, 0))
        # Пистолет с разной анимацией (до и после выстрела)
        if self.started:
            self.screen.blit(PISTOL_STARTED, self.pistol.coords)
        else:
            self.screen.blit(PISTOL, self.pistol.coords)
        # Отображение максимального отклонения бруска после выстрела на экран
        if self.delta_x != 0:
            font = pygame.font.SysFont("comicsansms", 30)
            text = font.render(f"z = {str(self.delta_x)} см", True, pygame.Color("Black"))
            self.screen.blit(text, (300, 500))
        # Предупреждение о невыбранной пуле
        if self.set_warning_message_bullet:
            font = pygame.font.SysFont("comicsansms", 20)
            text = font.render(f"Выберите пулю!", True, pygame.Color("red"))
            self.screen.blit(text, (1000, 510))
        elif self.set_warning_message_ticker:
            font = pygame.font.SysFont("comicsansms", 15)
            text = font.render("Маятник не на исходной", True, pygame.Color("red"))
            self.screen.blit(text, (1000, 510))
        # Пуля
        if self.started:
            pygame.draw.circle(self.screen, pygame.Color(bullet_colors[self.bullet_chosen]), self.pistol.bullet.coords,
                               self.pistol.bullet.radius)
        pygame.display.flip()

    def start(self):
        if self.bullet_chosen is not None:  # Если пуля не выбрана - выстрел не произойдет,и будет отображено
            # предупредительное сообщение
            # Создание экземпляров пули и бруска для текущего высрела и сам выстрел
            self.ticker = Ticker(ticker_coords, self.bullet_chosen)
            self.pistol = Pistol(self.ticker.get_coords())
            self.started = True
            self.delta_x = 0  # Смещение по оси X
            self.pistol.shoot()
        else:
            self.set_warning_message_bullet = True


class Pistol():
    def __init__(self, ticker_coords):
        self.coords = (ticker_coords[0] + ticker_coords[2] + 200, ticker_coords[1] + (
                ticker_coords[3] / 4))  # Координаты верхего левого угла прямоугольника с картинкой пистолета

    def shoot(self):
        """
        Выстрел (создание пули)
        :return:
        """
        self.bullet = Bullet([self.coords[0] + 5, self.coords[1] + 10])


class Bullet():
    def __init__(self, coords):
        self.coords = coords  # Координаты пули (x,y) левого верхнего угла квадрата, в который вписан круг
        self.radius = 6  # Радиус шарика (модель пули) на экране
        self.velocity = 500  # Скорость шарика на экране

    def collide(self, ticker):
        """
        Проверка на пересечение пули и бруска
        :param ticker:
        :return: Bool
        """
        if ticker.left <= self.coords[0] <= ticker.left + ticker.width and ticker.top <= self.coords[
            1] <= ticker.top + ticker.height:
            self.coords[0] = ticker.left + ticker.width
            self.coords[1] = ticker.top + ticker.height / 4 + 10
            return True
        return False

    def move(self):
        """
        Движение пули
        :return:
        """
        self.coords[0] -= self.velocity / FPS


class Ticker():
    def __init__(self, coords, bullet):
        self.left = coords[0]  # Х координата левого верхнего угла
        self.top = coords[1]  # У координата левого верхнего угла
        self.width = coords[2]  # ширина маятника
        self.height = coords[3]  # высота маятника
        self.acceleration = 10  # Ускорение маятника
        self.bullet = bullet  # Индекс выбранной пули или None, если пуля не выбрана
        self.theta = False
        self.reached_most_left_point = False
        self.finished = False  # Остановился ли маятник
        self.start_time = 0  # Время начала движения
        if self.bullet is not None:
            self.velocity = bullet_velocities[self.bullet]
            self.time = bullet_times[self.bullet]
        else:
            self.velocity = 0
            self.time = 0
        self.start_velocity = self.velocity

    def set_coords(self, coords):
        """
        Меняет координаты маятника на переданные в аргументы
        :param coords: (x,y)
        :return:
        """
        self.left = coords[0]
        self.top = coords[1]

    def return_to_start_position(self):
        """
        Изменяет координаты маятника на начальные (возвращает в положение равновесия)
        :return:
        """
        self.set_coords(ticker_coords[:2])
        self.velocity = 0
        self.acceleration = 0
        self.start_velocity = 0

    def rect(self):
        """
        Возвращает объект прямоугольника текущекого маятника
        :return: Rect
        """
        return pygame.Rect(self.left, self.top, self.width, self.height)

    def get_coords(self):
        """
        Возвращает координаты левого верхнего угла, ширину и высоту
        :return: tuple
        """
        return self.left, self.top, self.width, self.height

    def update_velocity(self):
        """
        Движение маятника после столкновения с пулей
        :return:
        """
        self.velocity -= self.acceleration
        if self.velocity < 0:
            self.velocity = 0
            self.reached_most_left_point = True

    def move(self):
        """
        Движение маятника при качании
        :return:
        """
        if self.reached_most_left_point:
            if not self.theta:
                self.theta_v()
            if abs(self.start_time - time.time()) > self.time:
                self.finished = True
                self.set_coords(ticker_coords[:2])
            else:
                acc = -.005 * math.sin(self.theta)
                self.velocity += acc
                self.velocity *= .995
                self.theta += self.velocity
                self.left = ticker_coords[0] + (self.v * math.sin(self.theta))
        else:
            self.update_velocity()
            self.left -= self.velocity / FPS

    def theta_v(self):
        """
        Расчет переменных для качания
        :return:
        """
        self.start_time = time.time()
        self.v = math.sqrt(math.pow(self.left - ticker_coords[0], 2) + math.pow(self.top, 2))
        self.theta = math.asin(((self.left - ticker_coords[0]) / self.v))
        self.reached_most_left_point = True


# Создание экземпляра лабораторной работы и его запуск
lab = Lab()
lab.run()
