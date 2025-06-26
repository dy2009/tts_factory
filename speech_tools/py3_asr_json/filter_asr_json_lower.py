import os
import sys
import random
import shutil
import json



def check_train_json_to_json(in_json,out_json):

    src_f_json = open(in_json,"r",encoding="utf8")
    #
    dst_f_json = open(out_json,"w",encoding="utf8")


    for cur_line in src_f_json.readlines():
        # print(cur_line)

        cur_line = cur_line.strip()
        if(cur_line == "" or len(cur_line) < 0):
            continue

        cur_json_dict = json.loads(cur_line)

        cur_json_dict["text"] = cur_json_dict["text"].lower()

        cur_wav_path = cur_json_dict["audio_filepath"]
        cur_wav_path = os.path.join("/data_3/data_asr_english/wiz_english_48461",cur_wav_path)

        if(not os.path.exists(cur_wav_path)):
            print(cur_wav_path)
            continue

        json_str = json.dumps(cur_json_dict, ensure_ascii=False)
        dst_f_json.write(json_str + "\n")
        #
    #
    src_f_json.close()
    dst_f_json.close()

    #
    return 




if __name__ == "__main__":
    in_json = sys.argv[1]
    out_json = sys.argv[2]

    check_train_json_to_json(in_json,out_json)

