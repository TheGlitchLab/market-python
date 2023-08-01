import typing
from PyQt6 import QtCore
from PyQt6.QtWidgets import QStyledItemDelegate, QPushButton
from PyQt6.QtGui import QColor, QBrush
from PyQt6.QtCore import Qt


class TextLimitDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def displayText(self, text, locale, limit=17):
        if len(text) > limit:
            text = ''.join(text[:limit]) + '...' 

        return super().displayText(text, locale)