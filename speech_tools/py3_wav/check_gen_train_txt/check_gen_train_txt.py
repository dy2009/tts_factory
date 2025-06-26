import os
import sys
import shutil


def read_txt_to_list(in_txt):
    #
    cur_f = open(in_txt,"r",encoding="utf8")
    #
    txt_list = []
    #
    for curLine in cur_f.readlines():
        line_cp = curLine.strip()
        #
        if(len(line_cp) <= 0):
            continue
        #
        txt_list.append(line_cp)
    #
    cur_f.close()
    #
    return txt_list





def filter_txt(in_txt,out_txt):
    #
    cur_f = open(in_txt,"r",encoding="utf8")
    dst_f = open(out_txt,"w",encoding="utf8")
    #
    out_dir = "step2_wav"
    #
    for curLine in cur_f.readlines():
        line_cp = curLine.strip()
        #
        if(len(line_cp) <= 0):
            continue
        #
        seg_list = line_cp.split("|")
        #
        cur_id = seg_list[0]
        cur_txt = seg_list[1]
        #
        if(cur_id.find("_letter_") >= 0):
            continue
        #
        seg_list2 = cur_id.split("_")
        #
        new_id = "tts_mark231101_" + seg_list2[2]
        #
        wav_path = os.path.join("wav1_mpeg",cur_id + ".mp3")
        #
        if(os.path.exists(wav_path)):
            wav_size = os.path.getsize(wav_path)
            #
            if(wav_size <= 5000):
                continue
            #
            out_line = new_id + "=" + cur_txt
            #
            dst_f.write(out_line + "\n")
            #
            dst_wav_path = os.path.join(out_dir,new_id + ".mpeg")
            #
            shutil.copy(wav_path,dst_wav_path)
            
    #
    cur_f.close()
    dst_f.close()
    #
    return 



if __name__ == "__main__":
    in_txt = sys.argv[1]
    out_txt = sys.argv[2]
    #
    #
    filter_txt(in_txt,out_txt)