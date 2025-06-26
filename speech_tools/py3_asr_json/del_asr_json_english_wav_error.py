import os
import sys
import random
import shutil
import json
# import enchant

# english_checker = enchant.Dict("en_US")




def check_text_is_english():
    return 



def read_json_to_dict(in_json):

    #
    wav_dict = {}
    #
    src_f_json = open(in_json,"r",encoding="utf8")
    #
    for cur_line in src_f_json.readlines():
        cur_line = cur_line.strip()
        if(cur_line == "" or len(cur_line) < 0):
            continue

        cur_json_dict = json.loads(cur_line)

        cur_wav_path = cur_json_dict["audio_filepath"]
        #
        if(os.path.exists(cur_wav_path)):
            # continue
            wav_dict[cur_wav_path] = True

    #
    src_f_json.close()
    #
    return wav_dict




def check_train_json_to_json(old_json,new_json):

    new_json_dict = read_json_to_dict(new_json)
    #
    dst_f_json = open(old_json,"r",encoding="utf8")

    del_num = 0

    for cur_line in dst_f_json.readlines():
        # print(cur_line)

        cur_line = cur_line.strip()
        if(cur_line == "" or len(cur_line) < 0):
            continue

        cur_json_dict = json.loads(cur_line)

        cur_wav_path = cur_json_dict["audio_filepath"]

        #
        if(cur_wav_path not in new_json_dict):
            if(os.path.exists(cur_wav_path)):
                del_num += 1
                print("del_num=",del_num)
                os.remove(cur_wav_path)
    #
    dst_f_json.close()

    #
    return 




if __name__ == "__main__":
    old_json = sys.argv[1]
    new_json = sys.argv[2]

    check_train_json_to_json(old_json,new_json)

