from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QFileDialog, QPushButton, QLineEdit, QVBoxLayout,
    QWidget, QMenuBar, QMessageBox
)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
from tracking.tracker import BarbellTracker
from analysis.depth_analysis import DepthAnalyzer
from analysis.utils import get_squat_feedback
import cv2
import numpy as np


class MainWindow(QMainWindow):
    def __init__(self):
        """
        Initializes the main GUI window and its components.
        """

        super().__init__()
        self.init_ui()
        self.cap = None
        self.tracker = BarbellTracker()
        self.depth_analyzer = DepthAnalyzer()
        self.timer = QTimer()
        self.in_squat = False
        self.rep_count = 0

        # User-defined depth parameter
        self.min_depth = 90

    def init_ui(self):
        """
        Initializes the GUI layout and widgets.
        """

        self.setWindowTitle("Barbell Tracker & Squat Analyzer")
        self.setGeometry(100, 100, 1000, 800)

        # Central widget and main layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()

        # Add a menu bar
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        # File menu
        file_menu = menu_bar.addMenu("File")
        open_action = file_menu.addAction("Open Video")
        open_action.triggered.connect(self.load_video)
        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(self.close)

        # QLabel for video display
        self.video_label = QLabel(self)
        self.video_label.setFixedSize(800, 600)
        main_layout.addWidget(self.video_label)

        # Depth parameter input
        self.min_depth_input = QLineEdit(self)
        self.min_depth_input.setPlaceholderText("Enter Min Depth (default: 90)")
        main_layout.addWidget(self.min_depth_input)

        # Load video button
        self.load_button = QPushButton("Load Video", self)
        self.load_button.clicked.connect(self.load_video)
        main_layout.addWidget(self.load_button)

        # Start analysis button
        self.track_button = QPushButton("Start Analysis", self)
        self.track_button.clicked.connect(self.start_analysis)
        main_layout.addWidget(self.track_button)

        central_widget.setLayout(main_layout)

    def load_video(self):
        """
        Opens a file dialog to load a video and initializes the barbell tracker
        with a user-defined region of interest (ROI).
        """
        if self.timer.isActive():
            self.timer.stop()

        video_path, _ = QFileDialog.getOpenFileName(self, "Open Video File", "", "Video Files (*.mp4 *.avi)")
        if video_path:
            self.tracker.barbell_path = []
            self.rep_count = 0
            self.in_squat = False

            self.cap = cv2.VideoCapture(video_path)
            _, frame = self.cap.read()
            self.display_frame(frame)
            roi = cv2.selectROI("Select Barbell", frame, fromCenter=False, showCrosshair=True)
            cv2.destroyWindow("Select Barbell")
            self.tracker.initialize_tracker(frame, roi)

    def start_analysis(self):
        """
        Reads the user-defined minimum depth parameter and starts processing video frames.
        """
        if not self.cap or not self.cap.isOpened():
            self.show_error_message("No video loaded. Please load a video first.")
            return
        self.rep_count = 0
        self.in_squat = False
        # Get user-defined depth parameter
        try:
            self.min_depth = int(self.min_depth_input.text()) if self.min_depth_input.text() else 90
        except ValueError:
            self.min_depth = 90

        self.timer.timeout.connect(self.process_frame)
        self.timer.start(30)


    def process_frame(self):
        """
        Processes video frames in real time:
            - Tracks the barbell position.
            - Analyzes squat depth.
            - Updates feedback and rep count.
        """

        ret, frame = self.cap.read()
        if not ret:
            self.timer.stop()
            self.cap.release()
            return

        # Perform tracking
        frame, success = self.tracker.update(frame)
        if not success:
            print("Tracker lost the barbell.")

        # Perform depth analysis
        frame, angles = self.depth_analyzer.analyze_frame(frame)

        # Display feedback and rep count
        if "knee_angle" in angles:
            knee_angle = angles["knee_angle"]
            feedback = get_squat_feedback(knee_angle, self.min_depth)

            # Update rep count
            if knee_angle <= self.min_depth and not self.in_squat:
                self.in_squat = True
            elif knee_angle > self.min_depth + 10 and self.in_squat:
                self.rep_count += 1
                self.in_squat = False

            cv2.putText(frame, f"Knee Angle: {knee_angle:.2f}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(frame, feedback, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"Rep Count: {self.rep_count}", (10, 110),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

        self.display_frame(frame)

    def display_frame(self, frame):
        """
        Resizes the given video frame to fit the QLabel and displays it.
        
        Args:
            frame (numpy.ndarray): The video frame to display.
        """
        label_width = self.video_label.width()
        label_height = self.video_label.height()
        frame_height, frame_width = frame.shape[:2]
        aspect_ratio = frame_width / frame_height

        if label_width / label_height > aspect_ratio:
            scaled_height = label_height
            scaled_width = int(scaled_height * aspect_ratio)
        else:
            scaled_width = label_width
            scaled_height = int(scaled_width / aspect_ratio)

        frame = cv2.resize(frame, (scaled_width, scaled_height), interpolation=cv2.INTER_AREA)
        blank_image = np.zeros((label_height, label_width, 3), dtype=np.uint8)
        x_offset = (label_width - scaled_width) // 2
        y_offset = (label_height - scaled_height) // 2
        blank_image[y_offset:y_offset + scaled_height, x_offset:x_offset + scaled_width] = frame

        frame = cv2.cvtColor(blank_image, cv2.COLOR_BGR2RGB)
        h, w, ch = frame.shape
        bytes_per_line = ch * w
        qt_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(qt_image))

    def show_error_message(self, message):
        """
        Displays an error message to the user.
        Args:
            message (str): The error message to display.
        """
        error_dialog = QMessageBox(self)
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setText(message)
        error_dialog.setWindowTitle("Error")
        error_dialog.exec_()