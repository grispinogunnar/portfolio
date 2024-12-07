from tracking.utils import draw_path
import cv2

class BarbellTracker:
    """
    A class to handle barbell tracking in video frames using OpenCV's CSRT tracker.

    Attributes:
        tracker (cv2.Tracker): The OpenCV tracker used to track the barbell.
        barbell_path (list): A list of (x, y) tuples representing the tracked barbell's path over time.
    """

    def __init__(self):
        """
        Initializes a new BarbellTracker instance.

        Attributes:
            tracker: Set to None until initialized with `initialize_tracker`.
            barbell_path: An empty list to store the tracked barbell's path.
        """
        self.tracker = None
        self.barbell_path = []

    def initialize_tracker(self, frame, roi):
        """
        Initializes the CSRT tracker with a region of interest (ROI) selected by the user.

        Args:
            frame (numpy.ndarray): The initial frame of the video where the barbell is visible.
            roi (tuple): The bounding box of the ROI, specified as (x, y, width, height).

        Returns:
            None
        """
        self.tracker = cv2.TrackerCSRT_create()
        self.tracker.init(frame, roi)

    def update(self, frame):
        """
        Updates the tracker for the current frame, calculates the barbell's position,
        and appends it to the path for visualization.

        Args:
            frame (numpy.ndarray): The current video frame.

        Returns:
            tuple:
                - frame (numpy.ndarray): The updated frame with the barbell's bounding box,
                  center point, and path drawn.
                - success (bool): True if the tracker successfully updates, False otherwise.

        Raises:
            RuntimeError: If the tracker is not initialized before calling `update`.
        """
        if not self.tracker:
            raise RuntimeError("Tracker not initialized. Call `initialize_tracker` first.")

        success, bbox = self.tracker.update(frame)
        if success:
            # Extract bounding box coordinates
            x, y, w, h = [int(v) for v in bbox]
            center_x, center_y = x + w // 2, y + h // 2

            # Append the center point to the barbell path
            self.barbell_path.append((center_x, center_y))

            # Draw the path and bounding box on the frame
            frame = draw_path(frame, bbox, self.barbell_path)

        return frame, success
