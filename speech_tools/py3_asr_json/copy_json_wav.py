import os
import sys
import random
import shutil
import json

from tqdm import tqdm

import soundfile as sf


def check_train_json_to_json(in_json,out_wav_dir):

    src_f_json = open(in_json,"r",encoding="utf8")


    for cur_line in src_f_json.readlines():
        # print(cur_line)

        cur_json_dict = json.loads(cur_line)

        cur_wav_path = cur_json_dict["audio_filepath"]

        shutil.copy(cur_wav_path,out_wav_dir)
        #
    #
    src_f_json.close()

    #
    return 




if __name__ == "__main__":
    in_json = sys.argv[1]
    out_wav_dir = sys.argv[2]

    check_train_json_to_json(in_json,out_wav_dir)

