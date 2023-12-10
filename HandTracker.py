# Hand tracking libraries
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
# Other needed libraries
import cv2
import numpy
import time

def draw_results(frame, detection_result):
    height = frame.shape[0]
    width = frame.shape[1]
    landmark_array = numpy.array(detection_result.hand_landmarks)

    # Empty image
    canvas = numpy.zeros((height, width, 3), numpy.uint8)

    if landmark_array.any():
        # Points
        count = 0
        for i in landmark_array[0]:
            x_coordinate = int(width  * i.x)
            y_coordinate = int(height * i.y)
            canvas = cv2.circle(canvas, (x_coordinate,y_coordinate), radius=5, color=(0, 0, 255), thickness=-1)
            count += 1

        # Lines
        connections = [[0, 1], [1, 2], [2, 3], [3, 4], [0, 5], [5, 6], [6, 7], [7, 8], [0, 9], [9, 10], [10, 11], [11, 12], [0, 13], [13, 14], [14, 15], [15, 16], [0, 17], [17, 18], [18, 19], [19, 20]]
        for connection in connections:
            start_point = (int(width * landmark_array[0][connection[0]].x), int(height * landmark_array[0][connection[0]].y))
            end_point = (int(width * landmark_array[0][connection[1]].x), int(height * landmark_array[0][connection[1]].y))
            canvas = cv2.line(canvas, start_point, end_point, color=(255, 255, 255), thickness=2)

    # Draw
    canvas = cv2.flip(canvas, 1)
    cv2.imshow('tracked',canvas)
    cv2.waitKey(0)

class HandTracker:
    __x = -1
    __y = -1
    __fps = 0
    __frame_count = 0
    __buffer_size = 32
    __read_buffer = numpy.zeros((2,__buffer_size))

    def __init__(self, video_capture, model_path):
        print("Initializing HandTracker object...")
        self.__cap = video_capture
        self.__model_path = model_path
        self.__width = int(self.__cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.__height = int(self.__cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        VisionRunningMode = mp.tasks.vision.RunningMode

        # Create an ImageClassifier object.
        self.__base_options = python.BaseOptions(model_asset_path=self.__model_path)
        self.__options = vision.HandLandmarkerOptions(base_options=self.__base_options,running_mode=VisionRunningMode.VIDEO)
        self.__detector = vision.HandLandmarker.create_from_options(self.__options)

        # Load the frame rate of the video using OpenCV’s CV_CAP_PROP_FPS
        # You’ll need it to calculate the timestamp for each frame.
        self.__fps = self.__cap.get(cv2.CAP_PROP_FPS)

    def calculate_finger_position(self, display=False):
        if self.__cap.isOpened():
            # Read a frame from the video capture object.
            ret, frame = self.__cap.read()
            # Convert the frame received from OpenCV to a MediaPipe’s Image object.
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
            # Detect hand landmarks from the input image.
            detection_result = self.__detector.detect_for_video(mp_image, self.__frame_count) # TODO: replace second argument with frame_timestamp
            self.__frame_count += 1

            if ret:

                if display:
                    draw_results(frame, detection_result)

                # Return scaled results
                landmark_array = numpy.array(detection_result.hand_landmarks)
                
                if landmark_array.any():
                    # Shift values 1 space to the left
                    self.__read_buffer[0][:-1] = self.__read_buffer[0][1:]
                    # Insert new X measurement to the back of the array
                    self.__read_buffer[0][-1] = int(landmark_array[0][8].x * self.__width)
                    # Shift values 1 space to the left
                    self.__read_buffer[1][:-1] = self.__read_buffer[1][1:]
                    # Insert new Y measurement to the back of the array
                    self.__read_buffer[1][-1] = int(landmark_array[0][8].y * self.__height)
                    # Average the whole list and asign it to __x and __y as the measurement. 
                    # Note that we could make other calculations instead, such as applying 'friction' depending on dx and dy, and so on.
                    self.__x = int(self.__read_buffer[0].mean())
                    self.__y = int(self.__read_buffer[1].mean())
                else:
                    print("No detection")
                    self.__read_buffer[0][:-1] = self.__read_buffer[0][1:]
                    self.__read_buffer[0][-1] = self.__x

                    self.__read_buffer[1][:-1] = self.__read_buffer[1][1:]
                    self.__read_buffer[1][-1] = self.__y
                    
                    self.__x = int(self.__read_buffer[0].mean())
                    self.__y = int(self.__read_buffer[1].mean())

            else:
                print("WARNING: No return in cap.read()")

    # Getters
    def get_coordinates(self):
        return self.__x, self.__y
    
    def get_framerate(self):
        return self.__fps
    
    def get_dimensions(self):
        return self.__width, self.__height
    