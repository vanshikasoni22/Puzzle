import cv2
import mediapipe as mp


class HandTracker:

    def __init__(self):

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils


    def find_hands(self, img):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:

            for handLms in self.results.multi_hand_landmarks:

                self.mpDraw.draw_landmarks(
                    img,
                    handLms,
                    self.mpHands.HAND_CONNECTIONS
                )

        return img


    def find_position(self, img):

        landmark_list = []

        if self.results.multi_hand_landmarks:

            hand = self.results.multi_hand_landmarks[0]

            for id, lm in enumerate(hand.landmark):

                h, w, c = img.shape

                cx = int(lm.x * w)
                cy = int(lm.y * h)

                landmark_list.append((id, cx, cy))

        return landmark_list