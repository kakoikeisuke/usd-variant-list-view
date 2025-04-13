import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog
from PySide6.QtGui import QIcon, QAction

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

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

        # 開く
        open_action = QAction('USDファイルを開く', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        # 開く
        open_action = QAction('アプリケーションを終了', self)
        open_action.setShortcut('Ctrl+Q')
        open_action.triggered.connect(self.close)
        file_menu.addAction(open_action)

        # メインウィジェットとレイアウト
        widget = QWidget()

        self.setCentralWidget(widget)

    def open_file(self):
        print('開いたよ')
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            'USDファイルを開く',
            '',
            'USD Files (*.usd *.usda *.usdc *.usdz)'
        )
        if file_path:
            self.setWindowTitle('USD Variant List View: ' + file_path)

def new_window():
    # アプリケーションの作成
    app = QApplication(sys.argv)

    # ウィンドウの作成
    window = Window()
    window.show()

    # イベントループ
    sys.exit(app.exec())