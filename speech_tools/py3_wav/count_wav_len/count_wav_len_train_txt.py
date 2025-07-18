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


def check_1data_fast(in_data_dict):

    in_text = in_data_dict["txt"]
    wav_path = in_data_dict["wav"]
    #

    if(len(in_text) <= 1):
        return False
    #
    wav_file_size = os.path.getsize(wav_path)

    # wav24k -> 58340 -> 793630
    if(wav_file_size <= 58340 or wav_file_size >= 793630):
        return False

    #
    return True

def read_txt_to_list_dict(in_txt):
    #
    out_list = []
    #
    cur_f = open(in_txt,"r",encoding="utf-8")
    #
    spk_id = 0
    spk_dict = {}
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
            if(key1 == "feat_encodec"):
                continue
            #
            if(key1 == "spk_name" and key1 not in spk_dict):
                spk_dict[key1] = spk_id
                #
                spk_id += 1
            #
            if(key1 == "txt" or key1 == "text"):
                cur_dict["txt"] = value1
            elif(key1 == "wav" or key1 == "audio_file"):
                cur_dict["wav"] = value1
            else:
                cur_dict[key1] = value1

        out_list.append(cur_dict)

    #
    cur_f.close()
    #
    return out_list



def count_wav_len_train_txt(in_txt):
    #
    train_list = read_txt_to_list_dict(in_txt)
    #
    #
    line_index = 0
    #
    len_all_s = 0.0
    #
    for i in range(len(train_list)):
        #
        cur_item_dict = train_list[i]
        #
        # seg_list = line_cp.split("|")
        # #
        cur_id = cur_item_dict["id"]
        cur_txt = cur_item_dict["txt"]
        cur_wav_path = cur_item_dict["wav"]
        #
        cur_wav_buf,cur_sr = sf.read(cur_wav_path)
        #
        cur_wav_len_s = int(len(cur_wav_buf) / cur_sr)
        #
        len_all_s += cur_wav_len_s
        line_index += 1
        #
        if(line_index % 2000 == 0):
            print_len_info(line_index,len_all_s)
    #
    print_len_info(line_index,len_all_s)
    #
    #
    return 



if __name__ == "__main__":
    in_txt = sys.argv[1]
    #
    count_wav_len_train_txt(in_txt)