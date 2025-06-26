import os
import sys
import random
import shutil
import json
import time



def check_json_wav_path(in_json,dst_f):

    text_list = []

    src_f_json = open(in_json,"r",encoding="utf8")

    for cur_line in src_f_json.readlines():
        # print(cur_line)

        cur_line = cur_line.strip()
        if(cur_line == "" or len(cur_line) <= 0):
            continue

        cur_json_dict = json.loads(cur_line)

        cur_wav_path = cur_json_dict["audio_filepath"]
        cur_text = cur_json_dict["text"]

        dst_f.write(cur_text + "\n")


    src_f_json.close()

    #
    return 


def read_txt_to_list(txt_path):
    with open(txt_path, 'r') as f:
        lines = f.readlines()
    return [line.strip() for line in lines]



if __name__ == "__main__":
    in_txt = sys.argv[1]

    out_text = sys.argv[2]

    in_json_list = read_txt_to_list(in_txt)

    dst_f = open(out_text,"w",encoding="utf8")

    for i in range(len(in_json_list)):
        in_json = in_json_list[i]

        lost_wav = check_json_wav_path(in_json,dst_f)

    dst_f.close()

