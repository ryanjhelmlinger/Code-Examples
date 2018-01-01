import numpy as np
import cv2, sys, random, copy
from time import sleep
img = np.zeros((800,800,3), np.uint8)
img.fill(0)
coords = []
for i in range(0, 1000): coords.append((int(random.uniform(10,img.shape[0]-10)),int(random.uniform(10,img.shape[1]-10)),int(random.uniform(0,255)),False))
count, reach = 0, True
while(True):
	reachCount, coo2 = -1, []
	count += 1
	for (x,y,i,fresh) in coords:
		cv2.circle(img,(x,y), 5, (0,int(i/3),int(1/3)), -1)
		if fresh==False:
			i2 = i+15
			if i2>225:
				cv2.circle(img,(x,y), 5, (0,255,255), -1)
				if reachCount!=count:
					reachCount = count
					if reach==False: reach=True
					else: reach=False
				i2=0
				if reach==False: coo2.append((x,y,i2,True))
				else: coo2.append((x,y,i2,False))
			else:coo2.append((x,y,i2,False))
		else:coo2.append((x,y,i,False))
	cv2.imshow("Dots", img)
	cv2.waitKey(27)
	sleep(.15)
	coords = copy.copy(coo2)