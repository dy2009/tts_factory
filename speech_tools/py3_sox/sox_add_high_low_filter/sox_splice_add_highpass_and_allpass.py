import os
import sys
import random
import shutil

global g_suffix_del
g_suffix_del = "wav"





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
        dst_file_path = os.path.join(out_dir,cur_file.replace(".wav","_sox2.wav"))
        #

        #
        sox_com1 = "sox " + cur_file_path + " " + mid_file + " highpass 100 "
        #
        os.system(sox_com1)
        #
        sox_com2 = "sox " + mid_file + " " + dst_file_path + " allpass 300 3000 "
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