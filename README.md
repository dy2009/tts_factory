# tts_factory
Speech Synthesis Factory 

Author: Kongdw 

kongdw8@gmail.com 

1, data_io format
id=cur_id|text=*|wav=cur_id.wav|phone=*|phone_npy=*|spk_embedding=*|whisper_feat_medium=*


2, tradition tts, parallel
    vits,fast-speech,matcha-tts,f5-tts
3, tradition tts, rnn
    tacotron,
4, gpt,Llama based TTS
    cosyvoice2
5, vocoder
    hiftnet


train:
python train.py

test:
python infer_01.py
