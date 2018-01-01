import numpy as np
import cv2
import sys
import urllib.request
import math
import copy

from PIL import Image
import pytesseract
import io
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'


threshold = 100

def grayScale(img):
	for x in range(img.shape[0]):
		for y in range(img.shape[1]):
			pixel = img[x, y]
			grayColor = .3*pixel[0] + .59*pixel[1] + .11*pixel[2]
			img[x, y] = [grayColor, grayColor, grayColor]
	return img

def topBorder(img,img2):
	global threshold
	count=0
	for x in range(img.shape[0]):
		linePoints = []
		for y in range(img.shape[1]):
			pixel = img[x, y]
			if pixel[0]<=threshold:
				count+=1
				linePoints.append((x,y))
			if pixel[0]>threshold or y==img.shape[1]-1:
				if count>200:
					for point in linePoints: img2[point[0],point[1]]=[0,0,255]
					return img2,x
				else:
					count=0
				linePoints = []
	return img

def bottomBorder(img,img2):
	global threshold
	count=0
	for x in range(img.shape[0]-1,-1,-1):
		linePoints = []
		for y in range(img.shape[1]):
			pixel = img[x, y]
			if pixel[0]<=threshold:
				count+=1
				linePoints.append((x,y))
			if pixel[0]>threshold or y==0:
				if count>200:
					for point in linePoints: img2[point[0],point[1]]=[0,0,255]
					return img2,x
				else:
					count=0
				linePoints = []
	return img

def leftBorder(img,img2):
	global threshold
	count=0
	for y in range(img.shape[1]):
		linePoints = []
		for x in range(img.shape[0]):
			pixel = img[x, y]
			if pixel[0]<=threshold:
				count+=1
				linePoints.append((x,y))
			if pixel[0]>threshold or x==img.shape[1]-1:
				if count>200:
					for point in linePoints: img2[point[0],point[1]]=[0,0,255]
					return img2,y
				else: count=0
				linePoints = []
	return img

def rightBorder(img,img2):
	global threshold
	count=0
	for y in range(img.shape[1]-1,-1,-1):
		linePoints = []
		for x in range(img.shape[0]):
			pixel = img[x, y]
			if pixel[0]<=threshold:
				count+=1
				linePoints.append((x,y))
			if pixel[0]>threshold or x==0:
				if count>200:
					for point in linePoints: img2[point[0],point[1]]=[0,0,255]
					return img2,y
				else: count=0
				linePoints = []
	return img

def horizontalLines(img,img2,top,bottom):
	global threshold
	pixelDiff = 5
	count=0
	horizons = [top]
	for x in range(top+pixelDiff,bottom-pixelDiff):
		if count>200 and x-1>horizons[len(horizons)-1]+pixelDiff:
			for point in linePoints: img2[point[0],point[1]]=[0,255,0]
			horizons.append(x-1)
		count=0
		linePoints = []
		for y in range(img.shape[1]):
			pixel = img[x, y]
			if pixel[0]<=threshold:
				count+=1
				linePoints.append((x,y))
			else:
				if count>200 and x>horizons[len(horizons)-1]+pixelDiff:
					for point in linePoints: img2[point[0],point[1]]=[0,255,0]
					horizons.append(x)
				count=0
				linePoints = []
	horizons.append(bottom)
	return img2,horizons

def verticalLines(img,img2,left,right):
	global threshold
	pixelDiff = 5
	count=0
	verticals = [left]
	for y in range(left+pixelDiff,right-pixelDiff):
		if count>200 and y-1>verticals[len(verticals)-1]+pixelDiff:
			for point in linePoints: img2[point[0],point[1]]=[0,255,0]
			verticals.append(y-1)
		count=0
		linePoints = []
		for x in range(img.shape[1]):
			pixel = img[x, y]
			if pixel[0]<=threshold:
				count+=1
				linePoints.append((x,y))
			else:
				if count>200 and y>verticals[len(verticals)-1]+pixelDiff:
					for point in linePoints: img2[point[0],point[1]]=[0,255,0]
					verticals.append(y)
				count=0
				linePoints = []
	verticals.append(right)
	return img2,verticals

def fillings(img,img2,horizontals,verticals):
	global threshold
	midHorizontals = []
	for i in range(0,len(horizontals)-1):
		midHorizontals.append(int((horizontals[i]+horizontals[i+1])/2))
	midVerticals = []
	for i in range(0,len(verticals)-1):
		midVerticals.append(int((verticals[i]+verticals[i+1])/2))
	count=0
	filled = []
	for x in midHorizontals:
		for y in midVerticals:
			pixel = img[x, y]
			if pixel[0]<=threshold:
				cv2.circle(img2,(y,x),3,(255,0,0),-1)
				filled.append(count)
			count+=1
	return img2,filled

def display(length,width,puzzle):
	count=0
	for i in range(0,length):
		for j in range(0,width):
			item = str(puzzle[count])
			if len(item)==1: print(item, "  ", end=" ")
			else: print(item, " ", end=" ")
			count+=1
		print()
		print()

def makePuzzle(length,width,filled):
	puzzle=[]
	count=0
	numbering = 1
	numbered = False
	across = []
	down = []
	for i in range(0,length):
		for j in range(0,width):
			if count in filled: puzzle.append("*")
			else:
				if count-1 in filled or count%width==0:
					across.append(numbering)
					numbered = True
				if count-width in filled or count-width<0:
					down.append(numbering)
					numbered = True
				if numbered == True:
					puzzle.append(numbering)
					numbering+=1
					numbered = False
				else:
					puzzle.append("_")
			count+=1
	display(length,width,puzzle)
	print()
	print()
	print("Across numbers: ", across)
	print()
	print("Down numbers: ", down)

def eraseGrid(img,top,bottom,left,right):
	for i in range(top,bottom+1):
		for j in range(left,right+1):
			img[i,j]=[255,255,255]
	return img


picture = sys.argv[1]
img = cv2.imread(picture, 1)
img = grayScale(img)
img2 = copy.copy(img)
img2,top = topBorder(img,img2)
img2,bottom = bottomBorder(img,img2)
img2,left = leftBorder(img,img2)
img2,right = rightBorder(img,img2)
img2,horizons = horizontalLines(img,img2,top,bottom)
img2,verticals = verticalLines(img,img2,left,right)
img2,filled = fillings(img,img2,horizons,verticals)
print("Size of puzzle: ", len(horizons)-1, "x", len(verticals)-1)
#print("Indexes of spots filled: ", filled)
print()

makePuzzle(len(horizons)-1,len(verticals)-1,filled)

img3 = copy.copy(img)
img3 = eraseGrid(img3,top,bottom,left,right)

cv2.imwrite("newBlank.jpg", img3)

f = open("newBlank.jpg", 'rb')
im = Image.open(f)
img = Image.fromarray(img3)
text = pytesseract.image_to_string(img)
print(text)

cv2.imshow("Color", img)

keypressed = -1
while keypressed!=27:
	keypressed = cv2.waitKey(0)
	if keypressed == 97:
		onBlur = False
		cv2.destroyAllWindows()
		cv2.imshow("Base Image", img)
	if keypressed == 115:
		onBlur = False
		cv2.destroyAllWindows()
		cv2.imshow("Grid Reading Visualization", img2)
	if keypressed == 100:
		onBlur = True
		cv2.destroyAllWindows()
		cv2.imshow("No Grid", img3)

cv2.destroyAllWindows()