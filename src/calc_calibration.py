import cv2
import numpy as np

img = cv2.imread('camera_cal.png')

lower_filter = np.array([57, 73, 65])
upper_filter = np.array([88, 255, 255])

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


mask = cv2.inRange(hsv, lower_filter, upper_filter)
res = cv2.bitwise_and(img, img, mask = mask)

#try other blurs


blur = cv2.GaussianBlur(res, (5, 5), 0)

kernel = np.ones((5, 5), np.uint8)
opening = cv2.morphologyEx(blur, cv2.MORPH_CLOSE, kernel)

#blur = cv2.medianBlur(opening, 5)
#convert to grayscale for thresholding
bgr = cv2.cvtColor(blur, cv2.COLOR_HSV2BGR)
gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)

#ret, thr = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
#thr = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

thr = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
ret, thr = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)
edges = cv2.Canny(blur, 100, 200)

contours, hierarchy = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

#find largest contour
if len(contours) > 0:
	cnt = contours[0]
	max_size = cv2.contourArea(cnt)

	for cont in contours:
		if cv2.contourArea(cont) > max_size:
			cnt = cont
			max_size = cv2.contourArea(cont)
	#cv2.drawContours(frame, cnt, -1, (0, 255, 0), 3)
	perimeter = cv2.arcLength(cnt,True)
	epsilon = 0.04*perimeter
	approx = cv2.approxPolyDP(cnt,epsilon,True)
	print(approx)
	dx = min(approx, key=lambda x:abs(x-approx[0]))[0]
	print(dx)

	print()
	cv2.drawContours(img, [approx], -1, (0, 255, 0), 3)
	#this line's gross sorry
	#extrema = [tuple(cnt[cnt[:,:,0].argmin()][0]), tuple(cnt[cnt[:,:,0].argmax()][0]), tuple(cnt[cnt[:,:,1].argmin()][0]), tuple(cnt[cnt[:,:,1].argmax()][0])]
	for i in extrema:
		print(i)
		cv2.circle(img, i, 5, 255, -1)
	#leftmost = tuple(cnt[cnt[:,:,0].argmin()][0])
	#rightmost = tuple(cnt[cnt[:,:,0].argmax()][0])
	#topmost = tuple(cnt[cnt[:,:,1].argmin()][0])
	#bottommost = tuple(cnt[cnt[:,:,1].argmax()][0])



cv2.imshow('img', img)


cv2.waitKey(0)

cv2.destroyAllWindows()