import cv2

class Window:
    def __init__(self, name, initial_size):
        self._name = name

    def show(self, width, height):
        cv2.namedWindow(self._name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self._name, width, height)
        cv2.setMouseCallback(self._name, self._mouse_callback)
    
    def _mouse_callback(self, event, x, y, flags, userdata):
        if event == cv2.EVENT_LBUTTONDOWN:
            print('clicked')

    def dispose(self):
        cv2.destroyWindow(self._name)

    def display_frame(self, frame):
        cv2.imshow(self._name, frame.cv_image)

def wait_for_key(miliseconds):
    # '& 0xFF' because we're interested in the last 8 bits only.
    return cv2.waitKey(miliseconds) & 0xFF
