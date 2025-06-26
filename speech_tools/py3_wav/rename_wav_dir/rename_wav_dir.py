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





def filter_txt(in_dir):
    #
    wav_list = os.listdir(in_dir)
    #
    for j in range(len(wav_list)):
        cur_wav = wav_list[j]
        #
        cur_id = cur_wav.split(".")[0]
        #
        if(cur_wav.split(".")[1] != "wav"):
            continue
        #
        cur_wav_path = os.path.join(in_dir,cur_wav)
        #
        new_name = "youbube3_" + cur_wav
        #
        out_wav_path = os.path.join(in_dir,new_name)
        #
        shutil.move(cur_wav_path,out_wav_path)
    #
    return 



if __name__ == "__main__":
    in_dir = sys.argv[1]
    # out_dir = sys.argv[2]
    #
    # in_txt = "step2_audio.txt"
    # out_txt = "step3_audio.txt"
    #
    filter_txt(in_dir)