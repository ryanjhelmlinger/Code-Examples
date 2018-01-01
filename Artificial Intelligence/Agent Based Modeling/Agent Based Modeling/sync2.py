import numpy as np
import cv2, sys, random, copy
from time import sleep
img = np.zeros((800,1600,3), np.uint8)
img.fill(255)
coords = []
for i in range(0, 1000): coords.append((int(random.uniform(10,img.shape[0]-10)),int(random.uniform(10,img.shape[1]-10)),int(random.uniform(-20,10)),int(random.uniform(-20,10)),False))
count, reach = 0, True
while(True):
	img.fill(255)
	countA=countB=0
	reachCount, coo2 = -1, []
	count += 1
	for (x,y,a,b,fresh) in coords:
		cv2.circle(img,(x,y), 75, (255,0,0), 1)
		cv2.circle(img,(x,y), 50, (0,255,0), 1)
		cv2.circle(img,(x,y), 25, (0,0,255), 1)
		cv2.circle(img,(x,y), 125, (255,255,0), 1)
		cv2.circle(img,(x,y), 150, (255,0,255), 1)
		cv2.circle(img,(x,y), 100, (0,255,255), 1)
		cv2.circle(img,(x,y), 225, (255,0,0), 1)
		cv2.circle(img,(x,y), 200, (0,255,0), 1)
		cv2.circle(img,(x,y), 175, (0,0,255), 1)
		cv2.circle(img,(x,y), 275, (255,255,0), 1)
		cv2.circle(img,(x,y), 300, (255,0,255), 1)
		cv2.circle(img,(x,y), 250, (0,255,255), 1)
		'''cv2.rectangle(img, (x-10, y-10), (x+10, y+10), (255,0,0), 1)
		cv2.rectangle(img, (x-20, y-20), (x+20, y+20), (0,255,0), 1)
		cv2.rectangle(img, (x-30, y-30), (x+30, y+30), (0,0,255), 1)
		cv2.rectangle(img, (x-40, y-40), (x+40, y+40), (255,255,0), 1)
		cv2.rectangle(img, (x-50, y-50), (x+50, y+50), (255,0,255), 1)
		cv2.rectangle(img, (x-60, y-60), (x+60, y+60), (0,255,255), 1)
		cv2.rectangle(img, (x-70, y-70), (x+70, y+70), (255,0,0), 1)
		cv2.rectangle(img, (x-80, y-80), (x+80, y+80), (0,255,0), 1)
		cv2.rectangle(img, (x-90, y-90), (x+90, y+90), (0,0,255), 1)
		cv2.rectangle(img, (x-100, y-100), (x+100, y+100), (255,255,0), 1)
		cv2.rectangle(img, (x-110, y-110), (x+110, y+110), (255,0,255), 1)
		cv2.rectangle(img, (x-120, y-120), (x+120, y+120), (0,255,255), 1)'''
		'''if a>0: a+=1
		else: a-=1
		if b>0: b+=1
		else: b-=1
		if a>10: a=-1
		if b>10: b=-1
		if a<-10: a=1
		if b<-10: b=1'''
		a+=2
		b+=1
		#if a>10: a=-10
		#if b>10: b=-10
		countA+=a
		countB+=b
		x+=a
		y+=b
		if x<10: x=img.shape[1]-10
		if x>img.shape[1]-10: x=10
		if y<10: y=img.shape[0]-10
		if y>img.shape[0]-10: y=10
		coo2.append((x,y,a,b,False))
	coords[:] = []
	avgA = int(countA/len(coo2))
	avgB = int(countB/len(coo2))
	#for (x,y,a,b,fresh) in coo2:
		#if a<avgA and int(random.uniform(0,2))==0: a+=1
		#if b<avgB and int(random.uniform(0,2))==0: b+=1
		#if a>avgA and int(random.uniform(0,2))==0: a-=1
		#if b>avgB and int(random.uniform(0,2))==0: b-=1
		#coords.append((x,y,a,b,False))
	cv2.imshow("Dots", img)
	cv2.waitKey(27)
	sleep(.000015)
	coords = copy.copy(coo2)