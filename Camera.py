import cv2
import numpy as np

class Camera:
    def __init__(self):
        # Dobot workspace coordinates in mm (replace with actual Dobot measurements)
        self.dobot_x_min = 0
        self.dobot_y_min = 0
        self.dobot_x_max = 470
        self.dobot_y_max = 363

        self.coordinates = []

        # Scaling factor to zoom out (adjust if needed)
        self.scaling_factor = 0.75

        # HSV color ranges for green, red, and blue
        self.lower_green = np.array([35, 50, 50])
        self.upper_green = np.array([85, 255, 255])
        self.lower_red1 = np.array([0, 100, 50])
        self.upper_red1 = np.array([10, 255, 255])
        self.lower_red2 = np.array([170, 100, 50])
        self.upper_red2 = np.array([180, 255, 255])
        self.lower_blue = np.array([102, 50, 50])
        self.upper_blue = np.array([130, 255, 255])

        self.min_pixels_threshold = 500
        self.kernel = np.ones((3, 3), np.uint8)

        # Initialize video capture
        self.vid = cv2.VideoCapture(1)

    def take_image(self):
        """Capture an image from the camera."""
        ret, self.frame = self.vid.read()
        if not ret:
            print("Failed to grab frame.")
            return

        # Resize the frame
        self.frame = cv2.resize(self.frame, None, fx=self.scaling_factor, fy=self.scaling_factor, interpolation=cv2.INTER_AREA)

        # Convert frame to HSV color space
        self.hsv_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)

        # Apply Gaussian blur to reduce noise
        self.hsv_frame = cv2.GaussianBlur(self.hsv_frame, (5, 5), 0)

        # Create color masks
        self.mask_green = cv2.inRange(self.hsv_frame, self.lower_green, self.upper_green)
        self.mask_red1 = cv2.inRange(self.hsv_frame, self.lower_red1, self.upper_red1)
        self.mask_red2 = cv2.inRange(self.hsv_frame, self.lower_red2, self.upper_red2)
        self.mask_blue = cv2.inRange(self.hsv_frame, self.lower_blue, self.upper_blue)

        # Combine red masks
        self.mask_red = self.mask_red1 + self.mask_red2

        # Preprocessing: erosion followed by dilation to reduce noise
        self.mask_green = cv2.erode(self.mask_green, self.kernel, iterations=1)
        self.mask_green = cv2.dilate(self.mask_green, self.kernel, iterations=2)

        self.mask_red = cv2.erode(self.mask_red, self.kernel, iterations=1)
        self.mask_red = cv2.dilate(self.mask_red, self.kernel, iterations=2)

        self.mask_blue = cv2.erode(self.mask_blue, self.kernel, iterations=1)
        self.mask_blue = cv2.dilate(self.mask_blue, self.kernel, iterations=2)

    def process_image(self):
        """Process the captured image and extract Dobot coordinates based on detected colors."""
        height, width, _ = self.frame.shape

        # Find contours for each color mask
        contours_green, _ = cv2.findContours(self.mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours_red, _ = cv2.findContours(self.mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours_blue, _ = cv2.findContours(self.mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Process contours for each color and calculate the Dobot coordinates
        self._process_contours(contours_green, "Green", (0, 255, 0), width, height)
        self._process_contours(contours_red, "Red", (0, 0, 255), width, height)
        self._process_contours(contours_blue, "Blue", (255, 0, 0), width, height)

    def _process_contours(self, contours, color_name, color_rgb, width, height):
        """Helper method to process contours and display coordinates."""
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            if cv2.contourArea(largest_contour) > self.min_pixels_threshold:
                M = cv2.moments(largest_contour)
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])

                    # Draw a small circle at the center of the object
                    cv2.circle(self.frame, (cX, cY), 5, color_rgb, -1)

                    # Transform pixel coordinates to Dobot's mm coordinates
                    dobot_x = self.dobot_x_min + (cX / width) * (self.dobot_x_max - self.dobot_x_min)
                    dobot_y = self.dobot_y_min + (cY / height) * (self.dobot_y_max - self.dobot_y_min)

                    # Apply the offset
                    dobot_x += self.x_offset
                    dobot_y += self.y_offset

                    # Display the color and Dobot coordinates
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(self.frame, f"{color_name} ({dobot_x:.2f}, {dobot_y:.2f} mm)", (cX + 10, cY),
                                font, 0.5, color_rgb, 1, cv2.LINE_AA)

                    # Append coordinates
                    self.coordinates.append([dobot_x, dobot_y])
