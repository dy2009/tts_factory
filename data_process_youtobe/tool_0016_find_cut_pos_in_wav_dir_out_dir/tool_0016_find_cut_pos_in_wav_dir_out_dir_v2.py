import os
import sys
import random
import shutil
import soundfile as sf

from tqdm import tqdm


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

    piece_point_1 = small_piece_wav_buf1000_head100[0]
    piece_point_2 = small_piece_wav_buf1000_head100[1]
    piece_point_3 = small_piece_wav_buf1000_head100[2]
    piece_point_4 = small_piece_wav_buf1000_head100[4]
    piece_point_5 = small_piece_wav_buf1000_head100[5]
    piece_point_6 = small_piece_wav_buf1000_head100[6]
    piece_point_7 = small_piece_wav_buf1000_head100[7]
    piece_point_8 = small_piece_wav_buf1000_head100[8]
    piece_point_9 = small_piece_wav_buf1000_head100[9]
    piece_point_10 = small_piece_wav_buf1000_head100[10]

    in_wav_list = os.listdir(big_wav_dir)
    in_wav_list.sort()

    bflag_find = False

    for w_index in range(len(in_wav_list)):
        cur_w_name = in_wav_list[w_index]
        #
        if(cur_w_name[-4:] != ".wav"):
            continue

        in_wav_path = os.path.join(big_wav_dir,cur_w_name)
        #
        print("big_wav=",in_wav_path)
        #
        in_audio_data, in_sr = sf.read(in_wav_path)
        #
        assert in_sr == 24000
        #
        for i in range(0,len(in_audio_data) - 1000,1):
            cur_i = in_audio_data[i]
            cur_i_j2 = in_audio_data[i + 1]
            cur_i_j3 = in_audio_data[i + 2]
            cur_i_j4 = in_audio_data[i + 3]
            cur_i_j5 = in_audio_data[i + 4]
            cur_i_j6 = in_audio_data[i + 5]
            cur_i_j7 = in_audio_data[i + 6]
            cur_i_j8 = in_audio_data[i + 7]
            cur_i_j9 = in_audio_data[i + 8]
            cur_i_j10 = in_audio_data[i + 9]
            #
            if(cur_i == piece_point_1):
                if(cur_i_j2 == piece_point_2):
                    if(cur_i_j3 == piece_point_3):
                        if(cur_i_j4 == piece_point_4 and cur_i_j5 == piece_point_5 and cur_i_j6 == piece_point_6):
                            if(cur_i_j7 == piece_point_7 and cur_i_j8 == piece_point_8 and cur_i_j9 == piece_point_9 and cur_i_j10 == piece_point_10):
                                # cur_i_buf100 = in_audio_data[i:i+100]
                                cur_i_buf500 = in_audio_data[i:i+500]
                                #
                                if(cur_i_buf500 == small_piece_wav_buf1000_head500).all():
                                    print("big_wav=",in_wav_path,",wav_len=",len(in_audio_data),"cut_pos=", i + 1000)
                                    exit(0)
                                    break

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

