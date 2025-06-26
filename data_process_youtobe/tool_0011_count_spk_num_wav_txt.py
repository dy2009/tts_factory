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

    # hour_rest = len_all_s - wav_len_hour * hour_to_second
    # #
    # wav_len_minute = int(hour_rest / minute_to_second)
    # minute_rest = int(hour_rest - wav_len_minute * minute_to_second)
    # #
    # print(line_index,"wav_len = ",wav_len_hour ," hour, ", wav_len_minute ," minute, ", minute_rest ," second.")
    # print("wav_len = {0:6d} hour, {0:2d} ",wav_len_hour ," hour, ", wav_len_minute ," minute, ", minute_rest ," second.")
    #
    return 



def tool_0011_count_spk_num_wav_txt(in_train_txt):
    #

    wav_list = read_txt_to_list(in_train_txt)
    #
    spk_dict = {}
    
    #
    for i in range(len(wav_list)):
        
        #
        cur_wav_path = wav_list[i]

        cur_id = os.path.basename(cur_wav_path)

        # haitian_mix_004692
        cur_spk = cur_id.split("_")[0]

        #
        if(cur_spk not in spk_dict):
            spk_dict[cur_spk] = 1
        else:
            spk_dict[cur_spk] = spk_dict[cur_spk] + 1

        #
        # cur_wav_buf,cur_sr = sf.read(cur_wav_path)
        # #
        # cur_wav_len_s = int(len(cur_wav_buf) / cur_sr)

        # #>>> print(1192 * 0.024) = 28.608
        # # 992 * 0.024 = 23.808
        # if(cur_wav_len_s >= 28.5):
        #     os.remove(cur_wav_path)
    #
    print(spk_dict)
    #
    return 




if __name__ == "__main__":
    in_train_txt = sys.argv[1]
    #
    tool_0011_count_spk_num_wav_txt(in_train_txt)