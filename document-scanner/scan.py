# USAGE
# From /adapters/: 
# pipenv run python ../scan.py -i ~/Downloads/opencv-master/imgs/2Stickies.jpg -o ~/Documents/Work/identity/samples/IMG_1397_bounds.JPG

# The bible: http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.59.4239&rep=rep1&type=pdf
# https://stackoverflow.com/questions/8667818/opencv-c-obj-c-detecting-a-sheet-of-paper-square-detection
# https://stackoverflow.com/questions/6555629/algorithm-to-detect-corners-of-paper-sheet-in-photo
# https://stackoverflow.com/questions/10893624/extract-lines-from-canny-edge-detection#10902423
# https://blogs.dropbox.com/tech/2016/08/fast-and-accurate-document-detection-for-scanning/
# https://stackoverflow.com/questions/1364976/rectangle-detection-with-hough-transform
# http://answers.opencv.org/question/74777/how-to-use-approxpolydp-to-close-contours/

# import the necessary packages
# from pyimagesearch.transform import four_point_transform
# from skimage.filters import threshold_local
import numpy as np
import argparse
import cv2
import imutils
import math
import itertools

def order_points(pts):
	# initialzie a list of coordinates that will be ordered
	# such that the first entry in the list is the top-left,
	# the second entry is the top-right, the third is the
	# bottom-right, and the fourth is the bottom-left
	rect = np.zeros((4, 2), dtype = "float32")

	# the top-left point will have the smallest sum, whereas
	# the bottom-right point will have the largest sum
	s = pts.sum(axis = 1)
	rect[0] = pts[np.argmin(s)]
	rect[2] = pts[np.argmax(s)]

	# now, compute the difference between the points, the
	# top-right point will have the smallest difference,
	# whereas the bottom-left will have the largest difference
	diff = np.diff(pts, axis = 1)
	rect[1] = pts[np.argmin(diff)]
	rect[3] = pts[np.argmax(diff)]

	# return the ordered coordinates
	return rect

def four_point_transform(image, pts):
	# obtain a consistent order of the points and unpack them
	# individually
	rect = order_points(pts)
	(tl, tr, br, bl) = rect

	# compute the width of the new image, which will be the
	# maximum distance between bottom-right and bottom-left
	# x-coordiates or the top-right and top-left x-coordinates
	widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
	widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
	maxWidth = max(int(widthA), int(widthB))

	# compute the height of the new image, which will be the
	# maximum distance between the top-right and bottom-right
	# y-coordinates or the top-left and bottom-left y-coordinates
	heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
	heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
	maxHeight = max(int(heightA), int(heightB))

	# now that we have the dimensions of the new image, construct
	# the set of destination points to obtain a "birds eye view",
	# (i.e. top-down view) of the image, again specifying points
	# in the top-left, top-right, bottom-right, and bottom-left
	# order
	dst = np.array([
		[0, 0],
		[maxWidth - 1, 0],
		[maxWidth - 1, maxHeight - 1],
		[0, maxHeight - 1]], dtype = "float32")

	# compute the perspective transform matrix and then apply it
	M = cv2.getPerspectiveTransform(rect, dst)
	warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

	# return the warped image
	return warped

def get_new(old):
    new = np.ones(old.shape, np.uint8)
    cv2.bitwise_not(new,new)
    return new

def getRectangle(gray, orig, ratio):
	gray = cv2.GaussianBlur(gray, (5, 5), 0)
	# gray = cv2.equalizeHist(gray)

	# this is to recognize white on white
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (MORPH,MORPH))
	gray = cv2.dilate(gray, kernel)

	# Dyanmically set threshold
	# https://stackoverflow.com/questions/4292249/automatic-calculation-of-low-and-high-thresholds-for-the-canny-operation-in-open
	threshold, _ = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
	edged = cv2.Canny(gray, threshold * 0.9, threshold, 5)
	edges = edged

	# show the original image and the edge detected image
	# print("STEP 1: Edge Detection")
	# cv2.imshow("Image", image)
	# cv2.imshow("Gray", gray)
	# cv2.imshow("Edged", edged)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()

	lines = cv2.HoughLinesP(edged, 1,  3.14/180, HOUGH)
	for line in lines[0]:
		cv2.line(edges, (line[0], line[1]), (line[2], line[3]), (255,0,0), 2, 8)

	# find the contours in the edged image, keeping only the
	# largest ones, and initialize the screen contour
	contoursImage, contours, hierarchy = cv2.findContours(edges.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	contours = sorted(contours, key = cv2.contourArea, reverse = True)[:100]
	cnts = contours

	lines = cv2.HoughLines(contoursImage, 1, math.pi/180.0, 50, np.array([]), 0, 0)[:10]
	if lines is None:
		return None

	a,b,c = lines.shape
	thetaThreshold = 3.0 / (2 * math.pi)
	positionThreshold = 50.0

	extendedPeaks = []
	for combination in list(itertools.combinations(range(a), r=2)):
		i = combination[0]
		j = combination[1]
		line1 = lines[i][0]
		line2 = lines[j][0]
		dPosition = abs(line1[0] - line2[0])
		dTheta = abs(line1[1] - line2[1])

		if(dTheta < thetaThreshold and dPosition > positionThreshold):
			position = (line1[0] + line2[0]) / 2
			theta = (line1[1] + line2[1]) / 2
			extendedPeaks.append(((position, theta), (dPosition, dTheta), (line1, line2)))

	extendedThetaThreshold = 3.0 / (2 * math.pi)

	rectangles = []
	for combination in list(itertools.combinations(extendedPeaks, r=2)):
		extendedPeak1 = combination[0] 
		extendedPeak2 = combination[1]
		dTheta = abs(abs(extendedPeak1[0][1] - extendedPeak2[0][1]) - (math.pi / 2))

		if(dTheta < extendedThetaThreshold):
			rectangles.append((extendedPeak1, extendedPeak2, dTheta))

	angularErrorWeight = 0.5
	distanceErrorWeight = 0.5
	bestRectangle = None
	bestRectangleError = float("inf")
	for rectangle in rectangles:
		error = angularErrorWeight * (rectangle[0][1][1] ** 2 + rectangle[1][1][1] ** 2 + rectangle[2] ** 2) + distanceErrorWeight * (rectangle[0][1][0] ** 2 + rectangle[1][1][0] ** 2)
		if error < bestRectangleError:
			bestRectangle = rectangle
			bestRectangleError = error

	if bestRectangle is None:
		return None

	bestRectangleLines = list([bestRectangle[0][2][0], bestRectangle[0][2][1], bestRectangle[1][2][0], bestRectangle[1][2][1]])
	# for i in bestRectangleLines:
	# 	rho = i[0]
	# 	theta = i[1]
	# 	a = math.cos(theta)
	# 	b = math.sin(theta)
	# 	x0, y0 = a*rho, b*rho

	# 	pt1 = ( int(x0+1000*(-b)), int(y0+1000*(a)) )
	# 	pt2 = ( int(x0-1000*(-b)), int(y0-1000*(a)) )
	# 	cv2.line(gray, pt1, pt2, (0, 0, 255), 1, cv2.LINE_AA)

	# print(bestRectangleLines)

	bestRectanglePoints = []
	for combination in list(((bestRectangleLines[0], bestRectangleLines[2]), (bestRectangleLines[0], bestRectangleLines[3]), (bestRectangleLines[1], bestRectangleLines[2]), (bestRectangleLines[1], bestRectangleLines[3]))):
		rho0 = combination[0][0]
		rho1 = combination[1][0]

		# Minimum value so we don't error out
		theta0 = max(combination[0][1], 0.0000001)
		theta1 = max(combination[1][1], 0.0000001)

		# https://web.archive.org/web/20130617222808/http://www.aishack.in/2010/03/converting-lines-from-normal-to-slope-intercept-form/
		x0 = a * rho0
		y0 = b * rho0

		x1 = a * rho1
		y1 = b * rho1
		
		b0 = rho0 / math.sin(theta0)
		m0 = -math.cos(theta0) / math.sin(theta0)
		y0 = m0 * x0 + b0

		b1 = rho1 / math.sin(theta1)
		m1 = -math.cos(theta1) / math.sin(theta1)
		y1 = m1 * x1 + b1
		
		x = (b1 - b0) / (m0 - m1)
		y = m1 * x + b1

		bestRectanglePoints.append([x, y])

		# pt1 = ( int(1000), int(m0*1000+(b0)) )
		# pt2 = ( int(-1000), int(m0*-1000+(b0)) )
		# cv2.line(gray, pt1, pt2, (0, 0, 255), 1, cv2.LINE_AA)

	# print(bestRectanglePoints)

	cv2.fillConvexPoly(gray, np.array([bestRectanglePoints], np.int), (255, 0, 0))

	# for i in range(a):
	# 	rho = lines[i][0][0]
	# 	theta = lines[i][0][1]
	# 	a = math.cos(theta)
	# 	b = math.sin(theta)
	# 	x0, y0 = a*rho, b*rho
	# 	pt1 = ( int(x0+1000*(-b)), int(y0+1000*(a)) )
	# 	pt2 = ( int(x0-1000*(-b)), int(y0-1000*(a)) )
	# 	print(pt1, pt2)
	# 	cv2.line(gray, pt1, pt2, (0, 0, 255), 1, cv2.LINE_AA)

	# print("STEP 3: Hough Lines")
	# cv2.imshow("Gray", gray)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()

	# print(bestRectanglePoints)

	# https://www.pyimagesearch.com/2014/09/01/build-kick-ass-mobile-document-scanner-just-5-minutes/
	# # apply the four point transform to obtain a top-down
	# # view of the original image
	warped = four_point_transform(orig, np.array(bestRectanglePoints, np.int).reshape(4, 2) * ratio)

	# # convert the warped image to grayscale, then threshold it
	# # to give it that 'black and white' paper effect
	# warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
	# T = threshold_local(warped, 11, offset = 10	, method = "gaussian")
	# warped = (warped > T).astype("uint8") * 255

	# # show the original and scanned images
	# print("STEP 3: Apply perspective transform")
	# cv2.imshow("Original", imutils.resize(orig, height = 650))
	# cv2.imshow("Scanned", imutils.resize(warped, height = 650))
	# cv2.waitKey(0)

	cv2.imwrite(args["output"], warped)

	return True

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True,
	help = "Path to the image to be scanned")
ap.add_argument("-o", "--output", required = True,
	help = "Path to save the output image")
args = vars(ap.parse_args())

# these constants are carefully picked
MORPH = 9
CANNY = 84
HOUGH = 25

# load the image and compute the ratio of the old height
# to the new height, clone it, and resize it
image = cv2.imread(args["image"])
ratio = image.shape[0] / 500.0
orig = image.copy()
image = imutils.resize(image, height = 500)

# convert the image to grayscale, blur it, and find edges in the image
# https://stackoverflow.com/questions/29156091/opencv-edge-border-detection-based-on-color
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
h,s,v = cv2.split(hsv)
gray = v

rectangle = getRectangle(s, orig, ratio)
if rectangle is None:
	rectangle = getRectangle(v, orig, ratio)

print(rectangle)