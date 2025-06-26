import os
import sys
import random
import shutil
import math
import numpy as np
from tqdm import tqdm
import soundfile as sf
import time

global g_suffix_del
g_suffix_del = "wav"


global g_index
g_index = 1

global g_sil_threshold
g_sil_threshold = 200


global g_sample_rate
g_sample_rate = 44100

global g_bit_depth
g_bit_depth = 16


global g_vad_frame_len_ms
global g_vad_hop_len_ms
g_vad_frame_len_ms = 20
g_vad_hop_len_ms = 5

global g_vad_frame_len
global g_vad_hop_len

g_vad_frame_len = int(g_vad_frame_len_ms * int(g_sample_rate / 1000))
g_vad_hop_len = int(g_vad_hop_len_ms * int(g_sample_rate / 1000))


print("g_vad_frame_len = ",g_vad_frame_len)
print("g_vad_hop_len = ",g_vad_hop_len)


# 10ms * 
global g_sil_energy_threshold
g_sil_energy_threshold = 0


def compute_energy(wav_buf):
    buf2 = np.abs(wav_buf)
    #
    e_sum = np.sum(buf2)
    #
    return e_sum


def scan_wav_min_energy(in_wav_short):
    global g_vad_frame_len_ms
    global g_vad_frame_len
    #
    global g_vad_hop_len
    global g_vad_hop_len_ms
    #
    min_e = 1000000.0
    #
    for i in range(0,len(in_wav_short),g_vad_hop_len):
        if(i + g_vad_frame_len >= len(in_wav_short)):
            break
        #
        cur_buf = in_wav_short[i:i+g_vad_frame_len]
        #
        cur_buf_e = compute_energy(cur_buf)
        #
        # print(cur_buf)
        # print(cur_buf_e)
        # exit(0)
        #
        if(cur_buf_e < min_e):
            min_e = cur_buf_e
    #
    return min_e



def write_buf_to_wav(in_wav_buf,out_dir):
    global g_index
    global g_sample_rate
    #
    dst_name = "eksklusif_piece_" + "{0:06d}".format(g_index) + ".wav"
    dst_wav_path = os.path.join(out_dir,dst_name)
    g_index += 1
    #
    print(dst_name)
    #
    sf.write(dst_wav_path,in_wav_buf,g_sample_rate)
    #
    return 



def cut_wav_sil(cur_file_path,out_dir):
    global g_sample_rate
    global g_bit_depth
    #
    global g_index
    global g_sil_threshold
    #
    global g_vad_frame_len_ms
    global g_vad_frame_len
    #
    global g_vad_hop_len
    global g_vad_hop_len_ms
    #
    global g_sil_energy_threshold
    #
    in_wav,in_sr = sf.read(cur_file_path)
    in_wav_short = in_wav * math.pow(2,g_bit_depth -1)
    #

    min_energy = scan_wav_min_energy(in_wav_short)
    g_sil_energy_threshold = min_energy + 1000

    # print("min_energy = ",min_energy)

    # # cut
    # head_sil = np.random.randint(-20,20,sil_90ms) / math.pow(2,g_bit_depth -1)
    # tail_sil = np.random.randint(-20,20,sil_90ms) / math.pow(2,g_bit_depth -1)
    
    #print("1-----",start_i,end_i)
    #
    i_start = 0
    i_end = 0
    bflag_in_wav = False

    for i in range(0,len(in_wav_short),g_vad_hop_len):
        cur_buf = in_wav_short[i:i+g_vad_frame_len]
        #
        cur_buf_e = compute_energy(cur_buf)
        #
        if(cur_buf_e > g_sil_energy_threshold):
            if(bflag_in_wav == False):
                bflag_in_wav = True
            else:
                pass
        else:
            if(bflag_in_wav == True):
                #
                cut_len_s = (i - i_start) / g_sample_rate
                if(cut_len_s <= 1.5):
                    continue
                #
                cut_buf = in_wav[i_start:i]
                #
                write_buf_to_wav(cut_buf,out_dir)
                #
                i_start = i
                bflag_in_wav = False
            else:
                pass
    #
    rest_len_s = (len(in_wav_short) - i_start) / g_sample_rate
    if(rest_len_s >= 1.5):
        rest_buf = in_wav[i_start:]
        #
        write_buf_to_wav(rest_buf,out_dir)
    #
    return 


def wav_to_wav44k(in_dir,out_dir):
    global g_suffix_del
    global g_index
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
        cut_wav_sil(cur_file_path,out_dir)
        #

        # exit(0)
        #sox_com = "sox " + cur_file_path + " -r 16000 -c 1 -b 16 " + dst_file_path
        #
        #os.system(sox_com)
    #
    return 


if __name__ == "__main__":
    in_dir = sys.argv[1]
    out_dir = sys.argv[2]
    # in_dir = "in_dir"
    # out_dir = "wav44k_piece"
    #
    wav_to_wav44k(in_dir,out_dir)
