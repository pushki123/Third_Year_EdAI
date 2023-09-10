import cv2
import easyocr

class CameraSnapshotProcessor:
    def __init__(self):
        # Initialize the camera
        self.camera = cv2.VideoCapture(0)

        # Check if the camera is opened successfully
        if not self.camera.isOpened():
            raise RuntimeError("Error: Could not open camera.")

        # Initialize the OCR reader
        self.reader = easyocr.Reader(['en'])  # Language selection

    def capture_and_process(self):
        while True:
            # Capture a frame from the camera
            ret, frame = self.camera.read()

            # Display the live camera feed
            cv2.imshow("Camera Feed", frame)

            # Press 'q' to capture a snapshot and concatenate words
            if cv2.waitKey(1) & 0xFF == ord('q'):
                # Save the captured frame as an image
                snapshot_path = 'snapshot.png'
                cv2.imwrite(snapshot_path, frame)

                # Perform OCR on the captured snapshot
                words, _ = self.read_words(snapshot_path)

                # Concatenate the words into a single line
                concatenated_text = " ".join(words)

                # Display the concatenated text
                print("Concatenated Text:", concatenated_text)

                # Save the text to a text file
                self.save_to_text_file(concatenated_text, 'output.txt')

            # Press 'Esc' to exit the camera feed
            if cv2.waitKey(1) & 0xFF == 27:
                break

        # Release the camera and close all windows
        self.camera.release()
        cv2.destroyAllWindows()

    def read_words(self, image_path):
        # Load the image
        image = cv2.imread(image_path)

        # Perform OCR on the image
        results = self.reader.readtext(image)

        # Extract words from OCR results
        words = [result[1] for result in results]

        return words, results

    def save_to_text_file(self, text, filename):
        with open(filename, 'w') as file:
            file.write(text)

if __name__ == "__main__":
    # Create an instance of the CameraSnapshotProcessor class
    processor = CameraSnapshotProcessor()

    # Capture snapshots, concatenate words, and save to a text file
    processor.capture_and_process()
