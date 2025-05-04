import os
from enum import Enum
from typing import Tuple
from PyQt5.QtGui import QColor


class TextPosition(Enum):
    TOP = 0
    BOTTOM = 1
    MIDDLE = 2


COLOR_PRIMARY = "#444444"
COLOR_SECONDARY = "#ffffff"
COLOR_ACCENT = "#00a8ff"
COLOR_ERROR = "#ff5252"
COLOR_SUCCESS = "#5ad45a"

MEME_COLORS = {
    "Білий": (255, 255, 255),
    "Чорний": (0, 0, 0),
    "Червоний": (255, 0, 0),
    "Синій": (0, 0, 255),
    "Зелений": (0, 255, 0),
    "Жовтий": (255, 255, 0),
}

DEFAULT_FONTS = [
    "Arial",
    "Impact",
    "Comic Sans MS",
    "Times New Roman",
    "Courier New"
]

MEME_TEMPLATES = {
    "Drake": {
        "template_text": ["Ні", "Так"],
        "positions": [TextPosition.TOP, TextPosition.BOTTOM]
    },
    "Distracted Boyfriend": {
        "template_text": ["Мені", "Спокуса", "Моя задача"],
        "positions": [TextPosition.BOTTOM, TextPosition.BOTTOM, TextPosition.BOTTOM]
    },
    "Two Buttons": {
        "template_text": ["Кнопка 1", "Кнопка 2", "Напружена людина"],
        "positions": [TextPosition.TOP, TextPosition.TOP, TextPosition.BOTTOM]
    }
}


def rgb_to_qcolor(rgb: Tuple[int, int, int]) -> QColor:
    return QColor(rgb[0], rgb[1], rgb[2])


def qcolor_to_rgb(qcolor: QColor) -> Tuple[int, int, int]:
    return (qcolor.red(), qcolor.green(), qcolor.blue())


def get_file_extension(filename: str) -> str:
    return os.path.splitext(filename)[1].lower() 