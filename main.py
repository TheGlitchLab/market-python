from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QTimer, QModelIndex, QRegularExpression
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtGui import QStandardItem, QStandardItemModel, QRegularExpressionValidator
import sys
from models import ListModel
from aditionalcontent import *

ui_file = 'market.ui'
Ui_MainWindow, QtBaseClass = uic.loadUiType(ui_file)

class UI(QtWidgets.QMainWindow, Ui_MainWindow):
    
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.model = ListModel()
        self.widgets = {'Status': None, 'Widgets': []}
        self.setupUi(self)
        self.setStyleSheet(open('style/stylesheet.qss', 'r').read())
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.listView.setModel(self.model)
        
        self.signals()
        self.timer = QTimer(self)
        self.timer.start(350)
        self.timer.timeout.connect(self.ButtonState)
        
    def signals(self):
        self.listView.clicked.connect(self.offer_widget)
        self.listView.clicked.connect(self.handleInformation)
        self.listView.clicked.connect(self.updateImage)
        self.load_button.clicked.connect(self.load_file)
        self.save_button.clicked.connect(self.save_file)
        self.item_search.returnPressed.connect(self.add_item)
        self.search_button.clicked.connect(self.add_item)
        self.start_button.clicked.connect(self.startApplication)
        self.minimize_button.clicked.connect(self.showMinimized)
        self.x_button.clicked.connect(self.close)
        self.settings_button.clicked.connect(self.settingsTab)
        self.select_client.clicked.connect(self.select)
        self.setButtonsToView()
        self.regex()
    
    def regex(self):
        regex_pattern = r"^[a-zA-Z0-9\- ']+$"
        regex = QRegularExpression(regex_pattern)
        text_validator = QRegularExpressionValidator(regex)
        self.item_search.setValidator(text_validator)
    
    def select(self):
        print('selected')
     
    def startApplication(self):
        if self.start_button.isChecked():
            self.start_button.setEnabled(False)
            self.listView.setEnabled(False)
            self.clear_widget()
            self.listView.setCurrentIndex(QModelIndex())
            self.updateImage()
            self.item_search.setEnabled(False)
            self.search_button.setEnabled(False)
        else:
            self.listView.setEnabled(True)

    def title(self, input):
        return ' '.join([word.capitalize() for word in input.split(' ')])   
    
    def clear_widget(self):
        for widget in self.widgets['Widgets']:
            widget.close()
        self.widgets['Widgets'].clear()
        self.widgets['Status'] = None
    
    def handleInformation(self):
        selected_index = self.returnIndex()
        
        if selected_index and self.item_search.text() != '':
            self.item_search.clear()
            
        Price = self.model.data(selected_index, Qt.ItemDataRole.DisplayRole, 'Price')
        Amount = self.model.data(selected_index, Qt.ItemDataRole.DisplayRole, 'Amount')
        Anonymous = self.model.data(selected_index, Qt.ItemDataRole.DisplayRole, 'Anonymous_type')
        Offer_Type = self.model.data(selected_index, Qt.ItemDataRole.DisplayRole, 'Offer_type')
        
        if Price:
            self.input.setText(str(Price))
        else:
            self.input.setText(str(''))
        if Amount is not None:
            self.amount_input.setText(str(Amount))
        if Anonymous:
            self.anonymous.setChecked(True)
        else:
            self.anonymous.setChecked(False)
                
        if Offer_Type == 'Buy':
            self.buy_radio_button.setChecked(True)
        elif Offer_Type == 'Sell':
            self.sell_radio_button.setChecked(True)
        
        if Price and Amount is not None:
            self.create_button.setText('Update')
        else:
            self.create_button.setText('Create')
    
    def changes(self):
        if self.input.text() != '':
            self.create_button.setEnabled(True)
            self.amount_input.setText('1')
        else:
            self.create_button.setEnabled(False) 
            self.amount_input.setText('0')    
            
    def create_offer(self):
        selected_index = self.returnIndex()
        if selected_index is None: return

        for index, item in enumerate(self.model.database):
            if item['Item'] == self.model.data(selected_index,role=Qt.ItemDataRole.DisplayRole, id='Item'):
                self.model.database[index]['Price'] = self.input.text()
                self.model.database[index]['Amount'] = self.amount_input.text()
                self.model.database[index]['Offer_type'] = self.button_group.checkedButton().text()
                self.model.database[index]['Anonymous_type'] = self.anonymous.isChecked()
                break
        
        self.clear_widget()
        self.listView.setCurrentIndex(QModelIndex())
        self.updateImage()
        self.item_search.setFocus()
        self.model.save()             

    def offer_widget(self):

        if self.widgets['Status'] is None:

            regex = QtCore.QRegularExpression(r"^[1-9][0-9]*$")
            regex_validator = QtGui.QRegularExpressionValidator(regex)

            self.label = QLabel('Piece Price: ', self)
            self.label.resize(75,18)
            self.label.setObjectName('offer_widget_label')
            self.label.move(170,45)

            self.input = QLineEdit(self)
            self.input.setValidator(QtGui.QIntValidator())
            self.input.setObjectName('offer_input')
            self.input.setPlaceholderText('0')
            self.input.resize(100,16)
            self.input.setValidator(regex_validator)
            self.input.textChanged.connect(self.changes)
            self.input.move(self.label.x() + self.label.width(), self.label.y())
            self.input.setFocus()
            
            self.coin_img = QLabel(self)
            self.coin_img.setObjectName('coin_img')
            self.coin_img.setFixedSize(8, 8)
            self.coin_img.move(self.input.x() + 88, self.input.y() + 4)
                    
            self.icon = QLabel('', self.input)
            self.icon.setFixedSize(9,9)
            self.icon.setObjectName('offer_widget_icon')
            self.icon.move(int(self.input.width() - self.icon.width() - 4), int((self.input.height() - self.icon.height()) / 2))

            self.amount = QLabel('Amount: ', self)
            self.amount.resize(55,18)        
            self.amount.move(self.label.x() + 20, self.label.y() + self.amount.height() + 2)

            self.amount_input = QLineEdit(self)
            self.amount_input.setObjectName('offer_input')
            self.amount_input.setValidator(QtGui.QIntValidator())
            self.amount_input.setValidator(regex_validator)
            self.amount_input.resize(50,18)
            self.amount_input.move(self.amount.x() + self.amount.width(), self.amount.y())
            self.amount_input.setText('0')
            
            self.anonymous = QCheckBox('Anonymous', self)
            self.anonymous.resize(100,20)
            self.anonymous.move(self.amount_input.x(), self.amount_input.y() + self.anonymous.height())

            self.create_button = QPushButton('Create', self)
            self.create_button.resize(48,18)
            self.create_button.move(self.amount_input.x() + self.amount.width() - 3, self.amount_input.y())
            self.create_button.setEnabled(False)
            self.create_button.clicked.connect(self.create_offer)

            self.offer_label = QLabel('Create Offer: ', self)
            self.offer_label.setObjectName('offer_label')
            self.offer_label.move(170,15)

            self.button_group = QButtonGroup(self)
            self.button_group.setExclusive(True)

            self.sell_radio_button = QRadioButton("Sell", self)
            self.sell_radio_button.move(self.offer_label.x() + self.offer_label.width() - 15, self.offer_label.y())
            self.sell_radio_button.setChecked(True)
            self.button_group.addButton(self.sell_radio_button)
            
            self.buy_radio_button = QRadioButton("Buy", self)
            self.buy_radio_button.move(self.sell_radio_button.x() + self.buy_radio_button.width() - 57, self.buy_radio_button.y() + 15)
            self.button_group.addButton(self.buy_radio_button)
            
            self.widgets['Widgets'] = [self.coin_img, self.label, self.input, self.amount, self.amount_input,
                           self.anonymous, self.create_button, self.offer_label,
                           self.sell_radio_button, self.buy_radio_button]
            
            for widget in self.widgets['Widgets']:
                widget.show()

            self.widgets['Status'] = True
    
    def add_item(self):
        self.item = self.item_search.text()
        if self.item and not self.item.isspace():
            self.item = self.title(self.item).lstrip()

            items = [item['Item'] for item in self.model.database]
            if self.item not in items:
                self.data_append(self.item)
                self.setButtonsToView()
                self.item_search.clear()
            else:
                self.item_search.clear()
                
    def data_append(self, item):
        data = {"Item": None,
                "Price": None,
                "Amount": None,
                "Offer_type": None,
                "Anonymous_type": None
                }
        
        data['Item'] = item
        self.model.database.append(data)
        self.model.save()
        self.model.layoutChanged.emit()

        # index = self.model.index(self.model.rowCount() - 1)
        # self.model.RemoveButtons(index)            

    def returnIndex(self):
        selected_indexes = self.listView.selectedIndexes()
        if not selected_indexes:
            return
        return selected_indexes[0]
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.clear_widget()
            self.listView.setCurrentIndex(QModelIndex())
            self.updateImage()
            self.item_search.setFocus()
        else:
            super().keyPressEvent(event)  

    def updateImage(self):
        item = self.model.data(self.returnIndex(), Qt.ItemDataRole.DisplayRole, 'Item')
        
        self.pixmap = QtGui.QPixmap(f'src/itens/{item}.png')
            
        if not self.pixmap.isNull():
            self.image.setPixmap(self.pixmap)
        else:
            self.image.clear()

    def ButtonState(self):
        if self.model.isEmpty():
            self.save_button.setEnabled(False)
            self.start_button.setEnabled(False)
            self.save_button.setEnabled(False)            
        else:
            self.save_button.setEnabled(True)
            self.start_button.setEnabled(True)
            self.save_button.setEnabled(True)
                
    def load_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Load File:", "", "File(*.json)")
        if filename:
            self.model.database.clear()
            self.model.load(filename)
            
    def save_file(self):
        if self.model.isEmpty(): return
        filename, _ = QFileDialog.getSaveFileName(self, "Save File", "", "File(*.json)")
        if filename:
            self.model.save(filename)
    
    def setButtonsToView(self):
        for row in range(self.model.rowCount()):
            index = self.model.index(row)
            self.RemoveButtons(index)
                        
    def RemoveButtons(self, index):
        self.button = QPushButton('')
        self.button.setFixedSize(16, 16)
        self.button.setObjectName('Remove_Button')
        self.button.clicked.connect(lambda checked, item=index: self.removeButton(item))
        
        widget_container = QWidget()
        widget_layout = QHBoxLayout(widget_container)

        widget_layout.addWidget(self.button)
        widget_layout.setContentsMargins(0, 0, 0, 0)
        widget_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.listView.setIndexWidget(index, widget_container)
        
    def removeButton(self, index):
        item = self.model.data(index, Qt.ItemDataRole.DisplayRole, 'Item')
        self.model.removeItem(item)
        self.clear_widget()
        self.listView.setCurrentIndex(QModelIndex())
        self.updateImage()
    
    def settingsTab(self):
        self.Dialog = QDialog(self, flags=Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window)
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        # self.SettingsPosition()

        self.Dialog.resize(500,295)
        
        self.title_top = QLabel('Settings', self.Dialog)
        self.title_top.resize(500, 18)
        self.title_top.move(0,1)
        self.title_top.setObjectName('title')
        self.title_top.setAlignment(Qt.AlignmentFlag.AlignCenter|Qt.AlignmentFlag.AlignCenter)
        
        widget_container = QWidget(self.Dialog)
        widget_container.setObjectName('W_Container')
        widget_container.setGeometry(0, 0, 110, 230 )
        widget_container.move(10, 25)
        
        self.LayoutWidget = QVBoxLayout(widget_container)
        self.LayoutWidget.setContentsMargins(7, 5, 7, 7)
        self.LayoutWidget.setSpacing(3)
        
        self.market_settings = QPushButton('Market Settings', self.Dialog)
        self.market_settings.setFixedSize(100, 20)
        self.market_settings.setCheckable(True)
        self.market_settings.setChecked(True)
        self.market_settings.clicked.connect(self.market)
        # self.market_settings.setIcon(QIcon('src/image/about_off.png'))
                
        self.premium_time = QPushButton('Premium Time', self.Dialog)
        self.premium_time.setFixedSize(100,20)
        
        self.alarms = QPushButton('Alarms', self.Dialog)
        self.alarms.setFixedSize(100,20)
        self.alarms.setCheckable(True)
        self.alarms.clicked.connect(self.AlarmsTab)
        
        self.reconnect = QPushButton('Reconnect', self.Dialog)
        self.reconnect.clicked.connect(self.ReconnectTab)
        self.reconnect.setCheckable(True)
        self.reconnect.setFixedSize(100,20)
        
        self.LayoutWidget.addWidget(self.market_settings)
        self.LayoutWidget.addWidget(self.premium_time)
        self.LayoutWidget.addWidget(self.alarms)
        self.LayoutWidget.addWidget(self.reconnect)
        self.LayoutWidget.addItem(self.verticalSpacer)
        
        WidgetFooter = QWidget(self.Dialog)
        WidgetFooter.setGeometry(9,260, 490, 30)
        
        self.LayoutWidgetFooter = QHBoxLayout(WidgetFooter)
        self.LayoutWidgetFooter.setContentsMargins(0, 1, 10, 0)
        self.LayoutWidgetFooter.setSpacing(6)
        
        self.history_button = QPushButton('History', widget_container)
        self.history_button.setFixedSize(50,21)
        self.history_button.clicked.connect(self.history)

        self.close_button = QPushButton('Close', widget_container)
        self.close_button.setFixedSize(50,21)
        self.close_button.clicked.connect(self.Dialog.close)

        self.LayoutWidgetFooter.addSpacerItem(QSpacerItem(40, 35, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.LayoutWidgetFooter.addWidget(self.history_button)
        self.LayoutWidgetFooter.addWidget(self.close_button)

        self.main_widget = QWidget(self.Dialog)
        self.main_widget.setObjectName('main_widget')
        self.main_widget.setGeometry(123, 25, 365, 230)
        
        self.background_title = QLabel('', self.main_widget)
        self.background_title.setObjectName('background_title')
        self.background_title.setGeometry(0,0,365,20)
        
        self.tab_title = QLabel('Market Settings', self.main_widget)
        self.tab_title.setAlignment(Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignCenter)
        self.tab_title.setObjectName('title_container')
        self.tab_title.setGeometry(0,0,365,20)
        
        ##Execute
        self.market()
        
        
        self.Dialog.exec()
        
    def market(self):
        if self.market_settings.isChecked():
            self.market_layout = QGridLayout(self.main_widget)
            refresh_label = QLabel('Refresh: ')
            refresh_time = QLineEdit()
            refresh_time.setText('60')
            refresh_time.setFixedSize(35,18)
            
            horizontal_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
            vertical_spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

            self.market_layout.addWidget(refresh_label,0,0)
            self.market_layout.addWidget(refresh_time, 0,1)
            self.market_layout.addItem(horizontal_spacer, 0, 3)
            self.market_layout.addItem(vertical_spacer, 3,3)

            self.market_layout.setContentsMargins(9, 25, 0, 0)
        else:
            self.clear_layout(self.market_layout)
        
    def AlarmsTab(self):
        if self.alarms.isChecked():
            self.alarm_layout = QGridLayout(self.main_widget)

            self.checkbox1 = QCheckBox('Disconnect')
            self.checkbox2 = QCheckBox('Private Message')

            horizontal_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
            vertical_spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

            self.alarm_layout.addWidget(self.checkbox1,0 ,1)
            self.alarm_layout.addWidget(self.checkbox2,1, 1)
            self.alarm_layout.addItem(horizontal_spacer, 0, 3)
            self.alarm_layout.addItem(vertical_spacer, 3,3)
            
            self.alarm_layout.setContentsMargins(9, 25, 0, 0)
        else:
            self.clear_layout(self.alarm_layout)
            
    def ReconnectTab(self):
        
        if self.reconnect.isChecked():
            
            login_label = QLabel("Login:")
            self.login_input = QLineEdit()
            self.login_input.setEchoMode(QLineEdit.EchoMode.Password)
            
            password_label = QLabel("Password:")
            self.password_input = QLineEdit()
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)  # To hide the password characters
            self.login_button = QPushButton("Reconnect")
            self.login_button.setCheckable(True)
            
            self.login_toggle_button = QPushButton('', self.login_input)
            self.login_toggle_button.setObjectName('toggle_off')
            self.login_toggle_button.setCheckable(True)
            self.login_toggle_button.setFixedSize(16,16)
            self.login_toggle_button.clicked.connect(lambda: self.toggle('login'))

            self.password_toggle_button = QPushButton('', self.password_input)
            self.password_toggle_button.setObjectName('toggle_off')
            self.password_toggle_button.setCheckable(True)
            self.password_toggle_button.setFixedSize(16,16)
            self.password_toggle_button.clicked.connect(lambda: self.toggle('password'))

            #Spacers
            horizontal_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
            vertical_spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

            # Create a grid layout and add the widgets to it
            self.GLayout = QGridLayout(self.main_widget)
            self.GLayout.addWidget(login_label, 0, 0)
            self.GLayout.addWidget(self.login_input, 0, 1)
            self.GLayout.addWidget(password_label, 1, 0)
            self.GLayout.addWidget(self.password_input, 1, 1)
            self.GLayout.addWidget(self.login_button, 2, 0, 1, 2)
            self.GLayout.addWidget(self.login_toggle_button, 0, 1, alignment=Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignCenter)
            self.GLayout.addWidget(self.password_toggle_button, 1, 1, alignment=Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignCenter)
            self.GLayout.addItem(horizontal_spacer, 0, 3)
            self.GLayout.addItem(vertical_spacer, 3, 3)
            
            self.GLayout.setContentsMargins(9, 25, 0, 0)
        else:
            self.clear_layout(self.GLayout)
            
    def toggle(self, var):
        if var == 'login':
            if self.login_toggle_button.isChecked():
                self.login_toggle_button.setStyleSheet("border-image: url('src/image/eye-on.png');")
                self.login_input.setEchoMode(QLineEdit.EchoMode.Normal)
                self.login_input.setFocus()
            else:
                self.login_toggle_button.setStyleSheet('')
                self.login_input.setEchoMode(QLineEdit.EchoMode.Password)
                self.login_input.setFocus()
        elif var == 'password':
            if self.password_toggle_button.isChecked():
                self.password_toggle_button.setStyleSheet("border-image: url('src/image/eye-on.png');")
                self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
                self.password_input.setFocus()
            else:
                self.password_toggle_button.setStyleSheet('')
                self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
                self.password_input.setFocus()
                

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
                layout.deleteLater()

    def history(self):
        self.table_widget = QTableView()        
        self.table_model = QStandardItemModel(self.table_widget)
        self.table_widget.setModel(self.table_model)
        self.table_model.setHorizontalHeaderLabels(['Date', 'Balance', 'Description', 'Amount'])
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)
        self.table_widget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_widget.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table_widget.verticalHeader().setDefaultSectionSize(3)
        self.table_widget.setItemDelegate(RowStylized())


        self.populate_table()
        self.tab_title.setText('History')
        self.history_layout = QGridLayout(self.main_widget)
        self.history_layout.addWidget(self.table_widget)
        self.history_layout.setContentsMargins(0, 20, 0, 0)

    def populate_table(self):
        # Example data to populate the table
        data = [
            ["2023-07-31", "10000", "Demon Helmet", "4"],
            ["2023-08-01", "1500", "Tibia coins", "25"],
            ["2023-08-05", "30000", "Boots of Haste", "10"],
            ["2023-08-01", "1500000000", "Golden Helmet", "1"]
        ]

        for row_data in data:
            row = []
            for item_data in row_data:
                item = QStandardItem(item_data)
                row.append(item)
            self.table_model.appendRow(row)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UI()
    window.show()
    sys.exit(app.exec())
