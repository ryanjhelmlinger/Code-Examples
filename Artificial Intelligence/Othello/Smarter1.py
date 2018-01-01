from random     import choice
#
from subprocess import Popen
from subprocess import PIPE
from subprocess import TimeoutExpired
#
from time       import time
from os         import path
import sys
import re

import random
from random import shuffle

import math

def compChoose3(board, turnLetter, level):
	if turnLetter == "X": otherLetter = "O"
	else: otherLetter = "X"
	possibles = findPossibilities(board, turnLetter)
	if level > 1: return [compVal(board, turnLetter), -1]
	level += 1
	if level%2 == 0:
		maxInd = -10000
		maxVal = -10000
		for ind, dist in possibles:
			value, throwaway = compChoose3(inputSpot(board, ind, turnLetter), turnLetter, level)
			if value > maxVal:
				maxVal = value
				maxInd = ind
		if maxVal == -10000: return [compVal(board, turnLetter), -1]
	else:
		maxInd = 10000
		maxVal = 10000
		for ind, dist in possibles:
			value, throwaway = compChoose3(inputSpot(board, ind, otherLetter), turnLetter, level)
			if value < maxVal:
				maxVal = value
				maxInd = ind
		if maxVal == 10000: return [compVal(board, turnLetter), -1]
	return [maxVal, maxInd]



def compVal(board, turnLetter):
	myVal = oppVal = 0
	for ind in range(0, 64):
		if board[ind] == turnLetter:
			myVal += weighting[ind]
		if board[ind] != "." and board[ind] != turnLetter:
			oppVal += weighting[ind]
	return myVal-oppVal


def findPossibilities(puzzle, letter):
	possibilities, eligible = set([]), True
	for x in range(0, 64):
		if puzzle[x] == ".":
			for part in neighbors[x]:
				if puzzle[part]!=letter and puzzle[part]!=".":
					difference, count = x-part, 0
					while(-1<part<64 and puzzle[part]!=letter and puzzle[part]!="." and eligible==True):
						count += 1
						part += -difference
						if math.fabs((part+difference)%8-part%8)==7:
							eligible = False
					if not(part<0 or part>63 or puzzle[part]=="." or eligible==False):
						edited = False
						for tup in possibilities:
							loc, num = tup
							if x==loc:
								edited = True
								num += count
								possibilities.remove(tup)
								possibilities.add((x,num))
						if edited == False: possibilities.add((x,count))
					eligible = True
	return possibilities

def inputSpot(puzzle, index, letter):
	mightWork, possibilities, eligible = set([]), set([]), True
	for part in neighbors[index]:
		if puzzle[part]!=letter and puzzle[part]!=".":
			mightWork, difference = set([]), index-part
			mightWork.add(part)
			while(-1<part<64 and puzzle[part]!=letter and puzzle[part]!="." and eligible==True):
				part += -difference
				mightWork.add(part)
				if math.fabs((part+difference)%8-part%8)==7:
					eligible = False
			if not(part<0 or part>63 or puzzle[part]=="." or eligible==False):
				#for node in mightWork: possibilities.add(node)
				for number in mightWork: puzzle = puzzle[:number] + letter + puzzle[number+1:]
				#possibilities.add(index)
			eligible = True
	puzzle = puzzle[:index] + letter + puzzle[index+1:]
	#for number in possibilities: puzzle = puzzle[:number] + letter + puzzle[number+1:]
	return puzzle


def findNeighbors():
	neighbors = {}
	for x in range(0,8):
		for y in range(0,8):
			neighborList = []
			lower, upper = -1, 2
			if y == 0: lower = 0
			if y == 7: upper = 1
			for w in range(-1,2):
				for z in range (lower,upper):
					index = 8*x+y+8*w+z
					if index > 0 and index < 64 and index != 8*x+y:
						neighborList.append(8*x+y+8*w+z)
			neighbors[8*x+y] = neighborList
	return neighbors


neighbors = findNeighbors()


#great = set([0, 7, 56, 63])
#good = set([2, 3, 4, 5, 16, 24, 32, 40, 23, 31, 39, 47, 58, 59, 60, 61])
#goodneut = set([])
#neutral = set([18, 19, 20, 21, 26, 27, 28, 29, 34, 35, 36, 37, 42, 43, 44, 45])
#bad = set([10, 11, 12, 13, 17, 25, 33, 41, 22, 30, 38, 46, 50, 51, 52, 53])
#terrible = set([1, 6, 8, 14, 48, 55, 57, 62, 9, 15, 49, 54])

weighting = {}
for index in set([0, 7, 56, 63]): weighting[index] = 120
for index in set([2, 5, 16, 23, 40, 47, 58, 61]): weighting[index] = 40
for index in set([18, 21, 42, 45]): weighting[index] = 15
for index in set([3, 4, 24, 31, 32, 39, 59, 60]): weighting[index] = 5
for index in set([19, 20, 26, 27, 28, 29, 34, 35, 36, 37, 43, 44]): weighting[index] = 3
for index in set([10, 11, 12, 13, 17, 22, 25, 30, 33, 38, 41, 46, 50, 51, 52, 53]): weighting[index] = -5
for index in set([1, 6, 8, 15, 48, 55, 57, 62]): weighting[index] = -20
for index in set([9, 14, 49, 54]): weighting[index] = -40



board = sys.argv[1]
turnLetter = sys.argv[2]

throwaway, ind = compChoose3(board, turnLetter, -1)
print(ind)