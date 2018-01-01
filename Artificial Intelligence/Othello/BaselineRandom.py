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

def compChoose2(board, turnLetter):
	possibleMoves = findPossibilities(board, turnLetter)
	index, num = random.choice(list(possibleMoves))
	return index
	board = inputSpot(board, index, turnLetter)
	if turnLetter == "O": turnLetter = "X"
	else: turnLetter = "O"
	return [board, turnLetter]


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

board = sys.argv[1]
turnLetter = sys.argv[2]

print(compChoose2(board, turnLetter))