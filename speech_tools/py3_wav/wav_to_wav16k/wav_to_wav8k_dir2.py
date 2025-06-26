import os
import sys
import random
import shutil
from tqdm import tqdm

global g_suffix_del
g_suffix_del = "wav"

def wav_to_wav16k(in_dir,out_dir):
    global g_suffix_del
    #
    if(not os.path.exists(out_dir)):
        os.mkdir(out_dir)

    
    file_list = os.listdir(in_dir)
    file_list.sort()
    #
    for i in tqdm(range(len(file_list))):
        cur_file = file_list[i]
        cur_file_path = os.path.join(in_dir,cur_file)
        dst_file_path = os.path.join(out_dir,cur_file)
        #
        if(os.path.isfile(cur_file_path)):
            if(cur_file.split(".")[-1] != g_suffix_del):
                continue
            #
            sox_com = "sox -t wav " + cur_file_path + " -t wav -r 8000 -c 1 -b 16 " + dst_file_path
            #
            os.system(sox_com)
        elif(os.path.isdir(cur_file_path)):
            os.makedirs(dst_file_path,exist_ok=True)
            #
            wav_to_wav16k(cur_file_path,dst_file_path)

    #
    return 


if __name__ == "__main__":
    in_dir = sys.argv[1]
    out_dir = sys.argv[2]
    #
    wav_to_wav16k(in_dir,out_dir)