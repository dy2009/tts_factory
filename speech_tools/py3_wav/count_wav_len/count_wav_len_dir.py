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



def count_wav_len_dir(in_dir):
    #
    file_list = os.listdir(in_dir)
    
    #
    txt_list = []
    line_index = 0
    #
    len_all_s = 0.0

    #
    for i in range(len(file_list)):
        
        line_cp = file_list[i]
        line_cp = os.path.join(in_dir,line_cp)
        #
        # seg_list = line_cp.split("|")
        # #
        # cur_id = seg_list[0].split("=")[1]
        # cur_txt = seg_list[1].split("=")[1]
        # cur_wav = seg_list[2].split("=")[1]
        # cur_spk = seg_list[3].split("=")[1]
        #
        cur_wav_buf,cur_sr = sf.read(line_cp)
        #
        cur_wav_len_s = int(len(cur_wav_buf) / cur_sr)
        #
        len_all_s += cur_wav_len_s
        line_index += 1
        #
        # if(line_index % 2000 == 0):
        print_len_info(line_index,len_all_s)
    #
    print_len_info(line_index,len_all_s)
    #

    #
    return 




if __name__ == "__main__":
    in_dir = sys.argv[1]
    #
    count_wav_len_dir(in_dir)