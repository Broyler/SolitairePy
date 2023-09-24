import pygame
from components import fs, object, scale

settings = fs.load("settings.json")["card"]


class Card(object.Object):
    scale = scale.Scale(settings["scale"]["mode"], settings["scale"]["factor"])
    width = scale.apply(settings["width"])
    height = scale.apply(settings["height"])
    border_width = scale.apply(settings["border"]["width"])

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        super().__init__()

    def draw(self):
        pygame.draw.rect(self.surface, settings["border"]["color"], self.rect)
        pygame.draw.rect(self.surface, settings["background_color"], self.inset_rect(self.border_width))
