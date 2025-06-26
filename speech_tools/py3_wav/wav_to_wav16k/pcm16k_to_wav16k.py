import os
import sys
import random
import shutil
from tqdm import tqdm

global g_suffix_del
g_suffix_del = "pcm"

def wav_to_wav16k(in_dir,out_dir):
    global g_suffix_del
    #
    file_list = os.listdir(in_dir)
    # file_list.sort()
    #
    for i in tqdm(range(len(file_list))):
        cur_file = file_list[i]
        #
        if(cur_file.split(".")[-1] != g_suffix_del):
            continue
        #
        cur_file_path = os.path.join(in_dir,cur_file)
        #
        dst_file_path = os.path.join(out_dir,cur_file.replace(".pcm",".wav"))
        #
        # sox_com = "sox " + cur_file_path + " -r 16000 -c 1 -b 16 " + dst_file_path + " & "

        sox_com = "sox -t raw -r 16000 -e signed-integer -b 16 -c 1 " + cur_file_path + " -t wav  -r 16000 -c 1 -b 16 " + dst_file_path + " & "
        #
        os.system(sox_com)
    #
    return 


if __name__ == "__main__":
    in_dir = sys.argv[1]
    out_dir = sys.argv[2]
    #
    wav_to_wav16k(in_dir,out_dir)