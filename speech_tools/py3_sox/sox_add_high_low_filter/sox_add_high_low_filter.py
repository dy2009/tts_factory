import os
import sys
import random
import shutil

global g_suffix_del
g_suffix_del = "wav"



def check_file_is_female(cur_file):
    #
    file_name = os.path.basename(cur_file)
    #
    seg_list = file_name.split("_")
    #
    for i in range(len(seg_list)):
        cur_str = seg_list[i]
        #
        if(cur_str == "female"):
            return True
        if(cur_str == "male"):
            return False
    return True


def sox_add_high_low_filter(in_dir,out_dir):
    global g_suffix_del
    #
    file_list = os.listdir(in_dir)
    file_list.sort()
    #
    for i in range(len(file_list)):
        cur_file = file_list[i]
        #
        if(cur_file.split(".")[-1] != g_suffix_del):
            continue
        #
        cur_file_path = os.path.join(in_dir,cur_file)
        #
        mid_file = os.path.join(in_dir,"mid_" + cur_file)
        #
        dst_file_path = os.path.join(out_dir,cur_file)
        #
        bflag_is_female = True
        #
        bflag_is_female = check_file_is_female(cur_file)

        #
        if(bflag_is_female):
            #
            sox_com1 = "sox " + cur_file_path + " " + mid_file + " highpass 200 "
            #
            os.system(sox_com1)
            #
            sox_com2 = "sox " + mid_file + " " + dst_file_path + " lowpass 8000 "
            #
            os.system(sox_com2)
            #
            os.remove(mid_file)

        else:
            #
            sox_com1 = "sox " + cur_file_path + " " + mid_file + " highpass 120 "
            #
            os.system(sox_com1)
            #
            sox_com2 = "sox " + mid_file + " " + dst_file_path + " lowpass 6000 "
            #
            os.system(sox_com2)
            #
            os.remove(mid_file)
    #
    return 


if __name__ == "__main__":
    in_dir = sys.argv[1]
    out_dir = sys.argv[2]
    #
    sox_add_high_low_filter(in_dir,out_dir)