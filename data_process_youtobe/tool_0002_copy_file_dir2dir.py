# -*- coding: utf-8 -*-
import os
import sys
import shutil

from tqdm import tqdm

# global g_suffix_list
# g_suffix_list = ["wav","npy"]


global g_tail_str
g_tail_str = ".wav"


def move_file_dir(in_dir,out_dir):
    global g_tail_str
    #
    g_tail_str_len = len(g_tail_str)
    #

    in_list = os.listdir(in_dir)
    # in_list.sort()


    error_num = 0

    #
    for i in tqdm(range(len(in_list))):
        cur_file = in_list[i]
        cur_file_path = os.path.join(in_dir,cur_file)
        #
        cur_str_tail_n = cur_file[-g_tail_str_len:]
        #
        
        # dir
        if(os.path.isdir(cur_file_path)):
            # print(cur_file_path)
            # exit(0)
            move_file_dir(cur_file_path,out_dir)
            
        else:
            #
            if(cur_str_tail_n == g_tail_str):
                #
                # error_num += 1

                # cur_file_path = os.path.join(in_dir,cur_file)
                dst_file_path = os.path.join(out_dir,cur_file)
                #
                if(cur_file_path == dst_file_path):
                    continue
                
                #
                else:
                    if(os.path.exists(dst_file_path)):
                        # pass
                        # print(cur_file_path)
                        src_file_size = os.path.getsize(cur_file_path)
                        dst_file_size = os.path.getsize(dst_file_path)
                        #
                        if(src_file_size == dst_file_size):
                            #os.remove(cur_file_path)
                            # os.system("rm -rf " + cur_file_path)
                            pass
                        else:
                            os.remove(dst_file_path)
                            #
                            shutil.copy(cur_file_path,dst_file_path)
                    else:
                        shutil.copy(cur_file_path,dst_file_path)
    #
    # print("error_num=",error_num)

    return


if __name__ == '__main__':
    #
    # in_dir = sys.argv[1]
    # out_dir = sys.argv[2]
    #
    in_dir = "D:\\data\\tts_indonesia\\youtobe_raw_data\\wav24k_piece_0002"
    out_dir = "F:\\tts_indonesia_youtobe_data\\wav24k_piece_0002"
    #
    move_file_dir(in_dir,out_dir)
