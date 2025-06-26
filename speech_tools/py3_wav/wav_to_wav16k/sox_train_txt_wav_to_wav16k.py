import os
import sys
import random
import shutil
import librosa
from tqdm import tqdm


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
            
        
        out_list.append(cur_dict)

    #
    cur_f.close()
    #
    return out_list



def filter_txt(in_txt,out_txt):
    #
    in_list_dict = read_txt_to_list_dict(in_txt)
    #
    dst_f = open(out_txt,"w")
    #
    for i in tqdm(range(len(in_list_dict))):
        cur_dict_item = in_list_dict[i]
        #
        cur_id =  cur_dict_item["id"]
        cur_wav =  cur_dict_item["wav"]
        cur_phone_npy =  cur_dict_item["phone_npy"]
        cur_spk_embedding =  cur_dict_item["spk_embedding"]
        #
        # print("cur_wav=",cur_wav)
        #

        new_wav_path = os.path.join("/data_2/data/indonesia/wav16k",cur_id + ".wav")
        #
        cur_dict_item["wav"] = new_wav_path

        new_line = combine_dict_to_line(cur_dict_item)
        #
        dst_f.write(new_line + "\n")
        #

        sox_com = "sox " + cur_wav + " -r 16000 -c 1 -b 16 " + new_wav_path
        #
        os.system(sox_com)

    #
    dst_f.close()
    #
    return 



if __name__ == "__main__":
    in_txt = sys.argv[1]
    out_txt = sys.argv[2]
    #
    filter_txt(in_txt,out_txt)