import os
import sys
import torch
import torch.utils.data
import numpy as np
# from librosa.util import normalize
from scipy.io.wavfile import read
from librosa.filters import mel as librosa_mel_fn

import soundfile as sf
import random
from tqdm import tqdm


MAX_WAV_VALUE = 32768.0

global g_suffix_del
g_suffix_del = "wav"



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


def load_wav(full_path):
    sampling_rate, data = read(full_path)
    return data, sampling_rate


def dynamic_range_compression(x, C=1, clip_val=1e-5):
    return np.log(np.clip(x, a_min=clip_val, a_max=None) * C)


def dynamic_range_decompression(x, C=1):
    return np.exp(x) / C


def dynamic_range_compression_torch(x, C=1, clip_val=1e-5):
    return torch.log(torch.clamp(x, min=clip_val) * C)


def dynamic_range_decompression_torch(x, C=1):
    return torch.exp(x) / C


def spectral_normalize_torch(magnitudes):
    output = dynamic_range_compression_torch(magnitudes)
    return output


def spectral_de_normalize_torch(magnitudes):
    output = dynamic_range_decompression_torch(magnitudes)
    return output


mel_basis = {}
hann_window = {}


def mel_spectrogram(y, n_fft, num_mels, sampling_rate, hop_size, win_size, fmin, fmax, center=False):
    if torch.min(y) < -1.:
        print('min2==', torch.min(y))
    if torch.max(y) > 1.:
        print('max2==', torch.max(y))

    global mel_basis, hann_window
    if fmax not in mel_basis:
        cur_mel = librosa_mel_fn(sr=sampling_rate, n_fft=n_fft, n_mels=num_mels, fmin=fmin, fmax=fmax)
        mel_basis[str(fmax)+'_'+str(y.device)] = torch.from_numpy(cur_mel).float().to(y.device)
        hann_window[str(y.device)] = torch.hann_window(win_size).to(y.device)

    y = torch.nn.functional.pad(y.unsqueeze(1), (int((n_fft-hop_size)/2), int((n_fft-hop_size)/2)), mode='reflect')
    y = y.squeeze(1)

    # complex tensor as default, then use view_as_real for future pytorch compatibility
    spec = torch.stft(y, n_fft, hop_length=hop_size, win_length=win_size, window=hann_window[str(y.device)],
                      center=center, pad_mode='reflect', normalized=False, onesided=True, return_complex=True)
    spec = torch.view_as_real(spec)
    spec = torch.sqrt(spec.pow(2).sum(-1)+(1e-9))

    spec = torch.matmul(mel_basis[str(fmax)+'_'+str(y.device)], spec)
    spec = spectral_normalize_torch(spec)

    return spec



def get_dataset_filelist(a):
    train_list = read_txt_to_list(a.train)
    valid_list = read_txt_to_list(a.valid)
    return train_list,valid_list




def get_16k_mel_hifigan_tensor(in_audio, In_Sample_Rate=16000, n_fft=1024, num_mels=80, win_size = 640, hop_size = 160, fmin = 0, fmax = 8000):

    audio5 = in_audio.unsqueeze(0)

    # print("in_wav = ",audio.shape)

    mel = mel_spectrogram(audio5, n_fft, num_mels,In_Sample_Rate, hop_size, win_size, fmin, fmax, center=False)
    #
    out_mel = mel.squeeze()#.numpy()
    #
    # print("out_mel = ",out_mel.shape)
    #
    return out_mel




def get_16k_mel_hifigan_wav(wav_path, In_Sample_Rate=16000, n_fft=1024, num_mels=80, win_size = 640, hop_size = 160, fmin = 0, fmax = 8000):

    # audio1, sampling_rate = load_wav(wav_path)
    wave, sampling_rate = sf.read(wav_path)

    assert sampling_rate == In_Sample_Rate

    #wave_abs = abs(wave)
    #max_v = max(wave_abs)
    #wave = (wave / max_v) * ( 0.4 + random.uniform(0.0,0.55))


    audio4 = torch.FloatTensor(wave)
    audio5 = audio4.unsqueeze(0)

    # print("in_wav = ",audio.shape)

    mel = mel_spectrogram(audio5, n_fft, num_mels,In_Sample_Rate, hop_size, win_size, fmin, fmax, center=False)
    #
    out_mel = mel.squeeze()#.numpy()
    #
    # print("out_mel = ",out_mel.shape)
    #
    return audio5, out_mel




def get_16k_mel_hifigan_dir(in_wav_dir,out_mel_dir):
    global g_suffix_del
    #
    # wav_file_list = read_txt_to_list(in_wav_txt)

    wav_file_list = os.listdir(in_wav_dir)

    #
    for i in tqdm(range(len(wav_file_list))):
        cur_file_path = os.path.join(in_wav_dir,wav_file_list[i])

        cur_file = os.path.basename(cur_file_path)
        #
        if(cur_file.split(".")[-1] != g_suffix_del):
            continue
        #
        dst_file_path = os.path.join(out_mel_dir,cur_file.split(".")[0] + "_16k_mel80_win40_hop10.npy")
        #
        wav_tensor,out_mel = get_16k_mel_hifigan_wav(cur_file_path)
        #
        # print("wav_tensor=",wav_tensor.shape,",out_mel=",out_mel.shape)
        #
        np.save(dst_file_path,out_mel)
    #
    return 



if __name__ == "__main__":
    in_wav = sys.argv[1]
    out_mel_dir = sys.argv[2]
    #
    get_16k_mel_hifigan_dir(in_wav, out_mel_dir)
