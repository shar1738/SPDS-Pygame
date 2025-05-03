import pygame as pg
from funcs_data.functions import Animation

SPACEMAN_MOVE_ANIMATION = {
    "paths": [
        "Assets/images/spaceman/spaceman1.png",
        "Assets/images/spaceman/spaceman2.png",
        "Assets/images/spaceman/spaceman3.png",
    ],
    "size":  (100, 100),
    "speed": 0.15,
}

class Spaceman():
    def __ini__(self):
        pass