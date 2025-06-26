import os
import sys
import random
import shutil
import soundfile as sf

import numpy as np

from multiprocessing import Process

from tqdm import tqdm



def scan_1big_wav_1small_buf(big_wav_dir,cur_w_name, small_piece_wav_buf1000_head500):
    #
    in_wav_path = os.path.join(big_wav_dir,cur_w_name)
    #
    print("big_wav=",in_wav_path)
    #
    in_audio_data, in_sr = sf.read(in_wav_path)
    #
    assert in_sr == 24000
    #
    dst_txt_name = cur_w_name.split(".")[0] + ".txt"

    
    #
    for i in tqdm(range(0,len(in_audio_data) - 1000,1)):
        cur_i = in_audio_data[i]
        cur_i_buf500 = in_audio_data[i:i+500]
        #
        bflag_check_rand100_ok = True
        #
        for j in range(500):
        # for j in range(1):
            #
            if(cur_i_buf500[j] == small_piece_wav_buf1000_head500[j]):
                continue
            else:
                bflag_check_rand100_ok = False
                break
        #
        # bflag_check_rand100_ok = False
        if(bflag_check_rand100_ok):
            #
            dst_f = open(dst_txt_name,"w",encoding="utf8")
            #
            out_str = big_wav_dir + ",big_wav=" + in_wav_path + ",wav_len=" + str(len(in_audio_data)) + ",cut_pos=" + str(i + 1000)
            #
            dst_f.write(out_str + "\n")

            dst_f.close()

            #
            # print("big_wav=",in_wav_path,",wav_len=",len(in_audio_data),"cut_pos=", i + 1000)
            exit(0)
            break
    #
    

    return 



def step4_cut_piece_wav24k_c1_in_wav_dir_out_dir(big_wav_dir, small_piece_wav_dir):
    # head_sil_point_num = int(90 * 16)

    print("big_wav_dir=",big_wav_dir)
    print("small_piece_wav_dir=",small_piece_wav_dir)


    small_piece_wav_list = os.listdir(small_piece_wav_dir)
    small_piece_wav_list.sort()



    last_small_wav = small_piece_wav_list[-1]
    last_small_wav_path = os.path.join(small_piece_wav_dir,last_small_wav)

    print("small_piece_wav=",last_small_wav_path)

    small_piece_audio_data, small_piece_sr = sf.read(last_small_wav_path)
    small_piece_wav_buf1000 = small_piece_audio_data[-1000:]


    small_piece_wav_buf1000_head100 = small_piece_wav_buf1000[:100]
    small_piece_wav_buf1000_head500 = small_piece_wav_buf1000[:500]


    in_wav_list = os.listdir(big_wav_dir)
    in_wav_list.sort()

    in_wav_list.reverse()

    bflag_find = False

    for w_index in range(len(in_wav_list)):
        cur_w_name = in_wav_list[w_index]
        #
        if(cur_w_name[-4:] != ".wav"):
           continue
        #
        scan_1big_wav_1small_buf(big_wav_dir,cur_w_name, small_piece_wav_buf1000_head500)

        # p = Process(target=scan_1big_wav_1small_buf, args=(big_wav_dir,cur_w_name, small_piece_wav_buf1000_head500,))
        # p.start()


    return 





if __name__ == "__main__":

    #
    big_wav_dir = sys.argv[1]
    small_piece_wav_dir = sys.argv[2]
    #
    # big_wav_dir = "/data7/tongqing/my_learn/wiz/idn_add_symbols/step4/0"
    # small_piece_wav_dir = "/data7/tongqing/my_learn/wiz/idn_add_symbols/step5/0"
    #
    step4_cut_piece_wav24k_c1_in_wav_dir_out_dir(big_wav_dir, small_piece_wav_dir)

