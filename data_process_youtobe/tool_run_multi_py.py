import os
import sys
import random
import shutil



def read_txt_to_list(in_txt):
    #
    cur_f = open(in_txt,"r",encoding="utf8")
    #
    txt_list = []
    #
    for curLine in cur_f.readlines():
        line_cp = curLine.strip()
        #
        if(len(line_cp) <= 0):
            continue
        #
        txt_list.append(line_cp)
    #
    cur_f.close()
    #
    return txt_list




def run_multi_py():

    for i in range(10,20,1):
        in_wav_txt = "/data-07/data/youbube_202406/spk_dir3/split_" + str(i + 1) + ".txt"
        out_wav_txt = "/data-07/data/youbube_202406/spk_dir3/split_" + str(i + 1) + "_spknum.txt"
        #
        run_com = "python3 step10_check_1wav_1spk_gpu_wav24k_txt.py " + in_wav_txt + " " + out_wav_txt + " > log_" + str(i + 1) + ".txt & "
        #
        os.system(run_com)
        #
    return 



if __name__ == "__main__":
    #
    #
    run_multi_py()
