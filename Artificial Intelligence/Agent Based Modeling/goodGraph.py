import numpy as np
import cv2, sys, random, copy
from time import sleep

def connect(net,k):
	for loc,con in net:
		for i in range(k):
			connect = int(random.uniform(0,len(net)))
			con.append(connect)

def add(net,k):
	new, count = [], 0
	truth=True
	while(truth==True):
		for loc,con in net:
			count+=1
			if int(random.uniform(len(con),len(net)))==len(con): 
				new.append(count)
				con.append(len(net))
				if len(new)==k: 
					truth=False
					break
		if truth==False: break
	return new


#img = np.zeros((800,800,3), np.uint8)
#img.fill(255)
network = []
for i in range(4):
	#x = int(random.uniform(10,img.shape[0]-10))
	#y = int(random.uniform(10,img.shape[1]-10))
	network.append(((1,1),[]))
connect(network, 1)


count=0
while(True):
	count+=1
	#img = display(img, network)
	new = add(network, 3)
	#x = int(random.uniform(10,img.shape[0]-10))
	#y = int(random.uniform(10,img.shape[1]-10))
	x=1
	y=1
	network.append(((x,y),new))
	'''for loc,con in network: 
		(x,y) = loc
		cv2.circle(img,(x,y), 2, (0,0,0), -1)
		for node in con:
			(conLoc, conCon) = network[node]
			(xCon,yCon) = conLoc'''
			#cv2.line(img,(x,y),(xCon,yCon),(0,0,0),1)
	#cv2.imshow("Dots", img)
	#cv2.waitKey(27)
	#sleep(.001)
	if count%1000==0: print(count)
	#print(count)
	if count>50000: break

print("\n\n\n")
frequency = {}
for loc,con in network:
	length = len(con)
	if length in frequency: frequency[length]+=1
	else: frequency[length] = 1

for key in frequency:
	print(key, ": ", frequency[key])