import os
import sys
import random
import shutil
import json

from tqdm import tqdm

import soundfile as sf


def check_train_json_to_json(in_json):

    name_dict = {}
    wav_path_dict = {}
    repeat_num = 0
    same_name_num = 0

    src_f_json = open(in_json,"r",encoding="utf8")


    for cur_line in src_f_json.readlines():
        # print(cur_line)

        cur_json_dict = json.loads(cur_line)

        cur_wav_path = cur_json_dict["audio_filepath"]
        cur_wav_name = os.path.basename(cur_wav_path)

        if(cur_wav_name not in name_dict):
            name_dict[cur_wav_name] = True
            wav_path_dict[cur_wav_name] = cur_wav_path
        else:
            same_name_num += 1

            if(cur_wav_path == wav_path_dict[cur_wav_name]):
                continue
            else:
                # print("cur_wav_name=",cur_wav_name)
                repeat_num += 1

    #
    print("repeat_num=",repeat_num,",same_name_num=",same_name_num)

    #
    return 




if __name__ == "__main__":
    in_json = sys.argv[1]

    check_train_json_to_json(in_json)

