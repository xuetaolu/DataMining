# -*- coding: UTF-8 -*-
from optparse import OptionParser
from math import sqrt
from collections import defaultdict

import random
import sys

def runOnce(list, k):
	list = list.copy()
	res = []
	
	if len(list) < k:
		sys.exit('too large K')
	
	indexSet = []
	for i in range(k):
		index = random.choice([i for i in (set(range(len(list))) - set(indexSet))])
		indexSet.append(index)
		res.append([list[index]])
		list.remove(list[index])
	
	def centerPoint(item):
		l = len(item)
		return tuple([j/l for j in [for i in item]])
	
	def minDest(item):
		return min([sum([sqrt((item[j] - centerPoint(resItemList))[j]**2) for j in range(len(item))]) for resItemList in res])
		
		
	while list != []:
		list.sort(key=minDest)
		
		
	return res
	
	
	

def runKmean(input, output, k):
	recordList = [record for record in dataFromFile(input)]

	res = runOnce(recordList, k)
	
	return res


def dataFromFile(fname, fix=0):
	"""Function which reads from the file and yields a generator"""
	file_iter = open(fname, 'r')
	for line in file_iter:
		line = line.strip().rstrip(',')					# Remove trailing comma
		record = line.split(',')
		for key,value in enumerate(record):
			if key < len(record)-fix:
				record[key] = float(value)
		
		yield tuple(record)

def dataToFile(fname):
	pass


if __name__ == '__main__':

	optparser = OptionParser()
	optparser.add_option('-f', '--inputFile',
						 dest='input',
						 help='filename containing csv',
						 default=None)
	optparser.add_option('-o', '--outputFile',
						 dest='output',
						 help='filename outputFile csv',
						 default=None)
	optparser.add_option('-k', '--kValue',
						 type=int,
						 dest='k',
						 help='value of K',
						 default=20)

	(options, args) = optparser.parse_args()

	if options.input is None or options.output is None:
			usage = \
"""
	Usage:
		python kmean.py -f DATASET.csv -o output.csv [-k kValue]
	etc.
		python kmean.py -f DATASET.csv -t output.csv -k 2
"""
			print(usage)
			sys.exit('System will exit')

	else:

		res = runKmean(options.input, options.output, options.k)

		print("finish, Output ot file : ", options.output)
