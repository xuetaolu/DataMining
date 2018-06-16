# -*- coding: UTF-8 -*-
from optparse import OptionParser
from math import sqrt
from collections import defaultdict

import random
import sys

def figureCost(pointLists):

  def singleCost(pointList):
    center = centerPoint(pointList)
    return sum([countDest(i, center) for i in pointList])

  return sum([singleCost(i) for i in pointLists])

def centerPoint(pointList):
    return tuple([sum(i)/len(i) for i in list(zip(*pointList))])

def countDest(pointA, pointB):
    return sum([(i[0]-i[1])**2 for i in list(zip(*[pointA, pointB]))])

def runOnce(listOrg, k):

  def minDest(point, targetLists):
      return min([countDest(point, centerPoint(i)) for i in targetLists])

  listCpy = listOrg.copy()
  res = []

  for i in range(k):
      point = random.choice(listCpy)
      res.append([point])
      listCpy.remove(point)

  while listCpy != []:
      listCpy.sort(key=lambda i: minDest(i, res))
      point = listCpy[0]
      listCpy.remove(listCpy[0])
      res.sort(key=lambda itemList: countDest(point, centerPoint(itemList)))
      res[0].append(point)
  
  return res
  

def runKmean(input, output, k, tryCount=10):
  recordList = [record for record in dataFromFile(input)]

  cost = float('inf')
  for i in range(tryCount):
      res_tmp = runOnce(recordList, k)
      cost_tmp = figureCost(res_tmp)
      if cost_tmp < cost:
          res, cost = res_tmp, cost_tmp
          print('Count: ', i + 1, ' ', 'Cost: ', cost_tmp, '!decrease')
      else:
          pass
          # print('Count: ', i + 1, ' ', 'Cost: ', cost_tmp)

  dataToFile(output, res)

  return res, cost


def dataFromFile(fname, fix=0):
  """Function which reads from the file and yields a generator"""
  file_iter = open(fname, 'r')
  for line in file_iter:
    line = line.strip().rstrip(',')          # Remove trailing comma
    record = line.split(',')
    for key,value in enumerate(record):
      if key < len(record)-fix:
        record[key] = float(value)
    
    yield tuple(record)

def dataToFile(fname, data):
  file = open(fname, 'w')
  for i, v in enumerate(data):
    for item in v:
      file.write(','.join([str(i) for i in item]) + ',' + 'Class_' + str(i + 1) + ',\n')


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
             default=2)
  optparser.add_option('-i', '--iterations',
             type=int,
             dest='iterations',
             help='value of iterations',
             default=10)

  (options, args) = optparser.parse_args()

  if options.input is None or options.output is None:
      usage = \
"""
  Usage:
    python kmean.py -f DATASET.csv -o output.csv [-k kValue] [-i iterations]
  etc.
    python kmean.py -f DATASET.csv -o output.csv -k 2 -i 10
"""
      print(usage)
      sys.exit('System will exit')

  else:

    res, cost = runKmean(options.input, options.output, options.k, options.iterations)

    print("finish, Output to file : ", options.output)
