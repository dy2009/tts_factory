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





def move_wav_dir(in_dir,out_dir):
    #
    dir_list = os.listdir(in_dir)

    for i in range(len(dir_list)):
        cur_wav = dir_list[i]
        cur_wav_path = os.path.join(in_dir,cur_wav)
        #
        if(os.path.isfile(cur_wav_path)):
            cur_suffix = cur_wav.split(".")[-1]
            #
            if(cur_suffix == "wav"):
                shutil.move(cur_wav_path, out_dir)
        else:
            move_wav_dir(cur_wav_path,out_dir)
        #
    #
    return 



if __name__ == "__main__":
    in_dir = sys.argv[1]
    out_dir = sys.argv[2]
    #
    #
    move_wav_dir(in_dir,out_dir)