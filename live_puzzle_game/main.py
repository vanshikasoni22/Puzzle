import cv2

# Start webcam
cap = cv2.VideoCapture(0)

while True:

    # Capture frame from camera
    success, img = cap.read()

    # If camera fails, stop program
    if not success:
        print("Failed to capture image")
        break

    # Display the frame
    cv2.imshow("Live Camera", img)

    # Press ESC to exit
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Release camera and close windows
cap.release()
cv2.destroyAllWindows()