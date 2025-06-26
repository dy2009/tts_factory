# coding=utf-8
import os
import sys
import shutil

import soundfile as sf

import requests
import json
import multiprocessing
from multiprocessing import Process

import time

# u"[\u4e00-\u9fa5]"

global g_letter_num
global g_question_num
global g_sigh_num
global g_declarative_num

g_letter_num = 0
g_question_num = 0
g_sigh_num = 0
g_declarative_num = 0


def api_get_1wav(in_txt,cur_id,out_dir):

    # api_com = curl  'https://api.voicelibrary.co/v1/voice-clone-pro/text-to-voice/Pevsdg4VqEIs7LRPOlpuL' \
    #     --header 'api-key: 86ac88a6939dcc15aa7c702e5a02db87' \
    #     --header 'content-type: application/json' \
    #     --header 'accept: application/json' \
    #     --data '{
    #     "text": "The online encyclopedia project Wikipedia"
    #     }'
    # #
    # os.system(api_com)
    # #

    cur_url = 'https://api.voicelibrary.co/v1/voice-clone-pro/text-to-voice/Pevsdg4VqEIs7LRPOlpuL' 
            # "--header 'api-key: 86ac88a6939dcc15aa7c702e5a02db87'" \
            # "--header 'content-type: application/json'" \
            # "--header 'accept: application/json'" \
            
    headers = {"api-key" : "86ac88a6939dcc15aa7c702e5a02db87",
               'content-type':  "application/json",
               "accept" : "application/json"}
        
    # data = {"text": in_txt}

    body = {"text": in_txt}

    # print("requests.post --------------- begin")

    response = requests.post(cur_url, data=json.dumps(body),headers=headers)

    # print("requests.post --------------- end")

    # print(response.text)

    out_wav_path = os.path.join(out_dir,cur_id + ".mp3")

    f = open(out_wav_path,"wb")
    f.write(response.content)
    f.close()


    return 



def api3_txt_to_wav():
    global g_letter_num
    global g_question_num
    global g_sigh_num
    global g_declarative_num

    file_i_path = "/data_1/kongdw_0001/tts_mark_20231029.txt"
    out_dir = "wav_dir"


    #
    i_line = 0
    cur_f = open(file_i_path,"r",encoding="utf8")
    #
    for curLine in cur_f.readlines():
        line_cp = curLine.strip()
        # line_cp = "tts_11lab_000001|Say, Jim, how about going for a few beers after dinner?"
        #
        if(len(line_cp) <= 0):
            continue
        #
        i_line += 1
        # print("1 = ")
        #
        seg_list = line_cp.split("|")
        #tts_11lab_000002|Do you really think so?
        cur_id = seg_list[0]
        cur_txt = seg_list[1]
        #
        # my_letter_
        # 
        head_str10 = cur_id[:10]
        #
        if(cur_id.find("_letter_") >= 0):
            continue

        # print("2 = ")



        out_wav_path = os.path.join(out_dir,cur_id + ".mp3")
        if(os.path.exists(out_wav_path)):
            continue

        out2_wav_path = os.path.join("wav1_mpeg",cur_id + ".mp3")
        if(os.path.exists(out2_wav_path)):
            continue



        last_char = cur_txt[-1:]


        if(head_str10 == "my_letter_"):
            continue
            # if(g_letter_num >= 0):
            #     continue
            # #
            # g_letter_num += 1
            # #
            # api_get_1wav(cur_txt,cur_id,out_dir)

        if(last_char == "?"):
            if(g_question_num >= 500):
                continue
            g_question_num += 1
            #
            print("g_question_num = ",g_question_num)
            api_get_1wav(cur_txt,cur_id,out_dir)


        if(last_char == "!"):
            if(g_sigh_num >= 500):
                continue
            g_sigh_num += 1

        else:
            if(g_declarative_num >= 500):
                continue
            g_declarative_num += 1
        
        #
        api_get_1wav(cur_txt,cur_id,out_dir)

        #exit(0)
        #
        cur_f.close()
        #
        time.sleep(1)
    return 



if __name__ == '__main__':
    #
    api3_txt_to_wav()
