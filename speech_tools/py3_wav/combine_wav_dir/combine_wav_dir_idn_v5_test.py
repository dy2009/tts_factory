import os
import sys
import random
import shutil
from tqdm import tqdm

global g_suffix_del
g_suffix_del = "wav"

def wav_to_wav16k(in_dir, out_dir):
    global g_suffix_del
    #
    dir_list = os.listdir(in_dir)
    for i in range(len(dir_list)):
        cur_dir_i = dir_list[i]
        cur_dir_i_path = os.path.join(in_dir,cur_dir_i)
        #
        dst_dir_i_path = os.path.join(out_dir,cur_dir_i)
        #
        if(not os.path.exists(dst_dir_i_path)):
            os.mkdir(dst_dir_i_path)
    

        file_list = os.listdir(cur_dir_i_path)
        file_list.sort()
        #
        # print("file_list=",file_list)

        print("\n\n")

        for j in range(7):
            cur_j_str = "{0:02d}".format(j+1)
            #
            print("cur_j_str=",cur_j_str)

            out_file = ""
            sox_combine = "sox "

            for k in range(len(file_list)):
                cur_file = file_list[k]
                cur_file_path = os.path.join(cur_dir_i_path,cur_file)
                #
                if(cur_file[:2] != cur_j_str):
                    continue

                #
                if(cur_file.split(".")[-1] != g_suffix_del):
                    continue
                #

                # 010001_ajeng5_matcha_v24
                #
                if(out_file == ""):
                    seg_list = cur_file.split("_")
                    #
                    out_file = cur_j_str +  "_" + "_".join(seg_list[1:])
                    #
                    out_file = os.path.join(dst_dir_i_path,out_file)

                #
                # cur_file_path = os.path.join(in_dir,cur_file)
                #
                sox_combine += cur_file_path
                sox_combine += " "
            #
            sox_combine += out_file
            #
            print(sox_combine)
            # exit(0)

            os.system(sox_combine)
    #
    return 


if __name__ == "__main__":
    in_dir = sys.argv[1]
    out_dir = sys.argv[2]
    #
    wav_to_wav16k(in_dir, out_dir)