import pygame
from components import fs

bg_color = fs.load("settings.json")["window"]["background_color"]


class Object:
    x, y = 0, 0
    width, height = 100, 100
    color = "#ff0000"

    def __init__(self):
        self.bg = pygame.Surface(self.dimensions)
        self.bg.fill(bg_color)
        self.surface = pygame.Surface(self.dimensions)
        self.draw()

    @property
    def position(self):
        return self.x, self.y

    @property
    def dimensions(self):
        return self.width, self.height

    @property
    def rect(self):
        return *self.position, *self.dimensions

    def is_inside(self, x, y):
        return self.x <= x <= self.x + self.width and self.y <= y <= self.height

    def draw(self):
        pygame.draw.rect(self.surface, self.color, self.rect)
