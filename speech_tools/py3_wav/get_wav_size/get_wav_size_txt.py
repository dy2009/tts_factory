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





def filter_txt(in_txt,out_txt):
    #
    cur_f = open(in_txt,"r",encoding="utf8")
    dst_f = open(out_txt,"w",encoding="utf8")
    #
    #
    for curLine in cur_f.readlines():
        line_cp = curLine.strip()
        #
        if(len(line_cp) <= 0):
            continue
        #
        wav_id = os.path.basename(line_cp).split(".")[0]
        file_size = os.path.getsize(line_cp)
        #
        out_line = wav_id + "=" + str(file_size)
        #
        dst_f.write(out_line + "\n")
        #
    #
    cur_f.close()
    dst_f.close()
    #
    return 



if __name__ == "__main__":
    in_txt = sys.argv[1]
    out_txt = sys.argv[2]
    #
    filter_txt(in_txt,out_txt)