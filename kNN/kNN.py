# -*- coding: UTF-8 -*-
from optparse import OptionParser
from math import sqrt
from collections import defaultdict

import sys

def runKNN(input, test, k):
    recordList = [record for record in dataFromFile(input, fix=1)]

    res = []
    for recordTest in dataFromFile(test):
        def sortedByDistance(record):
            # print(record)
            # print(recordTest)
            distances = [sqrt((record[i] - recordTest[i])**2) for i, value in enumerate(recordTest)]
            # print(distances)
            return sum(distances)

        countDict = defaultdict(int)
        for index, item in enumerate(sorted(recordList, key=sortedByDistance)):
            # print(item)
            
            if index >= k:
                break;
            countDict[frozenset(item[len(item)-1])] += 1;

        tagSet = None
        maxFreq = 0;
        for key, count in countDict.items():
            if maxFreq < count:
                maxFreq = count
                tagSet = key

        res.append([countDict, recordTest + tuple(tagSet)])

    return  res


def dataFromFile(fname, fix=0):
    """Function which reads from the file and yields a generator"""
    file_iter = open(fname, 'r')
    for line in file_iter:
        line = line.strip().rstrip(',')                    # Remove trailing comma
        record = line.split(',')
        for key,value in enumerate(record):
            if key < len(record)-fix:
                record[key] = float(value)
        # print(tuple(record))
        yield tuple(record)


if __name__ == '__main__':

    optparser = OptionParser()
    optparser.add_option('-f', '--inputFile',
                         dest='input',
                         help='filename containing csv',
                         default=None)
    optparser.add_option('-t', '--testFile',
                         dest='test',
                         help='filename test csv',
                         default=None)
    optparser.add_option('-k', '--kValue',
                         type=int,
                         dest='k',
                         help='value of K',
                         default=20)
    optparser.add_option('-b', '--brief',
                         action="store_true",
                         dest='brief',
                         help='print details',
                         default=False)

    (options, args) = optparser.parse_args()

    if options.input is None or options.test is None:
            usage = \
"""
    Usage:
        python kNN.py -f DATASET.csv -t test.csv [-k kValue] [-b]
    etc.
        python kNN.py -f DATASET.csv -t test.csv -k 20 -b
"""
            print(usage)
            sys.exit('System will exit')

    else:

        res = runKNN(options.input, options.test, options.k)

        print(options.brief)
        print("--result:--------")
        for i in res:
            if options.brief:
                print(i[0])
            print(i[1])