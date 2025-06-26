import os
import sys
import random
import shutil
from tqdm import tqdm

global g_suffix_del
g_suffix_del = "wav"

def wav_to_wav16k(in_dir,out_file):
    global g_suffix_del
    #
    file_list = os.listdir(in_dir)
    file_list.sort()
    #
    sox_combine = "sox "
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
    #
    sox_combine += out_file
    #
    os.system(sox_combine)
    return 


if __name__ == "__main__":
    in_dir = sys.argv[1]
    out_file = sys.argv[2]
    #
    wav_to_wav16k(in_dir,out_file)