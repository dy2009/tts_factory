import os
import sys
import random
import shutil
from tqdm import tqdm

global g_suffix_del
g_suffix_del = "wav"


def read_txt_to_list(in_txt):
    #
    out_list = []
    #
    cur_f = open(in_txt,"r",encoding="utf-8")
    #
    for curLine in cur_f.readlines():
        line_cp = curLine.strip()
        #
        if(len(line_cp) <= 0):
            continue
        #
        out_list.append(line_cp)
    #
    cur_f.close()
    #
    return out_list


def wav_to_wav16k(in_wav_txt,out_dir):
    global g_suffix_del
    #
    file_list = read_txt_to_list(in_wav_txt)

    #
    for i in tqdm(range(len(file_list))):
        cur_file = file_list[i]
        #
        if(cur_file.split(".")[-1] != g_suffix_del):
            continue
        #
        cur_file_path = cur_file
        dst_file = os.path.basename(cur_file)
        #
        dst_file_path = os.path.join(out_dir,dst_file)
        #
        if(os.path.exists(dst_file_path)):
            continue
        #
        sox_com = "sox " + cur_file_path + " -r 16000 -c 1 -b 16 " + dst_file_path + " & "
        #
        os.system(sox_com)
    #
    return 


if __name__ == "__main__":
    in_wav_txt = sys.argv[1]
    out_dir = sys.argv[2]
    #
    wav_to_wav16k(in_wav_txt,out_dir)