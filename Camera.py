import numpy as np
import cv2

class Camera():
    def __init__(self):
        self.vid = cv2.VideoCapture(0)
        self.img = cv2.imread(self.img)
        self.coordinates = []

    # def GetColor(self):
    #     while True:
    #         _, frame = self.vid.read()      # capturing the current frame
    #         cv2.imshow("frame", frame) # displaying the current frame

    #                                 # setting values for base colors
    #         b = frame[:, :, 0]         # Blue channel
    #         g = frame[:, :, 1]         # Green channel
    #         r = frame[:, :, 2]         # Red channel

    #         # computing the mean
    #         b_mean = np.mean(b)
    #         g_mean = np.mean(g)
    #         r_mean = np.mean(r)

    #         # displaying the most prominent color
    #         if b_mean > g_mean and b_mean > r_mean:
    #             print("Blue")
    #         elif g_mean > r_mean and g_mean > b_mean:
    #             print("Green")
    #         else:
    #             print("Red")

    #         # breaking the loop if 'q' is pressed
    #         if cv2.waitKey(1) & 0xFF == ord('q'):
    #             break

    #     # releasing the video capture object and closing all windows
    #         self.vid.release()
    #         cv2.destroyAllWindows()

    def take_image(self):
        frame = cv2.videocapture(0)
        cv2.imwrite('captured_frame.jpg', frame)
    
    def process_image(self):
        img = self.img
        hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Red color range
        lower_red = np.array([0, 120, 70])
        upper_red = np.array([10, 255, 255])

        # Green color range
        lower_green = np.array([36, 100, 100])
        upper_green = np.array([86, 255, 255])

        # Blue color range
        lower_blue = np.array([94, 80, 2])
        upper_blue = np.array([126, 255, 255])

        # Create masks for each color
        mask_red = cv2.inRange(hsv_image, lower_red, upper_red)
        mask_green = cv2.inRange(hsv_image, lower_green, upper_green)
        mask_blue = cv2.inRange(hsv_image, lower_blue, upper_blue)

        # Find contours for each mask
        contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours_green, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        def find_object_center(contours):
            for contour in contours:
                # Get the moments of the contour to calculate the center
                M = cv2.moments(contour)
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    return (cX, cY)
            return None
        red_object_coord = find_object_center(contours_red)
        green_object_coord = find_object_center(contours_green)
        blue_object_coord = find_object_center(contours_blue)

        self.coordinates.append(red_object_coord)
        self.coordinates.append(green_object_coord)
        self.coordinates.append(blue_object_coord)


        

    





      