from flask import Flask, render_template, jsonify
from datetime import datetime
import random
from typing import List, Dict, Tuple
import cv2
from ultralytics import YOLO
import threading
import time
import os

# Import configuration
from config import (
    MODEL_PATH, VIDEO_SOURCE, CONFIDENCE_THRESHOLD, FRAME_SKIP_RATE,
    VEHICLE_CLASSES, ANIMAL_CLASSES, TRAFFIC_CLASSES,
    TRAFFIC_THRESHOLDS, FLASK_HOST, FLASK_PORT, FLASK_DEBUG
)

app = Flask(__name__)

# ============================================================================
# YOLO DETECTOR INTEGRATION
# ============================================================================

class YOLODetector:
    """
    Real-time YOLO detector that processes video frames in a background thread.
    """

    def __init__(self, model_path: str, video_source: str, conf_threshold: float = 0.45):
        self.model_path = model_path
        self.video_source = video_source
        self.conf_threshold = conf_threshold
        self.model = None
        self.cap = None
        self.current_detections = []
        self.running = False
        self.thread = None
        self.last_frame_time = 0
        self.frame_skip_rate = FRAME_SKIP_RATE

        # Load model on initialization
        self._load_model()

    def _load_model(self):
        """Load the YOLO model."""
        try:
            if not os.path.exists(self.model_path):
                print(f"Warning: Model not found at {self.model_path}")
                return False

            print(f"Loading YOLO model: {self.model_path}")
            self.model = YOLO(self.model_path)
            print("Model loaded successfully!")
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False

    def _process_frames(self):
        """Process video frames continuously in background thread."""
        if not self.model:
            print("Model not loaded, cannot start detection")
            return

        # Open video source
        self.cap = cv2.VideoCapture(self.video_source)
        if not self.cap.isOpened():
            print(f"Error: Could not open video source {self.video_source}")
            return

        print(f"Starting YOLO detection on {self.video_source}...")

        frame_count = 0
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                print("End of video stream or error, restarting...")
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Restart video
                continue

            frame_count += 1

            # Skip frames for performance (configurable)
            if frame_count % self.frame_skip_rate != 0:
                continue

            try:
                # Run YOLO inference
                results = self.model.predict(
                    frame,
                    conf=self.conf_threshold,
                    imgsz=640,
                    verbose=False
                )

                # Extract detected class names
                detected_classes = []
                if results and results[0].boxes:
                    for cls in results[0].boxes.cls:
                        class_name = self.model.names[int(cls)]
                        detected_classes.append(class_name)

                # Update current detections
                self.current_detections = detected_classes
                self.last_frame_time = time.time()

            except Exception as e:
                print(f"Error processing frame: {e}")
                continue

        print("Detection thread stopped")

    def start(self):
        """Start the detection thread."""
        if not self.running and self.model:
            self.running = True
            self.thread = threading.Thread(target=self._process_frames, daemon=True)
            self.thread.start()
            print("YOLO detector started")
            return True
        return False

    def stop(self):
        """Stop the detection thread."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=2.0)
        if self.cap:
            self.cap.release()
        print("YOLO detector stopped")

    def get_current_detections(self) -> List[str]:
        """Get the latest detections."""
        return self.current_detections.copy()

    def is_active(self) -> bool:
        """Check if detector is actively processing."""
        return self.running and (time.time() - self.last_frame_time) < 5.0  # 5 second timeout


# ============================================================================
# DETECTION DATA MODULE - Structure for easy YOLO integration
# ============================================================================

class DetectionProcessor:
    """
    Processes raw detection data from YOLO or mock sources.
    Easy to replace with actual YOLO output later.
    """

    # Based on your traffic monitoring requirements
    VEHICLE_CLASSES = {'car', 'motorcycle', 'bus', 'truck', 'bicycle', 'vehicle'}
    ANIMAL_CLASSES = {'cow', 'dog', 'cat', 'bird', 'horse', 'animal'}
    TRAFFIC_CLASSES = {'traffic_light', 'barrier', 'stop_sign', 'traffic_sign'}

    def __init__(self):
        self.current_detections = []

    def mock_detection(self) -> List[str]:
        """
        Simulates YOLO detection output.
        Used as fallback when YOLO is not available.

        Returns:
            List[str]: List of detected object class names
        """
        detections = []

        # Simulate variable traffic conditions
        num_vehicles = random.randint(2, 8)
        num_animals = random.randint(0, 2)

        # Add vehicle detections
        for _ in range(num_vehicles):
            vehicle = random.choice(list(self.VEHICLE_CLASSES))
            detections.append(vehicle)

        # Occasionally add animal (cow) detections
        if random.random() < 0.3:  # 30% chance of animal detection
            animal = random.choice(list(self.ANIMAL_CLASSES))
            detections.append(animal)

        # Add traffic infrastructure detections
        if random.random() < 0.7:
            traffic = random.choice(list(self.TRAFFIC_CLASSES))
            detections.append(traffic)

        # Update current detections
        self.current_detections = detections
        return detections

    def process_yolo_output(self, detections: List[str]) -> None:
        """
        Process actual YOLO detection output.

        Args:
            detections: List of object class names from YOLO

        Example:
            # After running YOLO inference
            # results = yolo_model.detect(frame)
            # processor.process_yolo_output(results.class_names)
        """
        self.current_detections = detections

    def get_vehicle_count(self) -> int:
        """Count vehicles in current detections."""
        return sum(1 for obj in self.current_detections if obj in self.VEHICLE_CLASSES)

    def has_animal(self) -> bool:
        """Check if any animals detected."""
        return any(obj in self.ANIMAL_CLASSES for obj in self.current_detections)

    def get_animal_types(self) -> List[str]:
        """Get list of detected animal types."""
        return [obj for obj in self.current_detections if obj in self.ANIMAL_CLASSES]

    def get_detected_objects(self) -> Dict[str, List[str]]:
        """Get organized detection types."""
        return {
            'vehicles': [obj for obj in self.current_detections if obj in self.VEHICLE_CLASSES],
            'animals': [obj for obj in self.current_detections if obj in self.ANIMAL_CLASSES],
            'traffic_infrastructure': [obj for obj in self.current_detections if obj in self.TRAFFIC_CLASSES],
        }

    def calculate_traffic_density(self) -> str:
        """
        Calculate traffic density based on vehicle count.
        Can be enhanced with more sophisticated metrics.
        """
        vehicle_count = self.get_vehicle_count()

        if vehicle_count <= 2:
            return "Low"
        elif vehicle_count <= 5:
            return "Medium"
        else:
            return "High"


# ============================================================================
# GLOBAL DETECTOR INSTANCES
# ============================================================================

# Configuration - Update these paths as needed
MODEL_PATH = r"C:\Users\VICUTUS\OneDrive\文档\Desktop\DL LAB PROJECT 59 61\95_e\cls_fix_30e\weights\best.pt"
VIDEO_SOURCE = r"C:\Users\VICUTUS\OneDrive\文档\Desktop\DL LAB PROJECT 59 61\WhatsApp Video 2026-04-08 at 10.31.39 PM.mp4"

# Initialize detectors
yolo_detector = YOLODetector(MODEL_PATH, VIDEO_SOURCE, conf_threshold=0.45)
detection_processor = DetectionProcessor()

# ============================================================================
# FLASK LIFECYCLE MANAGEMENT
# ============================================================================

@app.before_first_request
def startup():
    """Start YOLO detector when Flask app starts."""
    print("Starting Flask app...")
    if yolo_detector.start():
        print("YOLO detector initialized and running")
    else:
        print("YOLO detector failed to start, will use mock data")

@app.teardown_appcontext
def shutdown(exception=None):
    """Stop YOLO detector when Flask app shuts down."""
    print("Shutting down Flask app...")
    yolo_detector.stop()

# ============================================================================
# FLASK ROUTES
# ============================================================================

@app.route('/')
def index():
    """Serve the dashboard HTML page."""
    return render_template('index.html')


@app.route('/data')
def get_detection_data():
    """
    API endpoint that returns current detection data.

    Returns:
        JSON with:
        - vehicle_count: int
        - animal_detected: bool
        - traffic_density: str ("Low", "Medium", "High")
        - timestamp
        - detected_objects: dict (optional, for frontend display)
    """
    # Try to get real YOLO detections first
    if yolo_detector.is_active():
        detections = yolo_detector.get_current_detections()
        detection_processor.process_yolo_output(detections)
        print(f"Using YOLO detections: {detections}")
    else:
        # Fallback to mock data if YOLO not available
        detection_processor.mock_detection()
        print("Using mock detections (YOLO not active)")

    vehicle_count = detection_processor.get_vehicle_count()
    animal_detected = detection_processor.has_animal()
    traffic_density = detection_processor.calculate_traffic_density()

    return jsonify({
        'vehicle_count': vehicle_count,
        'animal_detected': animal_detected,
        'traffic_density': traffic_density,
        'timestamp': datetime.now().isoformat(),
        'detected_objects': detection_processor.get_detected_objects(),
        'animal_types': detection_processor.get_animal_types(),
        'yolo_active': yolo_detector.is_active(),
    })


@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'ok',
        'yolo_active': yolo_detector.is_active(),
        'model_loaded': yolo_detector.model is not None,
        'video_source': VIDEO_SOURCE,
        'model_path': MODEL_PATH,
    })


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    # Import config for validation
    from config import validate_config, print_config
    
    # Validate configuration
    errors = validate_config()
    if errors:
        print("❌ Configuration Errors:")
        for error in errors:
            print(f"  - {error}")
        print("\n💡 For production deployment, ensure model and video files are available")
        print("   or set VIDEO_SOURCE=0 for webcam (if supported)")
    
    # Print configuration
    print_config()
    
    # Check if running on Render (production)
    is_render = os.getenv('RENDER') == 'true'
    
    if is_render:
        print("🌐 Running on Render - Production Mode")
        # On Render, use production settings
        app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=False)
    else:
        print("💻 Running locally - Development Mode")
        # Local development
        app.run(debug=FLASK_DEBUG, host=FLASK_HOST, port=FLASK_PORT)