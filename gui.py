import cv2
import numpy as np

class Window:
    def __init__(self, name):
        self._name = name
        self._selecting = False

        self.selection = None

    def show(self, width, height):
        cv2.namedWindow(self._name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self._name, width, height)
        cv2.setMouseCallback(self._name, self._mouse_callback)
    
    def _mouse_callback(self, event, x, y, flags, userdata):
        if event == cv2.EVENT_LBUTTONDOWN:
            self._selecting = True
            self.selection = Selection([x,y])
        elif event == cv2.EVENT_MOUSEMOVE and self._selecting:
            self.selection.update([x,y])
        elif event == cv2.EVENT_LBUTTONUP:
            self.selection.update([x,y])
            self._selecting = False

    def dispose(self):
        cv2.destroyWindow(self._name)

    def display_frame(self, frame):
        if self.selection is not None:
            frame = frame.copy()
            frame.draw_polygon(self.selection.vertices)
        
        cv2.imshow(self._name, frame.cv_image)

class Selection:
    def __init__(self, start_point):
        self.vertices = np.full((4,2), start_point, dtype=int)
    
    def update(self, end_point):
        self.vertices[2] = end_point
        start_point = self.vertices[0] 

        if start_point[0] < end_point[0] and start_point[1] < end_point[1]:
            self.vertices[1] = [end_point[0], start_point[1]]    
            self.vertices[3] = [start_point[0], end_point[1]]
        elif start_point[0] > end_point[0] and start_point[1] < end_point[1]:
            self.vertices[1] = [start_point[0], end_point[1]]
            self.vertices[3] = [end_point[0], start_point[1]]
        elif start_point[0] > end_point[0] and start_point[1] > end_point[1]:
            self.vertices[1] = [end_point[0], start_point[1]]
            self.vertices[3] = [start_point[0], end_point[1]]
        else:
            self.vertices[1] = [start_point[0], end_point[1]]
            self.vertices[3] = [end_point[0], start_point[1]] 

def wait_for_key(miliseconds):
    # '& 0xFF' because we're interested in the last 8 bits only.
    return cv2.waitKey(miliseconds) & 0xFF
