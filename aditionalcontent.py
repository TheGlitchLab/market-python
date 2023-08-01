from PyQt6.QtWidgets import QStyledItemDelegate
from PyQt6.QtGui import QColor


class FormatItem(QStyledItemDelegate):
    def paint(self, painter, option, index):
        text = index.data()
        if len(text) > 18:
            text = text[:15] + '...'  # Truncate and add ellipsis
            
        super().paint(painter, option, index)
        
class RowStylized(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def paint(self, painter, option, index):
        if index.row() % 2 == 0:
            option.backgroundBrush = QColor('#484848')
        else:
            option.backgroundBrush = QColor('#414141')

        super().paint(painter, option, index)