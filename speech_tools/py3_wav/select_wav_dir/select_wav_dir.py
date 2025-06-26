import os
import sys
import random
import shutil

global g_suffix_del
g_suffix_del = "wav"

def select_wav_dir(in_dir,out_dir):
    global g_suffix_del
    #
    dir_list = os.listdir(in_dir)
    dir_list.sort()
    #
    for i in range(len(dir_list)):
        cur_dir = dir_list[i]
        cur_dir_path = os.path.join(in_dir,cur_dir)
        #
        file_list = os.listdir(cur_dir_path)
        file_list.sort()
        #
        for j in range(len(file_list)):
            cur_file = file_list[j]
            cur_file_path = os.path.join(cur_dir_path,cur_file)
            #
            if(cur_file.split(".")[-1] != g_suffix_del):
                continue
            #
            dst_name = cur_dir.lower().replace(" ","_").replace("-","_") + "_{0:06d}".format(j) + ".wav"
            #
            dst_file_path = os.path.join(out_dir,dst_name)
            #
            shutil.copy(cur_file_path,dst_file_path)
            #
            break
    #
    return 


if __name__ == "__main__":
    in_dir = sys.argv[1]
    out_dir = sys.argv[2]
    #
    select_wav_dir(in_dir,out_dir)