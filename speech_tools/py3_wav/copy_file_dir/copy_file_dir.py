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





def filter_txt(in_txt):
    #
    cur_f = open(in_txt,"r",encoding="utf8")
    dst_f = open("tmp1.txt","w",encoding="utf8")
    #
    i_index = 0
    #
    for curLine in cur_f.readlines():
        line_cp = curLine.strip()
        #
        if(len(line_cp) <= 0):
            continue
        #
        i_index += 1
        #
        if(i_index % 10000 == 0):
            # shutil.copy(line_cp,"tmp1")
            #
            dst_f.write(line_cp + "\n")

    #
    cur_f.close()
    dst_f.close()
    #
    #
    return 



if __name__ == "__main__":
    in_txt = sys.argv[1]
    # out_txt = sys.argv[2]
    #
    # in_txt = "step2_audio.txt"
    # out_txt = "step3_audio.txt"
    #
    filter_txt(in_txt)