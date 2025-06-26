import os
import sys
import random
import shutil


def run_multi_py(big_wav_dir, small_piece_wav_dir):

    for i in range(0,10,1):
        in_dir_i_num = str(i)
        #
        in_big_dir_i = big_wav_dir + in_dir_i_num
        out_big_dir_i = small_piece_wav_dir + in_dir_i_num
        #
        run_com = "nohup python3 tool_0016_find_cut_pos_in_wav_dir_out_dir_v4.py " + in_big_dir_i + " " + out_big_dir_i + " > log_" + str(i) + ".txt & "
        #
        os.system(run_com)
        #
    return 



if __name__ == "__main__":
    #
    big_wav_dir = "/data7/tongqing/my_learn/wiz/idn_add_symbols/step4/"
    small_piece_wav_dir = "/data7/tongqing/my_learn/wiz/idn_add_symbols/step5/"
    #
    run_multi_py(big_wav_dir,small_piece_wav_dir)
