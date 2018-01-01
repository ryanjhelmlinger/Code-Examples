import itertools

allPerm = list(itertools.permutations([1,2,3,4], 4))
for perm in allPerm:
	print (perm)