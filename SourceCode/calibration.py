import cv2


cap = cv2.VideoCapture(0)

while True:
	_, frame = cap.read()

	cv2.imshow('frame', frame)

	k = cv2.waitKey(1) & 0xFF
	if k == 27:
		break

_, frame = cap.read()
cv2.imwrite('camera_cal2.png', frame)
cap.release()
cv2.destroyAllWindows()