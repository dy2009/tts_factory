import os
import sys
import random
import shutil


from multiprocessing import Process

import soundfile as sf 
import numpy as np

from tqdm import tqdm

import hashlib

global g_suffix_del
g_suffix_del = "wav"


global g_sil_point_value_int
global g_win_ms_len
global g_hop_ms_len
global g_win_point_num
global g_hop_point_num
global g_sil_win_energy

g_sil_point_value_int = 50
g_win_ms_len = 20
g_hop_ms_len = 10
g_win_point_num = int( g_win_ms_len * 24)
g_hop_point_num = int( g_hop_ms_len * 24)

g_sil_win_energy = (g_win_point_num * g_sil_point_value_int)


global g_out_index
g_out_index = 1


global g_already_cut_md5_dict
g_already_cut_md5_dict = {}

g_already_cut_md5_dict[0] = True

# global g_md5_obj
# g_md5_obj = hashlib.md5()



def get_out_wav_path(out_dir):
    global g_out_index
    #
    out_wav_name = "{0:08d}".format(g_out_index) + ".wav"
    g_out_index += 1
    #
    out_wav_path = os.path.join(out_dir,out_wav_name)
    #
    return out_wav_path


def check_already_cut_md5_dict(cut_wav_buf):
    global g_already_cut_md5_dict
    # global g_md5_obj
    #
    point_str = ""
    point_v = 0
    #
    for i in range(len(cut_wav_buf)):
        buf_i = cut_wav_buf[i]
        #
        if(abs(buf_i) > 1500):
            point_v += abs(buf_i)
    #
    # print("point_v=",point_v)
    #
    # g_md5_obj.update(str(point_v).encode("utf8"))
    # md5_value = g_md5_obj.hexdigest()
    #
    # print("md5_value=",md5_value)

    if(point_v not in g_already_cut_md5_dict):
        g_already_cut_md5_dict[point_v] = True
        return False
    else:
        return True
    #
    return True



def step4_cut_piece_wav24k_c1_wavbuf_param(in_audio_data, in_sr, out_wav_dir, win_ms_len, hop_ms_len, sil_point_value_int):
    global g_sil_point_value_int
    global g_win_ms_len
    global g_hop_ms_len
    global g_win_point_num
    global g_hop_point_num
    global g_sil_win_energy

    global g_already_cut_md5_dict


    g_sil_point_value_int = sil_point_value_int
    g_win_ms_len = win_ms_len
    g_hop_ms_len = hop_ms_len

    g_win_point_num = int( g_win_ms_len * 24)
    g_hop_point_num = int( g_hop_ms_len * 24)

    g_sil_win_energy = (g_win_point_num * g_sil_point_value_int)

    #

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

    bflag_in_voice = False


    cut_start_i = 0
    cut_end_i = 0


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

            # sil -> voice, cut start
            if(not bflag_in_voice):
                bflag_in_voice = True
                #
                cut_start_i = start_i
            # in voice
            else:
                bflag_in_voice = True
                cut_end_i = end_i


        else:
            sil_frame_num += 1

            # in sil
            if(not bflag_in_voice):
                bflag_in_voice = False

                cut_start_i = start_i
        
            # voice end
            else:
                
                #
                cut_end_i = end_i
                #
                cut_wav_len = ( cut_end_i - cut_start_i ) / 24000

                # cut wav is too short
                if(cut_wav_len <= 1.3 or cut_wav_len >= 20.0):
                    cut_start_i = start_i
                    #
                    # continue

                else:
                    bflag_in_voice = False

                    cut_wav_buf = in_audio_data[cut_start_i:cut_end_i]
                    cut_wav_buf_short_int = in_audio_data_abs[cut_start_i:cut_end_i]
                    #
                    bflag_check_md5 = check_already_cut_md5_dict(cut_wav_buf_short_int)
                    #
                    if(bflag_check_md5):
                        cut_start_i = start_i
                        cut_end_i = 0
                    #
                    else:
                        cut_wav_path = get_out_wav_path(out_wav_dir)
                        sf.write(cut_wav_path,cut_wav_buf,in_sr)
                        #
                        # print(cut_wav_path)
                        #
                        cut_start_i = start_i
                        cut_end_i = 0

    return






def step4_cut_piece_wav24k_c1_in_wav_dir_out_dir(in_wav_dir, out_wav_dir):
    # head_sil_point_num = int(90 * 16)

    in_wav_list = os.listdir(in_wav_dir)
    in_wav_list.sort()

    for w_index in range(len(in_wav_list)):
        cur_w_name = in_wav_list[w_index]
        #
        if(cur_w_name[-4:] != ".wav"):
            continue

        in_wav_path = os.path.join(in_wav_dir,cur_w_name)
        #
        in_audio_data, in_sr = sf.read(in_wav_path)

        #
        assert in_sr == 24000

        for i in range(50,300,50):
            for j in range(10,80,10):
                sil_point_value_int = i
                win_ms_len = 2 * j
                hop_ms_len = j
                #
                step4_cut_piece_wav24k_c1_wavbuf_param(in_audio_data, in_sr, out_wav_dir, win_ms_len, hop_ms_len, sil_point_value_int)


    return 





if __name__ == "__main__":
    #
    in_wav_dir = sys.argv[1]
    out_wav_dir = sys.argv[2]
    #
    step4_cut_piece_wav24k_c1_in_wav_dir_out_dir(in_wav_dir, out_wav_dir)

