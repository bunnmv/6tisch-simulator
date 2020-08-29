
import os
import sys

import netaddr

if __name__ == '__main__':
	here = sys.path[0]
	sys.path.insert(0, os.path.join(here, '..'))

# ========================== imports ==========================================

import json
import glob
import numpy as np
from pathlib import Path
import argparse
from shutil import copy

def parse_args():
    # parse options
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--inputfolder',
        help       = 'The simulation result folder.',
        default    = None,
    )
    return parser.parse_args()


def main(options):


	global subfolder

	if options.inputfolder:
		subfolder = options.inputfolder
		print('\n##### START JOIN METRIC HELPER FOR -> ', subfolder)

		subfolders = list([os.path.join(subfolder, x) for x in os.listdir(subfolder)])
		for item in subfolders:
			if '2.4Ghz' in item:
				subfolder_2_4Ghz = item
			elif '868Mhz' in item:
				subfolder_868Mhz = item
		

		assert subfolder_2_4Ghz
		assert subfolder_868Mhz

		print('\n##### FOUND NESTED 2.4Ghz folder -> ', subfolder_2_4Ghz)
		print('\n##### FOUND NESTED 868Mhz folder -> ', subfolder_868Mhz)
	else:
		print('\n##### --inputfolder PARAM is mandatory, should contain both 2.4Ghz and 868Mhz directories\n')
		assert false
        #defatult to simData
        


	#search on 2.4ghz Folder
	inside_2_4Ghz_folder = list([os.path.join(subfolder_2_4Ghz, x) for x in os.listdir(subfolder_2_4Ghz)])
	for item in inside_2_4Ghz_folder:
		if item.endswith('config.json'):
			config_2_4Ghz=item
		if item.endswith('.dat.kpi'):
			kpi_2_4Ghz=item
		if item.endswith('.dat'):
			dat_2_4Ghz=item



	#faster like this
	
	dir_to_create = subfolder+"join_metric/"

	# filename2 = subfolder+"test/test2.txt"
	if not os.path.exists(os.path.dirname(dir_to_create)):
		print('\n##### CREATING join_metric FOLDER')
		try:
			os.makedirs(os.path.dirname(dir_to_create))
			print('\n##### CREATED join_metric FOLDER')
		except OSError as exc: # Guard against race condition
			if exc.errno != errno.EEXIST:
				raise
	else:
		print('\n##### join_metric FOLDER ALREADY EXISTS')

	# with open(filename, "w") as f:
	# 	f.write("FOOBAR eee")

	# with open(filename2, "w") as f:
	# 	f.write("FOOBAR AAAA")


	#copy 2.4 config.json to join metric folder
	print('\n##### COPY 2.4Ghz config.json TO join_metric FOLDER')
	copy(config_2_4Ghz, dir_to_create)

	print('\n##### COPY 2.4Ghz .dat.kpi AND .dat TO join_metric FOLDER')

	#copy 2.4 dat to join metric folder
	copy(kpi_2_4Ghz, dir_to_create)

	#copy 2.4 dat to join metric folder
	copy(dat_2_4Ghz, dir_to_create)

	#store new file paths 
	new_kpi_2_4GhzPath = dir_to_create+os.path.basename(kpi_2_4Ghz)
	new_dat_2_4GhzPath = dir_to_create+os.path.basename(dat_2_4Ghz)


	#rename 2.4Ghz dat.kpi
	print('\n##### RENAME exec_numMotes.dat.kpi to 2_4Ghz.dat in join_metric FOLDER')
	os.rename(new_kpi_2_4GhzPath, dir_to_create+'2_4Ghz.dat.kpi')

	

	#rename 2.4 dat to join metric
	print('\n##### RENAME exec_numMotes.dat to 2.4Ghz.dat in join_metric FOLDER')
	os.rename(new_dat_2_4GhzPath, dir_to_create+'join_metric.dat')


	#search on 868Mghz Folder
	inside_868Mhz_folder = list([os.path.join(subfolder_868Mhz, x) for x in os.listdir(subfolder_868Mhz)])
	for item in inside_868Mhz_folder:
		if item.endswith('.dat.kpi'):
			kpi_868Mhz=item
		if item.endswith('.dat'):
			dat_868Mhz=item



	print('\n##### COPY 868Mhz .dat.kpi AND .dat TO join_metric FOLDER')

	#copy 868 dat to join metric folder
	copy(kpi_868Mhz, dir_to_create)

	#copy 868 dat to join metric folder
	copy(dat_868Mhz, dir_to_create)


	
	#store new file paths 
	new_kpi_868MhzPath = dir_to_create+os.path.basename(kpi_868Mhz)
	new_dat_868MhzPath = dir_to_create+os.path.basename(dat_868Mhz)


	#concat 868 to join_metric(renamed from 2.4 dat ) to create join metric dat file
	print('\n##### APPEND 868Mhz dat file to 2.4Ghz file')
	os.system("cat "+ new_dat_868MhzPath +" >>" + dir_to_create+'join_metric.dat')

	
	#rename 868 dat.kpi
	print('\n##### RENAME exec_numMotes.dat.kpi to 868Mhz.dat.kpi in join_metric FOLDER')
	os.rename(new_kpi_868MhzPath, dir_to_create+'868Mhz.dat.kpi')

	#delete 868 dat
	print('\n##### DELETE 868Mhz exec_numMotes.dat from join_metric FOLDER')
	os.remove(new_dat_868MhzPath)


	#delete 2.4 dat from original
	print('\n##### DELETE 868Mhz exec_numMotes.dat from ->',subfolder_2_4Ghz)
	os.remove(dat_2_4Ghz)


	#delete 868 dat from original
	print('\n##### DELETE 868Mhz exec_numMotes.dat from ->',subfolder_868Mhz)
	os.remove(dat_868Mhz)

	
	print('\n##### HELPER SCRIPT DONE #####')

	print('\n##### CALL python compute_kpis.py')

	print('\n##### CALL python plot.py\n')

	# Path(os.path.dirname(os.path.abspath(subfolder))).mkdir(parents=True, exist_ok=True)
	# Path("/my/directory").mkdir(parents=True, exist_ok=True)




if __name__ == '__main__':

	options = parse_args()

	main(options)


