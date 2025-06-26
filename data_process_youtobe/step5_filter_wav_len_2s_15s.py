import os
import sys
import random
import shutil
from tqdm import tqdm
import soundfile as sf 


global g_suffix_del
g_suffix_del = "wav"

def step5_filter_wav_len_2s_15s(in_dir):
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
        #
        # sox_com = "sox " + cur_file_path + " -r 24000 -c 1 -b 16 " + dst_file_path
        # #
        # os.system(sox_com)
        
        audio_data, in_sr = sf.read(cur_file_path)
        #
        # print(audio_data.shape)
        
        wav_len = audio_data.shape[0] / in_sr
        #
        if(wav_len <= 1.6 or wav_len >= 15.6):
            os.remove(cur_file_path)
        
        
    #
    return 


if __name__ == "__main__":
    # in_dir = sys.argv[1]
    #
    in_dir = "tmp_0001"
    #
    step5_filter_wav_len_2s_15s(in_dir)