import os
import sys
import random
import shutil
import soundfile as sf
# import torch
import numpy as np


def read_txt_to_list(in_txt):
    #
    cur_f = open(in_txt,"r",encoding="utf8")
    #
    txt_list = []
    #
    for curLine in cur_f.readlines():
        line_cp = curLine.strip()
        #
        txt_list.append(line_cp)
    #
    cur_f.close()
    #
    return txt_list



def count_wav_len_dir(in_dir,short_wav_len):
    #
    file_list = os.listdir(in_dir)
    # file_list.sort()

    del_num = 0
    count_num = 0

    #
    for i in range(len(file_list)):
        
        cur_wav = file_list[i]
        cur_wav_path = os.path.join(in_dir,cur_wav)
        #
        #
        try:
            cur_wav_buf, cur_sr = sf.read(cur_wav_path)
            #
            # cur_wav_buf = cur_wav_buf * 32768
            # cur_wav_buf = cur_wav_buf.astype(np.int16)

            #
            cur_wav_len_s = int(len(cur_wav_buf) / cur_sr)
            #
            count_num += 1
            #
            if(cur_wav_len_s <= short_wav_len):
                os.remove(cur_wav_path)

                del_num += 1
                print("count_num=",count_num,",del_num = ",del_num)
        except Exception as e:
            os.remove(cur_wav_path)
            pass

    #
    print("count_num=",count_num,",del_num = ",del_num)

    return 




if __name__ == "__main__":
    in_dir = sys.argv[1]

    short_wav_len = 1.5
    #
    count_wav_len_dir(in_dir,short_wav_len)