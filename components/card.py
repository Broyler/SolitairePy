import pygame
from components import fs
from components import object

settings = fs.load("settings.json")["card"]


class Card(object.Object):
    color = "#00ff00"
