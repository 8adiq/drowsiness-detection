from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal

import cv2
import numpy as np


class VideoThread(QThread):
    """Video thread class to handle opencv video window"""
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self, camera):
        super().__init__()
        self._run_flag = True
        self.camera = camera

    def run(self):
        #  capture from web cam
        cap = cv2.VideoCapture(self.camera)
        while self._run_flag:
            ret, cv_img = cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)
        # shut down capture system
        cap.release()

    def stop(self):
        """Sets up flag to false and wait for thread to finish"""
        self._run_flag = False
        self.wait()


class Detection(QtWidgets.QWidget):
    """Detect position of eyes"""

    def __init__(self, face_haarcascade_name, eyes_haarcascade_name, parent=None):
        super().__init__(parent)
        self.eye_classifier = cv2.CascadeClassifier(
            cv2.data.haarcascades + eyes_haarcascade_name)
        self.image = QtGui.QImage()
        self._red = (0, 0, 255)
        self._width = 2
        self._min_size = (30, 30)

    def detect_eye_face(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        eyes = self.eye_classifier.detectMultiScale(
            gray, scaleFactor=1.3, minNeighbors=4,
            flags=cv2.CASCADE_SCALE_IMAGE, minSize=self._min_size
        )

        return eyes

    def image_data_slot(self, image_data):
        eyes = self.detect_eye_face(image_data)

        for x, y, w, h in eyes:
            cv2.rectangle(image_data, (x, y), (x+w, y+h),
                          self._red, self._width)

        self.image = image_data

        return self.image
