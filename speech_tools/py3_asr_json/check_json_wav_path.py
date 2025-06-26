import os
import sys
import random
import shutil
import json

from tqdm import tqdm

import soundfile as sf


def check_json_wav_path(in_json):

    src_f_json = open(in_json,"r",encoding="utf8")

    lost_wav = 0

    for cur_line in src_f_json.readlines():
        # print(cur_line)

        # cur_line = cur_line.strip()
        # if(cur_line == ""):
        #     continue

        cur_json_dict = json.loads(cur_line)

        cur_wav_path = cur_json_dict["audio_filepath"]

        if(not os.path.exists(cur_wav_path)):
            lost_wav += 1
            continue
        
    print("lost_wav=",lost_wav)

    #
    return 




if __name__ == "__main__":
    in_json = sys.argv[1]

    check_json_wav_path(in_json)

