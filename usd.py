# from pxr import Usd

class UsdFileHandler:
    def __init__(self, path, list_reverse):
        # USDファイルのパス
        self.path = path
        # リストの並べ替え
        self.list_reverse = list_reverse