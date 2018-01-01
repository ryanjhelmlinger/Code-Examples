import numpy as np
import cv2, sys, random, copy
from time import sleep

def connect(net,k):
	count = 0
	for loc,con in net:
		for i in range(k):
			connect = int(random.uniform(0,len(net)))
			con.append(connect)
			loc2,con2 = net[connect]
			con2.append(i)


img = np.zeros((800,800,3), np.uint8)
img.fill(255)
network = []
for i in range(40000):
	x = int(random.uniform(10,img.shape[0]-10))
	y = int(random.uniform(10,img.shape[1]-10))
	network.append(((x,y),[]))

connect(network, 3)
'''
#while(True):
	#img = display(img, network)
for loc,con in network: 
	(x,y) = loc
	#cv2.circle(img,(x,y), 2, (0,0,0), -1)
	for node in con:
		(conLoc, conCon) = network[node]
		(xCon,yCon) = conLoc
			#cv2.line(img,(x,y),(xCon,yCon),(0,0,0),1)
	#cv2.imshow("Dots", img)
	#cv2.waitKey(27)
	#sleep(5)
'''
graphDict = {}

for loc,con in network:
	length = len(con)
	if length in graphDict:
		graphDict[length]+=1
	else:
		graphDict[length]=1

for part in graphDict:
	print(part, ": ", graphDict[part])