from pxr import Usd

class UsdFileHandler:
    def __init__(self, path, list_reverse):

        # USDファイルのパス
        self.path = path

        # リストの並べ替え
        self.list_reverse = list_reverse

        # USDファイルを開く
        self.stage = self.get_stage()

        # USDファイル内のVariant Setを持ったPrim
        self.prims = self.get_prims()

        # Primの文字列リスト
        self.prim_list = self.get_prim_list()

    def get_stage(self):
        return Usd.Stage.Open(self.path)

    def get_prims(self):
        prims = []
        for prim in self.stage.TraverseAll():
            if prim.HasVariantSets():
                prims.append(prim)
        return prims

    def get_prim_list(self):
        prim_list = []
        for prim in self.prims:
            prim_data = [prim.GetPath(), prim.GetName()]
            prim_list.append(prim_data)
        prim_list.sort(key=lambda x: x[1], reverse=self.list_reverse[0])
        return prim_list

    def gui_prim_list(self):
        return self.prim_list