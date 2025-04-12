import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QIcon
# QLabel, QVBoxLayout, QWidget

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        # ウィンドウのタイトル
        self.setWindowTitle('PySide6 GUI')

        # ウィンドウのアイコン
        self.setWindowIcon(QIcon('icon/window-icon.svg'))

        # ウィンドウの位置, サイズ
        self.setGeometry(100, 100, 500, 500)

def new_window():
    # アプリケーションの作成
    app = QApplication(sys.argv)

    # ウィンドウの作成
    window = Window()
    window.show()

    # イベントループ
    sys.exit(app.exec())