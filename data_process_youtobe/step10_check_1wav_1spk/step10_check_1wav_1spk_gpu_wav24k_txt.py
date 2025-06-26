# coding=utf-8
import os
import sys
import torch
import math
import numpy as np
from tqdm import tqdm

import torchaudio

from speechbrain.pretrained import SpeakerRecognition


#g_model_dir = "m_09"
# g_model_dir = "/data_1/kongdw/speechbrean/pretrained_models/spkrec-ecapa-voxceleb"

# g_model_dir = "D:\\research\\spk_speechbrean\\spkrec-ecapa-voxceleb"
#g_model_dir = "/data_2/research/speechbrean/pretrained_models/spkrec-ecapa-voxceleb"
g_model_dir = "/data-07/kongdw/speechbrean/spkrec-ecapa-voxceleb"

verification = SpeakerRecognition.from_hparams(source=g_model_dir)


global g_spk_cos_threshold
g_spk_cos_threshold = 0.60


global g_sil_v_threshold
g_sil_v_threshold = 0.0010

#
def read_txt_to_list(in_txt):
    cur_f = open(in_txt, "r", encoding="utf8")
    #
    list_01 = []
    #
    for curLine in cur_f.readlines():
        line_cp = curLine.strip()
        #
        if(len(line_cp) <= 0):
            continue
        #
        list_01.append(line_cp)
    #
    cur_f.close()
    #
    return list_01



def del_tensor_sil_point(in_tensor):
    global g_sil_v_threshold
    #
    z_tensor = torch.zeros_like(in_tensor)
    #
    wav_len = in_tensor.size(0)
    #
    step_j = 0
    #
    for i in range(wav_len):
        cur_i = torch.abs(in_tensor[i])
        #
        if(cur_i > g_sil_v_threshold):
            z_tensor[step_j] = in_tensor[i]
            #
            step_j += 1
    #
    z_tensor = z_tensor[:step_j]
    #
    return z_tensor




def check_1wav_is_more_1spk(wav_path):
    global g_spk_cos_threshold
    
    #
    # print("wav=",wav_path)
    
    
    head_sil_point_num = int(90 * 16)
    hop_size = int(0.3 * 16000)
    win_size = int(1.0 * 16000)
    
    # print("hop_size=",hop_size)
    # print("win_size=",win_size)
    
    # wav_emb
    wav16k_tensor = verification.read_wav_to_tensor(wav_path)
    #
    wav16k_tensor = torch.squeeze(wav16k_tensor)
    
    wav16k_tensor = del_tensor_sil_point(wav16k_tensor)
    
    wav16k_tensor = wav16k_tensor.unsqueeze(0)
     
    # print("wav16k_tensor=",wav16k_tensor.shape)
    
    # print("wav16k_tensor=",wav16k_tensor)
    
    # exit(0)
    
    wav16k_tensor = wav16k_tensor[:,head_sil_point_num:-head_sil_point_num]
    
    # print("wav16k_tensor2=",wav16k_tensor.shape)
    
    wav_point_num = wav16k_tensor.shape[1]
    if(wav_point_num <= int(16000 * 1.2)):
        return 9999

    
    #
    cur_spk_embedding_01 = verification.get_wav16k_tensor_spk_embedding(wav16k_tensor)
    #
    cur_spk_embedding_01 = torch.squeeze(cur_spk_embedding_01)
    #
    
    # print("spk_emb=",cur_spk_embedding_01.shape)
    
    # print("wav_point_num=",wav_point_num)

    #
    s_list = []
    #
    min_score = 100.0
    # 
    spk_num = 1
    
    #
    for i in range(0,wav_point_num - win_size,hop_size):
        start_i = int(i)
        end_i = int(i + win_size)
        #
        cur_wav_buf = None
        #
        # print("start_i=",start_i,",end_i=",end_i)
        #
        cur_wav_buf = wav16k_tensor[:,start_i : end_i]
        #
        # print("cur_wav_buf=",cur_wav_buf.shape)
        
        #
        if(cur_wav_buf.shape[1] < win_size):
            break
        #
        # print("cur_wav_buf=",cur_wav_buf.shape)
        #
        cur_wav_buf_spk_embedding_01 = verification.get_wav16k_tensor_spk_embedding(cur_wav_buf)
        #
        
        #
        buf_emb_0001 = torch.squeeze(cur_wav_buf_spk_embedding_01)
        #
        cur_score = verification.compute_2emb_similarity(cur_spk_embedding_01,buf_emb_0001).cpu().numpy().item()
        #
        # print("cur_score=",cur_score)
        cur_score = round(cur_score,3)
        #
        s_list.append(str(cur_score))
        #
        if(cur_score <= g_spk_cos_threshold):
            spk_num += 1
        if(cur_score < min_score):
            min_score = cur_score
            
        # break
    #
    # print("wav=",wav_path,",spk_num=",spk_num)

    return spk_num,min_score,s_list




def step10_check_1wav_1spk_cpu(wav_txt,out_wav_txt):
    #

    # wav_list = read_txt_to_list(wav_txt)
    
    src_f = open(wav_txt,"r",encoding="utf8")
    dst_f = open(out_wav_txt,"w",encoding="utf8")


    # print("get_ok_embedding...")
    #
    # torch.cuda.empty_cache()
    #
    #
    for curLine in src_f.readlines():
        #
        #seg_list = wav_list[i].split("|")
        #
        wav_path = curLine.strip()
        #
        wav_name = os.path.basename(wav_path)

        wav_id = wav_name.split(".")[0]

        #
        cur_wav_spk_num,min_s,s_list = check_1wav_is_more_1spk(wav_path)


        s_list_str = "-".join(s_list)
        
        # exit(0)
        
        out_line = "id=" + wav_id + "|spk_num=" + str(cur_wav_spk_num) + "|min_score=" + str(min_s) + "|s_list=" + s_list_str
        #
        dst_f.write(out_line + "\n")

    
    dst_f.close()

    #
    # torch.cuda.empty_cache()
    #
    return


def check_dir(in_wav_dir):
    #
    i_list = os.listdir(in_wav_dir)
    #
    for i in range(len(i_list)):
        cur_w = i_list[i]
        #
        cur_w_path = os.path.join(in_wav_dir,cur_w)
        #
        check_1wav_is_more_1spk(cur_w_path)
        
        # break
        
        
    #
    return 


# if __name__ == '__main__':
#     in_wav_dir = sys.argv[1]
#     #
#     check_dir(in_wav_dir)
    

# if __name__ == '__main__':
#     wav_path = sys.argv[1]
#     #
#     check_1wav_is_more_1spk(wav_path)


if __name__ == '__main__':
    wav_txt = sys.argv[1]
    out_wav_txt = sys.argv[2]
    #
    step10_check_1wav_1spk_cpu(wav_txt,out_wav_txt)
