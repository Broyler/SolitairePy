import pygame
from components import fs, object, scale
from enum import Enum, auto

settings = fs.load("settings.json")["card"]


class Suit(Enum):
    DIAMOND = auto()
    CLUB = auto()
    HEART = auto()
    SPADE = auto()


class Value(Enum):
    ACE = auto()
    TWO = auto()
    THREE = auto()
    FOUR = auto()
    FIVE = auto()
    SIX = auto()
    SEVEN = auto()
    EIGHT = auto()
    NINE = auto()
    TEN = auto()
    JACK = auto()
    QUEEN = auto()
    KING = auto()


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
