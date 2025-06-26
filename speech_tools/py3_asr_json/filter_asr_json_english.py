import os
import sys
import random
import shutil
import json
import re


def has_digit(text):
    return bool(re.search(r'\d', text))  # \d 匹配任何数字字符



def filter_text_illegal(new_text):
    new_text = new_text.replace("-"," ").strip().lower()
    new_text = new_text.replace("\t"," ").strip()
    new_text = new_text.replace("  "," ").strip()
    new_text = new_text.replace(","," ").strip()
    new_text = new_text.replace("."," ").strip()
    new_text = new_text.replace("?"," ").strip()
    new_text = new_text.replace("!"," ").strip()

    new_text = new_text.replace("  "," ").strip()
    new_text = new_text.replace("  "," ").strip()
    new_text = new_text.replace("  "," ").strip()
    new_text = new_text.replace("  "," ").strip()
    new_text = new_text.replace("  "," ").strip()

    return new_text



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

        new_text = cur_json_dict["text"].lower()

        new_text = filter_text_illegal(new_text)

        bflag_have_num = has_digit(new_text)
        if(bflag_have_num):
            continue

        cur_json_dict["text"] = new_text

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

