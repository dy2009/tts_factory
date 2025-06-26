import os
import sys
import random
import shutil
from tqdm import tqdm

global g_suffix_del
g_suffix_del = "wav"


def wav_to_wav16k(cur_file_path,dst_file_path):
    global g_suffix_del
    #
    #
    sox_com = "sox " + cur_file_path + " -r 16000 -c 1 -b 16 " + dst_file_path
    #
    os.system(sox_com)
    #
    return 


if __name__ == "__main__":
    in_dir = sys.argv[1]
    out_dir = sys.argv[2]
    #
    wav_to_wav16k(in_dir,out_dir)