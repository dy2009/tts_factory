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


global g_index
g_index = 1

global g_sil_threshold
g_sil_threshold = 200


global g_sample_rate
g_sample_rate = 44100

global g_bit_depth
g_bit_depth = 16


global g_vad_frame_len_ms
g_vad_frame_len_ms = 30

global g_vad_frame_len
g_vad_frame_len = g_vad_frame_len_ms * int(g_sample_rate / 1000)


# 10ms * 
global g_sil_energy_threshold
g_sil_energy_threshold = g_vad_frame_len * 100


def compute_energy(wav_buf):
    buf2 = np.abs(wav_buf)
    #
    e_sum = np.sum(buf2)
    return e_sum


def cut_wav_sil(cur_file_path,out_dir):
    global g_sample_rate
    global g_bit_depth
    #
    global g_index
    global g_sil_threshold
    #
    global g_vad_frame_len_ms
    global g_vad_frame_len
    global g_sil_energy_threshold
    #
    in_wav,in_sr = sf.read(cur_file_path)
    in_wav_short = in_wav * math.pow(2,g_bit_depth -1)
    #
    start_i = 0
    end_i = 0
    #
    # 90ms
    sil_90ms = 20 * int(g_sample_rate / 1000)


    #
    for i in range(len(in_wav_short)):
        cur_p_i = in_wav_short[i]
        #
        if(abs(cur_p_i) >= g_sil_threshold):
            start_i = i
            break
        #
    for i in range(len(in_wav_short)-1,0,-1):
        cur_p_i = in_wav_short[i]
        #
        if(abs(cur_p_i) >= g_sil_threshold):
            end_i = i
            break
        #
    #
    #print("1-----",start_i,end_i)
    #
    in_wav2 = in_wav[start_i:end_i]
    in_wav2_short = in_wav_short[start_i:end_i]
    #

    start_index = 0
    bflag_have_wav = False
    #
    step1_point = 44

    i_step = -step1_point
    #
    while(True):
        i_step += step1_point
        #
        if(i_step + g_vad_frame_len >= len(in_wav2_short)):
             break
        #
        cur_buf = in_wav2_short[i_step: i_step + g_vad_frame_len]
        #cur_p_i = abs(in_wav2_short[i])
        #
        cur_buf_e = compute_energy(cur_buf)

        # print(cur_buf_e)
        # print(g_sil_energy_threshold)
        # exit(0)

        #
        if(not bflag_have_wav):
            if(cur_buf_e < g_sil_energy_threshold):
                start_index = i_step
                continue
            else:
                bflag_have_wav = True
                pass


        elif(bflag_have_wav):
            if(cur_buf_e < g_sil_energy_threshold):
                # cut
                head_sil = np.random.randint(-20,20,sil_90ms) / math.pow(2,g_bit_depth -1)
                tail_sil = np.random.randint(-20,20,sil_90ms) / math.pow(2,g_bit_depth -1)
                #
                wav_piect_i = np.hstack((head_sil,in_wav2[start_index:i_step + g_vad_frame_len],tail_sil))
                #
                dst_name = "raydalio_tts_cut_" + "{0:06d}".format(g_index) + ".wav"
                dst_wav_path = os.path.join(out_dir,dst_name)
                g_index += 1
                #
                sf.write(dst_wav_path,wav_piect_i,g_sample_rate)
                #
                start_index = i_step + g_vad_frame_len
                i_step += g_vad_frame_len
                i_step -= step1_point
                #
                bflag_have_wav = False
            else:
                pass
    


    return 


def wav_to_wav16k(in_dir,out_dir):
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

        #exit(0)


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
    wav_to_wav16k(in_dir,out_dir)
