import os
import sys
import random
import shutil
from tqdm import tqdm

global g_suffix_del
g_suffix_del = "wav"


def wav_to_wav16k(in_dir):
    global g_suffix_del
    #
    dir_list = os.listdir(in_dir)
    dir_list.sort()
    #
    for i in range(len(dir_list)):
        cur_dir = dir_list[i]
        cur_dir_path = os.path.join(in_dir,cur_dir)
        #
        dst_dir = cur_dir + "_big"
        dst_dir_path = os.path.join(in_dir,dst_dir)
        #
        if(not os.path.exists(dst_dir_path)):
            #
            os.mkdir(dst_dir_path)
        #

        file_list = os.listdir(cur_dir_path)
        file_list.sort()
        #

        out_id_dict = {}

        #
        for k in range(10):
            #
            cur_out_id = ""
            #
            out_file = ""
            sox_combine = "sox "
            bflag_wav_num = 0

            for j in range(len(file_list)):
                cur_file = file_list[j]
                #
                if(cur_file.split(".")[-1] != g_suffix_del):
                    continue
                #
                out_id = cur_file[:2] + cur_file[6:]
                #
                #
                if(out_id in out_id_dict):
                    continue


                if(out_file == ""):
                    out_file = out_id
                    cur_out_id = out_id
                elif(cur_out_id != out_id):
                    continue

                #
                # 100001_ajeng5_matcha_v24.wav
                #
                cur_file_path = os.path.join(cur_dir_path,cur_file)
                #
                sox_combine += cur_file_path
                sox_combine += " "
                #
                bflag_wav_num += 1
            #
            out_file = os.path.join(dst_dir_path,out_file)

            sox_combine += out_file
            #
            if(bflag_wav_num <= 0):
                break
            
            print(sox_combine)
            # exit(0)

            os.system(sox_combine)
            #
            
            #
            if(cur_out_id not in out_id_dict):
                out_id_dict[cur_out_id] = True
    #
    return 


if __name__ == "__main__":
    in_dir = sys.argv[1]
    #
    wav_to_wav16k(in_dir)