import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog
from PySide6.QtGui import QIcon, QAction
from usd import UsdFileHandler

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.usd_file_path = ''

        # ウィンドウのタイトル
        self.setWindowTitle('USD Variant List View')

        # ウィンドウのアイコン
        self.setWindowIcon(QIcon('icon/window-icon.svg'))

        # ウィンドウの位置, サイズ
        self.setGeometry(100, 100, 500, 500)

        # メニューバー
        menubar = self.menuBar()

        # ファイルメニュー
        file_menu = menubar.addMenu('ファイル')

        # USDファイルを開く
        open_action = QAction('USDファイルを開く', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        # ファイルを再読み込み
        reload_action = QAction('ファイルを再読み込み', self)
        reload_action.setShortcut('Ctrl+R')
        reload_action.triggered.connect(self.reload_file)
        file_menu.addAction(reload_action)
        reload_action.setEnabled(False)
        self.reload_action = reload_action

        # アプリケーションを終了
        close_action = QAction('アプリケーションを終了', self)
        close_action.setShortcut('Ctrl+Q')
        close_action.triggered.connect(self.close)
        file_menu.addAction(close_action)

        # メインウィジェットとレイアウト
        widget = QWidget()

        self.setCentralWidget(widget)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            'USDファイルを開く',
            '',
            'USD Files (*.usd *.usda *.usdc *.usdz)'
        )
        if file_path:
            self.usd_file_path = file_path
            self.setWindowTitle('USD Variant List View: ' + file_path)
            self.reload_action.setEnabled(True)
            self.load_usd()

    def reload_file(self):
        self.load_usd()

    def load_usd(self):
        UsdFileHandler(self.usd_file_path)

def new_window():
    # アプリケーションの作成
    app = QApplication(sys.argv)

    # ウィンドウの作成
    window = Window()
    window.show()

    # イベントループ
    sys.exit(app.exec())