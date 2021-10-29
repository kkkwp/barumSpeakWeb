import pandas as pd
import numpy as np
from module.saliency import sali
from module.compare.frame_number import f_num
from module.frame_cut import cut_vid
import os

def grade(original, test):
    #print('original_1')

    #cut_vid(original_1, 'original_1.mp4')
    #cut_vid(test_1, 'test_dif_1.mp4')

    # 영상 가져오기
    #original = 'original_1.mp4'
    #test = 'test_dif_1.mp4'

    on = int(f_num(original))
    tn = int(f_num(test))

    if on <= tn:
        fn = on

    else:
        fn = tn

    ori_list = sali(original, fn)
    sam_list = sali(test, fn)
    #print(ori_list)
    #print(sam_list)

    ori = np.array(ori_list)
    sam = np.array(sam_list)

    # 최종 비교값
    compare_sub = ori - sam

    #print(compare_sub)

    compare_ab = np.absolute(compare_sub)

    mean_list = []

    for i in range(0, fn):
        x_axis = compare_ab[i].mean(axis=0)
        # print(x_axis)
        mean_list.append(x_axis)


    mean_list_a = np.array(mean_list)

    x_axis_m = mean_list_a.mean(axis=0)

    #print(x_axis_m)

    final_mean = np.mean(x_axis_m)
    #print(final_mean)



    score = int(100-final_mean*50)

    return score


