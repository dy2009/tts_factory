import os
import sys
import random
import shutil
import time
from tqdm import tqdm

global g_suffix_del
g_suffix_del = "wav"

def norm_f0(in_dir,out_dir):
    global g_suffix_del
    #
    file_list = os.listdir(in_dir)
    #
    for i in tqdm(range(len(file_list))):
        cur_file = file_list[i]
        #
        if(cur_file.split(".")[-1] != g_suffix_del):
            continue
        #
        cur_file_path = os.path.join(in_dir,cur_file)
        #
        dst_file_path = os.path.join(out_dir,cur_file)
        #
        sox_com = "sox --norm=-1 " + cur_file_path + " " + dst_file_path + " &"
        #
        os.system(sox_com)
        #
        if(i % 500 ==0):
            time.sleep(3)

    #
    return 


if __name__ == "__main__":
    in_dir = sys.argv[1]
    out_dir = sys.argv[2]
    #
    norm_f0(in_dir,out_dir)