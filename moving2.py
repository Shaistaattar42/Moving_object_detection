import cv2
import time
import imutils
import tkinter as tk
from tkinter import Label, Frame
from PIL import Image, ImageTk

# Initialize the stop flag
stop_video = False

# Function to start the video stream and motion detection
def start_video_stream():
    global stop_video, firstFrame

    cam = cv2.VideoCapture(0)
    time.sleep(1)
    firstFrame = None
    area = 500

    while not stop_video:
        _, img = cam.read()
        text = "normal"
        img = imutils.resize(img, width=500)

        grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gaussianImg = cv2.GaussianBlur(grayImg, (21, 21), 0)

        if firstFrame is None:
            firstFrame = gaussianImg
            continue

        imgDiff = cv2.absdiff(firstFrame, gaussianImg)
        threshImg = cv2.threshold(imgDiff, 25, 255, cv2.THRESH_BINARY)[1]
        threshImg = cv2.dilate(threshImg, None, iterations=2)

        cnts = cv2.findContours(threshImg.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        for c in cnts:
            if cv2.contourArea(c) < area:
                continue
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            text = "Moving Object Detected"

        # Display text on frame
        cv2.putText(img, text, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # Convert image for Tkinter
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(imgRGB)
        img_tk = ImageTk.PhotoImage(image=img_pil)

        # Update the image panel
        panel.img_tk = img_tk
        panel.config(image=img_tk)
        panel.update()

        # Check for 'q' key press to exit
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            stop_video_stream()

    cam.release()

def stop_video_stream():
    global stop_video
    stop_video = True

# Set up the GUI
root = tk.Tk()
root.title("Motion Detector")

root.geometry("1000x600")

# Create a label in the root window to hold the video frame
panel = Label(root)
panel.pack(padx=10, pady=10)

# Create a frame to hold the buttons and center them
button_frame = Frame(root)
button_frame.pack(pady=10)

# Style the buttons
button_style = {
    'width': 20,  # Increase width
    'height': 2,  # Increase height
    'bg': 'black',  # Button background color
    'fg': 'white',  # Button text color
    'font': ('Helvetica', 14),  # Font size
    'relief': 'raised',  # Button border style
    'bd': 2  # Button border width
}

# Add buttons to start and stop the video stream
start_button = tk.Button(button_frame, text="Start", command=start_video_stream, **button_style)
start_button.pack(side="left", padx=20)

stop_button = tk.Button(button_frame, text="Stop", command=stop_video_stream, **button_style)
stop_button.pack(side="right", padx=20)

# Run the Tkinter main loop
root.mainloop()
