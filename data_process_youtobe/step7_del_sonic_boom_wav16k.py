import os
import sys
import random
import shutil


from multiprocessing import Process

import soundfile as sf 
import numpy as np

from tqdm import tqdm

global g_suffix_del
g_suffix_del = "wav"




def step7_del_sonic_boom_wav44k(in_dir):
    global g_suffix_del
    #
    file_list = os.listdir(in_dir)
    # file_list.sort()
   
    
    
    # file_list.reverse()
    #
    for i in tqdm(range(len(file_list))):
        cur_file = file_list[i]
        #
        if(cur_file.split(".")[-1] != g_suffix_del):
            continue
        #
        cur_file_path = os.path.join(in_dir,cur_file)
        #
        if(not os.path.exists(cur_file_path)):
            continue
        
        #
        in_audio_data,in_sr = sf.read(cur_file_path)
        #
        assert in_sr == 16000
        #
        in_audio_data_abs = np.abs(in_audio_data)
        #
        boom_point_num = np.sum(in_audio_data_abs >= 0.99)
        #
        # print("boom_point_num=",boom_point_num)

        if(boom_point_num >= 2):
            os.remove(cur_file_path)
        #
        # print("cur_file=",cur_file,",boom_num=",boom_point_num)

        # if(i >= 4):
        #     break
        
    #
    return 


if __name__ == "__main__":
    in_dir = sys.argv[1]
    #
    step7_del_sonic_boom_wav44k(in_dir)
