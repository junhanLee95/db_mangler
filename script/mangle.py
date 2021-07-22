import glob
import os
from collections import OrderedDict
import re

class Mangler:
# constants
    PREFIX_LEN = 4 # in hexadecimal
# methods
    def __init__(self, kmap, kmap_files, type):
        self.kmap = kmap
        self.kmap_files = kmap_files
        self.type = type

    def mangle(self):
        if self.type == 'k':
            self.kmangle()
        else:
            self.vmangle()

    def mangle_write(self, out_file):
        f = open(out_file, 'w')
        for k, v in self.kmap.items():
            line_str = "{}\t{}\n".format(k,v)
            f.write(line_str)
        f.close()

    def kmangle(self): 
        old_k = ""
        for k, v in self.kmap.items():
            if old_k == "":
                kl = len(k)
                self.kmap[k] = prefix(self.PREFIX_LEN, k).ljust(kl, '0')
            elif suffix(self.PREFIX_LEN, old_k) == suffix(self.PREFIX_LEN, k):
                self.kmap[k] = prefix(self.PREFIX_LEN, self.kmap[k]) + suffix(PREIFX_LEN, self.kmap[old_k])
            else:
                kl = len(k)
                okl = len(old_k)
                minl = min(kl, okl)
                i = 0
                while i < minl:
                    if(k[i] != old_k[i]):
                        break
                    i = i + 1
                self.kmap[k] = (prefix(self.PREFIX_LEN, k) + self.kmap[old_k][self.PREFIX_LEN:i] + k[i]).ljust(kl, '0')
            old_k = k

    def vmangle(self):
        old_k = ""
        for k, v in self.kmap.items():
            kl = len(k)
            self.kmap[k] = "".ljust(kl, '0')


def prefix(PREFIX_LEN, string):
        return string[:PREFIX_LEN]

def suffix(PREFIX_LEN, string):
        return string[PREFIX_LEN:]

def getItemFromLine(line):
    args = re.split('\t', line)
    return args[0], args[1]

def main():
    dict_path = "/home/junhan/db_mangler/mangled_map/"
# key mangling
    kmap_files = glob.glob(dict_path+"*_kmap.csv")
    kmap = {}
    for kmap_filei in kmap_files:
        with open(kmap_filei, 'r', errors='ignore') as kmap_file:
            while True:
                line = kmap_file.readline()
                if not line:
                    break
                k, v = getItemFromLine(line)
                kmap[k] = v
    kmangler = Mangler(kmap, kmap_files, 'k')
    kmangler.mangle()
    kmangler.mangle_write(dict_path+"sst_kmap_mangle.csv")
# value mangling
    vmap_files = glob.glob(dict_path+"*_vmap.csv")
    vmap = {}
    for vmap_filei in vmap_files:
        with open(vmap_filei, 'r', errors='ignore') as vmap_file:
            while True:
                line = vmap_file.readline()
                if not line:
                    break
                k, v = getItemFromLine(line)
                vmap[k] = v
    vmangler = Mangler(vmap, vmap_files, 'v')
    vmangler.mangle()
    vmangler.mangle_write(dict_path+"sst_vmap_mangle.csv")

if __name__ == "__main__":
    main()
