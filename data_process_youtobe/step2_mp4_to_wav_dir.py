import os
import sys
import random
import shutil
from tqdm import tqdm

global g_suffix_del
g_suffix_del = "mp4"


def wav_to_wav16k(in_dir,out_dir):
    global g_suffix_del
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
        #
        dst_file_path = os.path.join(out_dir,cur_file.split(".")[0] + ".wav")
        #
        if(os.path.exists(dst_file_path)):
            continue
        
        # print(cur_file_path)
        # print(dst_file_path)
        # sox_com = "sox -t flac " + cur_file_path + " -r 16000 -c 1 -b 16 " + dst_file_path

        com1 = "ffmpeg -i " + cur_file_path + " -f wav " + dst_file_path

        #
        os.system(com1)

        # exit(0)
    #
    return 


if __name__ == "__main__":
    in_dir = sys.argv[1]
    out_dir = sys.argv[2]
    #
    wav_to_wav16k(in_dir,out_dir)