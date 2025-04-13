from pxr import Usd

class UsdFileHandler:
    def __init__(self, path):
        self.path = path
        self.stage = self.get_stage()
        self.prims = self.get_prims()

    def get_stage(self):
        return Usd.Stage.Open(self.path)

    def get_prims(self):
        prims = []
        for prim in self.stage.TraverseAll():
            if prim.HasVariantSets():
                prims.append(prim)
        if not prims:
            print('指定されたUSDファイルにはVariant SetをもつPrimがありませんでした。')
            sys.exit(1)
        return prims