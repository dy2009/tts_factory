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

    # hour_rest = len_all_s - wav_len_hour * hour_to_second
    # #
    # wav_len_minute = int(hour_rest / minute_to_second)
    # minute_rest = int(hour_rest - wav_len_minute * minute_to_second)
    # #
    # print(line_index,"wav_len = ",wav_len_hour ," hour, ", wav_len_minute ," minute, ", minute_rest ," second.")
    # print("wav_len = {0:6d} hour, {0:2d} ",wav_len_hour ," hour, ", wav_len_minute ," minute, ", minute_rest ," second.")
    #
    return 



def split_json_train_test(in_txt,out_json_name):
    #
    cur_f = open(in_txt,"r",encoding="utf8")
    #

    dst_f_train = open(out_json_name + "_train.json","w")
    dst_f_test = open(out_json_name + "_test.json","w")
    
    line_index = 0
    #
    len_all_s = 0.0

    #
    for curLine in cur_f.readlines():
        line_cp = curLine.strip()
        #
        line_index += 1
        #
        if(line_index % 5 == 0):
            dst_f_test.write(line_cp + "\n")
        else:
            dst_f_train.write(line_cp + "\n")

    #
    cur_f.close()
    dst_f_train.close()
    dst_f_test.close()
    #
    return 



if __name__ == "__main__":
    in_txt = sys.argv[1]
    out_json_name = sys.argv[2]
    #
    split_json_train_test(in_txt,out_json_name)