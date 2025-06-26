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
    dir_list = os.listdir(in_dir)
    dir_list.sort()


    for j in range(len(dir_list)):
        cur_dir = dir_list[j]
        cur_dir_path = os.path.join(in_dir,cur_dir)
        #
        dst_dir_path = os.path.join(out_dir,cur_dir)
        #
        if(not os.path.exists(dst_dir_path)):
            os.mkdir(dst_dir_path)

        file_list = os.listdir(cur_dir_path)
        file_list.sort()

        #
        for i in tqdm(range(len(file_list))):
            cur_file = file_list[i]
            #
            if(cur_file.split(".")[-1] != g_suffix_del):
                continue
            #
            cur_file_path = os.path.join(cur_dir_path,cur_file)
            #
            dst_file_path = os.path.join(dst_dir_path,cur_file)
            #
            sox_com = "sox --norm=-1 " + cur_file_path + " " + dst_file_path + " &"
            #
            os.system(sox_com)
            #

    #
    return 


if __name__ == "__main__":
    in_dir = sys.argv[1]
    out_dir = sys.argv[2]
    #
    norm_f0(in_dir,out_dir)