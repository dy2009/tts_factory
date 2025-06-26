import os
import sys
import random
import shutil
from tqdm import tqdm
import soundfile as sf 


global g_suffix_del
g_suffix_del = "wav"



def move_wav_dir(in_dir,out_dir):
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
        out_file_path = os.path.join(out_dir,cur_file)
        #
        shutil.move(cur_file_path,out_file_path)

        
        
    #
    return 




if __name__ == "__main__":
    # in_dir = sys.argv[1]
    # out_dir = sys.argv[2]
    #
    in_dir = sys.argv[1]
    out_dir = sys.argv[2]
    

    
    # in_dir = "tmp_0001"
    #
    move_wav_dir(in_dir,out_dir)