# USAGE
# python scan.py --image images/page.jpg

# import the necessary packages
from pyimagesearch.transform import four_point_transform
from skimage.filters import threshold_local
import numpy as np
import argparse
import cv2
import imutils


def transform(pos):
	# This function is used to find the corners of the object and the dimensions of the object
	pts = []
	n = len(pos)
	for i in range(n):
		pts.append(list(pos[i][0]))

	sums = {}
	diffs = {}
	tl = tr = bl = br = 0
	for i in pts:
		x = i[0]
		y = i[1]
		sum = x + y
		diff = y - x
		sums[sum] = i
		diffs[diff] = i
	sums = sorted(sums.items())
	diffs = sorted(diffs.items())
	n = len(sums)
	rect = [sums[0][1], diffs[0][1], diffs[n - 1][1], sums[n - 1][1]]
	#      top-left   top-right   bottom-left   bottom-right

	h1 = np.sqrt((rect[0][0] - rect[2][0]) ** 2 + (rect[0][1] - rect[2][1]) ** 2)  # height of left side
	h2 = np.sqrt((rect[1][0] - rect[3][0]) ** 2 + (rect[1][1] - rect[3][1]) ** 2)  # height of right side
	h = max(h1, h2)

	w1 = np.sqrt((rect[0][0] - rect[1][0]) ** 2 + (rect[0][1] - rect[1][1]) ** 2)  # width of upper side
	w2 = np.sqrt((rect[2][0] - rect[3][0]) ** 2 + (rect[2][1] - rect[3][1]) ** 2)  # width of lower side
	w = max(w1, w2)

	return int(w), int(h), rect


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True,
	help = "Path to the image to be scanned")
args = vars(ap.parse_args())

# load the image and compute the ratio of the old height
# to the new height, clone it, and resize it
image = cv2.imread(args["image"])
ratio = 500.0/image.shape[1]
dim = (500, int(image.shape[0] * ratio))

#image = imutils.resize(image, height = 500)
image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
orig = image.copy()

cv2.imshow('INPUT', image)
# convert the image to grayscale, blur it, and find edges
# in the image
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (11, 11), 0)
edged = cv2.Canny(gray, 100, 200)

# show the original image and the edge detected image
print("STEP 1: Edge Detection")
cv2.imshow("Image", image)
cv2.imshow("Edged", edged)
cv2.waitKey(0)
cv2.destroyAllWindows()

# find the contours in the edged image, keeping only the
# largest ones, and initialize the screen contour
_,contours,_=cv2.findContours(edged.copy(), 1, 1)
cv2.drawContours(image, contours, -1, (0, 255, 0), 2)
print("STEP 2: Find Contours")
cv2.imshow("Contours", image)
n = len(contours)
max_area = 0
pos = 0

# loop over the contours
index = 0
for i in contours:
	area = cv2.contourArea(i)
	# Determine max area
	if area > max_area:
		max_area = area
		pos = i

	# Crop each contour into a new image
	x,y,w,h = cv2.boundingRect(i)
	if w > 100 and h > 100:
		index+=1
		new_image = orig[y:y+h, x:x+w]
		cv2.imwrite(str(index) + '.jpg', new_image)

# approximate the contour
peri = cv2.arcLength(pos,True)
approx = cv2.approxPolyDP(pos, 0.02*peri, True)

size = image.shape
w, h, arr = transform(approx)
print("STEP 3: Apply perspective transform")
points2 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
points1 = np.float32(arr)
M = cv2.getPerspectiveTransform(points1, points2)
distance = cv2.warpPerspective(image, M, (w, h))
image = cv2.cvtColor(distance, cv2.COLOR_BGR2GRAY)
#image=cv2.adaptiveThreshold(image,255,1,0,11,2)
image = cv2.resize(image, (w, h), interpolation=cv2.INTER_AREA)
cv2.imshow('OUTPUT', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
