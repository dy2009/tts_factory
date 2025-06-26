
import numpy as np
import wave
import os
import sys


def remove_silence(input_path, output_path, energy_threshold=0.01, frame_length_ms=20, frame_shift_ms=10):
    """
    删除wav文件中的静音段并保存
    
    参数:
        input_path: 输入wav文件路径
        output_path: 输出wav文件路径
        energy_threshold: 能量阈值(0-1)，默认0.01
        frame_length_ms: 帧长(毫秒)，默认20ms
        frame_shift_ms: 帧移(毫秒)，默认10ms
    """
    # 读取wav文件
    with wave.open(input_path, 'rb') as wav_file:
        params = wav_file.getparams()
        sample_width = params.sampwidth
        frame_rate = params.framerate
        n_frames = params.nframes
        audio_data = np.frombuffer(wav_file.readframes(n_frames), dtype=np.int16)
    
    # 计算帧参数
    frame_length = int(frame_rate * frame_length_ms / 1000)
    frame_shift = int(frame_rate * frame_shift_ms / 1000)
    
    # 计算短时能量
    energy = []
    for i in range(0, len(audio_data) - frame_length, frame_shift):
        frame = audio_data[i:i+frame_length]
        frame_energy = np.sum(np.abs(frame.astype(np.float32))) / frame_length
        energy.append(frame_energy)
    
    # 归一化能量
    max_energy = max(energy) # if max(energy) > 0 else 1
    # energy = [e/max_energy for e in energy]

    # print(energy)
    # exit(0)
    
    # 标记非静音帧
    non_silent_frames = []
    for i, e in enumerate(energy):
        if e >= energy_threshold:
            start = i * frame_shift
            end = start + frame_length
            non_silent_frames.append((start, end))
    
    # 合并相邻的非静音段
    merged_segments = []
    if non_silent_frames:
        current_start, current_end = non_silent_frames[0]
        for start, end in non_silent_frames[1:]:
            if start <= current_end:
                current_end = end
            else:
                merged_segments.append((current_start, current_end))
                current_start, current_end = start, end
        merged_segments.append((current_start, current_end))
    
    # 提取非静音音频
    output_audio = np.array([], dtype=np.int16)
    for start, end in merged_segments:
        output_audio = np.concatenate((output_audio, audio_data[start:end]))
    
    # 保存处理后的音频
    with wave.open(output_path, 'wb') as out_file:
        out_file.setparams(params)
        out_file.writeframes(output_audio.tobytes())

# 批量处理目录中的wav16k文件
def process_directory(input_dir, output_dir, energy_threshold=40.0):
    """批量处理目录中的所有wav16k文件"""
    os.makedirs(output_dir, exist_ok=True)
    
    for filename in os.listdir(input_dir):
        if filename.endswith(".wav"):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            remove_silence(input_path, output_path, energy_threshold)
            print(f"处理完成: {filename}")

# 使用示例
if __name__ == "__main__":
    # input_dir = sys.argv[1]
    # output_dir = sys.argv[2]  # 输出目录

    input_dir = "in_dir"
    output_dir = "out_dir"

    process_directory(input_dir, output_dir)