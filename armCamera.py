import cv2
import numpy as np
import DoBotArm as dbt
import time

# Define the operational limits of the Dobot arm (adjust as per your specifications)
DOBOT_X_MIN = 0      # Minimum X coordinate
DOBOT_X_MAX = 470    # Maximum X coordinate
DOBOT_Y_MIN = 0      # Minimum Y coordinate
DOBOT_Y_MAX = 363    # Maximum Y coordinate
DOBOT_Z = -35        # Initial Z position (hovering above the object)
LOWER_Z = DOBOT_Z - 7  # Lower by 7mm to pick up the object
RAISE_Z = DOBOT_Z + 50  # Raise by 50mm after suction

# Camera settings
class Camera:
    def __init__(self, cam_index=1, scaling_factor=0.5):
        self.cam_index = cam_index
        self.scaling_factor = scaling_factor
        self.vid = cv2.VideoCapture(cam_index)

        if not self.vid.isOpened():
            raise Exception("Error: Could not open video.")
        
        # Green color detection ranges in HSV
        self.lower_green = np.array([35, 50, 50])
        self.upper_green = np.array([85, 255, 255])

        # Minimum pixel count threshold for valid color detection
        self.min_pixels_threshold = 500
        self.kernel = np.ones((3, 3), np.uint8)

    def capture_frame(self):
        ret, frame = self.vid.read()
        if not ret:
            raise Exception("Error: Could not read frame.")
        return cv2.resize(frame, None, fx=self.scaling_factor, fy=self.scaling_factor, interpolation=cv2.INTER_AREA)

    def detect_green_object(self, frame):
        # Convert frame to HSV color space
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask_green = cv2.inRange(hsv_frame, self.lower_green, self.upper_green)

        # Preprocessing: Erosion followed by dilation to reduce noise
        mask_green = cv2.erode(mask_green, self.kernel, iterations=1)
        mask_green = cv2.dilate(mask_green, self.kernel, iterations=2)

        contours, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return contours

    def release(self):
        self.vid.release()
        cv2.destroyAllWindows()

# Arm settings
class Arm:
    def __init__(self):
        self.homeX, self.homeY, self.homeZ = 225, 0, -43
        self.device = dbt.DoBotArm("COM5", self.homeX, self.homeY, self.homeZ, home=False)

    def is_within_limits(self, x, y):
        """Check if the given coordinates are within the operational limits of the Dobot."""
        return (DOBOT_X_MIN <= x <= DOBOT_X_MAX) and (DOBOT_Y_MIN <= y <= DOBOT_Y_MAX)

    def go_to_position(self, x, y, z):
        """Moves the arm to the specified (x, y, z) coordinates if within limits."""
        if self.is_within_limits(x, y):
            self.device.moveArmXYZ(x, y, z)
            print(f"Moving arm to position: X={x}, Y={y}, Z={z}")
        else:
            print(f"Warning: Attempted to move out of range to ({x}, {y}). Movement skipped.")

    def activate_suction(self):
        """Activate the suction mechanism."""
        self.device.toggleSuction(True)
        print("Suction activated.")

    def deactivate_suction(self):
        """Deactivate the suction mechanism."""
        self.device.toggleSuction(False)
        print("Suction deactivated.")

    def move_to_home(self):
        """Move the arm to the home position."""
        self.go_to_position(self.homeX, self.homeY, self.homeZ)

def main():
    camera = Camera()
    arm = Arm()

    try:
        while True:
            frame = camera.capture_frame()
            contours = camera.detect_green_object(frame)

            if contours:
                largest_contour = max(contours, key=cv2.contourArea)
                if cv2.contourArea(largest_contour) > camera.min_pixels_threshold:
                    M = cv2.moments(largest_contour)
                    if M["m00"] != 0:
                        cX = int(M["m10"] / M["m00"])
                        cY = int(M["m01"] / M["m00"])

                        # Draw a circle at the center of the detected object
                        cv2.circle(frame, (cX, cY), 5, (0, 255, 0), -1)

                        # Calculate adjusted coordinates for the arm
                        adjusted_x = cX - 160
                        adjusted_y = camera.vid.get(cv2.CAP_PROP_FRAME_HEIGHT) * camera.scaling_factor - cY - 130  # Invert Y
                        arm_position_x = arm.homeX + adjusted_x
                        arm_position_y = arm.homeY + adjusted_y + 50

                        # Move the arm to the calculated XY position with a higher Z value (hovering)
                        arm.go_to_position(arm_position_x, arm_position_y, DOBOT_Z)

                        # Lower the arm by 7mm to pick up the object
                        arm.go_to_position(arm_position_x, arm_position_y, LOWER_Z)

                        # Activate suction to grab the object
                        arm.activate_suction()

                        # Raise the arm by 50mm after suction
                        arm.go_to_position(arm_position_x, arm_position_y, RAISE_Z)

                        # Move to the -Y position by 150mm
                        new_y_position = arm_position_y - 150
                        arm.go_to_position(arm_position_x, new_y_position, RAISE_Z)

                        # Deactivate suction to release the object
                        arm.deactivate_suction()

                        # Move the arm back to the home position
                        arm.move_to_home()

            # Display the frame
            cv2.imshow("Frame", frame)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(30) & 0xFF == ord('q'):
                break

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        camera.release()

if __name__ == "__main__":
    main()
