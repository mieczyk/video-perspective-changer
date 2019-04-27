import cv2
import numpy as np

class Window:
    def __init__(self, name):
        self._name = name
        self._selecting = False
        self._dragging = False

        self.selection = None

    def show(self, width, height):
        cv2.namedWindow(self._name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self._name, width, height)
        cv2.setMouseCallback(self._name, self._mouse_callback)
    
    def _mouse_callback(self, event, x, y, flags, userdata):
        if event == cv2.EVENT_LBUTTONDOWN:
            if self.selection is not None and self.selection.activate_vertex([x,y]):
                self._dragging = True
            else:
                self._selecting = True
                self.selection = Selection([x,y])
        elif event == cv2.EVENT_MOUSEMOVE and self.selection is not None: 
            if self._selecting:
                self.selection.update([x,y])
            elif self._dragging:
                self.selection.update_active_vertex([x,y])
        elif event == cv2.EVENT_LBUTTONUP and self.selection is not None:
            if self._selecting:
                self.selection.update([x,y])
                self._selecting = False
            elif self._dragging:
                self.selection.update_active_vertex([x,y])
                self.selection.deactivate_vertex()
                self._dragging = False
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.remove_selection()

    def dispose(self):
        cv2.destroyWindow(self._name)
        
    def remove_selection(self):
        self.selection = None
        self._selecting = False
        self._dragging = False

    def display_frame(self, frame):
        if self.selection is not None:
            frame = frame.copy()
            frame.draw_polygon(self.selection.vertices)
            for vertex in self.selection.vertices:
                frame.draw_point(vertex)
        
        cv2.imshow(self._name, frame.cv_image)

class Selection:
    def __init__(self, start_point):
        self._active_vertex_idx = -1

        self.vertices = np.full((4,2), start_point, dtype=int)
        self.top_left_vertex_idx = 0
    
    def update(self, end_point):
        self.vertices[2] = end_point
        start_point = self.vertices[0] 

        if start_point[0] < end_point[0] and start_point[1] < end_point[1]:
            self.vertices[1] = [end_point[0], start_point[1]]    
            self.vertices[3] = [start_point[0], end_point[1]]
            self.top_left_vertex_idx = 0
        elif start_point[0] > end_point[0] and start_point[1] < end_point[1]:
            self.vertices[1] = [start_point[0], end_point[1]]
            self.vertices[3] = [end_point[0], start_point[1]]
            self.top_left_vertex_idx = 3
        elif start_point[0] > end_point[0] and start_point[1] > end_point[1]:
            self.vertices[1] = [end_point[0], start_point[1]]
            self.vertices[3] = [start_point[0], end_point[1]]
            self.top_left_vertex_idx = 2
        else:
            self.vertices[1] = [start_point[0], end_point[1]]
            self.vertices[3] = [end_point[0], start_point[1]] 
            self.top_left_vertex_idx = 1

    def update_active_vertex(self, end_point):
        if self._active_vertex_idx > -1:
            self.vertices[self._active_vertex_idx] = end_point

    def activate_vertex(self, point, margin=20):
        matched_point_enum = (
            idx for idx, vertex 
            in enumerate(self.vertices) 
            if self._points_match(vertex, point, margin)
        ) 
        self._active_vertex_idx = next(matched_point_enum, -1)

        return self._active_vertex_idx > -1

    def deactivate_vertex(self):
        self._active_vertex_idx = -1

    def _points_match(self, p1, p2, margin):
        return (
            p2[0]-margin <= p1[0] <= p2[0]+margin 
            and p2[1]-margin <= p1[1] <= p2[1]+margin
        )

def wait_for_key(miliseconds):
    # '& 0xFF' because we're interested in the last 8 bits only.
    return cv2.waitKey(miliseconds) & 0xFF
