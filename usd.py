from pxr import Usd

class UsdFileHandler:
    def __init__(self, path, list_reverse):

        # USDファイルのパス
        self.path = path

        # リストの並べ替え
        self.list_reverse = list_reverse

        # USDファイルを開く
        self.stage = self.get_stage()

        # Prims
        self.prims = self.get_prims()

        # Variant Sets
        self.variant_sets = self.get_variant_sets()

        # Variant Values
        self.variant_values = self.get_variant_values()

    def get_stage(self):
        return Usd.Stage.Open(self.path)

    def get_prims(self):
        prims = []
        for prim in self.stage.TraverseAll():
            if prim.HasVariantSets():
                prims.append(prim)
        prims.sort(key=lambda x: x.GetName(), reverse=self.list_reverse[0])
        return prims

    def get_variant_sets(self):
        all_variant_sets = []
        for prim in self.prims:
            variant_sets = []
            for variant_set in prim.GetVariantSets().GetNames():
                variant_sets.append(variant_set)
            variant_sets.sort(reverse=self.list_reverse[1])
            all_variant_sets.append(variant_sets)
        return all_variant_sets

    # def get_variant_values(self):
    #     all_variant_values = []
    #     for prim in self.prims:
    #         variant_sets = []
    #         for variant_set in prim.GetVariantSets().GetNames():
    #             variant_values = []
    #             for variant_value in prim.GetVariantSets().GetVariantSet(variant_set).GetVariantNames():
    #                 variant_values.append(variant_value)
    #             variant_values.sort(reverse=self.list_reverse[2])
    #             variant_sets.append(variant_values)
    #         all_variant_values.append(variant_sets)
    #     return all_variant_values
    def get_variant_values(self):
        all_variant_values = []
        for prim in self.prims:
            variant_sets_obj = prim.GetVariantSets()
            variant_sets = []
            for variant_set_name in variant_sets_obj.GetNames():
                variant_values = []
                variant_set = variant_sets_obj.GetVariantSet(variant_set_name)
                for variant_value in variant_set.GetVariantNames():
                    variant_values.append(variant_value)
                variant_values.sort(reverse=self.list_reverse[2])
                variant_sets.append(variant_values)
            all_variant_values.append(variant_sets)
        return all_variant_values


    def gui_prims(self):
        prim_list = []
        for prim in self.prims:
            prim_list.append(prim.GetName())
        return prim_list

    def gui_variant_sets(self):
        return self.variant_sets

    def gui_variant_values(self):
        return self.variant_values