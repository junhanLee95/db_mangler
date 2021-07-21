import glob
import os
from collections import OrderedDict
import re

def main():
    bin_path = "/home/junhan/db_mangler/bin/"
    db_path = "/home/junhan/db_mangler/db_export/db/"
    dict_path = "/home/junhan/db_mangler/mangled_map/"
    
    db_sst_files = glob.glob(db_path+"*.sst")
    for sst in db_sst_files:
        sst_dump = bin_path+"sst_dump"
        command = sst_dump + " --file=" + sst + " --output_hex --command=raw"
        os.system(command)
    
    k_dict = {}
    v_dict = {}
    
    db_sst_dump_files = glob.glob(db_path+"*_dump.txt")
    for sst_dump in db_sst_dump_files:
        print(sst_dump)
        data_block_start = False
        with open(sst_dump, 'r', errors='ignore') as sst_dump_file:
            while True:
                line = sst_dump_file.readline()
                if not line:
                    break
                if (not data_block_start and line.find('Data Block') != -1):
                    data_block_start = True
                if (data_block_start and line.find('HEX') != -1):
                    k, v = getItemFromLine(line)
                    k_dict[k] = 1
                    v_dict[v] = 1 
    
    saveItemsAsFile(k_dict, dict_path+"sst_kmap.csv")
    saveItemsAsFile(v_dict, dict_path+"sst_vmap.csv")

def getItemFromLine(line):
    args = re.split(':| ', line)
    return args[6], args[8][:-1]

def saveItemsAsFile(d, dict_path):
    f = open(dict_path, 'w')
    for k, v in d.items():
        line_str = "{}\t{}\n".format(k,v)
        f.write(line_str)
    f.close()
        
    

if __name__ == "__main__":
    main()
