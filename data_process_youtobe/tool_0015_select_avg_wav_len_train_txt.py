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




def tool_0015_select_avg_wav_len_train_txt(in_train_txt,out_train_txt):
    #

    file_list = read_txt_to_list_dict(in_train_txt)


    wav_len_less_2s_num = 0
    wav_len_2s_4s_num = 0
    wav_len_4s_6s_num = 0
    wav_len_6s_8s_num = 0
    wav_len_8s_10s_num = 0
    wav_len_10s_13s_num = 0
    wav_len_13s_16s_num = 0
    wav_len_16s_20s_num = 0
    wav_len_more_20s_num = 0


    wav_len_less_2s_list = []
    wav_len_2s_4s_list = []
    wav_len_4s_6s_list = []
    wav_len_6s_8s_list = []
    wav_len_8s_10s_list = []
    wav_len_10s_13s_list = []
    wav_len_13s_16s_list = []
    wav_len_16s_20s_list = []
    wav_len_more_20s_list = []

    #
    for i in range(len(file_list)):
        
        #
        cur_dict = file_list[i]
        cur_wav_path = cur_dict["wav"]
        #
        cur_wav_buf,cur_sr = sf.read(cur_wav_path)
        #
        cur_wav_len_s = int(len(cur_wav_buf) / cur_sr)
        #
        if(cur_wav_len_s < 2.0):
            wav_len_less_2s_num += 1
            wav_len_less_2s_list.append(cur_dict)

        elif(cur_wav_len_s >= 2.0 and cur_wav_len_s < 4.0):
            wav_len_2s_4s_num += 1
            wav_len_2s_4s_list.append(cur_dict)

        elif(cur_wav_len_s >= 4.0 and cur_wav_len_s < 6.0):
            wav_len_4s_6s_num += 1
            wav_len_4s_6s_list.append(cur_dict)

        elif(cur_wav_len_s >= 6.0 and cur_wav_len_s < 8.0):
            wav_len_6s_8s_num += 1
            wav_len_6s_8s_list.append(cur_dict)

        elif(cur_wav_len_s >= 8.0 and cur_wav_len_s < 10.0):
            wav_len_8s_10s_num += 1
            wav_len_8s_10s_list.append(cur_dict)

        elif(cur_wav_len_s >= 10.0 and cur_wav_len_s < 13.0):
            wav_len_10s_13s_num += 1
            wav_len_10s_13s_list.append(cur_dict)

        elif(cur_wav_len_s >= 13.0 and cur_wav_len_s < 16.0):
            wav_len_13s_16s_num += 1
            wav_len_13s_16s_list.append(cur_dict)

        elif(cur_wav_len_s >= 16.0 and cur_wav_len_s < 20.0):
            wav_len_16s_20s_num += 1
            wav_len_16s_20s_list.append(cur_dict)

        else:
            wav_len_more_20s_num += 1
            wav_len_more_20s_list.append(cur_dict)
        #

    #
    num_1 = len(wav_len_less_2s_list)
    num_2 = len(wav_len_2s_4s_list)
    num_3 = len(wav_len_4s_6s_list)
    num_4 = len(wav_len_6s_8s_list)
    num_5 = len(wav_len_8s_10s_list)
    num_6 = len(wav_len_10s_13s_list)
    num_7 = len(wav_len_13s_16s_list)
    num_8 = len(wav_len_16s_20s_list)
    num_9 = len(wav_len_more_20s_list)

    #
    max_num = max(max(max(max(max(num_1,num_2),max(num_3,num_4)),max(num_5,num_6)),max(num_7,num_8)),num_9)
    #

    wav_big_list = []
    wav_i_list = []

    wav_big_list.append(wav_len_less_2s_list)
    wav_big_list.append(wav_len_2s_4s_list)
    wav_big_list.append(wav_len_4s_6s_list)
    wav_big_list.append(wav_len_6s_8s_list)
    wav_big_list.append(wav_len_8s_10s_list)
    wav_big_list.append(wav_len_10s_13s_list)
    wav_big_list.append(wav_len_13s_16s_list)
    wav_big_list.append(wav_len_16s_20s_list)
    wav_big_list.append(wav_len_more_20s_list)

    for i in range(len(wav_big_list)):
        wav_i_list.append(0)


    dst_f = open(out_train_txt,"w",encoding="utf8")

    for i in range(max_num):
        #
        for j in range(len(wav_big_list)):
            cur_wav_j_list = wav_big_list[j]
            cur_wav_j_list_i = wav_i_list[j]
            #
            #
            cur_dict_i_j = cur_wav_j_list[cur_wav_j_list_i]
            #
            cur_wav_j_list_i += 1
            #
            if(cur_wav_j_list_i >= len(cur_wav_j_list)):
                cur_wav_j_list_i = 0
            #
            wav_i_list[j] = cur_wav_j_list_i
            #
            cur_out_line = combine_dict_to_line(cur_dict_i_j)

            dst_f.write(cur_out_line + "\n")
    #
    dst_f.close()
    #
    #
    return 




if __name__ == "__main__":
    in_train_txt = sys.argv[1]
    out_train_txt = sys.argv[2]
    #
    tool_0015_select_avg_wav_len_train_txt(in_train_txt,out_train_txt)