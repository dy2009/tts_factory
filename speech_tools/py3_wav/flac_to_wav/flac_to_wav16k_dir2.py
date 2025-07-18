import os
import sys
import random
import shutil
from tqdm import tqdm

global g_suffix_del
g_suffix_del = "flac"

def wav_to_wav16k(in_dir,out_dir):
    global g_suffix_del
    #
    dir_list = os.listdir(in_dir)
    dir_list.sort()
    #
    for j in tqdm(range(len(dir_list))):
        j_dir = dir_list[j]
        j_dir_path = os.path.join(in_dir,j_dir)
        #
        file_list = os.listdir(j_dir_path)
        file_list.sort()
        #
        for i in range(len(file_list)):
            cur_file = file_list[i]
            cur_file_name = cur_file.split(".")[0]
            #
            if(cur_file.split(".")[-1] != g_suffix_del):
                continue
            #
            cur_file_path = os.path.join(j_dir_path,cur_file)
            #
            dst_file_path = os.path.join(out_dir,cur_file_name + ".wav")
            #
            sox_com = "sox -t flac " + cur_file_path + " -r 16000 -c 1 -b 16 " + dst_file_path
            #
            os.system(sox_com)
    #
    return 


if __name__ == "__main__":
    in_dir = sys.argv[1]
    out_dir = sys.argv[2]
    #
    wav_to_wav16k(in_dir,out_dir)