import sys

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtMultimedia



class MainWindow(QtWidgets.QMainWindow):
    """Main window of the program"""

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.display_width = 500
        self.display_height = 400
        self.camera_label = QtWidgets.QLabel(self)
        self._run = False

        self.ui()


    # User interface of the application
    def ui(self):
        """Setting up the UI"""

        #general window settings
        self.setWindowTitle('Drowsiness detector')
        self.setFixedSize(QtCore.QSize(900, 600))
        self.show()

        #setting up the layouts
        self.general_layout = QtWidgets.QVBoxLayout()
        self.camera_layout = QtWidgets.QVBoxLayout()
        self.info_layout = QtWidgets.QHBoxLayout()

        #container and layout for the feed
        self.feed_container = QtWidgets.QWidget()
        self.feed_layout = QtWidgets.QVBoxLayout()
        self.feed_container.setLayout(self.feed_layout)

        #container and layout for the settings
        self.settings_container = QtWidgets.QWidget()
        self.settings_layout = QtWidgets.QVBoxLayout()
        self.settings_container.setLayout(self.settings_layout)

        self.general_layout.addLayout(self.camera_layout)
        self.general_layout.addLayout(self.info_layout)

        #separator widget [line dividing feed and settings]
        separator = QtWidgets.QFrame()
        separator.setFrameShape(QtWidgets.QFrame.VLine)
        separator.setLineWidth(1)

        #adding containers to info layout
        self.info_layout.addWidget(self.feed_container)
        self.info_layout.addWidget(separator)
        self.info_layout.addWidget(self.settings_container)

        #setting up the central widget
        self.central_widget = QtWidgets.QWidget()
        self.central_widget.setLayout(self.general_layout)
        self.setCentralWidget(self.central_widget)

        self.setStyleSheet('''
            QMainWindow {
                background-color: #282c34; 
                color: #abb2bf; 
                font-family: Fira code; 
                font-size: 15px;
            } 

            .QPushButton {
                background-color: #5c6370;
                color: #abb2bf;
                font-family: Fira code;
                font-size: 15px;
                margin-top: 5px;
                border-radius: 5px;
            }

            .QLabel {
                color: #abb2bf;
                font-size: 15px;
            }

        ''')

        self.menu_bar()
        self.camera_section()
        self.info_section()

    def menu_bar(self):
        """Setting up the menu bar"""

        self.menu = self.menuBar()
        self.menu.setStyleSheet('font-size: 15px; background-color: #21252b; color: #abb2bf;')

        self.exit_action = QtWidgets.QAction('Exit', self)
        self.exit_action.triggered.connect(sys.exit)

        self.file_menu = self.menu.addMenu('&File')
        self.file_menu.addAction(self.exit_action)

        self.about_menu = self.menu.addMenu('&About')

    def camera_section(self):
        """Setting up the camera section"""

        self.background = QtGui.QPixmap(self.display_width, self.display_height)
        self.background.fill(QtGui.QColor('darkGray'))
        self.camera_label.setPixmap(self.background)
        self.camera_label.setAlignment(QtCore.Qt.AlignCenter)
        self.camera_layout.addWidget(self.camera_label)

    def info_section(self):
        """Merging the feed and settings section"""

        self.feed()
        self.settings()

    def feed(self):
        """Setting up the feed section"""

        header = QtWidgets.QLabel('<h2>Feed</h2>')
        header.setAlignment(QtCore.Qt.AlignCenter)
        self.feed_layout.addWidget(header)

        bottom_layout = QtWidgets.QGridLayout()
        self.feed_layout.addLayout(bottom_layout)

        duration = QtWidgets.QLabel('Duration:                    ')
        placeholder_duration = QtWidgets.QLabel('00 : 00 : 00')
        bottom_layout.addWidget(duration, 0, 0)
        bottom_layout.addWidget(placeholder_duration, 0, 1)

        activity = QtWidgets.QLabel('Activity:')
        placeholder_activity = QtWidgets.QLabel('Drowsiness Detected')
        bottom_layout.addWidget(activity, 1, 0)
        bottom_layout.addWidget(placeholder_activity, 1, 1)

        self.start_button = QtWidgets.QPushButton('START')
        self.start_button.setCheckable(True)
        self.start_button.setFixedSize(QtCore.QSize(70, 30))
        bottom_layout.addWidget(self.start_button)



    def settings(self):
        header = QtWidgets.QLabel('<h2>Settings</h2>')
        header.setAlignment(QtCore.Qt.AlignCenter)
        self.settings_layout.addWidget(header)

        bottom_layout = QtWidgets.QGridLayout()
        self.settings_layout.addLayout(bottom_layout)

        camera_label = QtWidgets.QLabel('Select camera:          ')
        camera_combo_box = QtWidgets.QComboBox()
        self.available_cameras = [device.description() for device in QtMultimedia.QCameraInfo.availableCameras()]
        camera_combo_box.addItems(self.available_cameras)
        bottom_layout.addWidget(camera_label, 0, 0)
        bottom_layout.addWidget(camera_combo_box, 0, 1)

        sound_label = QtWidgets.QLabel('Select sound:')
        sound_combo_box = QtWidgets.QComboBox()
        sound_combo_box.addItems(['Siren', 'Soft', 'Cools'])
        bottom_layout.addWidget(sound_label, 1, 0)
        bottom_layout.addWidget(sound_combo_box, 1, 1)

        log_button = QtWidgets.QPushButton('LOGS')
        log_button.setFixedSize(QtCore.QSize(70, 30))
        bottom_layout.addWidget(log_button)

        self.camera = 0
        camera_combo_box.currentIndexChanged.connect(self.selectionChange)

    def selectionChange(self, i):
        self.camera = i
        print(self.camera)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())