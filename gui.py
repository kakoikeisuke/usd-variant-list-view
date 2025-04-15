import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog, QHBoxLayout, QVBoxLayout, QListWidget, QLabel
from PySide6.QtGui import QIcon, QAction

import usd

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        # 読み込むUSDファイルのパス
        self.usd_file_path = ''

        # USD Handler
        self.usd_handler = None

        # リストの並べ替え, 直前の選択項目, 現在の選択項目
        self.sort_reverse = [False, False, False]
        self.past_selected = [0, 0, 0]
        self.current_selected = [0, 0, 0]

        # ウィンドウのタイトル, アイコン, 位置とサイズ
        self.setWindowTitle('USD Variant List View')
        self.setWindowIcon(QIcon('icon/window-icon.svg'))
        self.setGeometry(100, 100, 500, 500)

        # メニューバー
        menubar = self.menuBar()

        # メニュー：File
        file_menu = menubar.addMenu('File')

        open_action = QAction('Open USD File', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open_file)
        open_action.setIcon(QIcon('icon/Open-USD-File.svg'))
        file_menu.addAction(open_action)

        reload_action = QAction('Reload Current File', self)
        reload_action.setShortcut('Ctrl+R')
        reload_action.triggered.connect(self.load_file)
        reload_action.setIcon(QIcon('icon/Reload-Current-File.svg'))
        file_menu.addAction(reload_action)
        reload_action.setEnabled(False)
        self.reload_action = reload_action

        close_action = QAction('Exit', self)
        close_action.setShortcut('Ctrl+Q')
        close_action.triggered.connect(self.close)
        close_action.setIcon(QIcon('icon/Exit.svg'))
        file_menu.addAction(close_action)

        # メニュー：Sort
        sort_menu = menubar.addMenu('Sort')

        prim_sort_action = QAction('Toggle Prim Sort Order', self)
        prim_sort_action.setShortcut('Ctrl+1')
        prim_sort_action.triggered.connect(self.sort_prim)
        prim_sort_action.setIcon(QIcon('icon/Toggle-Sort-Order.svg'))
        sort_menu.addAction(prim_sort_action)

        variant_set_sort_action = QAction('Toggle Variant Set Sort Order', self)
        variant_set_sort_action.setShortcut('Ctrl+2')
        variant_set_sort_action.triggered.connect(self.sort_variant_set)
        variant_set_sort_action.setIcon(QIcon('icon/Toggle-Sort-Order.svg'))
        sort_menu.addAction(variant_set_sort_action)

        variant_value_sort_action = QAction('Toggle Variant Value Order', self)
        variant_value_sort_action.setShortcut('Ctrl+3')
        variant_value_sort_action.triggered.connect(self.sort_variant_value)
        variant_value_sort_action.setIcon(QIcon('icon/Toggle-Sort-Order.svg'))
        sort_menu.addAction(variant_value_sort_action)

        # ウィジェットとレイアウト
        widget = QWidget()
        layout = QHBoxLayout()

        # Prim, Variant Set, Variant Value のリスト
        prim_box = QVBoxLayout()
        prim_label = QLabel('Prim')
        self.prim_list = QListWidget()
        prim_box.addWidget(prim_label)
        prim_box.addWidget(self.prim_list)
        layout.addLayout(prim_box)

        variant_set_box = QVBoxLayout()
        variant_set_label = QLabel('Variant Set')
        self.variant_set_list = QListWidget()
        variant_set_box.addWidget(variant_set_label)
        variant_set_box.addWidget(self.variant_set_list)
        layout.addLayout(variant_set_box)

        variant_value_box = QVBoxLayout()
        variant_value_label = QLabel('Variant Value')
        self.variant_value_list = QListWidget()
        variant_value_box.addWidget(variant_value_label)
        variant_value_box.addWidget(self.variant_value_list)
        layout.addLayout(variant_value_box)

        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # ラベルのデザイン
        label_style = """
            QLabel {
                font-weight: bold;
            }
        """
        prim_label.setStyleSheet(label_style)
        variant_set_label.setStyleSheet(label_style)
        variant_value_label.setStyleSheet(label_style)

        # リストのデザイン
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

        # Prim の選択変更 → Variant Set の取得
        self.prim_list.itemSelectionChanged.connect(self.load_variant_sets)

        # Variant Set の選択変更 → Variant Value の取得
        self.variant_set_list.itemSelectionChanged.connect(self.load_variant_values)

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
            self.load_file()

    # 読み込み・再読み込み
    def load_file(self):
        self.send_sort_reverse()
        usd.load_stage(self.usd_file_path)

    # 並べ替え
    def sort_prim(self):
        self.sort_reverse[0] = not self.sort_reverse[0]
        self.send_sort_reverse()
    def sort_variant_set(self):
        self.sort_reverse[1] = not self.sort_reverse[1]
        self.send_sort_reverse()
    def sort_variant_value(self):
        self.sort_reverse[2] = not self.sort_reverse[2]
        self.send_sort_reverse()

    # Prim の読み込み・追加
    def load_prims(self):

    # Variant Set の読み込み・追加
    def load_variant_sets(self):

    # Variant Value の読み込み・追加
    def load_variant_values(self):

    # 現在の選択している行を記録
    def record_current_row(self):

    # 昇順・降順の処理
    def send_sort_reverse(self):
        usd.receive_sort_reverse(self.sort_reverse)

def new_window():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())