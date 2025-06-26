import os
import sys
import random
import shutil

import soundfile as sf 
import numpy as np

from tqdm import tqdm

from multiprocessing import Process

global g_suffix_del
g_suffix_del = "wav"


sil_90ms_point_num = int((24000 / 1000) * 90)


def step7_add_90ms_sil_to_wav24k_1wav(cur_file_path,dst_file_path,cur_file):
    #
    if(not os.path.exists(cur_file_path)):
        return 
    #
    in_audio_data,in_sr = sf.read(cur_file_path)
    #
    assert in_sr == 24000
    #
    # max_v = np.max(in_audio_data)
    # min_v = np.min(in_audio_data)
    
    # print("in_audio_data=",in_audio_data.shape)
    # print("max_v=",max_v)
    # print("min_v=",min_v)
    # exit(0)
    #
    
    # 0-1
    sil_90ms_buf = (np.random.randn(sil_90ms_point_num) - 0.5) * 0.0009
    
    in_audio_data = np.concatenate((sil_90ms_buf,in_audio_data,sil_90ms_buf))
    # exit(0)
    
    # print("in_audio_data=",in_audio_data.shape)
    # exit(0)
    
    #
    sf.write(dst_file_path,in_audio_data,in_sr)
    #
    # dst_file_path2 = os.path.join("F:\\tts_indonesia_youtobe_data\\wav24k_piece_0002\\",cur_file)
    
    # sf.write(dst_file_path2,in_audio_data,in_sr)
    #
    os.remove(cur_file_path)
    #
    
    #
    return 




def step7_add_90ms_sil_to_wav24k(in_dir,out_dir,cur_part_n):
    global g_suffix_del
    #
    file_list = os.listdir(in_dir)
    # file_list.sort()
    
    wav_len = len(file_list)
    
    wav_len_10fz1 = int(wav_len / 5.0)
    
    assert cur_part_n >= 1 and cur_part_n <= 10
    
    part_i = cur_part_n - 1
    
    start_i = (part_i) *  wav_len_10fz1
    end_i = (part_i + 1) *  wav_len_10fz1
    
    file_list = file_list[ start_i : end_i ]
    
    
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
        # if(os.path.exists(dst_file_path)):
        #     continue
        #
        # sox stereo.wav left.wav remix 1 # 提取左声道音频
        
        step7_add_90ms_sil_to_wav24k_1wav(cur_file_path,dst_file_path,cur_file)
        
        # p = Process(target=step7_add_90ms_sil_to_wav24k_1wav, args=(cur_file_path,dst_file_path,cur_file))
        # p.start()
        
    #
    return 


if __name__ == "__main__":
    cur_part_n = int(sys.argv[1])
    
    # out_dir = sys.argv[2]
    #
    in_dir = "D:\\wav24k_piece_0001"
    out_dir = "D:\\data\\tts_indonesia\\youtobe_raw_data\\wav24k_piece_0002"
    
    
    step7_add_90ms_sil_to_wav24k(in_dir,out_dir,cur_part_n)
