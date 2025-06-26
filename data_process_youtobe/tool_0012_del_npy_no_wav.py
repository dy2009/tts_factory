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
    #
    return 



def tool_0012_del_npy_no_wav(in_wav_dir,in_npy_dir):
    #

    npy_list = os.listdir(in_npy_dir)

    
    #
    for i in range(len(npy_list)):
        
        #
        cur_npy = npy_list[i]
        cur_npy_path = os.path.join(in_npy_dir,cur_npy)
        #
        cur_id = cur_npy.split(".")[0]
        #
        cur_wav_path = os.path.join("wav24k",cur_id + ".wav")
        #
        if(not os.path.exists(cur_wav_path)):
            os.remove(cur_npy_path)


    #
    return 




if __name__ == "__main__":
    in_npy_dir = sys.argv[1]
    in_wav_dir = sys.argv[2]
    #
    tool_0012_del_npy_no_wav(in_wav_dir,in_npy_dir)