import os
import sys
import random
import shutil
import json
import re

from tqdm import tqdm

import soundfile as sf

from langdetect import detect,detect_langs



# def check_text_is_english(in_text):
#     try:
#         return detect(in_text) == 'en'
#     except:
#         return False

# 0->en, 1->tamil, 2->mix, 3-> other
def check_text_is_english(in_text):
    try:
        results = detect_langs(in_text)
        #
        for result in results:
            if result.lang == 'ta' and result.prob > 0.8:
                return 1
            elif result.lang == 'en' and result.prob > 0.8:
                return 0
        return 2
    except:
        return 3


def is_pure_english(text):
    """
    判断文本是否为纯英文（包含字母、空格和英文标点符号）
    规则：所有字符必须是ASCII字符，且属于英文可接受字符集
    """
    # 正则表达式匹配：字母、空格和常见英文标点
    pattern = r'^[A-Za-z\s,.!?\'"-]+$'
    return bool(re.fullmatch(pattern, text))



def is_pure_tamil(text):
    """
    判断文本是否为纯泰米尔语（包含字母、空格和泰米尔语标点符号）
    规则：所有字符必须在泰米尔语Unicode范围内（U+0B80-U+0BFF）
    """
    # 泰米尔语Unicode范围：U+0B80到U+0BFF（含字母、数字和标点）
    tamil_pattern = r'^[\u0B80-\u0BFF\s]+$'
    return bool(re.fullmatch(tamil_pattern, text))



def check_train_json_to_json(in_json,out_json):

    src_f_json = open(in_json,"r",encoding="utf8")
    #
    dst_f_json = open(out_json,"w",encoding="utf8")

    dst2_f_json = open("asr_tamil.json","w",encoding="utf8")

    dst3_f_json = open("asr_english_tamil_mix.json","w",encoding="utf8")

    mix_num = 0


    for cur_line in src_f_json.readlines():
        # print(cur_line)

        cur_json_dict = json.loads(cur_line)

        cur_wav_path = cur_json_dict["audio_filepath"]
        cur_text = cur_json_dict["text"]

        bflag_is_eng = is_pure_english(cur_text)
        bflag_is_tamil = is_pure_tamil(cur_text)

# 0->en, 1->tamil, 2->mix, 3-> other
        if(bflag_is_eng):
            json_str = json.dumps(cur_json_dict, ensure_ascii=False)
            dst_f_json.write(json_str + "\n")
            #
        elif(bflag_is_tamil):
            json_str = json.dumps(cur_json_dict, ensure_ascii=False)
            dst2_f_json.write(json_str + "\n")
        else:
            json_str = json.dumps(cur_json_dict, ensure_ascii=False)
            dst3_f_json.write(json_str + "\n")
    #
    src_f_json.close()
    dst_f_json.close()

    dst2_f_json.close()
    dst3_f_json.close()

    #
    return 




if __name__ == "__main__":
    in_json = sys.argv[1]
    out_json = sys.argv[2]

    check_train_json_to_json(in_json,out_json)

