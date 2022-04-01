import pygame
import random

pygame.init()
pygame.display.set_caption("Physics lab")
PISTOL = pygame.image.load('img/pistol.jpg')
START = pygame.image.load('img/start.png')

EMPTY_ALLIMINIUM_BULLET = pygame.image.load("img/empty_alluminium.png")
ALLIMINIUM_BULLET = pygame.image.load("img/alluminium.png")
STEEL_BULLET = pygame.image.load("img/steel.png")
EMPTY_BRASS_BULLET = pygame.image.load("img/empty_brass.png")
BRASS_BULLET = pygame.image.load("img/brass.png")
INFO = pygame.image.load("img/info.png")
bullet_coords = [(700, 2), (810, 2), (920, 2), (1030, 9), (1140, 2)]
bullet_weights = [5.2, 6.8, 13.6, 13.8, 19, 9]
angles = [(195, 220, 1), (235, 250, 1), (325, 350, 1), (325, 350, 1), (375, 400, 1)]
FPS = 60
ticker_coords = (350, 300, 250, 100)


class Lab:
    def __init__(self):
        self.doing = True
        self.started = False
        self.screen = pygame.display.set_mode((1280, 600))
        self.screen.fill(pygame.Color("White"))
        self.clock = pygame.time.Clock()
        self.ticker = Ticker(*ticker_coords)
        self.pistol = Pistol(self.ticker.get_coords())
        self.bullet_chosen = None
        self.angle = 0

    def run(self):
        self.render()
        while self.doing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.doing = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    if 1200 < pos[0] < 1280 and 530 < pos[1] < 600:
                        self.start()
                    for bullet in bullet_coords:
                        if bullet[0] <= pos[0] <= bullet[0] + 105 and bullet[1] <= pos[1] <= bullet[1] + 100:
                            self.bullet_chosen = bullet_coords.index(bullet)
            if self.started:
                if not self.pistol.bullet.collide(self.ticker) and self.ticker.velocity == 50:
                    self.pistol.bullet.move()
                else:
                    self.ticker.move()
                    self.pistol.bullet.coords = [self.ticker.left + self.ticker.width, self.pistol.bullet.coords[1]]
                if self.ticker.velocity == 0:
                    self.angle = random.randrange(*angles[self.bullet_chosen]) / 10
                    self.started = False
            self.clock.tick(60)
            self.render()
            pygame.display.flip()

    def render(self):
        self.screen.fill(pygame.Color("White"))
        # Установка
        pygame.draw.line(self.screen, pygame.Color('black'), (300, 120), (700, 120), width=5)
        pygame.draw.line(self.screen, pygame.Color('black'), (550, 120),
                         (self.ticker.left + self.ticker.width - 50, self.ticker.top), width=2)
        pygame.draw.line(self.screen, pygame.Color('black'), (400, 120), (self.ticker.left + 50, self.ticker.top),
                         width=2)
        pygame.draw.rect(self.screen, pygame.Color('black'), self.ticker.rect(), width=0)
        # Кнопки
        self.screen.blit(START, (1200, 530))
        self.screen.blit(EMPTY_ALLIMINIUM_BULLET, bullet_coords[0])
        self.screen.blit(ALLIMINIUM_BULLET, bullet_coords[1])
        self.screen.blit(STEEL_BULLET, bullet_coords[2])
        self.screen.blit(EMPTY_BRASS_BULLET, bullet_coords[3])
        self.screen.blit(BRASS_BULLET, bullet_coords[4])
        if self.bullet_chosen is not None:
            pygame.draw.rect(self.screen, pygame.Color('red'),
                             pygame.Rect(bullet_coords[self.bullet_chosen], (100, 100)), width=3)
        # Информация об установке
        self.screen.blit(INFO, (0, 0))
        # Пистолет
        self.screen.blit(PISTOL, self.pistol.coords)
        pygame.draw.line(self.screen, pygame.Color("black"), (self.pistol.coords[0], self.pistol.coords[1] + 65),
                         (self.pistol.coords[0] + 100, self.pistol.coords[1] + 65),
                         width=2)
        # Угол отклонения
        font = pygame.font.SysFont("comicsansms", 20)
        text = font.render(f"α = {str(self.angle)}", True, pygame.Color("Black"))
        self.screen.blit(text, (500, 500))
        if self.started:
            pygame.draw.circle(self.screen, pygame.Color("red"), (self.pistol.bullet.coords),
                               self.pistol.bullet.radius)
        pygame.display.flip()

    def start(self):
        if self.bullet_chosen is not None:
            self.ticker = Ticker(*ticker_coords)
            self.pistol = Pistol(self.ticker.get_coords())
            self.started = True
            self.angle = 0
            self.pistol.shoot()


class Pistol():
    def __init__(self, ticker_coords):
        self.coords = (ticker_coords[0] + ticker_coords[2] + 200, ticker_coords[1] + (ticker_coords[3] / 4))

    def shoot(self):
        current_bullet_coords = [self.coords[0] + 50, self.coords[1] + 20]
        self.bullet = Bullet(current_bullet_coords)


class Bullet():
    def __init__(self, coords):
        self.coords = coords
        self.radius = 6
        self.weight = 0
        self.velocity = 25

    def collide(self, ticker):
        if ticker.left <= self.coords[0] <= ticker.left + ticker.width and ticker.top <= self.coords[
            1] <= ticker.top + ticker.height:
            self.coords[0] = ticker.left + ticker.width
            return True
        return False

    def move(self):
        self.coords[0] -= self.velocity


class Ticker():
    def __init__(self, left, top, width, height):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.weight = 0
        self.velocity = 50
        self.acceleration = 1

    def rect(self):
        return pygame.Rect(self.left, self.top, self.width, self.height)

    def get_coords(self):
        return self.left, self.top, self.width, self.height

    def update_velocity(self):
        self.old_velocity = self.velocity
        self.velocity = self.old_velocity - self.acceleration
        if self.velocity < 0:
            self.velocity = 0

    def move(self):
        self.update_velocity()
        self.left -= self.velocity / FPS


lab = Lab()
lab.run()
