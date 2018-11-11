import cv2
import numpy as np

class RoombaCV:

	def __init__(self):
		self.window_name = 'frame'
		self.cap = cv2.VideoCapture(0)
		self.lower_filter = np.array([57, 73, 65])
		self.upper_filter = np.array([88, 255, 255])
		cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
		cv2.resizeWindow(self.window_name, 1920, 1080)
		_, frame = self.cap.read()
		cv2.imshow(self.window_name, frame)

	def readFrame(self):
		_, frame = self.cap.read()
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


		mask = cv2.inRange(hsv, self.lower_filter, self.upper_filter)
		res = cv2.bitwise_and(frame, frame, mask = mask)

		blur = cv2.GaussianBlur(res, (5, 5), 0)

		kernel = np.ones((5, 5), np.uint8)
		opening = cv2.morphologyEx(blur, cv2.MORPH_CLOSE, kernel)

		#convert to grayscale for thresholding
		#bgr = cv2.cvtColor(blur, cv2.COLOR_HSV2BGR)
		#gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)

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
			perimeter = cv2.arcLength(cnt,True)
			epsilon = 0.04*perimeter
			M = cv2.moments(cnt)
			approx = cv2.approxPolyDP(cnt,epsilon,True)
			cv2.drawContours(frame, [approx], -1, (0, 255, 0), 3)
			#this line's gross sorry
			extrema = [tuple(cnt[cnt[:,:,0].argmin()][0]), tuple(cnt[cnt[:,:,0].argmax()][0]), tuple(cnt[cnt[:,:,1].argmin()][0]), tuple(cnt[cnt[:,:,1].argmax()][0])]
			for i in extrema:
				cv2.circle(frame, i, 5, 255, -1)
			cv2.imshow(self.window_name, frame)
			cv2.waitKey(1)
			try:
				if len(approx) == 4:
					#success
					center = (int(M['m10']/M['m00']), int(M['m01']/M['m00']))
					top = cnt[cnt[:,:,1].argmin()][0]
					bottom = cnt[cnt[:,:,1].argmax()][0]
					left = cnt[cnt[:,:,0].argmin()][0]
					right = cnt[cnt[:,:,0].argmax()][0]

					dy = bottom[1] - top[1]
					dy2 = abs(left[1] - right[1])

					height = int((dy + dy2) / 2)
					return True, center, height
			except:
				return False, None, None
		return False, None, None


rb = RoombaCV()
while True:
	rb.readFrame()