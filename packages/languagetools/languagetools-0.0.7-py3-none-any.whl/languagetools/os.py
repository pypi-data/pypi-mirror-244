import os
import tempfile
import pytesseract
import pyautogui
import cv2
import numpy as np
import pytesseract
from pytesseract import Output
import time
from PIL import Image

# DISABLED as it doesn't work. I don't know why.
# import matplotlib
# matplotlib.use('agg') # all images will be just rasterized and sent up, not interactive

import matplotlib.pyplot as plt

def screenshot(show=True):
    temp_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    os.system(f"screencapture -x {temp_file.name}")
    
    # Open the image file with PIL
    img = Image.open(temp_file.name)

    # Delete the temporary file
    os.remove(temp_file.name)

    if show:
        # Show the image using matplotlib
        plt.imshow(np.array(img))
        plt.show()

    return img

def find_text_in_image(img, text):
    # Convert the image to grayscale
    gray = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)

    # Use pytesseract to get the data from the image
    d = pytesseract.image_to_data(gray, output_type=Output.DICT)

    # Initialize an empty list to store the centers of the bounding boxes
    centers = []

    # Get the number of detected boxes
    n_boxes = len(d['level'])

    # Create a copy of the image to draw on
    img_draw = np.array(img.copy())

    id = 0

    # Loop through each box
    for i in range(n_boxes):
        # Print the text of the box
        # If the text in the box matches the given text
        if text.lower() in d['text'][i].lower():
            # Find the start index of the matching text in the box
            start_index = d['text'][i].lower().find(text.lower())
            # Calculate the percentage of the box width that the start of the matching text represents
            start_percentage = start_index / len(d['text'][i])
            # Move the left edge of the box to the right by this percentage of the box width
            d['left'][i] = d['left'][i] + int(d['width'][i] * start_percentage)

            # Calculate the width of the matching text relative to the entire text in the box
            text_width_percentage = len(text) / len(d['text'][i])
            # Adjust the width of the box to match the width of the matching text
            d['width'][i] = int(d['width'][i] * text_width_percentage)

            # Calculate the center of the bounding box
            center = (d['left'][i] + d['width'][i] / 2, d['top'][i] + d['height'][i] / 2)

            # Half both coordinates
            center = (center[0] / 2, center[1] / 2)
                        
            # Add the center to the list
            centers.append(center)

            # Draw the bounding box on the image in red and make it slightly larger
            larger = 10
            cv2.rectangle(img_draw, (d['left'][i] - larger, d['top'][i] - larger), (d['left'][i] + d['width'][i] + larger, d['top'][i] + d['height'][i] + larger), (0, 0, 255), 7)

            # Create a small black square background for the ID
            cv2.rectangle(img_draw, (d['left'][i] + d['width'][i] // 2 - larger*2, d['top'][i] + d['height'][i] // 2 - larger*2), (d['left'][i] + d['width'][i] // 2 + larger*2, d['top'][i] + d['height'][i] // 2 + larger*2), (0, 0, 0), -1)

            # Put the ID in the center of the bounding box in red
            cv2.putText(img_draw, str(id), (d['left'][i] + d['width'][i] // 2 - larger, d['top'][i] + d['height'][i] // 2 + larger), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # Increment id
            id += 1

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

    img_draw_rgb = cv2.cvtColor(img_draw, cv2.COLOR_BGR2RGB)
    img_show = Image.fromarray(img_draw_rgb)
    
    # Debug by showing bounding boxes:
    # img_show.show()

    return centers, img_show


def click(text, show=True, index=None):
    # Take a screenshot
    img = screenshot(show=False)

    # Find the text in the screenshot
    centers, bounding_box_image = find_text_in_image(img, text)

    # If the text was found
    if centers:

        # This could be refactored to be more readable
        if len(centers) > 1:
            if index == None:
                print("This text was found multiple times on screen. Please try 'click()' again, but pass in an `index` int to identify which one you want to click. The indices have been drawn on the attached image.")
                # Show the image using matplotlib
                plt.imshow(np.array(bounding_box_image))
                plt.show()
                return
            else:
                center = centers[index]
        else:
            center = centers[0]

        # Slowly move the mouse from its current position to the click position
        pyautogui.moveTo(center[0], center[1], duration=0.5)
        pyautogui.click(center[0], center[1])

    else:
        print("Your text was not found on the screen. Please try again.")

    time.sleep(0.5)

    img = screenshot(show=show)
    return img

def keyboard(text, show=True, modifiers=None):

    start_delay=0.07
    end_delay=0.01

    # Calculate the delay decrement
    delay_decrement = (start_delay - end_delay) / (len(text) / 2)

    # Initialize the current delay
    current_delay = start_delay

    # Type each character
    for i, char in enumerate(text):
        # Type the character
        if modifiers:
            pyautogui.hotkey(*modifiers, char, interval=current_delay)
        else:
            pyautogui.typewrite(char, interval=current_delay)

        # Update the delay
        if i < len(text) / 2:
            current_delay -= delay_decrement
        else:
            current_delay += delay_decrement

    time.sleep(0.5)

    img = screenshot(show=show)
    return img
