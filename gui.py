import sys
from PyQt6.QtCore import Qt, QPoint, QPropertyAnimation, QRect, QEasingCurve
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout,
    QWidget, QHBoxLayout, QLabel, QPlainTextEdit
)
from PyQt6.QtGui import QScreen
import flaskServer


app = QApplication(sys.argv)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._offset = QPoint(0, 0)
        self._is_maximized = False
        self._normal_geometry = None

        self._main_window_atr_()
        self._main_button_atr_()
        self._side_bar_atr_()

    def _main_window_atr_(self):
        """
        Configure the main window, remove system title bar, create a custom dark title bar.
        """
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint, True)
        self.setWindowTitle("Omni Mouse")
        self.resize(1200, 800)

        self.central = QWidget()
        self.central_layout = QVBoxLayout(self.central)
        self.central_layout.setContentsMargins(0, 0, 0, 0)
        self.central_layout.setSpacing(0)
        self.setCentralWidget(self.central)

        self.title_bar = QWidget()
        self.title_bar.setObjectName("title_bar")
        self.title_bar_layout = QHBoxLayout(self.title_bar)
        self.title_bar_layout.setContentsMargins(10, 0, 0, 0)
        self.title_bar_layout.setSpacing(0)

        self.label_title = QLabel("Omni Mouse")
        self.label_title.setStyleSheet("color: white; padding: 5px;")
        self.title_bar_layout.addWidget(self.label_title)
        self.title_bar_layout.addStretch()

        self.button_min = QPushButton("—")
        self.button_min.setFixedSize(40, 30)
        self.button_min.setStyleSheet("""
            QPushButton {
                color: white;
                background: none;
                border: none;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #50565B;
            }
        """)
        self.button_min.clicked.connect(self._animate_minimize)
        self.title_bar_layout.addWidget(self.button_min)

        self.button_max = QPushButton("□")
        self.button_max.setFixedSize(40, 30)
        self.button_max.setStyleSheet("""
            QPushButton {
                color: white;
                background: none;
                border: none;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #50565B;
            }
        """)
        self.button_max.clicked.connect(self._toggle_max_restore)
        self.title_bar_layout.addWidget(self.button_max)

        self.button_close = QPushButton("x")
        self.button_close.setFixedSize(40, 30)
        self.button_close.setStyleSheet("""
            QPushButton {
                color: white;
                background: none;
                border: none;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #50565B;
            }
        """)
        self.button_close.clicked.connect(self.close)
        self.title_bar_layout.addWidget(self.button_close)

        self.title_bar.setStyleSheet("QWidget#title_bar { background-color: #303539; }")

        self.central_layout.addWidget(self.title_bar)

        self.main_container = QWidget()
        self.main_layout = QHBoxLayout(self.main_container)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.central_layout.addWidget(self.main_container)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #303539;
            }
        """)

    def _animate_minimize(self):
        """
        Animate from current geometry down to (width=0, height=0),
        then restore geometry so OS sees the real size, then showMinimized().
        """
        # 1) Store the normal geometry
        self._normal_geometry = self.geometry()

        # 2) Animate
        start_rect = self._normal_geometry
        end_rect = QRect(start_rect.x(), start_rect.y(), 0, 0)

        self._ani_min = QPropertyAnimation(self, b"geometry")
        self._ani_min.setDuration(300)  # 300 ms
        self._ani_min.setStartValue(start_rect)
        self._ani_min.setEndValue(end_rect)
        self._ani_min.setEasingCurve(QEasingCurve.Type.InCubic)

        def do_minimize():
            # 3) Revert geometry so the OS sees the real size
            self.setGeometry(self._normal_geometry)
            # 4) Actually minimize
            self.showMinimized()

        self._ani_min.finished.connect(do_minimize)
        self._ani_min.start()

    def _toggle_max_restore(self):
        """
        Toggle between an animated 'maximize' and 'restore'.
        We skip true fullscreen, just do normal maximize.
        """
        if not self._is_maximized:
            self._animate_maximize()
        else:
            self._animate_restore()

    def _animate_maximize(self):
        """
        Animate from current geometry to the screen's available geometry,
        then call showMaximized().
        """
        self._normal_geometry = self.geometry()
        start_rect = self._normal_geometry

        screen_geo = QScreen.availableGeometry(app.primaryScreen())
        end_rect = screen_geo

        self._ani_max = QPropertyAnimation(self, b"geometry")
        self._ani_max.setDuration(300)
        self._ani_max.setStartValue(start_rect)
        self._ani_max.setEndValue(end_rect)
        self._ani_max.setEasingCurve(QEasingCurve.Type.OutCubic)

        def on_finished():
            self.showMaximized()
            self._is_maximized = True
            self.button_max.setText("❐")

        self._ani_max.finished.connect(on_finished)
        self._ani_max.start()

    def _animate_restore(self):
        """
        Animate from the full screen geometry back to our saved 'normal' geometry,
        then call showNormal().
        """
        if not self._normal_geometry:
            self.showNormal()
            self._is_maximized = False
            self.button_max.setText("□")
            return

        screen_geo = QScreen.availableGeometry(app.primaryScreen())
        start_rect = screen_geo
        end_rect = self._normal_geometry

        self._ani_restore = QPropertyAnimation(self, b"geometry")
        self._ani_restore.setDuration(300)
        self._ani_restore.setStartValue(start_rect)
        self._ani_restore.setEndValue(end_rect)
        self._ani_restore.setEasingCurve(QEasingCurve.Type.OutCubic)

        def on_finished():
            self.showNormal()
            self._is_maximized = False
            self.button_max.setText("□")

        self._ani_restore.finished.connect(on_finished)
        self._ani_restore.start()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self._mouse_on_titlebar(event):
            self._offset = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self._mouse_on_titlebar(event):
            self.move(event.globalPosition().toPoint() - self._offset)
            event.accept()

    def mouseDoubleClickEvent(self, event):
        if self._mouse_on_titlebar(event):
            event.ignore()

    def _mouse_on_titlebar(self, event):
        y = event.position().y()
        return 0 <= y <= self.title_bar.height()

    def _main_button_atr_(self):
        """
        Create a main content area with a text box for gyroscopic info and a primary button (right side).
        """
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)

        self.gyro_textedit = QPlainTextEdit()
        self.gyro_textedit.setStyleSheet("""
            background-color: #3a3f42;
            color: white;
            border: 1px solid #50565B;
            padding: 5px;
        """)
        self.gyro_textedit.setPlainText("Gyroscopic Information goes here")
        self.content_layout.addWidget(self.gyro_textedit)

        self.main_button = QPushButton("Get Mac Address")
        self.main_button.setObjectName("main_button")
        self.content_layout.addWidget(self.main_button, alignment=Qt.AlignmentFlag.AlignCenter)

        main_button_style = """
            #main_button {
                background-color: #3a3f42;
                color: white;
                qproperty-alignment: 'AlignCenter';
            }
        """
        self.main_button.setStyleSheet(main_button_style)

        self.main_layout.addWidget(self.content_widget, stretch=3)

    def _side_bar_atr_(self):
        """Create a sidebar with multiple filler buttons (left side)."""
        self.sidebar_widget = QWidget()
        self.sidebar_layout = QVBoxLayout(self.sidebar_widget)
        self.sidebar_widget.setStyleSheet("background-color: #3a3f42;")

        for i in range(5):
            filler_button = QPushButton(f"Filler {i + 1}")
            filler_button.setObjectName("sidebar_button")
            self.sidebar_layout.addWidget(filler_button)

        self.sidebar_layout.addStretch()

        sidebar_style_sheet = """
            #sidebar_button {
                background-color: #3a3f42;
                color: white;
                qproperty-alignment: 'AlignCenter';
            }
        """
        self.sidebar_widget.setStyleSheet(sidebar_style_sheet)

        self.main_layout.insertWidget(0, self.sidebar_widget, stretch=1)

def run():
    flaskServer.run_server()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
