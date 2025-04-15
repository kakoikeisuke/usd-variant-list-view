from pxr import Usd

global stage
global prims
global sort_reverse

# USD Stage を読み込み
def load_stage(path):
    global stage
    stage = Usd.Stage.Open(path)

def receive_sort_reverse(sort):
    global sort_reverse
    sort_reverse = sort