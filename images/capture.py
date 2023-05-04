# program to capture single image from webcam in python

# importing OpenCV library
from cv2 import VideoCapture, imshow, imwrite, destroyWindow
import time

# initialize the camera
# If you have multiple camera connected with 
# current device, assign a value in cam_port 
# variable according to that


# If image will detected without any error, 
# show result
def capture():
    i = 0
    while True:
        cam_port = 0
        cam = VideoCapture(cam_port)

        # reading the input using the camera
        result, image = cam.read()
        if result:
            # showing result, it take frame name and image
            # output
            imshow("GeeksForGeeks", image)

            # saving image in local storage
            imwrite(f"img-{i}.jpg", image)
            i += 1
            # If keyboard interrupt occurs, destroy image
            # window
            # time.sleep(2)
            destroyWindow("GeeksForGeeks")
            print("hihihihihi")

            break

        # If captured image is corrupted, moving to else part
        else:
            print("No image detected. Please! try again")


if __name__ == '__main__':
    capture()
