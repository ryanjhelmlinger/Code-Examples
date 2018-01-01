import numpy as np
import cv2
import sys
import urllib.request
import math
import copy
#import time, os
#import msvcrt
#import curses
#import pygame
#import pygame.locals()

def grayScale(img):
	for x in range(img.shape[0]):
		for y in range(img.shape[1]):
			pixel = img[x, y]
			grayColor = .3*pixel[0] + .59*pixel[1] + .11*pixel[2]
			img[x, y] = [grayColor, grayColor, grayColor]
	return img

def blur(img):
	count = 0
	numtimes = 0
	for x in range(img.shape[0]):
		for y in range(img.shape[1]):
			count = 0
			numtimes = 0
			pixel = img[x, y]
			count += 4*pixel[0]
			numtimes+=4
			if x!=0:
				pixel = img[x-1, y]
				count += 2*pixel[0]
				numtimes+=2
			if y!=0:
				pixel = img[x, y-1]
				count += 2*pixel[0]
				numtimes+=2
			if x!=0 and y!=0:
				pixel = img[x-1, y-1]
				count += pixel[0]
				numtimes+=1
			if x!=img.shape[0]-1:
				pixel = img[x+1, y]
				count += 2*pixel[0]
				numtimes+=2
			if y!=img.shape[1]-1:
				pixel = img[x, y+1]
				count += 2*pixel[0]
				numtimes+=2
			if y!=img.shape[1]-1 and x!=0:
				pixel = img[x-1, y+1]
				count += pixel[0]
				numtimes+=1
			if y!=img.shape[1]-1 and x!=img.shape[0]-1:
				pixel = img[x+1, y+1]
				count += pixel[0]
				numtimes+=1
			if x!=img.shape[0]-1 and y!=0:
				pixel = img[x+1, y-1]
				count += pixel[0]
				numtimes+=1
			#print (numtimes)
			count = count/numtimes
			img[x, y] = [count, count, count]
			#img[x, y] = [count, count, count]
	return img

def sobel(img, imgb, limit, upLimits, gradients, upGradients, allGrad):
	for x in range(img.shape[0]):
		for y in range(img.shape[1]):
			count = xcount = ycount = 0
			pixel = img[x, y]
			if x!=0:
				pixel = img[x-1, y]
				xcount += -2*pixel[0]
			if y!=0:
				pixel = img[x, y-1]
				ycount += -2*pixel[0]
			if x!=0 and y!=0:
				pixel = img[x-1, y-1]
				xcount += -1*pixel[0]
				ycount += -1*pixel[0]
			if x!=img.shape[0]-1:
				pixel = img[x+1, y]
				xcount += 2*pixel[0]
			if y!=img.shape[1]-1:
				pixel = img[x, y+1]
				ycount += 2*pixel[0]
			if y!=img.shape[1]-1 and x!=0:
				pixel = img[x-1, y+1]
				xcount += -1*pixel[0]
				ycount += 1*pixel[0]
			if y!=img.shape[1]-1 and x!=img.shape[0]-1:
				pixel = img[x+1, y+1]
				xcount += 1*pixel[0]
				ycount += 1*pixel[0]
			if x!=img.shape[0]-1 and y!=0:
				pixel = img[x+1, y-1]
				xcount += 1*pixel[0]
				ycount += -1*pixel[0]
			count = math.sqrt(xcount*xcount + ycount*ycount)
			#print (count)
			#if xcount == 0: allGrad[100000*x + y] = [count, 1000]
			#else: allGrad[100000*x + y] = [count, math.atan(ycount/xcount)]
			allGrad[100000*x + y] = [count, math.atan(ycount/xcount)]		
			if count > upLimits:
				imgb[x, y] = [0, 0, 255]
				gradients[100000*x + y] = [count, math.atan(ycount/xcount)]
			else: imgb[x, y] = [255, 255, 255]
			if count > limit:
				upGradients[100000*x + y] = count
	return imgb


def canny(img, imgSob, imgCan, imgCan1, limit, upLimit, gradients, upGradients, finalEdges):
	partOneGrad = {}
	for x in range(img.shape[0]):
		for y in range(img.shape[1]):
			#pixel = imgSob[x, y]
			imgCan[x, y] = [255, 255, 255]
			imgCan1[x, y] = [255, 255, 255]
			if x*100000+y in gradients:
				#angle = math.atan(ycount/xcount)
				non, angle = gradients[100000*x + y]
				angle = 360*angle/(2*math.pi)
				if angle<67.5 and angle>112.5: xdir,ydir = 0,1
				elif angle<22.5: xdir,ydir = 1,0
				elif angle>157.5: xdir,ydir = -1,0
				elif angle>22.5 and angle<67.5: xdir,ydir = 1,1
				else: xdir,ydir = -1, 1
				inGrad = {}
				xlast, ylast = x, y
				while(True):
					xlast = xlast + xdir
					ylast = ylast + ydir
					if xlast*100000+ylast in gradients: inGrad[xlast*100000+ylast], non = gradients[xlast*100000+ylast]
					else: break
				xlast, ylast = x, y
				while(True):
					xlast = xlast - xdir
					ylast = ylast - ydir
					if xlast*100000+ylast in gradients: inGrad[xlast*100000+ylast], non = gradients[xlast*100000+ylast]
					else: break
				minGrad, minLoc = -100000000, -1
				for grad in inGrad:
					if inGrad[grad] > minGrad:
						minGrad = inGrad[grad]
						minLoc = grad
				yLoc = minLoc%10000
				xLoc = int(minLoc/100000)
				if minLoc != -1: 
					imgCan[xLoc, yLoc] = [0, 0, 255]
					imgCan1[xLoc, yLoc] = [0, 0, 255]
					partOneGrad[minLoc] = 0
					finalEdges[minLoc] = 0
				#else:
				#	imgCan[x, y] = [0, 0, 0]
	
	for x in range(img.shape[0]):
		for y in range(img.shape[1]):
			#pixel = imgSob[x, y]
			#if pixel[2] == 255:
			if x*100000+y in upGradients:
				goodNeighbor = False
				if not x*100000+y in partOneGrad:
					if (x+1)*100000+y in partOneGrad: goodNeighbor = True
					if (x-1)*100000+y in partOneGrad: goodNeighbor = True
					if x+100000+(y+1) in partOneGrad: goodNeighbor = True
					if x+100000+(y-1) in partOneGrad: goodNeighbor = True
					if (x+1)+100000+(y+1) in partOneGrad: goodNeighbor = True
					if (x+1)+100000+(y-1) in partOneGrad: goodNeighbor = True
					if (x-1)*100000+(y+1) in partOneGrad: goodNeighbor = True
					if (x-1)*100000+(y-1) in partOneGrad: goodNeighbor = True
					if goodNeighbor == True:
						imgCan[x, y] = [0, 0, 255]
						finalEdges[x*100000+y] = 0
						#partOneGrad[x*100000+y] = 0

	return [imgCan, imgCan1]

def canny2(img, imgSob, imgCan, limit, upLimit, gradients, upGradients):
	for x in range(img.shape[0]):
		for y in range(img.shape[1]):
			#pixel = imgSob[x, y]
			imgCan[x, y] = [255, 255, 255]
			if x*100000+y in gradients:
				#angle = math.atan(ycount/xcount)
				non, angle = gradients[100000*x + y]
				angle = 360*angle/(2*math.pi)
				if angle<67.5 and angle>112.5: xdir,ydir = 0,1
				elif angle<22.5: xdir,ydir = 1,0
				elif angle>157.5: xdir,ydir = -1,0
				elif angle>22.5 and angle<67.5: xdir,ydir = 1,1
				else: xdir,ydir = -1, 1
				inGrad = {}
				xlast, ylast = x, y
				while(True):
					xlast = xlast + xdir
					ylast = ylast + ydir
					if xlast*100000+ylast in gradients: inGrad[xlast*100000+ylast], non = gradients[xlast*100000+ylast]
					else: break
				xlast, ylast = x, y
				while(True):
					xlast = xlast - xdir
					ylast = ylast - ydir
					if xlast*100000+ylast in gradients: inGrad[xlast*100000+ylast], non = gradients[xlast*100000+ylast]
					else: break
				minGrad, minLoc = -100000000, -1
				for grad in inGrad:
					if inGrad[grad] > minGrad:
						minGrad = inGrad[grad]
						minLoc = grad
				yLoc = minLoc%10000
				xLoc = int(minLoc/100000)
				if minLoc != -1: imgCan[xLoc, yLoc] = [0, 0, 255]
				#else:
				#	imgCan[x, y] = [0, 0, 0]
	return imgCan

def circles(img, imgEdges, finalEdges, allGrad, circleThresh):
	maxVal, maxInd = 0, -1
	lineToCenter = {}
	lineIntersects = {}
	circles = {}
	aboveTresh = set()
	for key in finalEdges:
		expendable, angle = allGrad[key]
		xVal, yVal = int(key/100000), key%100000
		#lineToCenter[xVal*100000+yVal] = ([set])
		for x in range(img.shape[0]):
			#if angle == 1000: slope = 0
			#else: slope = math.tan(angle)
			slope = math.tan(angle)
			y = int(slope*(x-xVal)+yVal)
			if y>0 and y<img.shape[1]:
				if x*100000+y in lineIntersects:
					val = lineIntersects[x*100000+y]+1
					lineIntersects[x*100000+y] += 1
					if val> maxVal: maxVal, maxInd = val, x*100000+y
				else: lineIntersects[x*100000+y] =1
				if x*100000+y in lineToCenter:
					lineToCenter[x*100000+y].add(xVal*100000+yVal)
				else:
					lineToCenter[x*100000+y] = set()
					lineToCenter[x*100000+y].add(xVal*100000+yVal)
	for x in range(img.shape[0]):
		for y in range(img.shape[1]):
			if x*100000+y in lineIntersects:
				brightness = 255*lineIntersects[x*100000+y]/maxVal
				imgEdges[x, y] = [255-brightness, 255-brightness, 255-brightness]
				if brightness > int(circleThresh):
					#imgEdges[x, y] = [0, 0, 255]
					aboveTresh.add(x*100000+y)
			else: imgEdges[x, y] = [255, 255, 255]
	for center in aboveTresh:
		x, y = int(center/100000), center%100000
		for radius in range(1, img.shape[1]):
			count = 0
			for location in lineToCenter[center]:
				xVal, yVal = int(location/100000), location%100000
				dist = math.sqrt((x-xVal)*(x-xVal) + (y-yVal)*(y-yVal))
				if int(dist) == radius:
					count += 1
			#print (count/(2*math.pi*radius))
			if count/(2*math.pi*radius) > .055:
				cv2.circle(imgEdges,(y,x), radius, (0,0,255), 1)
	'''for point in aboveTresh:
		x, y = int(point/100000), point%100000
		radius = 0
		for location in lineToCenter[point]:
			xVal, yVal = int(location/100000), location%100000
			radius += math.sqrt((x-xVal)*(x-xVal) + (y-yVal)*(y-yVal))
			#imgEdges[xVal, yVal] = [0, 0, 255]
		radius = int(radius/len(lineToCenter[point]))
		if lineIntersects[x*100000+y]/(2*math.pi*radius) > .3:
			minDistance = 1000000000
			for spot in circles:
				xs, ys = int(spot/100000), spot%100000
				distance = math.sqrt((ys-y)*(ys-y)+(xs-x)*(xs-x))
				#print (distance)
				if distance < minDistance:
					minDistance = distance
			#if minDistance > 2:
			cv2.circle(imgEdges,(y,x), radius, (0,0,255), 1)
				#circles[x*100000+y] = 0
		#cv2.circle(img, center, radius, color, thickness=1, lineType=8, shift=0)'''
	return imgEdges

def lines(img, imgEdges, lineIMG, finalEdges, allGrad, circleThresh):
	squiggleCross = {}
	dMaxVal = 0
	maxIntersect = 0
	for key in finalEdges:
		xVal, yVal = int(key/100000), key%100000
		for angle in range (0, 360):
			rad = angle*math.pi/180
			d = int(yVal*math.cos(rad) - xVal*math.sin(rad))
			#d = math.ceil(d*3)/3
			if d>dMaxVal:
				dMaxVal = d
			if (angle,d) in squiggleCross:
				intersect = squiggleCross[(angle,d)] + 1
				if intersect > maxIntersect:
					maxIntersect = intersect
				squiggleCross[(angle,d)] = intersect
			else:
				squiggleCross[(angle,d)] = 1
	for x in range(img.shape[0]):
		for y in range(img.shape[1]):
			imgEdges[x, y] = [255, 255, 255]
	threshers = {}
	for key in squiggleCross:
		angle, d = key[0], key[1]
		x = int(d*(img.shape[0]-1)/dMaxVal)
		y = int(angle*(img.shape[1]-1)/360)
		brightness = 255*squiggleCross[key]/maxIntersect
		imgEdges[x, y] = [255-brightness, 255-brightness, 255-brightness]
		if brightness>170:
			canAdd = True
			for angle2,d2 in threshers:
				x2 = int(d2*(img.shape[0]-1)/dMaxVal)
				y2 = int(angle2*(img.shape[1]-1)/360)
				if math.sqrt((x2-x)*(x2-x)+(y2-y)*(y2-y)) < 15: canAdd = False
			if canAdd==True:
				threshers[angle, d] = 0
				#imgEdges[x, y] = [0, 0, 255]
	for key in threshers:
		angle, d = key[0], key[1]
		rad = angle*math.pi/180
		if rad==90: rad=89.999999999
		if d>0:
			for x in range(0, img.shape[0]):
				y = int((d+x*math.sin(rad))/math.cos(rad))
				if y>0 and y<img.shape[1]:
					lineIMG[x,y] = [0, 0, 255]
			#rad = rad + math.pi/2
			if rad==0: rad=0.000000001
			for y in range(0, img.shape[1]):
				x = int((y*math.cos(rad)-d)/math.sin(rad))
				if x>0 and x<img.shape[0]:
					lineIMG[x,y] = [0, 0, 255]
	return [imgEdges, lineIMG]




picture = sys.argv[1]
if picture == "url":
	picture = sys.argv[2]
	threshold = sys.argv[3]
	upperT = sys.argv[4]
	circleThresh = sys.argv[5]
	resp = urllib.request.urlopen(picture)
	img = np.asarray(bytearray(resp.read()), dtype="uint8")
	img = cv2.imdecode(img, cv2.IMREAD_COLOR)
	img2 = cv2.imdecode(img, cv2.IMREAD_COLOR)
else:
	threshold = sys.argv[2]
	upperT = sys.argv[3]
	circleThresh = sys.argv[4]
	img = cv2.imread(picture, 1)
	img2 = cv2.imread(picture, 1)

gradients = {}
upGradients = {}
finalEdges = {}
allGrad = {}

cv2.imshow("Color", img)
img2 = grayScale(img2)
####cv2.imshow("Black and White", img2)
img3 = copy.copy(img2)
img3 = blur(img3)
#cv2.imshow("Blur", img3)
img4 = copy.copy(img3)
img5 = copy.copy(img3)
img6 = copy.copy(img3)
img7 = copy.copy(img3)
img8 = copy.copy(img3)
img9 = copy.copy(img3)
img10 = copy.copy(img)
#img4 = lines(img4)

threshold = int(threshold)
upperT = int(upperT)

img5 = sobel(img4, img5, threshold, upperT, gradients, upGradients, allGrad)
img6, img7 = canny(img4, img5, img6, img7, threshold, upperT, gradients, upGradients, finalEdges)
#img7 = canny2(img4, img5, img7, threshold, upperT, gradients, upGradients)
#img8 = circles(img4, img8, finalEdges, allGrad, circleThresh)
(img9, img10) = lines(img4, img9, img10, finalEdges, allGrad, circleThresh)
#length = img3.shape[0]
#width = img.shape[1]
#gradient = [length][width]

#cv2.imwrite( "sobel.jpg", sobel );

onBlur = False

keypressed = -1
while keypressed!=27:
	keypressed = cv2.waitKey(0)
	if keypressed == 114:
		onBlur = False
		cv2.destroyAllWindows()
		cv2.imshow("Regular", img)
	if keypressed == 103:
		onBlur = False
		cv2.destroyAllWindows()
		cv2.imshow("Grayed", img2)
	if keypressed == 98:
		onBlur = True
		cv2.destroyAllWindows()
		cv2.imshow("Blurred", img3)
	if keypressed == 112 and onBlur==True:
		img3 = blur(img3)
		print("here")
		cv2.destroyAllWindows()
		cv2.imshow("Blurred", img3)
	if keypressed == 101:
		onBlur = False
		cv2.destroyAllWindows()
		cv2.imshow("Sober", img5)
	if keypressed == 99:
		onBlur = False
		cv2.destroyAllWindows()
		cv2.imshow("Canny", img6)	
	if keypressed == 100:
		onBlur = False
		cv2.destroyAllWindows()
		cv2.imshow("Canny", img7)	
	if keypressed == 113:
		onBlur = False
		cv2.destroyAllWindows()
		cv2.imshow("Circle Detection", img8)
	if keypressed == 108:
		onBlur = False
		cv2.destroyAllWindows()
		cv2.imshow("Line Detection", img9)
	if keypressed == 111:
		onBlur = False
		cv2.destroyAllWindows()
		cv2.imshow("Line Detection", img10)

cv2.destroyAllWindows()