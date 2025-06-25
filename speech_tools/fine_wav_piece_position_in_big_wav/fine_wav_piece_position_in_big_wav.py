import os
import sys
import random
import shutil
from tqdm import tqdm
import numpy as np

global g_suffix_del
g_suffix_del = "wav"


import torch

# 假设tensor1和tensor2是你的两个[80, 87]张量
# tensor1 = torch.randn(80, 87)
# tensor2 = torch.randn(80, 87)
def computer_2tensor_score(tensor1,tensor2):
    # 计算整体相似度（将所有元素视为一个长向量）
    cos_sim = torch.cosine_similarity(tensor1.flatten(), tensor2.flatten(), dim=0)

    # print(f"整体余弦相似度: {cos_sim.item()}")

    # 计算每行的相似度（80个相似度值）
    # row_wise_cos_sim = torch.cosine_similarity(tensor1, tensor2, dim=1)
    # print(f"每行余弦相似度的平均值: {row_wise_cos_sim.mean().item()}")
    #
    return cos_sim



def scan_1piece_1big(cur_i_mel_tensor,big_mel_j_tensor):
    #
    piece_mel_len = cur_i_mel_tensor.size(1)
    big_mel_len = big_mel_j_tensor.size(1)
    #
    if(piece_mel_len >= big_mel_len):
        return -1.0 , 0
    #
    best_s = 0.0
    best_i = 0
    #
    for i in range(0,big_mel_len-piece_mel_len,1):
        #
        big_mel_tensor_i = big_mel_j_tensor[:,i:i+piece_mel_len]
        #
        if(big_mel_tensor_i.size(1) < piece_mel_len):
            continue
        #
        cur_s = computer_2tensor_score(cur_i_mel_tensor,big_mel_tensor_i)
        #
        if(cur_s > best_s):
            best_s = cur_s
            best_i = i
    #
    #
    return best_s,best_i



def find_mel_pos(in_piece_dir,big_wav_mel_dir):
    #
    mel_list = os.listdir(in_piece_dir)
    mel_list.sort()
    #
    in_big_wav_list = os.listdir(big_wav_mel_dir)

    #
    big_wav_path_list = []
    for i in range(len(in_big_wav_list)):
        cur_i_path = os.path.join(big_wav_mel_dir,in_big_wav_list[i])
        big_wav_path_list.append(cur_i_path)
    #

    #
    for i in range(len(mel_list)):
        cur_i_mel = mel_list[i]
        cur_i_mel_path = os.path.join(in_piece_dir,cur_i_mel)
        #
        print(cur_i_mel_path)
        #
        cur_i_mel_npy = np.load(cur_i_mel_path)
        cur_i_mel_tensor = torch.from_numpy(cur_i_mel_npy)

        # in_mel= torch.Size([80, 176])
        piece_mel_len = cur_i_mel_tensor.size(1)
        
        #
        best_score = 0.0
        best_big_index = 0
        best_big_name = ""
        #
        for j in range(len(big_wav_path_list)):
            big_mel_j_path = big_wav_path_list[j]
            #
            big_mel_j_npy = np.load(big_mel_j_path)
            big_mel_j_tensor = torch.from_numpy(big_mel_j_npy)



            cur_s,mel_index = scan_1piece_1big(cur_i_mel_tensor,big_mel_j_tensor)
            #
            if(cur_s > best_score):
                best_score = cur_s
                best_big_index = mel_index
                best_big_name = big_mel_j_path
        #
        start_s_f = best_big_index * 0.01
        end_s_f = start_s_f + piece_mel_len * 0.01
        #
        print("piece=",cur_i_mel_path,",big=",best_big_name,",start_second=",best_big_index * 0.01,"end_s=",end_s_f,",score=",best_score)
        # exit(0)

    #
    return 



if __name__ == "__main__":
    # in_dir = sys.argv[1]
    # out_dir = sys.argv[2]
    #

    wav_piece_dir = sys.argv[1]
    big_wav_mel_dir = sys.argv[2]
    #
    find_mel_pos(wav_piece_dir,big_wav_mel_dir)