import os
import sys
import random
import shutil

global g_suffix_del
g_suffix_del = "wav"

def add_sil(in_dir,out_dir):
    global g_suffix_del
    #
    file_list = os.listdir(in_dir)
    #
    for i in range(len(file_list)):
        cur_file = file_list[i]
        #
        if(cur_file.split(".")[-1] != g_suffix_del):
            continue
        #
        cur_file_path = os.path.join(in_dir,cur_file)
        #
        dst_file_path = os.path.join(out_dir,cur_file)
        #
        sox_com = "sox  sil_50ms.wav " + cur_file_path + " sil_50ms.wav " + dst_file_path
        #
        os.system(sox_com)
    #
    return 


if __name__ == "__main__":
    in_dir = sys.argv[1]
    out_dir = sys.argv[2]
    #
    add_sil(in_dir,out_dir)