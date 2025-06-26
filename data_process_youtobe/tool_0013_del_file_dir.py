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




def tool_0013_del_file_dir(in_dir):
    #

    file_list = os.listdir(in_dir)

    
    #
    for i in range(len(file_list)):
        
        #
        cur_file = file_list[i]
        cur_file_path = os.path.join(in_dir,cur_file)
        #
        os.remove(cur_file_path)


    #
    return 




if __name__ == "__main__":
    in_dir = sys.argv[1]
    #
    tool_0013_del_file_dir(in_dir)