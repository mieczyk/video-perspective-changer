import cv2
import numpy as np

class Frame:
    def __init__(self, cv_image):
        self.cv_image = cv_image
        self.height, self.width = self.cv_image.shape[:2]
      
    def focus_on_area(self, area_coordinates):
        '''
        Changes the frame's perspective using OpenCV's warpPerspective() method.

        :param area_coordinates: Four points indicating the area of focus. 
            The method assumes that points are passed in the following order: 
            top-left, top-right, bottom-right, bottom-left.
        '''
        dst_coordinates = np.float32([
            [0, 0],
            [self.width, 0],
            [self.width, self.height],
            [0, self.height]
        ])

        self.cv_image = cv2.warpPerspective(
            self.cv_image,
            cv2.getPerspectiveTransform(
                area_coordinates.astype(np.float32),
                dst_coordinates
            ),
            (self.width, self.height)
        )

    def draw_polygon(self, vertices, color=(0,255,0), thickness=5):
        cv2.polylines(self.cv_image, [vertices.reshape((-1,1,2))], True, color, thickness)

    def draw_point(self, center, radius=5, color=(0,0,255)):
        cv2.circle(self.cv_image, tuple(center), radius, color, cv2.FILLED)

    def copy(self):
        return Frame(self.cv_image.copy())

class VideoStream:
    def __init__(self, source):
        self._cap = cv2.VideoCapture(source)
        
        self.width = int(self._cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self._cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    def next_frame(self):
        success, cv_image = self._cap.read()

        frame = None

        if success:
            frame = Frame(cv_image)

        return frame

    def close(self):
        self._cap.release()

class OutputVideoFile:
    def __init__(self, path, width, height, fps=25):
        codec = cv2.VideoWriter_fourcc(*'XVID')
        self._writer = cv2.VideoWriter(path, codec, fps, (width, height))
        self._width = width
        self._height = height

    def add_frame(self, frame):
        resized_cv_img = cv2.resize(frame.cv_image, (self._width, self._height), cv2.INTER_AREA)
        self._writer.write(resized_cv_img)

    def save(self):
        self._writer.release()

