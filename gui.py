import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog, QHBoxLayout, QVBoxLayout, QListWidget, QLabel
from PySide6.QtGui import QIcon, QAction
from usd import UsdFileHandler

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        # usd.py のデータ
        self.usd_data = None

        # 読み込むUSDファイルのパス
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

        layout = QHBoxLayout()

        prim_box = QVBoxLayout()
        prim_label = QLabel('Prim Name')
        self.prim_list = QListWidget()
        prim_box.addWidget(prim_label)
        prim_box.addWidget(self.prim_list)

        variant_set_box = QVBoxLayout()
        variant_set_label = QLabel('Variant Set Name')
        self.variant_set_list = QListWidget()
        variant_set_box.addWidget(variant_set_label)
        variant_set_box.addWidget(self.variant_set_list)

        variant_value_box = QVBoxLayout()
        variant_value_label = QLabel('Variant Value')
        self.variant_value_list = QListWidget()
        variant_value_box.addWidget(variant_value_label)
        variant_value_box.addWidget(self.variant_value_list)

        layout.addLayout(prim_box)
        layout.addLayout(variant_set_box)
        layout.addLayout(variant_value_box)

        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # リストの並べ替え
        self.list_reverse = [False, False, False]

    # USDファイルを選択
    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            'USDファイルを開く',
            '',
            'USDファイル (*.usd *.usda *.usdc *.usdz)'
        )
        if file_path:
            self.usd_file_path = file_path
            self.setWindowTitle('USD Variant List View: ' + file_path)
            self.reload_action.setEnabled(True)
            self.load_usd()

    # 現在のUSDファイルを再読み込み
    def reload_file(self):
        self.load_usd()

    # USDファイルを読み込む
    def load_usd(self):
        self.usd_data = UsdFileHandler(self.usd_file_path, self.list_reverse)
        for prim in UsdFileHandler.gui_prims(self.usd_data):
            self.prim_list.addItem(prim)

def new_window():
    # アプリケーションの作成
    app = QApplication(sys.argv)

    # ウィンドウの作成
    window = Window()
    window.show()

    # イベントループ
    sys.exit(app.exec())