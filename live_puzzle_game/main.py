import cv2
import random
from hand_tracking import HandTracker

detector = HandTracker()

# ---------------------------
# STEP 1 : CAPTURE PUZZLE IMAGE
# ---------------------------

cap = cv2.VideoCapture(0)

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

    # press S to capture image
    if key == ord('s'):
        puzzle_image = img.copy()
        print("Image Captured!")
        break

    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()


# ---------------------------
# TILE CLASS
# ---------------------------

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
        return self.x < px < self.x + self.w and self.y < py < self.y + self.h


# ---------------------------
# STEP 2 : CREATE PUZZLE
# ---------------------------

rows = 3
cols = 3

h, w, _ = puzzle_image.shape

tile_h = h // rows
tile_w = w // cols


# store grid positions
grid_positions = []

for r in range(rows):
    for c in range(cols):

        x = c * tile_w
        y = r * tile_h

        grid_positions.append((x, y))


# create tile objects
tile_objects = []

for r in range(rows):
    for c in range(cols):

        tile = puzzle_image[
            r * tile_h:(r + 1) * tile_h,
            c * tile_w:(c + 1) * tile_w
        ]

        x = c * tile_w
        y = r * tile_h

        tile_objects.append(Tile(tile, x, y, tile_w, tile_h))


# shuffle tiles
random.shuffle(tile_objects)
for i, tile in enumerate(tile_objects):
    tile.x, tile.y = grid_positions[i]


# ---------------------------
# STEP 3 : INTERACTION LOOP
# ---------------------------

cap = cv2.VideoCapture(0)

selected_tile = None

while True:

    success, img = cap.read()
    img = cv2.flip(img, 1)

    img = detector.find_hands(img)

    landmark_list = detector.find_position(img)

    if landmark_list:

        x, y = landmark_list[8][1], landmark_list[8][2]

        cv2.circle(img, (x, y), 15, (255, 0, 255), cv2.FILLED)

        if selected_tile is None:

            for tile in tile_objects:

                if tile.is_over(x, y):
                    selected_tile = tile
                    break

        if selected_tile is not None:

            selected_tile.x = max(0, min(w - selected_tile.w, x - selected_tile.w // 2))
            selected_tile.y = max(0, min(h - selected_tile.h, y - selected_tile.h // 2))

    else:

        if selected_tile:

            # snap to nearest grid
            min_dist = float("inf")
            nearest = None

            for gx, gy in grid_positions:

                dist = (selected_tile.x - gx)**2 + (selected_tile.y - gy)**2

                if dist < min_dist:
                    min_dist = dist
                    nearest = (gx, gy)

            selected_tile.x, selected_tile.y = nearest
            selected_tile = None


    # draw puzzle
    puzzle = img.copy()

    for tile in tile_objects:
        tile.draw(puzzle)

    cv2.imshow("Puzzle", puzzle)
    cv2.imshow("Camera", img)

    key = cv2.waitKey(1)

    if key == 27:
        break


cap.release()
cv2.destroyAllWindows()