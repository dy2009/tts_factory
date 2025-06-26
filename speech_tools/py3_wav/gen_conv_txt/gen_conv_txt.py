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
        txt_list.append(line_cp)
    #
    cur_f.close()
    #
    return txt_list




def mix2_txt(in1_txt,in2_txt,out_txt):
    global g_spk_str
    #
    txt1_list = read_txt_to_list(in1_txt)
    txt2_list = read_txt_to_list(in2_txt)
    #
    dst_f = open(out_txt,"w",encoding="utf8")
    #
    txt_list = []
    #
    for i in range(len(txt1_list)):
        txt_i = txt1_list[i]
        #
        for j in range(len(txt2_list)):
            txt_j = txt2_list[j]
            #
            out_line = txt_i + "," + txt_j
            #
            dst_f.write(out_line + "\n")

    #
    dst_f.close()
    #
    return 



if __name__ == "__main__":
    in1_txt = sys.argv[1]
    in2_txt = sys.argv[2]

    out_txt = sys.argv[3]
    #
    mix2_txt(in1_txt,in2_txt,out_txt)