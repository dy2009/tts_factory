import os
import sys
import random
import shutil

global g_suffix_del
g_suffix_del = "wav"

def norm_f0(in_dir,out_dir):
    global g_suffix_del
    #
    file_list = os.listdir(in_dir)
    #
    for i in range(len(file_list)):
        cur_file = file_list[i]
        cur_file_path = os.path.join(in_dir,cur_file)
        #
        dst_file_path = os.path.join(out_dir,cur_file)
        #
        sox_com = "sox --norm=0 " + cur_file_path + " " + dst_file_path
        #
        os.system(sox_com)
    #
    return 


if __name__ == "__main__":
    in_dir = sys.argv[1]
    out_dir = sys.argv[2]
    #
    norm_f0(in_dir,out_dir)