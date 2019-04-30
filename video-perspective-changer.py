import os, argparse, glob
import cv2
import numpy as np

from video import VideoStream, OutputVideoFile
from gui import Window, wait_for_key

class VideoWorker:
    def __init__(self, stream, window):
        self._stream = stream
        self._window = window
        self._stop = False

        self.focused_area_vertices = None

    def process(self, paused=True):
        frame = self._stream.next_frame()

        if paused:
            self._pause_loop(frame)
        
        while(frame is not None and not self._stop):
            key_pressed = wait_for_key(1)
            
            # <SPACE>: Pause
            if key_pressed == ord(' '):
                self._pause_loop(frame)
            else:
                self._process_control_key(key_pressed)

            self._display_frame(frame)
            frame = self._stream.next_frame()
    
    def _pause_loop(self, frame):
        while(not self._stop):
            key_pressed = wait_for_key(1)
            
            # <SPACE>: Pause
            if key_pressed == ord(' '):
                break
            else:
                self._process_control_key(key_pressed)

            paused_frame = frame.copy()
            self._display_frame(paused_frame)
    
    def _process_control_key(self, key):
        # <q>: Quit
        if key == ord('q'):
            self._stop = True
        # <RETURN>: Change perspective
        elif key == 13 and self._window.selection is not None:
            # Make sure the first vertex is the top left vertex 
            self.focused_area_vertices = np.roll(
                self._window.selection.vertices, 
                -self._window.selection.top_left_vertex_idx,
                axis=0
            )
            self._window.remove_selection()
        # <u>: Undo the perspective transformation
        elif key == ord('u'):
            self.focused_area_vertices = None

    def _display_frame(self, frame):
        if self.focused_area_vertices is not None:
            frame.focus_on_area(self.focused_area_vertices)
        self._window.display_frame(frame)
 
def find_video_files_in_directory(directory, recursive_search=False):
    VIDEO_FILE_EXT = ['*.mp4', '*.mov', '*.avi']
    video_files_paths = []
    for ext in VIDEO_FILE_EXT:
        pattern = os.path.join(
            directory, 
            ('**/' + ext) if recursive_search else ext
        )
        video_files_paths.extend(glob.glob(pattern, recursive=recursive_search))
    return video_files_paths

if __name__  == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='Input video file or directory with video files.')
    parser.add_argument(
        '-d', 
        '--dir', 
        action='store_true', 
        help='The input argument is treated as a directory containing input video files.'
    )
    args = parser.parse_args()
    
    videos = {}

    if args.dir:
        video_files_paths = find_video_files_in_directory(args.input)
        for path in video_files_paths:
            video_name = os.path.splitext(os.path.basename(path))[0]
            videos[video_name] = VideoStream(path)
    else:
        video_name = os.path.splitext(os.path.basename(args.input))[0]
        videos[video_name] = VideoStream(args.input)

    for name, stream in videos.items():
        window = Window(name)
        window.show(640,480) 
        worker = VideoWorker(stream, window)
        worker.process()
        window.dispose()
        stream.close()
