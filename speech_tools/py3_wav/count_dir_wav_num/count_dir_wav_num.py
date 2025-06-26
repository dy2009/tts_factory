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



def count_wav_len_dir(in_dir,file_suffix=".wav"):
    #
    file_list = os.listdir(in_dir)

    #
    file_all_num = len(file_list)
    print("file_all_num=",file_all_num)
    cur_wav_num = 0

    #
    for i in range(len(file_list)):

        cur_wav = file_list[i]
        #
    #
    file_list = os.listdir(in_dir)

    #
    file_all_num = len(file_list)
    print("file_all_num=",file_all_num)
    cur_wav_num = 0

    #
    for i in range(len(file_list)):
        
        cur_wav = file_list[i]
        #
        if(cur_wav.endswith(file_suffix)):
            cur_wav_path = os.path.join(in_dir,cur_wav)
            #
            cur_wav_num += 1

    print("cur_wav_num=",cur_wav_num)

    #
    return 




if __name__ == "__main__":
    in_dir = sys.argv[1]
    file_suffix = sys.argv[2]
    #
    count_wav_len_dir(in_dir,file_suffix)