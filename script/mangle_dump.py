import glob
import os
from collections import OrderedDict
import re

def main():
    bin_path = "/home/junhan/db_mangler/bin/"
    db_path = "/home/junhan/db_mangler/db_export/db/"
    dict_path = "/home/junhan/db_mangler/mangled_map/"
    mangled_db_path = "/home/junhan/db_mangler/mangled_data/"

# read mangled map
    k_dict = {}
    v_dict = {}
    kmangle_path = glob.glob(dict_path + "*kmap_mangle.csv")[0]
    vmangle_path = glob.glob(dict_path + "*vmap_mangle.csv")[0]

    with open(kmangle_path, 'r', errors='ignore') as kmangle_file:
        while True:
            line = kmangle_file.readline()
            if not line:
                break
            k, v = getItemFromMangledFile(line)
            k_dict[k] = v
 
    with open(vmangle_path, 'r', errors='ignore') as vmangle_file:
        while True:
            line = vmangle_file.readline()
            if not line:
                break
            k, v = getItemFromMangledFile(line)
            v_dict[k] = v
       

# update sst_dump to be mangled
    db_sst_dump_files = glob.glob(db_path+"*_dump.txt")
    for sst_dump in db_sst_dump_files:
        print(sst_dump)
        data_block_start = False
        mangled_sst_name = getFileName(sst_dump)+".mangle"
        print(mangled_sst_name)
        mangled_sst = open(mangled_db_path+mangled_sst_name, 'w')
        with open(sst_dump, 'r', errors='ignore') as sst_dump_file:
            while True:
                line = sst_dump_file.readline()
                if not line:
                    break
                if (not data_block_start and line.find('Data Block') != -1):
                    data_block_start = True
                if (data_block_start and line.find('HEX') != -1):
                    k, v = getItemFromLine(line)
                    print('---------')
                    print(k)
                    print(v)
                    new_k = k[:4] +  k_dict[k[4:]]
                    new_v = v_dict[v]
                    new_line = "{}\t{}\n".format(new_k, new_v)
#                    new_line = line.replace(k, new_k).replace(v, new_v)
                    mangled_sst.write(new_line)
        mangled_sst.close()
    

def getItemFromLine(line):
    args = re.split(':| ', line)
    return args[6], args[8][:-1]

def getItemFromMangledFile(line):
    args = re.split('\t', line)
    return args[0], args[1][:-1]

def getFileName(line):
    args = re.split('/', line)
    return args[-1]

if __name__ == "__main__":
    main()
