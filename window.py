import sys
from PySide6 import QtWidgets, QtCore, QtGui
from pxr import Usd, UsdUtils
from pxr.Usdviewq.stageView import StageView
from pxr.Usdviewq import common

# 使用するUSDファイルの絶対パス
USD_FILE_PATH = ''

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
        self.model.viewSettings.renderMode = 'Smooth Shaded'
        # 背面カリング(GUI対応)
        self.model.viewSettings.cullBackfaces = False
        # 背景色(GUI対応)
        # Black, Grey (Dark), Grey (Light), White
        self.model.viewSettings.clearColorText = 'White'

        if stage:
            self.set_stage(stage)

        # メニューバーの作成
        self.create_menu()
        
        # メインのスプリッター（左：リスト, 右：StageView）
        self.main_splitter = QtWidgets.QSplitter()
        self.setCentralWidget(self.main_splitter)

        # メインリストのスプリッター（左：Primリスト, 右：Variantリスト）
        self.list_splitter = QtWidgets.QSplitter()
        self.main_splitter.addWidget(self.list_splitter)

        # Primリスト
        self.prim_list = QtWidgets.QListWidget()
        self.prim_list.itemSelectionChanged.connect(self.create_variant_list)

        # Variantリスト
        self.variant_list = QtWidgets.QListWidget()

        # StageViewの作成
        self.view = StageView(dataModel=self.model)
        self.main_splitter.addWidget(self.view)
        
        # メイン画面（リスト, StageView）の作成
        self.create_main_content()

    def create_main_content(self):
        # Primリストの作成
        self.create_prim_list()
        self.list_splitter.addWidget(self.prim_list)
        # Variantリストの作成
        self.create_variant_list()
        self.list_splitter.addWidget(self.variant_list)

    def create_prim_list(self):
        # Primのリストを初期化
        self.prim_list.clear()
        # Primを取得し, 1行目を選択
        prims = self.get_prims()
        for prim in prims:
            self.prim_list.addItem(prim.GetName())
        if self.prim_list.count() > 0:
            self.prim_list.setCurrentRow(0)
        else:
            self.prim_list.setCurrentRow(-1)

    def create_variant_list(self):
        # variantのリストを初期化
        self.variant_list.clear()
        # Variantを持つPrimがなければスルー
        if self.prim_list.currentRow() < 0:
            return
        variant_sets = self.get_variant_sets()
        for variant_set in variant_sets:
            # Variant Setをラベルに追加
            label = QtWidgets.QLabel(variant_set)
            combobox = QtWidgets.QComboBox()
            # Variant Valueをコンボボックスに追加
            variant_values = self.get_variant_values(variant_set)
            combobox.addItems(variant_values)
            # コンボボックスの選択を現在のVariant Valueに変更
            current_variant_value = self.get_current_variant_value(variant_set)
            combobox.setCurrentText(current_variant_value)
            # コンボボックスの値が変更された際にUSDのVariantも変更
            combobox.currentTextChanged.connect(
                lambda text, vs=variant_set: self.change_variant(vs, text)
            )
            # ラベルとコンボボックスをまとめてリストに追加
            container = QtWidgets.QWidget()
            layout = QtWidgets.QHBoxLayout(container)
            layout.addWidget(label)
            layout.addWidget(combobox)
            item = QtWidgets.QListWidgetItem()
            item.setSizeHint(container.sizeHint())
            self.variant_list.addItem(item)
            self.variant_list.setItemWidget(item, container)
    
    def create_menu(self):
        # メニューバーの作成
        menubar = self.menuBar()

        # メニュー：ファイル
        file_menu = menubar.addMenu('File')
        # メニューアクション：USDファイルを開く
        open_action = QtGui.QAction('Open USD File', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
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

    def open_file(self):
        selected_file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Open USD File', '', 'USD Files (*.usd *.usda *.usdc *.usdz)'
        )
        set_usd_file_path(selected_file_path)

    def closeEvent(self, event):
        self.view.closeRenderer()

    def get_prims(self):
        prims = []
        for prim in self.model.stage.Traverse():
            if prim.HasVariantSets():
                prims.append(prim)
        prims.sort(key=lambda x: x.GetName(), reverse=False)
        return prims

    def get_variant_sets(self):
        current_prim = self.get_prims()[self.prim_list.currentRow()]
        variant_sets = current_prim.GetVariantSets().GetNames()
        variant_sets.sort(reverse=False)
        return variant_sets

    def get_variant_values(self, variant_set):
        current_prim = self.get_prims()[self.prim_list.currentRow()]
        variant_values = current_prim.GetVariantSets().GetVariantSet(variant_set).GetVariantNames()
        variant_values.sort(reverse=False)
        return variant_values

    def get_current_variant_value(self, variant_set):
        current_prim = self.get_prims()[self.prim_list.currentRow()]
        current_variant_value = current_prim.GetVariantSets().GetVariantSet(variant_set).GetVariantSelection()
        return current_variant_value

    def change_variant(self, variant_set, variant_value):
        current_prim = self.get_prims()[self.prim_list.currentRow()]
        current_prim.GetVariantSets().GetVariantSet(variant_set).SetVariantSelection(variant_value)
        # ビューを更新（Variantの更新を即時反映する）
        self.view.updateView(resetCam=False, forceComputeBBox=True)

def create_window():
    app = QtWidgets.QApplication([])

    # スタイルシートの読み込み
    with open('style/style.qss', 'r') as file:
        style = file.read()
    app.setStyleSheet(style)

    with Usd.StageCacheContext(UsdUtils.StageCache.Get()):
        stage = Usd.Stage.Open(USD_FILE_PATH)

    window = MainWindow(stage)
    # ウィンドウタイトル
    window.setWindowTitle('OpenUSD Viewer')

    # ウィンドウサイズと比率（リストと3Dビュー）
    window.resize(QtCore.QSize(1000, 600))
    window.main_splitter.setSizes([400, 600])
    window.show()

    window.view.updateView(resetCam=True, forceComputeBBox=True)

    sys.exit(app.exec())

def set_usd_file_path(usd_file_path):
    global USD_FILE_PATH
    USD_FILE_PATH = usd_file_path