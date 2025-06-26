import os
import sys
import random
import shutil
import json
import time



def check_json_wav_path(in_json):

    src_f_json = open(in_json,"r",encoding="utf8")

    lost_wav = 0

    cur_dict1_text = {}
    cur_dict2_path = {}
    cur_dict3_size = {}


    for cur_line in src_f_json.readlines():
        # print(cur_line)

        cur_line = cur_line.strip()
        if(cur_line == "" or len(cur_line) <= 0):
            continue

        cur_json_dict = json.loads(cur_line)
        cur_wav_path = cur_json_dict["audio_filepath"]
        cur_text = cur_json_dict["text"]

        cur_wav_name = os.path.basename(cur_wav_path)
        cur_text = cur_text.lower()
        cur_wav_size = os.path.getsize(cur_wav_path)


        cur_dict1_text[cur_wav_name] = cur_text
        cur_dict2_path[cur_wav_name] = cur_wav_path
        cur_dict3_size[cur_wav_name] = cur_wav_size

    # print("lost_wav=",lost_wav)

    src_f_json.close()

    #
    return lost_wav


def read_txt_to_list(txt_path):
    with open(txt_path, 'r') as f:
        lines = f.readlines()
    return [line.strip() for line in lines]



if __name__ == "__main__":
    in_train_txt = sys.argv[1]
    in_test_txt = sys.argv[2]

    in_train_json_list = read_txt_to_list(in_train_txt)
    in_test_json_list = read_txt_to_list(in_test_txt)

    # wav_path,text
    train_dict = {}

    for i in range(len(in_train_json_list)):
        in_train_json = in_train_json_list[i]
        #
        cur_dict = check_json_wav_path(in_train_json)


