from PyQt6.QtCore import QAbstractListModel, Qt, QModelIndex, pyqtSignal
import json

class ListModel(QAbstractListModel):
    
    def __init__(self, list=None):
        super().__init__()
        self.database = []
        self.filename = 'data_market.json'
        self.load()

    def data(self, index: QModelIndex, role=None, id='Item'):
        if index is None or not index.isValid(): return None

        if role == Qt.ItemDataRole.DisplayRole:
            return self.database[index.row()][id]
        elif role == Qt.ItemDataRole.UserRole:
            return self.database[index.row()]

    def rowCount(self, parent=QModelIndex):
        return len(self.database)

    def getIndex(self):
        indexes = []
        for row, data in enumerate(self.database):
            index = self.index(row)
            indexes.append(index)
        return indexes
    
    def isEmpty(self):
        if self.rowCount() == 0:
            return True
        return False
    
    def clear(self):
        self.beginResetModel()
        self.database.clear()
        self.endResetModel()
    
    def removeItem(self, item):
        for row, data in enumerate(self.database):
            if data['Item'] == item:
                del self.database[row]
                self.save()
                self.layoutChanged.emit()
                return

    def save(self, filename=None):
        try:
            if filename:
                with open(filename, 'w') as file:
                    json.dump(self.database, file, indent=4)
            else:
                with open(self.filename, 'w') as file:
                    json.dump(self.database, file, indent=4)
        except Exception as e:
            print(e)
                    
    def load(self, filename=None):
        try:
            if filename:
                with open(filename, 'r') as file:
                    self.database = json.load(file)
                    self.layoutChanged.emit()
            else:
                with open(self.filename, 'r') as file:
                    self.database = json.load(file)
                    self.layoutChanged.emit()
        except FileNotFoundError:
            pass
        except json.decoder.JSONDecodeError:    
            return {}
        except Exception as e:
            print(e)
            
