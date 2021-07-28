#!/usr/bin/env python3
import glob
import os
from collections import OrderedDict
import subprocess
import re

def case_finder(query) :
	if query.startswith("PUT") :
		return "KV"
	elif query.startswith("MERGE") :
		return "KV"
	elif query.startswith("SINGLE_DELETE") :
		return "K"
	elif query.startswith("DELETE_RANGE") :
		return "KV"
	elif query.startswith("DELETE(") :
		return "K"
	else :
		return "NOOP"


def main() :
	bin_path = "../bin/"
	db_path = "../db_export/db/"
	dict_path = "../mangled_map/"

	db_wal_files = glob.glob(db_path + "*.log")

	# dump wal
	for wal in db_wal_files : 
		ldb = bin_path + "ldb"
		command = ldb + " dump_wal --walfile=" + wal + " --print_value"
		with open(wal + ".dump", "w") as f :
			subprocess.call([command], shell=True, stdout=f)

	# remove redundant filename because it appends all writes
	k_name = dict_path + 'wal_kmap.csv'
	v_name = dict_path + 'wal_vmap.csv'
	print("Remove " + k_name + ", " + v_name + " if it exists")
	os.system("rm " + k_name)
	os.system("rm " + v_name)
	print("Write a new dumped wal kv-map in " + k_name + " and " + v_name)

	wal_dump_files = glob.glob(db_path + "*.log.dump")
	for wal_dump in wal_dump_files : 
		print(os.path.abspath(wal_dump))
		with open(wal_dump, 'r') as wal_dump_file : 
			
			kmap = open(k_name, 'a')
			vmap = open(v_name, 'a')

			while True :
				# read line and replace ',' and ':' to ' '
				line = wal_dump_file.readline().replace(',', ' ').replace(':', ' ')

				# eliminate redundant empty space
				line = re.sub(' +', ' ', line)

				if not line :
					break

				# split line using empty space
				strings = line.split(' ')

				# open as append mode and write kv map
				#f.write("Sequence	count	query	key	value\n")
					
				i = 1
				j = 4
				while i <= int(strings[1]) :

					if case_finder(strings[j]) == "KV" :
						kmap.write(strings[j + 1] + "	\n")
						vmap.write(strings[j + 2] + "	\n")
						j = j + 3

					elif case_finder(strings[j]) == "K" :
						kmap.write(strings[j + 1] + "	\n")
						j = j + 2

					elif case_finder(strings[j]) == "NOOP" :
						j = j + 1

					i = i + 1
			
			kmap.close()
			vmap.close()

if __name__ == "__main__":
	main()

