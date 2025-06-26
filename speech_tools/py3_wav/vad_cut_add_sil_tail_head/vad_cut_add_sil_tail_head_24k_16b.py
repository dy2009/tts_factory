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


global g_sil_threshold
g_sil_threshold = 40


global g_sample_rate
g_sample_rate = 24000

global g_bit_depth
g_bit_depth = 16


def find_start_pos(in_wav_short):
    global g_sil_threshold
    #
    start_i = 0
    #
    for i in range(len(in_wav_short)):
        cur_p_i = in_wav_short[i]
        #
        if(abs(cur_p_i) >= g_sil_threshold):
            return i
    #
    return start_i


def find_end_pos(in_wav_short):
    global g_sil_threshold
    #
    for i in range(len(in_wav_short)-1,0,-1):
        cur_p_i = in_wav_short[i]
        #
        if(abs(cur_p_i) >= g_sil_threshold):
            return i
        #
    #
    return len(in_wav_short) - 1


def cut_head_tail_and_add_sil(cur_file_path,out_dir,cur_file):
    global g_sil_threshold
    global g_sample_rate
    global g_bit_depth
    #
    in_wav,in_sr = sf.read(cur_file_path)

    assert in_sr == g_sample_rate

    #in_wav_short = in_wav * 32768
    #
    in_wav_short_01 = in_wav * math.pow(2,g_bit_depth -1)
    in_wav_short = in_wav_short_01.astype(int)

    #
    start_i = 0
    end_i = 0

    # 150ms
    sil_150ms = 90 * int(g_sample_rate / 1000)

    #
    # head_sil = np.zeros(800,dtype=float)
    # tail_sil = np.zeros(800,dtype=float)

    head_sil = np.random.randint(-20,20,sil_150ms) / math.pow(2,g_bit_depth -1)
    tail_sil = np.random.randint(-20,20,sil_150ms) / math.pow(2,g_bit_depth -1)


    start_i = find_start_pos(in_wav_short)
    end_i = find_end_pos(in_wav_short)

    wav_mid = in_wav[start_i:end_i]

    out_wav = np.hstack((head_sil,wav_mid,tail_sil))

    dst_wav_path = os.path.join(out_dir,cur_file)

    #
    sf.write(dst_wav_path,out_wav,g_sample_rate)

    return 


def wav_to_wav16k_16b(in_dir,out_dir):
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
        cut_head_tail_and_add_sil(cur_file_path,out_dir,cur_file)

        # exit(0)
    #
    return 


if __name__ == "__main__":
    in_dir = sys.argv[1]
    out_dir = sys.argv[2]
    #
    wav_to_wav16k_16b(in_dir,out_dir)