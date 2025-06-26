import os
import sys
import random
import shutil
import json
import soundfile as sf


def read_txt_to_list(in_txt):
    #
    cur_f = open(in_txt,"r",encoding="utf8")
    #
    txt_list = []
    #
    for curLine in cur_f.readlines():
        line_cp = curLine.strip()
        #
        if(len(line_cp) <= 0):
            continue
        #
        txt_list.append(line_cp)
    #
    cur_f.close()
    #
    return txt_list


def get_wav_duration(file_path):
    # 方法1：直接读取文件信息（推荐）
    with sf.SoundFile(file_path) as f:
        duration = f.frames / f.samplerate
        return duration
    
    # 方法2：通过读取数据计算（适用于需要处理数据的情况）
    # data, samplerate = sf.read(file_path)
    # duration = len(data) / samplerate
    # return duration




def read_txt_to_list_dict(in_txt):
    #
    cur_f = open(in_txt,"r",encoding="utf8")
    #
    txt_list = []
    #
    for curLine in cur_f.readlines():
        line_cp = curLine.strip()
        #
        if(len(line_cp) <= 0):
            continue
        #
        
        cur_wav = line_cp.split("|")[0].split("=")[1] + ".wav"
        cur_txt = line_cp.split("|")[1].split("=")[1]


        cur_wav_path = os.path.join("wav16k",cur_wav)

        assert os.path.exists(cur_wav_path)


        cur_wav_len = get_wav_duration(cur_wav_path)
        cur_wav_len = round(cur_wav_len,2)

        cur_dict = {}
        cur_dict["audio_filepath"] = cur_wav_path
        cur_dict["duration"] = cur_wav_len
        cur_dict["text"] = cur_txt

        txt_list.append(cur_dict)
    #
    cur_f.close()
    #
    return txt_list


def check_train_json_to_json(in_train_txt,out_json):

    in_train_dict = read_txt_to_list_dict(in_train_txt)
    #
    dst_f_json = open(out_json,"w",encoding="utf8")


    for i in range(len(in_train_dict)):
        cur_dict = in_train_dict[i]
        #print(cur_line)
        #
        # cur_dict["audio_filepath"] = cur_wav_path
        # cur_dict["duration"] = cur_wav_len
        # cur_dict["text"] = cur_txt



        cur_json_dict = {}

        cur_json_dict["audio_filepath"] =  cur_dict["audio_filepath"]
        cur_json_dict["duration"] = cur_dict["duration"]
        cur_json_dict["text"] = cur_dict["text"]

        # if(len(cur_dict["text"]) >= 100):
        #     print(cur_dict["duration"])
        #     print(cur_dict["text"])
        #     continue
        
        json_str = json.dumps(cur_json_dict, ensure_ascii=False)
        dst_f_json.write(json_str + "\n")
        #
    #
    dst_f_json.close()

    #
    return 




if __name__ == "__main__":
    in_train_txt = sys.argv[1]
    out_json = sys.argv[2]

    check_train_json_to_json(in_train_txt,out_json)

