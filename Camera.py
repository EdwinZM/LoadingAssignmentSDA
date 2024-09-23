import numpy as np
import cv2
import glob

class Camera:
    def __init__(self):
        self.vid = cv2.VideoCapture(0)
        self.coordinates = []  # To store coordinates of red, green, and blue objects
        self.camera_matrix = None
        self.distortion_coefficients = None
        self.load_calibration()

    def load_calibration(self):
        # Load calibration data if available
        try:
            self.camera_matrix = np.load('camera_matrix.npy')
            self.distortion_coefficients = np.load('distortion_coefficients.npy')
        except:
            print("Calibration data not found. Calibrating the camera...")
            self.calibrate_camera()

    def calibrate_camera(self, chessboard_size=(9, 6), square_size=25):
        # Termination criteria for corner subpix
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        # Prepare object points (3D points in real world space)
        objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
        objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2) * square_size

        objpoints = []  # 3D points in real world space
        imgpoints = []  # 2D points in image plane

        # Read images for calibration
        images = glob.glob('calibration_images/*.jpg')  # Adjust path if needed

        for fname in images:
            img = cv2.imread(fname)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)

            if ret:
                objpoints.append(objp)
                corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
                imgpoints.append(corners2)

        # Perform camera calibration
        ret, self.camera_matrix, self.distortion_coefficients, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
        
        # Save calibration data
        np.save('camera_matrix.npy', self.camera_matrix)
        np.save('distortion_coefficients.npy', self.distortion_coefficients)

    def take_image(self):
        ret, frame = self.vid.read()
        if ret:
            cv2.imwrite('captured_frame.jpg', frame)
            return frame
        else:
            print("Error: Unable to capture image.")
            return None

    def process_image(self):
        frame = self.take_image()
        if frame is None:
            return
        
        # Undistort the image using the calibration data
        frame = cv2.undistort(frame, self.camera_matrix, self.distortion_coefficients)

        # Convert the image from BGR to HSV color-space
        hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define color ranges for red, green, and blue objects
        lower_red = np.array([0, 120, 70])
        upper_red = np.array([10, 255, 255])

        lower_green = np.array([36, 100, 100])
        upper_green = np.array([86, 255, 255])

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

        # Function to find the center of an object based on contours
        def find_object_center(contours):
            for contour in contours:
                M = cv2.moments(contour)
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    return (cX, cY)
            return None

        # Get coordinates of red, green, and blue objects
        red_object_coord = find_object_center(contours_red)
        green_object_coord = find_object_center(contours_green)
        blue_object_coord = find_object_center(contours_blue)

        # Convert image coordinates to world coordinates
        def convert_image_to_world(px, py):
            # Assuming a fixed Z value (or calculate it if you have depth information)
            z_world = 500  # You may want to adjust this based on your setup
            world_x = (px - frame.shape[1] / 2) * (z_world / self.camera_matrix[0, 0])  # Focal length adjustment
            world_y = (frame.shape[0] / 2 - py) * (z_world / self.camera_matrix[1, 1])
            return world_x, world_y, z_world

        # Append coordinates to the list, converting to world coordinates
        if red_object_coord:
            red_world_coords = convert_image_to_world(*red_object_coord)
            self.coordinates.append(('red', red_world_coords))
        else:
            self.coordinates.append(('red', None))

        if green_object_coord:
            green_world_coords = convert_image_to_world(*green_object_coord)
            self.coordinates.append(('green', green_world_coords))
        else:
            self.coordinates.append(('green', None))

        if blue_object_coord:
            blue_world_coords = convert_image_to_world(*blue_object_coord)
            self.coordinates.append(('blue', blue_world_coords))
        else:
            self.coordinates.append(('blue', None))

        # Print coordinates for debugging
        print(f"Red object world coordinates: {self.coordinates[0][1]}")
        print(f"Green object world coordinates: {self.coordinates[1][1]}")
        print(f"Blue object world coordinates: {self.coordinates[2][1]}")


