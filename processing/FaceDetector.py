import threading
import mediapipe as mp
import cv2

from deviceIO.camera import Camera

class FaceDetector:
    def __init__(self, callback=None):
        self.camera = Camera()
        self.callback = callback
        self.face_detected = False
        self.running = False
        self.thread = None
        
        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection(min_detection_confidence=0.5)

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._run)
            self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()

    def _run(self):
        while self.running:
            frame = self.camera.capture_frame()
            if frame is None:
                continue

            # Convert the image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            cv2.imwrite("frame.jpg", frame)

            # Process the image
            results = self.face_detection.process(image)
            
            # Check if a face was detected
            face_detected = results.detections is not None and len(results.detections) > 0

            # Update the status
            self.face_detected = face_detected

            # Call the callback if provided
            if self.callback:
                self.callback(face_detected)

    def is_face_detected(self):
        return self.face_detected