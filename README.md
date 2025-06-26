# tts_factory
Speech Synthesis Factory 

Author: Kongdw 

kongdw8@gmail.com <br>
dy2009@126.com


Eagle-TTS <br>
Eagle-TTS: A Hybrid Architecture for Real-Time, Human-Indistinguishable Speech Synthesis <br>
<!-- Eagle-TTS: A Hybrid Llama-Transformer Architecture for Real-Time Diffusion-Based Speech Synthesis <br>
Eagle-TTS: a Unified Framework for Human-Indistinguishable TTS mixed Llama,Flow Matching and Diffusion <br>
Eagle-TTS: Breaking the Speed-Fidelity Trade-off in Neural TTS via Llama-Transformer and Flow Matching <br>
Revisiting Diffusion-Based TTS: Eagle-TTS Achieves State-of-the-Art Naturalness with 2x Speedup <br>
​Eagle-TTS: An Industrial-Grade TTS System Combining Llama, Diffusion and Parallel Transformer <br> -->

<br>
1, data_io format <br>
id=cur_id|text=*|wav=cur_id.wav|phone=*|phone_npy=*|spk_embedding=*|whisper_feat_medium=*
 <br>
 <br>
2, tradition tts, parallel <br>
    vits,fast-speech,matcha-tts,f5-tts
 <br>
 <br>
3, tradition tts, rnn <br>
    tacotron,
 <br>
 <br>
4, gpt,Llama based TTS <br>
    cosyvoice2
 <br>
 <br>
5, vocoder <br>
    hiftnet
 <br>
 <br>
train: <br>
python train.py
 <br>
test: <br>
python infer_01.py
