import cv2
import easyocr

# Create an OCR reader
reader = easyocr.Reader(['en'])  # 'en' for English, you can specify other languages too

# Create a VideoCapture object to access the camera (usually 0 for the default camera)
cap = cv2.VideoCapture(0)

while True:
    # Capture a frame from the camera
    ret, frame = cap.read()

    # Display the frame
    cv2.imshow("Camera", frame)

    # Check for user input to take a snapshot (press 's' key)
    key = cv2.waitKey(1)
    if key == ord('s'):
        # Save the frame as an image
        cv2.imwrite("snapshot.png", frame)
        print("Snapshot saved as snapshot.png")

        # Perform OCR on the saved snapshot
        results = reader.readtext("snapshot.png")

        # Extract and print all the text found in the snapshot
        for result in results:
            text = result[1]
            print(text)

    # Break the loop if the 'q' key is pressed
    elif key == ord('q'):
        break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
