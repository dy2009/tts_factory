import os
import sys
import random
import shutil
import numpy as np
from tqdm import tqdm
import soundfile as sf

global g_suffix_del
g_suffix_del = "wav"


global g_index
g_index = 1

global g_sil_threshold
g_sil_threshold = 50

def cut_wav_sil(cur_file_path,out_dir):
    global g_index
    global g_sil_threshold
    #
    in_wav,in_sr = sf.read(cur_file_path)
    in_wav_short = in_wav * 32768
    #
    start_i = 0
    end_i = 0
    #
    head_sil = np.zeros(800,dtype=float)
    tail_sil = np.zeros(800,dtype=float)
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

    sil_p_num = 0
    start_index = 0
    bflag_cut = False
    #
    for i in range(len(in_wav2_short)):
        cur_p_i = abs(in_wav2_short[i])
        #
        if(cur_p_i <= g_sil_threshold):
            if(bflag_cut):
                start_index = i
                continue
            #
            else:
                sil_p_num += 1
                #
                #print(sil_p_num)
                if(sil_p_num >= 600):
                    #
                    if(i - start_index < 16000 * 0.4):
                        #print("2-----")
                        continue
                    #
                    wav_piect_i_s = in_wav2_short[start_index:i]
                    wav_piect_i_s_sum = np.sum(abs(wav_piect_i_s))
                    #
                    if(wav_piect_i_s_sum < (i - start_index) * 40):
                        sil_p_num = 0
                        bflag_cut = False
                        #print("3-----")
                        continue
                    #
                    wav_piect_i = np.hstack((head_sil,in_wav2[start_index:i],tail_sil))
                    #
                    dst_name = "chloe2_online_" + "{0:04d}".format(g_index) + ".wav"
                    dst_wav_path = os.path.join(out_dir,dst_name)
                    g_index += 1
                    #
                    sf.write(dst_wav_path,wav_piect_i,16000)
                    #

                    #cut
                    sil_p_num = 0
                    start_index = i
                    bflag_cut = True
        else:
            sil_p_num = 0
            bflag_cut = False

    #
    if(len(in_wav2_short) - start_index > 16000 * 0.4):
        #
        wav_piect_i_s = in_wav2_short[start_index:]
        wav_piect_i_s_sum = np.sum(abs(wav_piect_i_s))
        #
        if(wav_piect_i_s_sum > (len(in_wav2_short) - start_index) * 40):
            #
            wav_piect_i = np.hstack((head_sil,in_wav2[start_index:],tail_sil))
            #
            dst_name = "chloe2_online_" + "{0:04d}".format(g_index) + ".wav"
            dst_wav_path = os.path.join(out_dir,dst_name)
            g_index += 1
            #
            sf.write(dst_wav_path,wav_piect_i,16000)
            #
    


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
    #
    wav_to_wav16k(in_dir,out_dir)