import os
import sys
import random
import shutil

global g_suffix_del
g_suffix_del = "wav"

global g_channel_str
g_channel_str = "left"


def sox_extract_channel(in_dir,out_dir):
    global g_channel_str
    global g_suffix_del
    #
    file_list = os.listdir(in_dir)
    file_list.sort()
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
        # sox stereo.wav left.wav remix 1 # 提取左声道音频
        #
        # 1= left, 2=right
        sox_com = "sox " + cur_file_path + " " + dst_file_path + " remix 1 "
        #
        os.system(sox_com)
    #
    return 


if __name__ == "__main__":
    in_dir = sys.argv[1]
    out_dir = sys.argv[2]
    #
    sox_extract_channel(in_dir,out_dir)