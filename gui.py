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

        # リストの並べ替え
        self.list_reverse = [False, False, False]

        # ウィンドウのタイトル
        self.setWindowTitle('USD Variant List View')

        # ウィンドウのアイコン
        self.setWindowIcon(QIcon('icon/window-icon.svg'))

        # ウィンドウの位置, サイズ
        self.setGeometry(100, 100, 500, 500)

        # メニューバー
        menubar = self.menuBar()

        # ファイルメニュー
        file_menu = menubar.addMenu('File')

        # USDファイルを開く
        open_action = QAction('Open USD File', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open_file)
        open_action.setIcon(QIcon('icon/Open-USD-File.svg'))
        file_menu.addAction(open_action)

        # ファイルを再読み込み
        reload_action = QAction('Reload Current File', self)
        reload_action.setShortcut('Ctrl+R')
        reload_action.triggered.connect(self.reload_file)
        reload_action.setIcon(QIcon('icon/Reload-Current-File.svg'))
        file_menu.addAction(reload_action)
        reload_action.setEnabled(False)
        self.reload_action = reload_action

        # アプリケーションを終了
        close_action = QAction('Exit', self)
        close_action.setShortcut('Ctrl+Q')
        close_action.triggered.connect(self.close)
        close_action.setIcon(QIcon('icon/Exit.svg'))
        file_menu.addAction(close_action)

        # 並べ替えメニュー
        sort_menu = menubar.addMenu('Sort')

        # Prim の並べ替え
        prim_sort_action = QAction('Toggle Prim Sort Order', self)
        prim_sort_action.setShortcut('Ctrl+1')
        prim_sort_action.triggered.connect(self.sort_prim)
        prim_sort_action.setIcon(QIcon('icon/Toggle-Sort-Order.svg'))
        sort_menu.addAction(prim_sort_action)

        # Variant Set の並べ替え
        variant_set_sort_action = QAction('Toggle Variant Set Sort Order', self)
        variant_set_sort_action.setShortcut('Ctrl+2')
        variant_set_sort_action.triggered.connect(self.sort_variant_set)
        variant_set_sort_action.setIcon(QIcon('icon/Toggle-Sort-Order.svg'))
        sort_menu.addAction(variant_set_sort_action)

        # Variant Value の並べ替え
        variant_value_sort_action = QAction('Toggle Variant Value Order', self)
        variant_value_sort_action.setShortcut('Ctrl+3')
        variant_value_sort_action.triggered.connect(self.sort_variant_value)
        variant_value_sort_action.setIcon(QIcon('icon/Toggle-Sort-Order.svg'))
        sort_menu.addAction(variant_value_sort_action)

        # ウィジェットとレイアウト
        widget = QWidget()
        layout = QHBoxLayout()

        # Prim リスト
        prim_box = QVBoxLayout()
        prim_label = QLabel('Prim')
        self.prim_list = QListWidget()
        prim_box.addWidget(prim_label)
        prim_box.addWidget(self.prim_list)
        layout.addLayout(prim_box)

        # Variant Set リスト
        variant_set_box = QVBoxLayout()
        variant_set_label = QLabel('Variant Set')
        self.variant_set_list = QListWidget()
        variant_set_box.addWidget(variant_set_label)
        variant_set_box.addWidget(self.variant_set_list)
        layout.addLayout(variant_set_box)

        # Variant Value リスト
        variant_value_box = QVBoxLayout()
        variant_value_label = QLabel('Variant Value')
        self.variant_value_list = QListWidget()
        variant_value_box.addWidget(variant_value_label)
        variant_value_box.addWidget(self.variant_value_list)
        layout.addLayout(variant_value_box)

        widget.setLayout(layout)
        self.setCentralWidget(widget)

        label_style = """
            QLabel {
                font-weight: bold;
            }
        """
        prim_label.setStyleSheet(label_style)
        variant_set_label.setStyleSheet(label_style)
        variant_value_label.setStyleSheet(label_style)

        list_style = """
            QListWidget {
                border-radius: 0;
                border-style: none;
                outline: none;
            }
            QListWidget::item {
                padding: 3px;
                margin: 0;
                border-style: none;
            }
            QListWidget::item:selected, QListWidget::item:selected:hover {
                color: #ffffff;
                background-color: #5391CB;
            }
            QListWidget::item:!selected {
                color: #222222;
            }
            QListWidget::item:hover {
                color: #444444;
                background-color: #eaeaea;
            }
        """
        self.prim_list.setStyleSheet(list_style)
        self.variant_set_list.setStyleSheet(list_style)
        self.variant_value_list.setStyleSheet(list_style)

    # USDファイルを選択
    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            'Open USD File',
            '',
            'USD File (*.usd *.usda *.usdc *.usdz)'
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
        self.list_clear()
        self.usd_data = UsdFileHandler(self.usd_file_path, self.list_reverse)
        for prim in UsdFileHandler.gui_prims(self.usd_data):
            self.prim_list.addItem(prim)
        self.prim_list.setCurrentRow(0)

    # リストをクリア
    def list_clear(self):
        self.prim_list.clear()
        self.variant_set_list.clear()
        self.variant_value_list.clear()

    def sort_prim(self):
        self.list_reverse[0] = not self.list_reverse[0]
        self.load_usd()

    def sort_variant_set(self):
        self.list_reverse[1] = not self.list_reverse[1]
        self.load_usd()

    def sort_variant_value(self):
        self.list_reverse[2] = not self.list_reverse[2]
        self.load_usd()

def new_window():
    app = QApplication(sys.argv)

    window = Window()
    window.show()

    sys.exit(app.exec())