import cv2
from hand_tracking import HandTracker

cap = cv2.VideoCapture(0)

detector = HandTracker()

puzzle_image = None

while True:

    success, img = cap.read()

    img = detector.find_hands(img)

    landmark_list = detector.find_position(img)

    if landmark_list:

        x, y = landmark_list[8][1], landmark_list[8][2]
        cv2.circle(img, (x, y), 15, (255, 0, 255), cv2.FILLED)

    cv2.imshow("Camera", img)

    key = cv2.waitKey(1)

    # press C to capture puzzle image
    if key == ord('c'):
        puzzle_image = img.copy()
        break

    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()

rows = 3
cols = 3

h, w, _ = puzzle_image.shape

tile_h = h // rows
tile_w = w // cols

tiles = []
# spliting image into tiles
for r in range(rows):
    for c in range(cols):

        tile = puzzle_image[
            r * tile_h:(r + 1) * tile_h,
            c * tile_w:(c + 1) * tile_w
        ]

        tiles.append(tile)


import random

random.shuffle(tiles)


# displaying puzzle
puzzle = puzzle_image.copy()

index = 0

for r in range(rows):
    for c in range(cols):

        puzzle[
            r * tile_h:(r + 1) * tile_h,
            c * tile_w:(c + 1) * tile_w
        ] = tiles[index]

        index += 1

cv2.imshow("Puzzle", puzzle)
cv2.waitKey(0)