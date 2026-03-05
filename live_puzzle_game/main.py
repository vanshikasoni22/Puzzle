import cv2
from hand_tracking import HandTracker

cap = cv2.VideoCapture(0)

detector = HandTracker()

while True:

    success, img = cap.read()

    img = detector.find_hands(img)

    landmark_list = detector.find_position(img)

    if landmark_list:

        x, y = landmark_list[8][1], landmark_list[8][2]

        cv2.circle(img, (x, y), 15, (255, 0, 255), cv2.FILLED)

    cv2.imshow("Hand Tracking", img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()