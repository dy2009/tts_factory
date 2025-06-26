import os
import sys
import random
import shutil
import json

from tqdm import tqdm

import soundfile as sf



def print_len_info(len_all_s):
    #
    hour_to_second = 60 * 60
    minute_to_second = 60
    #
    # wav_len_hour = int(len_all_s / hour_to_second)
    wav_len_hour_f = len_all_s / hour_to_second
    #
    print("wav_len = ",wav_len_hour_f ," hour")

    #
    return 



def check_train_json_to_json(in_json,out_wav_dir):

    len_all_s = 0.0
    line_index = 0

    src_f_json = open(in_json,"r",encoding="utf8")


    for cur_line in src_f_json.readlines():
        # print(cur_line)

        cur_json_dict = json.loads(cur_line)

        cur_wav_path = cur_json_dict["audio_filepath"]

        cur_wav_buf,cur_sr = sf.read(cur_wav_path)
        #
        cur_wav_len_s = int(len(cur_wav_buf) / cur_sr)
        #
        len_all_s += cur_wav_len_s

        if(line_index % 2000 == 0):
            print_len_info(len_all_s)

    #
    src_f_json.close()

    print_len_info(len_all_s)

    #
    return 




if __name__ == "__main__":
    in_json = sys.argv[1]

    check_train_json_to_json(in_json)

