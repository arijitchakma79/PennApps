import subprocess
import cv2
import numpy as np

class Camera:
    def __init__(self):
        self.__commandArgs = [
            "libcamera-still",
            "-n",  # No preview
            "-o", "-",  # Output to stdout
            "-t", "1",  # Minimum capture time (in milliseconds)
            "--width", "640",  # Reduced width
            "--height", "480",  # Reduced height
            "--immediate",  # Capture immediately
            "--nopreview",  # Disable preview
            "--encoding", "jpg",  # Use JPEG encoding for faster processing
            "--quality", "80"  # Slightly reduce quality for speed
        ]

    def capture_frame(self):
        try:
            # Capture an image using libcamera-still with optimized settings
            result = subprocess.run(self.__commandArgs, capture_output=True, check=True)

            # Convert the captured image data to a numpy array
            nparr = np.frombuffer(result.stdout, np.uint8)
            # Decode the image
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            if frame is None:
                print("Error: Failed to decode captured image.")
                return None

            # Flip the frame vertically
            frame = cv2.flip(frame, 0)

            return frame
        except subprocess.CalledProcessError as e:
            print(f"Error capturing image: {e.stderr.decode()}")
            return None