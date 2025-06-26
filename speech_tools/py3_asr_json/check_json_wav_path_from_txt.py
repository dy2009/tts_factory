import os
import sys
import random
import shutil
import json
import time



def check_json_wav_path(in_json,out_json):

    src_f_json = open(in_json,"r",encoding="utf8")

    dst_f_json = open(out_json,"w",encoding="utf8")

    lost_wav = 0

    for cur_line in src_f_json.readlines():
        # print(cur_line)

        cur_line = cur_line.strip()
        if(cur_line == "" or len(cur_line) <= 0):
            continue

        cur_json_dict = json.loads(cur_line)

        cur_wav_path = cur_json_dict["audio_filepath"]

        if(not os.path.exists(cur_wav_path)):
            lost_wav += 1
            continue

        cur_wav_size = os.path.getsize(cur_wav_path)
        if(cur_wav_size <= 2000):
            lost_wav += 1
            continue

        json_str = json.dumps(cur_json_dict, ensure_ascii=False)
        dst_f_json.write(json_str + "\n")

    # print("lost_wav=",lost_wav)

    src_f_json.close()
    dst_f_json.close()

    #
    return lost_wav


def read_txt_to_list(txt_path):
    with open(txt_path, 'r') as f:
        lines = f.readlines()
    return [line.strip() for line in lines]



if __name__ == "__main__":
    in_txt = sys.argv[1]

    in_json_list = read_txt_to_list(in_txt)

    for i in range(len(in_json_list)):
        in_json = in_json_list[i]
        out_json = "tmp.json"

        lost_wav = check_json_wav_path(in_json,out_json)

        if(lost_wav > 0):
            print("lost_wav=",lost_wav,"in_json=",in_json)
            os.remove(in_json)
            time.sleep(1)
            shutil.move(out_json,in_json)
            time.sleep(1)

