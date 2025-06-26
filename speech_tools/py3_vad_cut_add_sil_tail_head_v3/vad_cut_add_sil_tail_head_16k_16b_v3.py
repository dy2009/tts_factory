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


global g_sil_threshold_head
global g_sil_threshold_tail

g_sil_threshold_head = 200
g_sil_threshold_tail = 200


global g_sample_rate
g_sample_rate = 16000

global g_bit_depth
g_bit_depth = 16

global g_sil_win_size_ms
g_sil_win_size_ms = 20



global g_sil_win_point_num
g_sil_win_point_num = int((g_sil_win_size_ms * g_sample_rate ) / 1000)



global g_sil_threshold_energy_head
global g_sil_threshold_energy_tail


g_sil_threshold_energy_head = g_sil_win_point_num * g_sil_threshold_head
g_sil_threshold_energy_tail = g_sil_win_point_num * g_sil_threshold_tail


print("g_sil_threshold_energy_head=",g_sil_threshold_energy_head)
print("g_sil_threshold_energy_tail=",g_sil_threshold_energy_tail)


def get_buf_sil_energy(in_buf):
    #
    e_all = np.sum(np.abs(in_buf))
    #
    return e_all





def find_start_pos(in_wav_short):
    global g_sil_win_point_num
    global g_sil_threshold_energy_head
    #
    start_i = 0
    #
    for i in range(0,len(in_wav_short) - g_sil_win_point_num - 1,1):
        # cur_p_i = in_wav_short[i]
        # #
        # if(abs(cur_p_i) >= g_sil_threshold):
        #     return i

        cur_i_buf = in_wav_short[i: i + g_sil_win_point_num]
        #
        cur_i_buf_e = get_buf_sil_energy(cur_i_buf)
        #
        if(cur_i_buf_e >= g_sil_threshold_energy_head):
            return i
    #
    return start_i



def find_end_pos(in_wav_short):
    global g_sil_win_point_num
    global g_sil_threshold_energy_tail
    #
    for i in range(len(in_wav_short) - g_sil_win_point_num, 0, -1):
        # cur_p_i = in_wav_short[i]
        # #
        # if(abs(cur_p_i) >= g_sil_threshold):
        #     return i
        #

        cur_i_buf = in_wav_short[i: i + g_sil_win_point_num]
        #
        cur_i_buf_e = get_buf_sil_energy(cur_i_buf)
        #
        if(cur_i_buf_e >= g_sil_threshold_energy_tail):
            return i + g_sil_win_point_num


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
    head_sil_150ms = 80 * int(g_sample_rate / 1000)
    tail_sil_150ms = 80 * int(g_sample_rate / 1000)

    #
    # head_sil = np.zeros(800,dtype=float)
    # tail_sil = np.zeros(800,dtype=float)

    head_sil = np.random.randint(-10,10,head_sil_150ms) / math.pow(2,g_bit_depth -1)
    tail_sil = np.random.randint(-10,10,tail_sil_150ms) / math.pow(2,g_bit_depth -1)

    head_sil_len = head_sil_150ms
    tail_sil_len = tail_sil_150ms


    start_i = find_start_pos(in_wav_short)
    end_i = find_end_pos(in_wav_short)


    wav_head = in_wav[:start_i]
    wav_end = in_wav[end_i:]
    #
    wav_mid = in_wav[start_i:end_i]

    #
    # print("wav_head=",wav_head.shape)
    # exit(0)
    #
    wav_head = np.hstack((head_sil,wav_head))
    #
    wav_head = wav_head[-head_sil_len:]
    #

    wav_end = np.hstack((wav_end,tail_sil))
    #
    wav_end = wav_end[:tail_sil_len]
    #

    out_wav = np.hstack((wav_head,wav_mid,wav_end))

    dst_wav_path = os.path.join(out_dir,cur_file)

    #
    sf.write(dst_wav_path,out_wav,g_sample_rate)

    return 


def wav_to_wav16k_16b(in_dir,out_dir):
    global g_suffix_del

    if(not os.path.exists(out_dir)):
        os.mkdir(out_dir)

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
