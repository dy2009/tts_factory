import os
import sys
import random
import shutil
from multiprocessing import Process

import time
import numpy as np

import soundfile as sf

from tqdm import tqdm

global g_suffix_del
g_suffix_del = "wav"


# {'qio': 935, 'haitian': 9462, 'ajeng': 1777, 'Indry': 989, 'Iyok': 1265, 'Natasha': 549, 'Nirmala': 475, 'Novinda': 1840, 'Robert': 952, 'hani': 894, 'panji': 351}

global g_spk_list
g_spk_list = ['qio', 'haitian', 'ajeng', 'Indry', 'Iyok', 'Natasha', 'Nirmala', 'Novinda', 'Robert', 'hani', 'panji']


global sil_90ms_point_num
sil_90ms_point_num = int((24000 / 1000) * 90)


global sil_80ms_point_num
sil_80ms_point_num = int((24000 / 1000) * 80)

global g_sil_80ms_buf
g_sil_80ms_buf = (np.random.randn(sil_80ms_point_num) - 0.5) * 0.0005


global g_out_wav24k_dir
g_out_wav24k_dir = "/data_1/data/indonesian/record_mixed_data/wav24k"

global g_out_phone_npy_dir
g_out_phone_npy_dir = "/data_1/data/indonesian/record_mixed_data/phone_npy"


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



def get_spk_id2_from_id(in_id):
    #
    out_str = ""
    #
    skip_num = 0
    #
    for i in range(len(in_id)):
        cur_char = in_id[i]
        #
        cur_char_lower = in_id[i].lower()
        #
        if(cur_char_lower >= "a" and cur_char_lower <= "z"):
            out_str += cur_char
        else:
            if(skip_num == 0):
                out_str += cur_char
            #
            skip_num += 1
            #
        #
        if(skip_num >= 2):
            return out_str
    #
    #
    return out_str


def get_spk_id1_from_id(in_id):
    #
    out_str = ""
    #
    skip_num = 0
    #
    for i in range(len(in_id)):
        cur_char = in_id[i]
        #
        cur_char_lower = in_id[i].lower()
        #
        if(cur_char_lower >= "a" and cur_char_lower <= "z"):
            out_str += cur_char_lower
        else:
            return out_str
    #
    #
    return out_str





def read_txt_to_list_dict(in_txt):
    #
    out_list = []
    #
    cur_f = open(in_txt,"r",encoding="utf-8")
    #
    for curLine in cur_f.readlines():
        line_cp = curLine.strip()
        #
        if(len(line_cp) <= 0):
            continue
        #
        cur_dict = {}
        #
        seg_list = line_cp.split("|")
        #
        for i in range(len(seg_list)):
            seg_list_i = seg_list[i]
            #
            key1 = seg_list_i.split("=")[0]
            value1 = seg_list_i.split("=")[1]

            # get_spk_id1_from_id(cur_id)
            if(key1 == "id"):
                cur_spk_id = get_spk_id1_from_id(value1)
                #
                cur_dict["spk_id"] = cur_spk_id

            #
            if(key1 == "txt" or key1 == "text"):
                cur_dict["text"] = value1
            elif(key1 == "wav" or key1 == "audio_file"):
                cur_dict["wav"] = value1
            else:
                cur_dict[key1] = value1
        #
        
        out_list.append(cur_dict)
    #
    cur_f.close()
    #
    return out_list


def tool_0009_combine_big_wav24k(in_train_txt,out_train_txt):
    global g_suffix_del
    global g_spk_list
    global g_out_wav24k_dir
    global g_out_phone_npy_dir

    global g_sil_80ms_buf

    # head_sil_point_num = int(90 * 16)
    #head_sil_point_num_half = int(20 * 16)
    # head_sil_point_num_half = 0

    #
    file_list_dict = read_txt_to_list_dict(in_train_txt)
    #
    spk_id_list = []
    spk_id_dict = {}
    #
    out_mix_num = 0

    dst_f = open(out_train_txt,"w",encoding="utf8")

    for i in range(len(g_spk_list)):
        cur_spk_name = g_spk_list[i].lower()
        #
        
        #
        #if(cur_spk_name in ["haitian",'ajeng','hani','panji','qio']):
        #    continue
        #
        print(cur_spk_name)

        out_index = 1
        #
        cur_spk_list_dict = []

        # find the same spk
        for j in range(len(file_list_dict)):
            #
            cur_dict = file_list_dict[j]
            #
            cur_spk_id = cur_dict["spk_id"]
            cur_id = cur_dict["id"]
            cur_file_path = cur_dict["wav"]
            #
            if(cur_spk_id == cur_spk_name):
                cur_spk_list_dict.append(cur_dict)
        #

        cur_spk_num = len(cur_spk_list_dict)

        for j in range(len(cur_spk_list_dict)):
            #
            cur_dict = cur_spk_list_dict[j]
            #
            cur_spk_id = cur_dict["spk_id"]
            #
            cur_id = cur_dict["id"]
            cur_txt = cur_dict["text"]
            cur_phone_txt = cur_dict["ph"]
            cur_phone_npy_file = cur_dict["phone_npy"]
            cur_file_path = cur_dict["wav"]
            #

            #
            cur_wav_buf,cur_sr = sf.read(cur_file_path)
            #
            cur_phone_npy = np.load(cur_phone_npy_file)

            #
            # print("in_id=",cur_id)
            # print("in_txt=",cur_txt)
            # # print("in_wav=",cur_file_path)
            # print("in_ph=",cur_phone_txt)
            # print("in_phone_npy=",cur_phone_npy)
            # print("\n")
            #
            for k in range(1,6,1):
                target_list = []
                #
                out_id = cur_spk_id + "_mix_" + "{0:06d}".format(out_index)
                out_index += 1
                #
                out_wav = out_id + ".wav"
                out_wav_path = os.path.join(g_out_wav24k_dir,out_wav)
                #
                out_npy_path = os.path.join(g_out_phone_npy_dir,out_id + ".npy")
                #
                out_txt = cur_txt
                out_txt += " "

                # / txt_end
                assert cur_phone_txt[-9:] == "/ txt_end"
                out_phone_txt = cur_phone_txt[:-9]
                #
                out_wav_buf = cur_wav_buf #[:-head_sil_point_num_half]
                #
                out_phone_npy = cur_phone_npy
                #
                for h in range(k):
                    
                    # cut tail 2 phone, = / txt_end
                    out_phone_npy = out_phone_npy[:-2]

                    cur_rand_i = np.random.randint(0,cur_spk_num)
                    #
                    h_dict = cur_spk_list_dict[cur_rand_i]
                    #
                    h_cur_id = h_dict["id"]
                    h_cur_txt = h_dict["text"]
                    h_cur_phone_txt = h_dict["ph"]
                    h_cur_phone_npy_file = h_dict["phone_npy"]
                    h_cur_file_path = h_dict["wav"]
                    #
                    h_cur_wav_buf,h_cur_sr = sf.read(h_cur_file_path)
                    #
                    # h_cur_wav_buf = h_cur_wav_buf[head_sil_point_num_half:]
                    #
                    out_wav_buf = np.concatenate((out_wav_buf,g_sil_80ms_buf,h_cur_wav_buf),axis=0)
                    #
                    out_txt += h_cur_txt
                    out_txt += " "
                    #
                    out_phone_txt += " / "
                    out_phone_txt += h_cur_phone_txt[11:]
                    assert h_cur_phone_txt[:11] == "txt_start /"

                    # phone_id
                    # txt_start = 1, 
                    # / = 9, 
                    # txt_end = 2 
                    # . = 8
                    h_cur_phone_npy = np.load(h_cur_phone_npy_file)

                    # cut head 1 phone, = txt_start
                    h_cur_phone_npy = h_cur_phone_npy[1:]
                    #
                    # print("h_cur_txt=",h_cur_txt)
                    # print("h_cur_phone_txt=",h_cur_phone_txt)
                    # print("h_cur_phone_npy=",h_cur_phone_npy)
                    # print("\n")

                    out_phone_npy = np.concatenate((out_phone_npy,h_cur_phone_npy),axis=0)
                    #

                #
                assert out_phone_txt[-9:] == "/ txt_end"
                #
                sf.write(out_wav_path,out_wav_buf,cur_sr)
                #
                np.save(out_npy_path,out_phone_npy)
                #
                out_txt = out_txt.strip()
                #
                # print("out_id=",out_id)
                # print("out_txt=",out_txt)
                # print("out_wav=",out_wav_path)
                # print("out_ph=",out_phone_txt)
                # print("out_phone_npy=",out_phone_npy)
                #
                out_line = "id=" + out_id + "|text=" + out_txt + "|wav=" + out_wav_path + "|ph=" + out_phone_txt + "|phone_npy=" + out_npy_path
                #
                dst_f.write(out_line + "\n")

                #
                # exit(0)

                #
                out_mix_num += 1
                #
                # if(out_mix_num >= 5):
                #     exit(0)
                #
                if(out_mix_num % 5000 == 0):
                    print(out_mix_num)

    #
    dst_f.close()
    #
    return 



if __name__ == "__main__":
    in_train_txt = sys.argv[1]
    out_train_txt = sys.argv[2]
    #
    tool_0009_combine_big_wav24k(in_train_txt,out_train_txt)
