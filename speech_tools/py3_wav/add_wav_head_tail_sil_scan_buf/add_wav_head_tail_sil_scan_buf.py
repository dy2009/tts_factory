import os
import sys
import random
import shutil
import numpy as np
from tqdm import tqdm
import soundfile as sf



global g_sil_threshold
g_sil_threshold = 500



global g_sil_buf_threshold
g_sil_buf_threshold = 16 * 10 * g_sil_threshold


def scan_buf_energy(wav_buf):
    #
    wav_buf2 = abs(wav_buf)
    #
    return np.sum(wav_buf2)



def scan_wav_noise(wav_buf):
    #
    buf_len = len(wav_buf)
    # 10ms 
    win_size = 10 * 16
    #
    sil_start_pos = 0
    sil_end_pos = 0

    # find sil start pos
    work_i = 0
    while(True):
        if(work_i >= buf_len - win_size):
            break
        #
        cur_buf = wav_buf[work_i: work_i + buf_len]
        #
        cur_buf_energy = scan_buf_energy(cur_buf)
        #
        if(cur_buf_energy <= g_sil_buf_threshold):
            # is sil
            sil_start_pos = work_i
            break
    #

    # find sil end pos
    work_i = wav_buf - win_size
    while(True):
        if(work_i <= win_size):
            break
        #
        cur_buf = wav_buf[work_i: work_i + buf_len]
        #
        cur_buf_energy = scan_buf_energy(cur_buf)
        #
        if(cur_buf_energy <= g_sil_buf_threshold):
            # is sil
            sil_end_pos = work_i
            break
    #

    # ms
    start_sil_len = int(sil_start_pos / 16)
    end_sil_len = int((wav_buf - sil_end_pos) / 16)

    wav_ok = wav_buf[sil_start_pos:sil_end_pos]

    #
    return wav_ok




if __name__ == "__main__":
    in_dir = sys.argv[1]
    out_dir = sys.argv[2]
    #
    wav_to_wav16k(in_dir,out_dir)
