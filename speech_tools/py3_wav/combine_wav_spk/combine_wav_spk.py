import os
import sys
import random
import shutil
from tqdm import tqdm

global g_suffix_del
g_suffix_del = "wav"


def scan_spk_list(in_dir):
    #
    file_list = os.listdir(in_dir)
    file_list.sort()
    #
    spk_list = []
    #
    for i in range(len(file_list)):
        cur_file = file_list[i]
        #
        cur_spk = cur_file.split("_")[0]
        #
        if(cur_spk not in spk_list):
            spk_list.append(cur_spk)
    #
    return spk_list


def wav_to_wav16k(in_dir,out_dir):
    global g_suffix_del
    #
    file_list = os.listdir(in_dir)
    file_list.sort()
    #
    spk_list = scan_spk_list(in_dir)
    #
    print("spk_list len = ",len(spk_list))

    #
    for i in range(len(spk_list)):
        big_spk_0001 = spk_list[i]
        #
        out_file = os.path.join(out_dir,"spk_" + big_spk_0001 + "_big.wav")
        #
        sox_combine = "sox "
        #
        for j in range(len(file_list)):
            cur_file = file_list[j]
            #
            # if(cur_file.split(".")[-1] != g_suffix_del):
            #     continue
            #
            cur_spk = cur_file.split("_")[0]
            #
            if(big_spk_0001 != cur_spk):
                continue
            #
            cur_file_path = os.path.join(in_dir,cur_file)
            #
            sox_combine += cur_file_path
            sox_combine += " "
        #
        sox_combine += out_file
        #
        os.system(sox_combine)
    #
    return 


if __name__ == "__main__":
    in_dir = sys.argv[1]
    out_dir = sys.argv[2]
    #
    wav_to_wav16k(in_dir,out_dir)