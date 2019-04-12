import cv2

class Frame:
    def __init__(self, cv_image):
        self.cv_image = cv_image
        self.height, self.width = self.cv_image.shape[:2]

class VideoStream:
    def __init__(self, source):
        self._cap = cv2.VideoCapture(source)
        
        self.width = self._cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self._cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def next_frame(self):
        success, cv_image = self._cap.read()

        frame = None

        if success:
            frame = Frame(cv_image)

        return frame

    def close(self):
        self._cap.release()
