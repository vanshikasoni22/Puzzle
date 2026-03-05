import cv2
import random
from hand_tracking import HandTracker

cap = cv2.VideoCapture(0)

detector = HandTracker()

puzzle_image = None

while True:

    success, img = cap.read()
    img = cv2.flip(img, 1)

    img = detector.find_hands(img)

    landmark_list = detector.find_position(img)

    if landmark_list:
        x, y = landmark_list[8][1], landmark_list[8][2]
        cv2.circle(img, (x, y), 15, (255, 0, 255), cv2.FILLED)

    cv2.imshow("Camera", img)

    key = cv2.waitKey(1)

    # press S to capture puzzle image
    if key == ord('s'):
        puzzle_image = img.copy()
        print("Image captured!")
        break

    if key == 27:
        break


cap.release()
cv2.destroyAllWindows()

class Tile:

    def __init__(self, img, x, y, w, h):
        self.img = img
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def draw(self, frame):
        frame[self.y:self.y+self.h, self.x:self.x+self.w] = self.img

    def is_over(self, px, py):
        if self.x < px < self.x + self.w and self.y < py < self.y + self.h:
            return True
        return False
# Puzzle creation

rows = 3
cols = 3

h, w, _ = puzzle_image.shape

tile_h = h // rows
tile_w = w // cols

tile_objects = []

# splitting image into tiles
for r in range(rows):
    for c in range(cols):

        tile = puzzle_image[
            r * tile_h:(r + 1) * tile_h,
            c * tile_w:(c + 1) * tile_w
        ]

        x = c * tile_w
        y = r * tile_h

        tile_objects.append(Tile(tile, x, y, tile_w, tile_h))


random.shuffle(tile_objects)

# displaying puzzle
puzzle = puzzle_image.copy()

for tile in tile_objects:
    tile.draw(puzzle)


cv2.imshow("Puzzle", puzzle)
cv2.waitKey(0)