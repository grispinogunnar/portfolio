import cv2
import mediapipe as mp
import numpy as np
import sys
import os

class DepthAnalyzer:
    def __init__(self):
        # Determine the base path for resources
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS  # PyInstaller's temp directory
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))

        # Set paths for the required MediaPipe models
        pose_detection_path = os.path.join(base_path, "mediapipe/modules/pose_detection/pose_detection.tflite")
        pose_landmark_path = os.path.join(base_path, "mediapipe/modules/pose_landmark/pose_landmark_cpu.binarypb")

        # Initialize MediaPipe Pose with the correct model paths
        self.pose = mp.solutions.pose.Pose(
            static_image_mode=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
            model_complexity=1
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.lower_body_connections = [
            (mp.solutions.pose.PoseLandmark.LEFT_HIP.value, mp.solutions.pose.PoseLandmark.LEFT_KNEE.value),
            (mp.solutions.pose.PoseLandmark.LEFT_KNEE.value, mp.solutions.pose.PoseLandmark.LEFT_ANKLE.value),
            (mp.solutions.pose.PoseLandmark.LEFT_ANKLE.value, mp.solutions.pose.PoseLandmark.LEFT_HEEL.value),
            (mp.solutions.pose.PoseLandmark.LEFT_ANKLE.value, mp.solutions.pose.PoseLandmark.LEFT_FOOT_INDEX.value),
            (mp.solutions.pose.PoseLandmark.RIGHT_HIP.value, mp.solutions.pose.PoseLandmark.RIGHT_KNEE.value),
            (mp.solutions.pose.PoseLandmark.RIGHT_KNEE.value, mp.solutions.pose.PoseLandmark.RIGHT_ANKLE.value),
            (mp.solutions.pose.PoseLandmark.RIGHT_ANKLE.value, mp.solutions.pose.PoseLandmark.RIGHT_HEEL.value),
            (mp.solutions.pose.PoseLandmark.RIGHT_ANKLE.value, mp.solutions.pose.PoseLandmark.RIGHT_FOOT_INDEX.value),
        ]
        self.bar_path = []  # Barbell path for visualization

    def analyze_frame(self, frame):
        """
        Analyze the frame for pose landmarks and calculate squat angles.
        Args:
            frame (numpy.ndarray): Input video frame.
        Returns:
            tuple: (annotated_frame, angles)
                annotated_frame (numpy.ndarray): Frame with pose landmarks drawn.
                angles (dict): Calculated joint angles (hip, knee, ankle).
        """
        results = self.pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if not results.pose_landmarks:
            return frame, {}

        # Get landmark coordinates
        landmarks = results.pose_landmarks.landmark
        hip = (landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP.value].x,
               landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP.value].y)
        knee = (landmarks[mp.solutions.pose.PoseLandmark.LEFT_KNEE.value].x,
                landmarks[mp.solutions.pose.PoseLandmark.LEFT_KNEE.value].y)
        ankle = (landmarks[mp.solutions.pose.PoseLandmark.LEFT_ANKLE.value].x,
                 landmarks[mp.solutions.pose.PoseLandmark.LEFT_ANKLE.value].y)

        # Calculate angles
        knee_angle = self.calculate_angle(hip, knee, ankle)

        # Draw lower body connections
        annotated_frame = frame.copy()
        for start, end in self.lower_body_connections:
            start_point = landmarks[start]
            end_point = landmarks[end]
            cv2.line(
                annotated_frame,
                (int(start_point.x * frame.shape[1]), int(start_point.y * frame.shape[0])),
                (int(end_point.x * frame.shape[1]), int(end_point.y * frame.shape[0])),
                (0, 255, 0),
                2,
            )

        # Return annotated frame and angles
        angles = {"knee_angle": knee_angle}
        return annotated_frame, angles

    def calculate_angle(self, a, b, c):
        """
        Calculate the angle between three points.
        Args:
            a, b, c (tuple): Coordinates of the points (x, y).
        Returns:
            float: Angle in degrees.
        """
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)

        # Vectors
        ba = a - b
        bc = c - b

        # Calculate the cosine of the angle
        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))

        return np.degrees(angle)
