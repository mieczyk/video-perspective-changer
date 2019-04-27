import argparse
import cv2
import numpy as np

from video import VideoStream
from gui import Window, wait_for_key

focused_area_vertices = None

def main_loop(stream, window, paused = True):
    global focused_area_vertices

    frame = stream.next_frame()
    
    if paused and pause_loop(frame, window) == ord('q'):
        return

    while(frame):
        key_pressed = wait_for_key(1)
        
        #<SPACE>: Pause
        if key_pressed == ord(' '):
            if pause_loop(frame, window) == ord('q'):
                break
        # <q>: Quit
        elif key_pressed == ord('q'):
            break
        else:
            process_video_control_keys(key_pressed, window)

        if focused_area_vertices is not None:
            frame.focus_on_area(focused_area_vertices)
        window.display_frame(frame)

        frame = stream.next_frame()
        
def pause_loop(frame, window):
    global focused_area_vertices
    
    key_pressed = None
    
    while(True):
        key_pressed = wait_for_key(1)
        if key_pressed == ord(' ') or key_pressed == ord('q'):
            break
        else:
            process_video_control_keys(key_pressed, window)

        paused_frame = frame.copy()
        if focused_area_vertices is not None:
            paused_frame.focus_on_area(focused_area_vertices)
        window.display_frame(paused_frame)

    return key_pressed

def process_video_control_keys(key, window): 
    global focused_area_vertices
    
    # <RETURN>: Change perspective
    if key == 13 and window.selection is not None:
        # Make sure the first vertex is the top left vertex 
        focused_area_vertices = np.roll(
            window.selection.vertices, 
            -window.selection.top_left_vertex_idx,
            axis=0
        )
        window.remove_selection()
    # <u>: Undo the perspective transformation
    elif key == ord('u'):
        focused_area_vertices = None
        
if __name__  == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='Input video file or directory with video files')
    args = parser.parse_args()
     
    window = Window('video'); 
    window.show(640, 480)
    
    stream = VideoStream(args.input)

    main_loop(stream, window)
    
    stream.close()
    window.dispose()
