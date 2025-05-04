import os
import sys
from PySide6 import QtWidgets, QtCore, QtGui
from pxr import Usd, UsdUtils
from pxr.Usdviewq.stageView import StageView
from pxr.Usdviewq import common

USD_FILE_PATH = str(os.path.abspath('data/shaderBall.usd'))

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, stage=None):
        super(MainWindow, self).__init__()

        self.model = StageView.DefaultDataModel()

        # HUD全体の表示(GUI対応)
        self.model.viewSettings.showHUD = False
        # HUDの各項目
        self.model.viewSettings.showHUD_Info = True
        self.model.viewSettings.showHUD_Complexity = True
        self.model.viewSettings.showHUD_Performance = True
        self.model.viewSettings.showHUD_GPUstats = True
        # バウンディングボックスの表示(GUI対応)
        self.model.viewSettings.showBBoxes = False
        # レンダリングモード(GUI対応)
        # Wireframe, WireframeOnSurface, Smooth Shaded, Flat Shaded, Points, Geom Only, Geom Flat, Geom Smooth, Hidden Surface Wireframe
        self.model.viewSettings.renderMode = 'Hidden Surface Wireframe'
        # 背面レンダリング(GUI対応)
        self.model.viewSettings.cullBackfaces = False
        # 背景色(GUI対応)
        # Black, Grey (Dark), Grey (Light), White
        self.model.viewSettings.clearColorText = 'White'

        # StageViewの作成
        self.view = StageView(dataModel=self.model)

        # コンテナ用ウィジェットを作成
        container = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(container)
        # layout.setContentsMargins(5, 5, 5, 5)

        # ラベルの作成
        label = QtWidgets.QLabel('Variant Set名：')

        # コンボボックスの作成
        combobox = QtWidgets.QComboBox()
        combobox.addItems(['Variant Set 1', 'Variant Set 2', 'Variant Set 3'])

        layout.addWidget(label)
        layout.addWidget(combobox)

        item = QtWidgets.QListWidgetItem()
        item.setSizeHint(container.sizeHint())

        # リストの作成
        self.prim_list_widget = QtWidgets.QListWidget()
        self.prim_list_widget.addItems(['Prim_A', 'Prim_B', 'Prim_C'])

        self.variant_list_widget = QtWidgets.QListWidget()
        self.variant_list_widget.addItem(item)
        self.variant_list_widget.setItemWidget(item, container)

        self.list_splitter = QtWidgets.QSplitter()
        self.list_splitter.addWidget(self.prim_list_widget)
        self.list_splitter.addWidget(self.variant_list_widget)

        self.main_splitter = QtWidgets.QSplitter()
        self.main_splitter.addWidget(self.list_splitter)
        self.main_splitter.addWidget(self.view)
        self.main_splitter.setSizes([350, 650])

        # 中央ウィジェットとしてスプリッターを登録
        self.setCentralWidget(self.main_splitter)

        # メニューバーの作成
        self.create_menu()

        if stage:
            self.set_stage(stage)

    def create_menu(self):
        # メニューバーの作成
        menubar = self.menuBar()

        # メニュー：ファイル
        file_menu = menubar.addMenu('File')
        # メニューアクション：終了
        exit_action = QtGui.QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # メニュー：レンダーモード
        render_mode_menu = menubar.addMenu('Render Mode')
        # メニューアクション：各レンダーモード
        for mode_name in dir(common.RenderModes):
            # 特殊な属性, 非公開属性をスキップ
            if mode_name.startswith('_') or not isinstance(getattr(common.RenderModes, mode_name), str):
                continue
            # レンダリングモードの値をメニューアクションとして追加
            mode_value = getattr(common.RenderModes, mode_name)
            render_mode_action = QtGui.QAction(mode_value, self)
            render_mode_action.setCheckable(True)
            render_mode_action.setChecked(self.model.viewSettings.renderMode == mode_value)
            render_mode_action.triggered.connect(lambda checked, mode=mode_value: self.set_render_mode(mode))
            render_mode_menu.addAction(render_mode_action)

        # メニュー：背景色
        background_color_menu = menubar.addMenu('Background Color')
        # メニューアクション：各色
        for background_color_name in dir(common.ClearColors):
            # 特殊な属性, 非公開属性をスキップ
            if background_color_name.startswith('_') or not isinstance(
                    getattr(common.ClearColors, background_color_name), str):
                continue
            # 用意されている背景色をメニューアクションとして追加
            background_color_value = getattr(common.ClearColors, background_color_name)
            background_color_action = QtGui.QAction(background_color_value, self)
            background_color_action.setCheckable(True)
            background_color_action.setChecked(self.model.viewSettings.clearColorText == background_color_value)
            background_color_action.triggered.connect(
                lambda checked, color=background_color_value: self.set_background_color(color))
            background_color_menu.addAction(background_color_action)

        # メニュー；その他のビュー設定
        view_setting_menu = menubar.addMenu('Other View Settings')
        # メニューアクション：背面カリング
        backface_culling_action = QtGui.QAction('Enable Backface Culling', self)
        backface_culling_action.setCheckable(True)
        backface_culling_action.setChecked(self.model.viewSettings.cullBackfaces)
        backface_culling_action.triggered.connect(self.set_backface_culling)
        view_setting_menu.addAction(backface_culling_action)
        # メニューアクション：HUD
        hud_action = QtGui.QAction('Show HUD', self)
        hud_action.setCheckable(True)
        hud_action.setChecked(self.model.viewSettings.showHUD)
        hud_action.triggered.connect(self.set_hud)
        view_setting_menu.addAction(hud_action)
        # メニューアクション：バウンディングボックス
        bounding_box_action = QtGui.QAction('Show Bounding Box', self)
        bounding_box_action.setCheckable(True)
        bounding_box_action.setChecked(self.model.viewSettings.showBBoxes)
        bounding_box_action.triggered.connect(self.set_bounding_box)
        view_setting_menu.addAction(bounding_box_action)

    def set_render_mode(self, mode):
        self.model.viewSettings.renderMode = mode

        menubar = self.menuBar()
        render_mode_menu = None

        for action in menubar.actions():
            if action.text() == 'Render Mode':
                render_mode_menu = action.menu()
                break

        if render_mode_menu:
            for action in render_mode_menu.actions():
                action.setChecked(action.text() == mode)

    def set_background_color(self, color):
        self.model.viewSettings.clearColorText = color

        menubar = self.menuBar()
        background_color_menu = None

        for action in menubar.actions():
            if action.text() == 'Background Color':
                background_color_menu = action.menu()
                break

        if background_color_menu:
            for action in background_color_menu.actions():
                action.setChecked(action.text() == color)

    def set_backface_culling(self):
        self.model.viewSettings.cullBackfaces = not self.model.viewSettings.cullBackfaces

        menubar = self.menuBar()
        backface_culling_menu = None

        for action in menubar.actions():
            if action.text() == 'Enable Backface Culling':
                backface_culling_menu = action.menu()
                break

        if backface_culling_menu:
            for action in backface_culling_menu.actions():
                if action.text() == 'Enable Backface Culling':
                    action.setChecked(self.model.viewSettings.cullBackfaces)

    def set_hud(self):
        self.model.viewSettings.showHUD = not self.model.viewSettings.showHUD

        menubar = self.menuBar()
        hud_menu = None

        for action in menubar.actions():
            if action.text() == 'Show HUD':
                hud_menu = action.menu()
                break

        if hud_menu:
            for action in hud_menu.actions():
                if action.text() == 'Show HUD':
                    action.setChecked(self.model.viewSettings.showHUD)

    def set_bounding_box(self):
        self.model.viewSettings.showBBoxes = not self.model.viewSettings.showBBoxes

        menubar = self.menuBar()
        bounding_box_menu = None

        for action in menubar.actions():
            if action.text() == 'Show Bounding Box':
                bounding_box_menu = action.menu()
                break

        if bounding_box_menu:
            for action in bounding_box_menu.actions():
                if action.text() == 'Show Bounding Box':
                    action.setChecked(self.model.viewSettings.showBBoxes)

    def set_stage(self, stage):
        self.model.stage = stage
        earliest = Usd.TimeCode.EarliestTime()
        self.model.currentFrame = Usd.TimeCode(earliest)

    def closeEvent(self, event):
        self.view.closeRenderer()


def create_window():
    app = QtWidgets.QApplication([])

    # with open('style/style.qss', 'r') as file:
    #     style = file.read()
    #
    # app.setStyleSheet(style)

    with Usd.StageCacheContext(UsdUtils.StageCache.Get()):
        stage = Usd.Stage.Open(USD_FILE_PATH)

    window = MainWindow(stage)
    window.setWindowTitle('OpenUSD Viewer')
    window.resize(QtCore.QSize(1100, 700))
    window.show()

    window.view.updateView(resetCam=True, forceComputeBBox=True)

    sys.exit(app.exec())