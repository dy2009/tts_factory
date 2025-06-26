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


global g_sil_point_value_int
global g_sil_point_value_f
g_sil_point_value_int = 300
g_sil_point_value_f = g_sil_point_value_int / 32768.0


global g_win_ms_len
global g_hop_ms_len

g_win_ms_len = 10
g_hop_ms_len = 5


global g_win_point_num
global g_hop_point_num
g_win_point_num = int( g_win_ms_len * 24)
g_hop_point_num = int( g_hop_ms_len * 24)


global g_sil_win_energy
g_sil_win_energy = (g_win_point_num * g_sil_point_value_int)


def read_txt_to_list(in_txt):
    #
    cur_f = open(in_txt,"r",encoding="utf8")
    #
    txt_list = []
    #
    for curLine in cur_f.readlines():
        line_cp = curLine.strip()
        #
        txt_list.append(line_cp)
    #
    cur_f.close()
    #
    return txt_list


def step9_del_wav24k_long_sil_1wav(in_wav_path):
    global g_win_point_num
    global g_hop_point_num
    global g_sil_point_value_int
    global g_sil_point_value_f
    global g_sil_win_energy

    #
    # head_sil_point_num = int(90 * 16)
    #
    in_audio_data, in_sr = sf.read(in_wav_path)
    #
    # print("in_audio_data=",in_audio_data.shape)
    # exit(0)
    #
    # in_audio_data = in_audio_data[head_sil_point_num:-head_sil_point_num]
    #
    assert in_sr == 24000
    #
    in_audio_data_abs = np.abs((in_audio_data) * 32768)
    #

    # if(len(in_audio_data_abs) <= (24000 * 1.3) ):
    #     os.remove(in_wav_path)
    #     return 

    # in_audio_data= (111360,)
    # print("in_audio_data=",in_audio_data.shape)



    max_v = np.max(in_audio_data_abs)
    min_v = np.min(in_audio_data_abs)

    # max_v= 0.994964599609375 ,min_v= 0.0
    # print("max_v=",max_v,",min_v=",min_v)

    voice_len_s = 0.0
    sil_len_s = 0.0

    voice_frame_num = 0
    sil_frame_num = 0

    #
    # for i in range(0,len(in_audio_data_abs) - g_win_point_num,g_hop_point_num):
    
    step_i = 0
    while(True):
        if(step_i >= (len(in_audio_data_abs) - g_win_point_num) ):
            break

        start_i = step_i
        end_i = start_i + g_win_point_num
        #
        step_i += g_hop_point_num
        #
        cur_buf = in_audio_data_abs[start_i:end_i]
        #
        if(len(cur_buf) < 240):
            break
        #
        cur_buf_e = np.sum(cur_buf)

        # print("\n\ncur_buf=",cur_buf.shape)
        # print("cur_buf=",cur_buf)
        # print("cur_buf_e=",cur_buf_e)
        # print("g_sil_win_energy=",g_sil_win_energy)

        # exit(0)

        #
        if(cur_buf_e >= g_sil_win_energy):
            voice_frame_num += 1
        else:
            sil_frame_num += 1
        #
        # print("cur_buf=",cur_buf.shape)
        # exit(0)

    # print("sil_frame_num=",sil_frame_num)
    # print("voice_frame_num=",voice_frame_num)

    if(voice_frame_num <= 120):
        return True

    sil_frame_rate = sil_frame_num / (voice_frame_num + sil_frame_num)

    # print("sil_frame_rate=",sil_frame_rate)

    if(sil_frame_rate >= 0.4):
        return True
    else:
        return False




def step9_del_long_sil_wav_txt(in_txt,out_txt):
    #
    cur_f = open(in_txt,"r",encoding="utf8")
    dst_f = open(out_txt,"w",encoding="utf8")
    #
    #
    for curLine in cur_f.readlines():
        line_cp = curLine.strip()
        #
        if(len(line_cp) <= 0):
            continue
        #
        bflag_is_sil = step9_del_wav24k_long_sil_1wav(line_cp)
        #
        if(bflag_is_sil):
            os.remove(line_cp)
        else:
            #
            dst_f.write(line_cp + "\n")
    #
    cur_f.close()
    dst_f.close()
    #
    return 





if __name__ == "__main__":
    # in_wav_path = sys.argv[1]
    #
    in_wav_txt = sys.argv[1]
    out_wav_txt = sys.argv[2]
    #
    step9_del_long_sil_wav_txt(in_wav_txt,out_wav_txt)
