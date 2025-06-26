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





def step8_del_wav24k_small_volume(in_dir):
    global g_suffix_del
    #
    head_sil_point_num = int(90 * 16)
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
        # print("in_audio_data=",in_audio_data.shape)
        # exit(0)
        #
        # in_audio_data = in_audio_data[head_sil_point_num:-head_sil_point_num]
        #
        assert in_sr == 24000
        #
        in_audio_data_abs = np.abs(in_audio_data)
        #
        average_num = np.mean(in_audio_data_abs)
        #
        if(average_num <= 0.05):
            #
            # print("cur_file=",cur_file,",avg_value=",average_num)
            # shutil.copy(cur_file_path,"tmp_0001/")
            # if(i > 5000):
            #     exit(0)

            os.remove(cur_file_path)


        #
        
    #
    return 


if __name__ == "__main__":
    in_dir = sys.argv[1]
    #
    step8_del_wav24k_small_volume(in_dir)
