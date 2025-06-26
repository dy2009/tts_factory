
import os
import sys
import torchaudio
import torch
import numpy as np
import soundfile as sf
import librosa
import scipy
import scipy.signal
import resampy


global g_low_speed
global g_high_speed
g_low_speed = 0.9
g_high_speed = 1.1


def wav24k_enhance_resampy(in_wav_tensor):
    global g_low_speed
    global g_high_speed

    #选择resampy重采样方法
    select_rato = np.random.uniform(g_low_speed,g_high_speed)
    # print(select_rato)

    # out_wav_tensor32 = torch.tensor(resampy.resample(in_wav_tensor[0].cpu().numpy(), 24000,32000))
    out_wav_tensor32 = torch.tensor(resampy.resample(in_wav_tensor[0].cpu().numpy(), 24000, int(32000*select_rato)))

    # print(out_wav_tensor32.shape)

    # out_wav_tensor32t = torch.tensor(resampy.resample(out_wav_tensor32.cpu().numpy(),32000,int(32000*select_rato)))

    # print(out_wav_tensor32t.shape[0])
    out_wav_tensor = torch.tensor(resampy.resample(out_wav_tensor32.cpu().numpy(), 32000,24000))

    return out_wav_tensor.unsqueeze(0)


def wav24k_enhance_scipy(in_wav_tensor):
    global g_low_speed
    global g_high_speed

    # 选择scipy重采样方法
    select_rato = np.random.uniform(g_low_speed, g_high_speed)
    # print(select_rato)

    out_wav_tensor32 = torch.tensor(scipy.signal.resample(in_wav_tensor[0].cpu().numpy(), int(32/24* in_wav_tensor.shape[1])))
    # print(out_wav_tensor32.shape)

    out_wav_tensor32t = torch.tensor(scipy.signal.resample(out_wav_tensor32.cpu().numpy(), int(select_rato * out_wav_tensor32.shape[0])))
    # print(out_wav_tensor32t.shape[0])

    out_wav_tensor = torch.tensor(scipy.signal.resample(out_wav_tensor32t.cpu().numpy(), int(24/32* out_wav_tensor32t.shape[0])))
    # print(out_wav_tensor.shape[0])
    #
    return out_wav_tensor.unsqueeze(0)


def wav24k_enhance_librosa(in_wav_tensor):
    global g_low_speed
    global g_high_speed

    #选择librosa重采样方法
    select_rato = np.random.uniform(g_low_speed,g_high_speed)

    # print(select_rato)
    out_wav_tensor32=torch.tensor(librosa.resample(in_wav_tensor.cpu().numpy(),24000,32000))

    out_wav_tensor32t=torch.tensor(librosa.resample(out_wav_tensor32.cpu().numpy(),32000,int(32000*select_rato)))

    out_wav_tensor=torch.tensor(librosa.resample(out_wav_tensor32t.cpu().numpy(),32000,24000))
    #
    return out_wav_tensor


def wav24k_enhance_torchaudio(in_wav_tensor):
    global g_low_speed
    global g_high_speed

    #选择torchaudio重采样方法
    resample = torchaudio.transforms.Resample # torchaudio
    select_rato = np.random.uniform(g_low_speed, g_high_speed)

    # out_wav_tensor32 = resample(24000, 32000)(in_wav_tensor)
    # out_wav_tensor32t = resample(32000, int(32000*select_rato))(out_wav_tensor32)

    out_wav_tensor_32k_ratio = resample(24000, int(32000*select_rato))(in_wav_tensor)

    out_wav_tensor=resample(32000, 24000)(out_wav_tensor_32k_ratio)
    #
    return out_wav_tensor



def enhance_wav24k_path(in_wav_path,out_wav_path):
    #
    # '/data_01/yanxu/yanxu/test_npy/singlish_chloe3_20001.wav'
    # 
    in_wav_tensor,sr=torchaudio.load(in_wav_path)

    out_wav_tensor_re=wav24k_enhance_resampy(in_wav_tensor)
    out_wav_tensor=wav24k_enhance(in_wav_tensor)
    out_wav_tensor_sc=wav24k_enhance_scipy(in_wav_tensor)
    out_wav_tensor_li=wav24k_enhance_librosa(in_wav_tensor)

    torchaudio.save('wav24k_resample/chloe_resampy.wav',out_wav_tensor_re,sr)
    torchaudio.save('wav24k_resample/chloe_torchaudio.wav',out_wav_tensor,sr)
    torchaudio.save('wav24k_resample/chloe_scipy.wav',out_wav_tensor_sc,sr)
    torchaudio.save('wav24k_resample/chloe_librosa.wav',out_wav_tensor_li,sr)
    
    #
    return 




if __name__=='__main__':
    in_wav = sys.argv[1]
    out_wav = sys.argv[2]
    #
    enhance_wav24k_path(in_wav,out_wav)
        
