
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



global g_src_sample_rate
global g_mid_sample_rate

g_src_sample_rate = 24000
g_mid_sample_rate = 32000


def wav24k_enhance_speed_torchaudio(in_wav_tensor,low_speed = 0.8,high_speed = 1.2):

    global g_src_sample_rate
    global g_mid_sample_rate

    # g_low_speed = 0.9
    # g_high_speed = 1.1



    #选择torchaudio重采样方法
    resample = torchaudio.transforms.Resample # torchaudio
    select_rato = np.random.uniform(low_speed, high_speed)

    # out_wav_tensor32 = resample(24000, 32000)(in_wav_tensor)
    # out_wav_tensor32t = resample(32000, int(32000*select_rato))(out_wav_tensor32)

    max_v = torch.max(in_wav_tensor)
    min_v = torch.min(in_wav_tensor)
    print("in_wav, max_v = ",max_v," ,min_v = ",min_v)

    out_wav_tensor_32k_ratio = resample(g_src_sample_rate, int(g_mid_sample_rate*select_rato))(in_wav_tensor)

    out_wav_tensor = resample(g_mid_sample_rate, g_src_sample_rate)(out_wav_tensor_32k_ratio)
    #
    return out_wav_tensor



def enhance_wav24k_path(in_wav_path,out_dir):
    #
    # '/data_01/yanxu/yanxu/test_npy/singlish_chloe3_20001.wav'
    # 
    in_wav_tensor, sr = torchaudio.load(in_wav_path)


    for i in range(10):
        out_file = "enhance_{0:06d}".format(i+1) + ".wav"
        #
        out_file_path = os.path.join(out_dir,out_file)
        #
        out_wav_tensor = wav24k_enhance_speed_torchaudio(in_wav_tensor)

        max_v = torch.max(in_wav_tensor)
        min_v = torch.min(in_wav_tensor)

        # print("out_wav, max_v = ",max_v," ,min_v = ",min_v)

        # exit(0)

        torchaudio.save(out_file_path,out_wav_tensor,sr,format="wav",encoding="PCM_S",bits_per_sample=16)
    #
    return 




if __name__=='__main__':
    in_wav = sys.argv[1]
    out_dir = sys.argv[2]
    #
    enhance_wav24k_path(in_wav,out_dir)
        
