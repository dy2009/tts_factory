import os
import sys
import random
import shutil
from tqdm import tqdm

global g_suffix_del
g_suffix_del = "wav"

global g_out_index
g_out_index = 1


def wav_to_wav16k(in_dir,out_dir):
    global g_suffix_del
    global g_out_index
    #
    file_list = os.listdir(in_dir)
    file_list.sort()
    #
    for i in tqdm(range(len(file_list))):
        cur_file = file_list[i]
        #
        if(cur_file.split(".")[-1] != g_suffix_del):
            continue
        #
        cur_file_path = os.path.join(in_dir,cur_file)
        #
        dst_file = "record_online_{0:06d}".format(g_out_index) + ".wav"
        g_out_index += 1
        #
        dst_file_path = os.path.join(out_dir,dst_file)
        #
        sox_com = "sox " + cur_file_path + " -r 16000 -c 1 -b 16 " + dst_file_path + " & "
        #
        os.system(sox_com)
    #
    return 


if __name__ == "__main__":
    in_dir = sys.argv[1]
    out_dir = sys.argv[2]
    #
    wav_to_wav16k(in_dir,out_dir)