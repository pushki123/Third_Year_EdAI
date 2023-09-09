import cv2
import easyocr
import re
import nltk
from nltk.corpus import words
nltk.download('words')


valid_words = set(words.words())

def predict_word(input_letters):
    # Find a word from the valid English words that starts with the input letters
    matching_words = [word for word in valid_words if word.startswith(input_letters)]
    if matching_words:
        return matching_words[0]
    else:
        return "Word not found"

def camera_ocr_and_save():
    # Create an OCR reader
    reader = easyocr.Reader(['en'])  # 'en' for English, you can specify other languages too

    # Create a VideoCapture object to access the camera (usually 0 for the default camera)
    cap = cv2.VideoCapture(0)

    # Set the confidence threshold for meaningful words (adjust as needed)
    confidence_threshold = 0.5

    sentence = ""  # Initialize an empty sentence

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

            # Create a text file to save recognized text and sentences
            with open("recognized_text.txt", "w") as text_file:
                # Extract and save recognized text and sentences
                for result in results:
                    text, confidence = result[1], result[2]
                    if confidence >= confidence_threshold and re.match(r'^[A-Za-z\s]+$', text):
                        text_file.write(text + '\n')
                        print("Recognized:", text)
                        sentence += text  # Add recognized word to the sentence
                    else:
                        # Attempt to predict a word based on the recognized letters
                        input_letters = ''.join([c for c in text if c.isalpha()])
                        if input_letters:
                            predicted_word = predict_word(input_letters.lower())
                            text_file.write(f"Predicted: {predicted_word}\n")
                            print(f"Predicted: {predicted_word}")

                if sentence.strip():  # Check if the sentence is not empty
                    text_file.write("Sentence: " + sentence.strip() + '\n')
                    print("Sentence:", sentence.strip())

                    # Write the sentence letter by letter
                    for letter in sentence:
                        text_file.write(letter + '\n')

                    sentence = ""  # Reset the sentence

        # Break the loop if the 'q' key is pressed
        elif key == ord('q'):
            break

    # Release the camera and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    camera_ocr_and_save()
