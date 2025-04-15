from pxr import Usd

global sort_reverse
global stage
global prims
global variant_sets
global variant_values

# USD のパスを取得
def receive_sort_reverse(sort):
    global sort_reverse
    sort_reverse = sort

# USD Stage を読み込み
def load_stage(path):
    global stage
    stage = Usd.Stage.Open(path)

def reset():
    global stage
    stage = None
    global prims
    prims = None
    global variant_sets
    variant_sets = None
    global variant_values
    variant_values = None

# Prims を取得
def load_prims():
    global prims
    prims = []
    for prim in stage.Traverse():
        if prim.HasVariantSets():
            prims.append(prim)
    prims.sort(key=lambda x: x.GetName(), reverse=sort_reverse[0])

def send_prim_list():
    prim_list = []
    for prim in prims:
        prim_list.append(prim.GetName())
    return prim_list

# Variant Sets を取得
def load_variant_sets(row):
    global variant_sets
    variant_sets = []
    prim = prims[row]
    variant_set_names = prim.GetVariantSets().GetNames()
    for variant_set_name in variant_set_names:
        variant_set = prim.GetVariantSets().GetVariantSet(variant_set_name)
        variant_sets.append(variant_set)
    variant_sets.sort(key=lambda x: x.GetName(), reverse=sort_reverse[1])

def send_variant_sets():
    variant_set_list = []
    for variant_set in variant_sets:
        variant_set_list.append(variant_set.GetName())
    return variant_set_list

def load_variant_values(row):
    global variant_values
    variant_set = variant_sets[row]
    variant_values = []
    for variant_value in variant_set.GetVariantNames():
        variant_values.append(variant_value)
    variant_values.sort(reverse=sort_reverse[2])

def send_variant_values():
    variant_value_list = []
    for variant_value in variant_values:
        variant_value_list.append(variant_value)
    return variant_value_list