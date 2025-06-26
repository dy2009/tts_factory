import os
import sys
import random
import shutil


global g_split_num
g_split_num = 20


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





def split_txt(in_txt,out_dir,split_num):
    global g_split_num
    #
    g_split_num = split_num
    #
    txt_list = read_txt_to_list(in_txt)
    #
    all_num = len(txt_list)
    #
    per_seg_num = int(all_num / split_num)
    #
    per_seg_num += 1
    #

    cur_seg_id = 1
    #
    out_name = "split_" + str(cur_seg_id) + ".txt"
    #
    out_txt_path = os.path.join(out_dir,out_name)

    dst_f = open(out_txt_path,"w",encoding="utf8")
    #
    #
    for i in range(all_num):
        #
        if(i >= (per_seg_num * cur_seg_id)):
            dst_f.close()
            #
            cur_seg_id += 1
            #
            out_name = "split_" + str(cur_seg_id) + ".txt"
            #
            out_txt_path = os.path.join(out_dir,out_name)
            #
            dst_f = open(out_txt_path,"w",encoding="utf8")
            #
            dst_f.write(txt_list[i] + "\n")
        else:
            dst_f.write(txt_list[i] + "\n")
    #
    dst_f.close()
    #

    #
    return 



if __name__ == "__main__":
    in_txt = sys.argv[1]
    out_dir = sys.argv[2]
    split_num = int(sys.argv[3])
    #
    split_txt(in_txt,out_dir,split_num)