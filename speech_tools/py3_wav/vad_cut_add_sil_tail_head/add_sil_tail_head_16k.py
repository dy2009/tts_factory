import os
import sys
import random
import shutil
import math
import numpy as np
from tqdm import tqdm
import soundfile as sf

global g_suffix_del
g_suffix_del = "wav"



def add_sil_tail_head_16k_one(cur_file_path,out_dir,cur_file):
    #
    in_wav,in_sr = sf.read(cur_file_path)

    # 90ms
    sil_150ms = 90 * 16

    #
    # head_sil = np.zeros(800,dtype=float)
    # tail_sil = np.zeros(800,dtype=float)

    head_sil = np.random.randint(-20,20,sil_150ms) / math.pow(2,15)
    tail_sil = np.random.randint(-20,20,sil_150ms) / math.pow(2,15)


    out_wav = np.hstack((head_sil,in_wav,tail_sil))

    dst_wav_path = os.path.join(out_dir,cur_file)

    #
    sf.write(dst_wav_path,out_wav,in_sr)

    return 



def add_sil_tail_head_16k(in_dir,out_dir):
    global g_suffix_del

    #
    file_list = os.listdir(in_dir)
    file_list.sort()

    #
    for i in tqdm(range(len(file_list))):
        cur_file = file_list[i]
        #
        if(cur_file.split(".")[-1] != g_suffix_del):
            continue
        #
        cur_file_path = os.path.join(in_dir,cur_file)
        #
        add_sil_tail_head_16k_one(cur_file_path,out_dir,cur_file)

        # exit(0)

    #
    return 


if __name__ == "__main__":
    in_dir = sys.argv[1]
    out_dir = sys.argv[2]
    #
    add_sil_tail_head_16k(in_dir,out_dir)