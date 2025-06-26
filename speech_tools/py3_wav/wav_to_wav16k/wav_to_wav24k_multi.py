import os
import sys
import random
import shutil
from multiprocessing import Process

import time

from tqdm import tqdm

global g_suffix_del
g_suffix_del = "wav"



def proce_1wav(cur_file_path,dst_file_path):
    #
    sox_com = "sox " + cur_file_path + " -r 24000 -c 1 -b 16 " + dst_file_path + " &"
    #
    os.system(sox_com)
    #
    
    time.sleep(5)
    #
    os.remove(cur_file_path)
        
    return 



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
        dst_file_path = os.path.join(out_dir,cur_file)
        #
        
        p = Process(target=proce_1wav, args=(cur_file_path,dst_file_path,))
        p.start()
        # p.join()
    

    #
    return 


if __name__ == "__main__":
    in_dir = sys.argv[1]
    out_dir = sys.argv[2]
    #
    wav_to_wav16k(in_dir,out_dir)