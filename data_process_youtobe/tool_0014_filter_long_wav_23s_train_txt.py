import os
import sys
import random
import shutil
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
        txt_list.append(line_cp)
    #
    cur_f.close()
    #
    return txt_list


def combine_dict_to_line(in_dict):
    #
    out_line = ""
    #
    for key in in_dict:
        value = in_dict[key]
        #
        out_line += key + "=" + value
        out_line += "|"
        #
    #
    out_line = out_line[:-1]
    #
    return out_line



def read_txt_to_list_dict(in_txt):
    #
    out_list = []
    #
    cur_f = open(in_txt,"r",encoding="utf-8")
    #
    for curLine in cur_f.readlines():
        line_cp = curLine.strip()
        #
        if(len(line_cp) <= 0):
            continue
        #
        cur_dict = {}
        #
        seg_list = line_cp.split("|")
        #
        for i in range(len(seg_list)):
            seg_list_i = seg_list[i]
            #
            key1 = seg_list_i.split("=")[0]
            value1 = seg_list_i.split("=")[1]
            #
            if(key1 == "txt" or key1 == "text"):
                cur_dict["text"] = value1
            elif(key1 == "wav" or key1 == "audio_file"):
                cur_dict["wav"] = value1
            else:
                cur_dict[key1] = value1
        #
        
        out_list.append(cur_dict)
    #
    cur_f.close()
    #
    return out_list




def print_len_info(line_index,len_all_s):
    #
    hour_to_second = 60 * 60
    minute_to_second = 60
    #
    # wav_len_hour = int(len_all_s / hour_to_second)
    wav_len_hour_f = len_all_s / hour_to_second
    #
    print(line_index,"wav_len = ",wav_len_hour_f ," hour")

    #
    #
    return 



def tool_0010_del_long_wav_wav_txt(in_train_txt,out_train_txt):
    #

    # wav_list = read_txt_to_list(in_train_txt)

    wav_list = read_txt_to_list_dict(in_train_txt)


    dst_f = open(out_train_txt,"w",encoding="utf8")
    
    #
    for i in range(len(wav_list)):
        
        #
        cur_dict_item = wav_list[i]
        #
        cur_wav_path = cur_dict_item["wav"]

        #
        cur_wav_buf, cur_sr = sf.read(cur_wav_path)
        #
        cur_wav_len_s = int(len(cur_wav_buf) / cur_sr)

        #>>> print(1192 * 0.024) = 28.608
        # 992 * 0.024 = 23.808
        if(cur_wav_len_s < 23):
            # os.remove(cur_wav_path)
            out_line = combine_dict_to_line(cur_dict_item)
            #
            dst_f.write(out_line + "\n")
    #
    dst_f.close()

    #
    return 




if __name__ == "__main__":
    in_train_txt = sys.argv[1]
    out_train_txt = sys.argv[2]
    #
    tool_0010_del_long_wav_wav_txt(in_train_txt,out_train_txt)