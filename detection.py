import cv2
import numpy as np

cap = cv2.VideoCapture(0)

def nothing(x):
	pass

#Prelim paper results
#Low[75, 0, 36]
#High[176, 136, 101]
#Hue varies dramatically with lighting
#Tends have a super low sat and value, 
#goes up with light reflection on surface

#Block
#low[45, 215, 0]
#high[85, 255, 166]


# flag top middle, flag center middle, flag bottom middle, left pole middle, right pole middle (in m)
# array 
tracking_points = []

cv2.namedWindow("Trackbars")
cv2.createTrackbar("L - H", "Trackbars", 45, 179, nothing)
cv2.createTrackbar("L - S", "Trackbars", 215, 255, nothing)
cv2.createTrackbar("L - V", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("U - H", "Trackbars", 85, 179, nothing)
cv2.createTrackbar("U - S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U - V", "Trackbars", 166, 255, nothing)

_, frame = cap.read()
print("width: " + str(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
print("height: " + str(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
white_img = np.zeros([cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, 3])
white_img[:,:] = (255, 255, 255)

cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
cv2.resizeWindow('frame', 1920, 1080)

while True:
	_, frame = cap.read()


	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	l_h = cv2.getTrackbarPos("L - H", "Trackbars")
	l_s = cv2.getTrackbarPos("L - S", "Trackbars")
	l_v = cv2.getTrackbarPos("L - V", "Trackbars")
	u_h = cv2.getTrackbarPos("U - H", "Trackbars")
	u_s = cv2.getTrackbarPos("U - S", "Trackbars")
	u_v = cv2.getTrackbarPos("U - V", "Trackbars")

	lower_filter = np.array([l_h, l_s, l_v])
	upper_filter = np.array([u_h, u_s, u_v])

	mask = cv2.inRange(hsv, lower_filter, upper_filter)
	res = cv2.bitwise_and(frame, frame, mask = mask)

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
		cv2.drawContours(frame, [approx], -1, (0, 255, 0), 3)
		#this line's gross sorry
		extrema = [tuple(cnt[cnt[:,:,0].argmin()][0]), tuple(cnt[cnt[:,:,0].argmax()][0]), tuple(cnt[cnt[:,:,1].argmin()][0]), tuple(cnt[cnt[:,:,1].argmax()][0])]
		for i in extrema:
			cv2.circle(frame, i, 5, 255, -1)
	#frame = cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)
	#thr = cv2.drawContours(thr, contours, -1, (0, 255, 0) , 3)

	'''
	for i in corners:
		x, y = i.ravel()
		cv2.circle(frame,(x,y), 3, 255, -1)
	'''

	


	cv2.imshow('frame', frame)
	cv2.imshow('mask', mask)
	cv2.imshow('blur', blur)
	cv2.imshow('thr', thr)
	cv2.imshow('edge', edges)


	k = cv2.waitKey(1) & 0xFF
	if k == 27:
		break

cap.release()
cv2.destroyAllWindows()