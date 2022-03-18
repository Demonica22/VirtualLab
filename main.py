import pygame

pygame.init()
pygame.display.set_caption("Physics lab")
PISTOL = pygame.image.load('img/pistol.png')
ALTMARK = pygame.image.load("img/Altmark.jpg")
FPS = 60


class Lab:
    def __init__(self):
        self.doing = True
        self.screen = pygame.display.set_mode((1280, 960))
        self.clock = pygame.time.Clock()
        self.setup = LabSetup(self.screen)

    def run(self):
        self.render()
        while self.doing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.doing = False

            self.clock.tick(60)
            self.render()
            pygame.display.flip()

    def render(self):
        self.screen = pygame.display.set_mode((1280, 960))
        self.screen.fill(pygame.Color("White"))
        self.setup.render()
        pygame.display.flip()


class LabSetup():
    def __init__(self, screen):
        self.screen = screen
        self.ticker = Ticker(350, 400, 250, 100)

    def render(self):
        pygame.draw.line(self.screen, pygame.Color('black'), (300, 120), (700, 120), width=5)
        pygame.draw.line(self.screen, pygame.Color('black'), (550, 120),
                         (self.ticker.left + self.ticker.width - 50, self.ticker.top), width=2)
        pygame.draw.line(self.screen, pygame.Color('black'), (400, 120), (self.ticker.left + 50, self.ticker.top),
                         width=2)
        pygame.draw.rect(self.screen, pygame.Color('black'), self.ticker.rect(), width=3)
        self.screen.blit(PISTOL,
                         (self.ticker.left + self.ticker.width + 200, self.ticker.top + (self.ticker.height / 4)))
        self.screen.blit(ALTMARK, (self.ticker.left, self.ticker.top))
        self.ticker.move()


class Ticker():
    def __init__(self, left, top, width, height):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.velocity = 20
        self.acceleration = 0.01

    def rect(self):
        return pygame.Rect(self.left, self.top, self.width, self.height)

    def update_velocity(self):
        self.old_velocity = self.velocity
        self.velocity = self.old_velocity - self.acceleration

    def move(self):
        self.update_velocity()
        self.left -= self.velocity / FPS


lab = Lab()
lab.run()
