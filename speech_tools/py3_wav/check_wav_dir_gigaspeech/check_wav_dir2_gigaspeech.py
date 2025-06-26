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



def check_wav_dir_gigaspeech(in_dir):
    #
    g_id_dict = {}
    error_num = 0
    #
    dir_list = os.listdir(in_dir)
    dir_list.sort()
    #
    for i in range(len(dir_list)):
        #
        cur_dir_name = dir_list[i]
        cur_dir_path = os.path.join(in_dir,cur_dir_name)
        #
        if(os.path.isdir(cur_dir_path)):
            #
            file_list = os.listdir(cur_dir_path)
            #
            for j in range(len(file_list)):
                cur_j = file_list[j]
                cur_wav_path = os.path.join(cur_dir_path,cur_j)
                #
                cur_id = cur_j.split(".")[0]
                cur_suffix = cur_j.split(".")[-1]
                #
                if(cur_suffix != "wav"):
                    continue
                #
                if(cur_id not in g_id_dict):
                    g_id_dict[cur_id] = 1
                else:
                    error_num += 1
    #
    print("error_num=",error_num)
    #
    return 




if __name__ == "__main__":
    in_dir = sys.argv[1]
    #
    check_wav_dir_gigaspeech(in_dir)