import os
import sys
import random
import shutil
from tqdm import tqdm

global g_suffix_del
g_suffix_del = "wav"

def wav_to_wav16k(in_dir,out_dir):
    global g_suffix_del
    #
    file_list = os.listdir(in_dir)
    file_list.sort()
    #
    sox_combine = "sox "
    #
    add_wav = 0
    out_i = 1
    #
    for i in range(len(file_list)):
        cur_file = file_list[i]
        #
        if(cur_file.split(".")[-1] != g_suffix_del):
            continue
        #
        cur_file_path = os.path.join(in_dir,cur_file)
        #
        sox_combine += cur_file_path
        sox_combine += " "
        add_wav += 1
        #
        if((i + 1) % 50 == 0):
            #
            # print(i)
            out_file = "big_{0:06d}".format(out_i) + ".wav"
            out_i += 1
            #
            # print(out_file)

            out_file_path = os.path.join(out_dir,out_file)
            sox_combine += out_file_path
            #
            os.system(sox_combine)
            #
            sox_combine = "sox "
            add_wav = 0
    #
    if(add_wav > 0):
        out_file = "big_{0:06d}".format(out_i) + ".wav"
        out_i += 1
        #
        out_file_path = os.path.join(out_dir,out_file)
        sox_combine += out_file_path
        #
        os.system(sox_combine)
        #
        sox_combine = "sox "
        add_wav = 0

    return 


if __name__ == "__main__":
    in_dir = sys.argv[1]
    out_dir = sys.argv[2]
    #
    wav_to_wav16k(in_dir,out_dir)