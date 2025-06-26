import os
import sys
import random
import shutil

global g_suffix_del
g_suffix_del = "wav"


global g_out_i
g_out_i = 1

def norm_f0(in_dir,out_dir):
    global g_out_i
    global g_suffix_del
    #
    file_list = os.listdir(in_dir)
    #
    for i in range(len(file_list)):
        for j in range(100):

            cur_file = file_list[i]
            cur_file_path = os.path.join(in_dir,cur_file)
            #

            dst_file = cur_file[:-4] + "_{0:06d}".format(g_out_i) + ".wav"
            g_out_i += 1

            dst_file_path = os.path.join(out_dir,dst_file)
            #

            rand_spped = random.uniform(0.8, 1.2)

            rand_spped_str = str(rand_spped)
            tmp_file = "tmp.wav"
            sox_cmd_speed = "sox " + cur_file_path + " " + tmp_file + " speed " + rand_spped_str
            os.system(sox_cmd_speed)


            random_number = random.uniform(-8, -0.5)
            random_str = str(random_number)

            # sox_com = "sox --norm=0 " + cur_file_path + " " + dst_file_path

            sox_com = "sox --norm=" + random_str + " " + tmp_file + " " + dst_file_path
            #
            os.system(sox_com)

            #

            os.remove(tmp_file)


    #
    return 


if __name__ == "__main__":
    in_dir = sys.argv[1]
    out_dir = sys.argv[2]
    #
    norm_f0(in_dir,out_dir)