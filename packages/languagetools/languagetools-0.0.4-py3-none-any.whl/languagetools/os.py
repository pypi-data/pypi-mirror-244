import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import tempfile
import pytesseract
import pyautogui
import cv2
import numpy as np
import pytesseract
from pytesseract import Output
from PIL import Image
import time

def screenshot():
    temp_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    os.system(f"screencapture -x {temp_file.name}")
    
    # Open the image file with PIL
    img = Image.open(temp_file.name)

    # Delete the temporary file
    os.remove(temp_file.name)

    return img

def find_text_in_image(img, text):
    # Convert the image to grayscale
    # Convert the image to grayscale
    gray = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)

    # Use pytesseract to get the data from the image
    d = pytesseract.image_to_data(gray, output_type=Output.DICT)

    # Assert that the size of the image is the same
    assert img.size == gray.shape[::-1]

    # Initialize an empty list to store the centers of the bounding boxes
    centers = []

    # Get the number of detected boxes
    n_boxes = len(d['level'])

    # Create a copy of the image to draw on
    img_draw = np.array(img.copy())

    # Loop through each box
    for i in range(n_boxes):
        # Print the text of the box
        print(d['text'][i])
        # If the text in the box matches the given text
        if text.lower() in d['text'][i].lower():
            # Calculate the center of the bounding box
            center = (d['left'][i] + d['width'][i] / 2, d['top'][i] + d['height'][i] / 2)

            # Half both coordinates
            center = (center[0] / 2, center[1] / 2)
                        
            # Add the center to the list
            centers.append(center)

            # Draw the bounding box on the image
            cv2.rectangle(img_draw, (d['left'][i], d['top'][i]), (d['left'][i] + d['width'][i], d['top'][i] + d['height'][i]), (0, 0, 255), 10)

    if not centers:
        word_centers = []
        for word in text.split():
            for i in range(n_boxes):
                if word.lower() in d['text'][i].lower():
                    center = (d['left'][i] + d['width'][i] / 2, d['top'][i] + d['height'][i] / 2)
                    center = (center[0] / 2, center[1] / 2)
                    word_centers.append(center)

        for center1 in word_centers:
            for center2 in word_centers:
                if center1 != center2 and ((center1[0]-center2[0])**2 + (center1[1]-center2[1])**2)**0.5 <= 400:
                    centers.append(((center1[0]+center2[0])/2, (center1[1]+center2[1])/2))
                    break
            if centers:
                break

    # Display the image with bounding boxes
    # plt.imshow(img_draw)
    # plt.show()

    # Return the list of centers
    return centers

def click(text):
    # Take a screenshot
    img = screenshot()

    # Find the text in the screenshot
    centers = find_text_in_image(img, text)

    print(centers)

    # If the text was found
    if centers:
        # Get the first center
        center = centers[0]

        # Slowly move the mouse from its current position to the click position
        pyautogui.moveTo(center[0], center[1], duration=0.5)
        pyautogui.click(center[0], center[1])

    else:
        print("Your text was not found on the screen. Please try again.")

    time.sleep(0.5)

    img = screenshot()
    img.show()
    return img

def keyboard(text):

    start_delay=0.07
    end_delay=0.01

    # Calculate the delay decrement
    delay_decrement = (start_delay - end_delay) / (len(text) / 2)

    # Initialize the current delay
    current_delay = start_delay

    # Type each character
    for i, char in enumerate(text):
        # Type the character
        pyautogui.typewrite(char, interval=current_delay)

        # Update the delay
        if i < len(text) / 2:
            current_delay -= delay_decrement
        else:
            current_delay += delay_decrement
