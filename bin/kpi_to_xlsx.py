
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
import subprocess
import json
import csv
import pandas as pd

def parse_args():
    # parse options
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--inputfolder',
        help       = 'The simulation result folder.',
        default    = None,
    )
    return parser.parse_args()

def writeXLSX(kpi_file,xlxs_file_name,sheet_name):

	print('\n\n##### READING {} KPI'.format(sheet_name))

	f = open(kpi_file)
	data = json.load(f)
	f.close()

	# TODO Fix for multiple runs in the future
	stats = data['0']['global-stats']	

	aux_col = 0
	print('\n\n##### START WRITING {} STATS'.format(sheet_name))

	writer = pd.ExcelWriter(xlxs_file_name, engine="openpyxl", mode='a')
	for k,v in stats.items():
		if hasattr(v, "__len__"):
			#it means its an array of key and values
			for index in range(len(v)):
				df = pd.json_normalize(stats[k][index])
				t = df.transpose()
				t.to_excel(writer, sheet_name=sheet_name,startcol=aux_col)  # Default position, cell A1.	
				aux_col = aux_col + 5	
	writer.close()
	print('\n\n##### FINISH WRITING ',sheet_name, 'STATS')

def main(options):

	print('\n\n##### INDENT ON TAB ######')

	global subfolder

	if options.inputfolder:
		subfolder = options.inputfolder

		if subfolder[-1] != '/':
			subfolder = subfolder+'/'

		print('\n\n##### START CONVERTING KPI TO XLSX FOR -> ', subfolder)

	else:
		print('\n\n##### --inputfolder PARAM is mandatory, should contain all 2.4Ghz, 868Mhz and join_metric .kpi files\n')
		assert false

	## CHECK IF join_metric.xlsx EXISTS AND CREATES IF NOT

	filename = subfolder+"join_metric.xlsx"
	if not os.path.isfile(filename):
		print('\n\n##### join_metric.xlsx FILE DOES NOT EXIST')
		run_data = {"folder":subfolder}
		df = pd.json_normalize(run_data)
		with pd.ExcelWriter(filename, engine="openpyxl", mode="w") as writer:
			print('\n\n##### CREATING join_metric.xlsx ')
			df.to_excel(writer, sheet_name='file_info')  
	
	

	#search for kpis
	for item in list([os.path.join(subfolder, x) for x in os.listdir(subfolder)]):
		if item.endswith('2_4Ghz.dat.kpi'):
			kpi_2_4Ghz=item
		if item.endswith('868Mhz.dat.kpi'):
			kpi_868Mhz=item
		if item.endswith('join_metric.dat.kpi'):
			kpi_join=item

	assert kpi_2_4Ghz
	assert kpi_868Mhz
	assert kpi_join
	
	
	writeXLSX(kpi_2_4Ghz,filename,'2.4Ghz')
	
	writeXLSX(kpi_868Mhz,filename,'868Mhz')

	writeXLSX(kpi_join,filename,'join_metric')


if __name__ == '__main__':

	options = parse_args()

	main(options)


