import pandas as pd
import numpy as np
#from compare.list_mouth_crop import list_video #normalization 한거
from module.compare.list_mouth import list_video #normalization 안한거

def sali(original, fn):

    ori_list = list_video(original)

    ori = np.array(ori_list)

    new_list = []

    first = ori[0] - ori[0]

    new_list.append(first)

    for i in range(0, fn-1):
        new_input = ori[i] - ori[i+1]
        new_list.append(new_input)

    return new_list
