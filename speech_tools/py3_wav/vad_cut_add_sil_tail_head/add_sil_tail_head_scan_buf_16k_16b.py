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
g_sil_threshold = 150


global g_sample_rate
g_sample_rate = 16000

global g_bit_depth
g_bit_depth = 16

# 10 ms
global g_win_len_ms
g_win_len_ms = 10

global g_win_len
g_win_len = int(g_sample_rate / 1000) * g_win_len_ms


global g_sil_buf_threshold
g_sil_buf_threshold = int(g_sample_rate / 1000) * g_win_len_ms * g_sil_threshold


def scan_buf_energy(wav_buf):
    #
    wav_buf2 = abs(wav_buf)
    #
    return np.sum(wav_buf2)



def find_start_pos(in_wav_short):
    global g_sil_threshold
    global g_sil_buf_threshold
    global g_win_len
    #
    wav_len = len(in_wav_short)
    hop_len = int(wav_len / 4)
    start_i = 0
    sil_start_pos = 0
    #

    while(True):
        if(start_i >= wav_len - g_win_len):
            break
        #
        cur_buf = in_wav_short[start_i: start_i + g_win_len]
        #
        cur_buf_energy = scan_buf_energy(cur_buf)
        #
        if(cur_buf_energy <= g_sil_buf_threshold):
            # is sil
            sil_start_pos = start_i
            return start_i
        #
        start_i += hop_len
    #
    return 0


def find_end_pos(in_wav_short):
    global g_sil_threshold
    global g_sil_buf_threshold
    global g_win_len
    #
    wav_len = len(in_wav_short)
    hop_len = int(wav_len / 4)

    end_i = wav_len - g_win_len
    sil_start_pos = 0
    #

    while(True):
        if(end_i >= wav_len - g_win_len):
            break
        #
        cur_buf = in_wav_short[end_i: end_i + g_win_len]
        #
        cur_buf_energy = scan_buf_energy(cur_buf)
        #
        if(cur_buf_energy <= g_sil_buf_threshold):
            # is sil
            sil_start_pos = end_i
            return end_i
        #
        end_i = end_i - hop_len

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