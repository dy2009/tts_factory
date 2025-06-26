import os
import sys
import random
import shutil
from tqdm import tqdm

global g_suffix_del
g_suffix_del = "mp4"


global g_index
g_index = 1


def rename_dir_file(in_dir,out_dir):
    global g_suffix_del
    global g_index
    #
    file_list = os.listdir(in_dir)
    file_list.sort()
    #
    #
    for i in tqdm(range(len(file_list))):
        cur_file = file_list[i]
        src_wav_path = os.path.join(in_dir,cur_file)
        #
        if(cur_file.split(".")[1] != g_suffix_del):
            continue

        #
        #
        new_file = "indonesia_youtobe_" + "{0:06d}".format(g_index) + ".mp4"
        #
        new_wav_path = os.path.join(in_dir,new_file)
        #
        # shutil.copy(src_wav_path,new_wav_path)
        
        os.rename(src_wav_path,new_wav_path)
        #
        g_index += 1


if __name__ == "__main__":
    in_dir = sys.argv[1]
    out_dir = sys.argv[2]
    #
    rename_dir_file(in_dir,out_dir)
