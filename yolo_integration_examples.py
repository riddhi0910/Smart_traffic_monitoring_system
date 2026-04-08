"""
YOLO Integration Example
=======================

This file demonstrates how to integrate YOLO object detection with the dashboard.
It's a reference implementation showing multiple approaches.

Choose the approach that fits your use case:
1. Video file processing
2. Webcam/real-time stream
3. Image file processing
"""

# ============================================================================
# APPROACH 1: YOLO + Video File Processing
# ============================================================================

"""
Install YOLO first:
    pip install ultralytics opencv-python

Then modify app.py:
"""

from ultralytics import YOLO
import cv2
from datetime import datetime

# Load YOLO model (yolov8n is lightweight, yolov8m/l/x for accuracy)
model = YOLO('yolov8n.pt')  # Download if not present
video_path = 'path/to/your/traffic_video.mp4'

# Global variable to store last detections
last_detections = []

def process_video_frame():
    """Process video frames and extract detections."""
    global last_detections
    
    cap = cv2.VideoCapture(video_path)
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Run YOLO inference
        results = model(frame)
        
        # Extract detected class names
        detected_classes = []
        if results[0].boxes:
            for cls in results[0].boxes.cls:
                class_name = model.names[int(cls)]
                detected_classes.append(class_name)
        
        # Store for API to use
        last_detections = detected_classes
        
        # Optional: visualize
        annotated_frame = results[0].plot()
        cv2.imshow('YOLO Detection', annotated_frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

"""
Then modify /data endpoint in app.py:

@app.route('/data')
def get_detection_data():
    # Use actual YOLO detections instead of mock
    detector.process_yolo_output(last_detections)
    
    vehicle_count = detector.get_vehicle_count()
    animal_detected = detector.has_animal()
    traffic_density = detector.calculate_traffic_density()
    
    return jsonify({
        'vehicle_count': vehicle_count,
        'animal_detected': animal_detected,
        'traffic_density': traffic_density,
        'timestamp': datetime.now().isoformat(),
        'detected_objects': detector.get_detected_objects(),
        'animal_types': detector.get_animal_types(),
    })
"""

# ============================================================================
# APPROACH 2: YOLO + Webcam/Real-Time Stream
# ============================================================================

"""
This approach uses threading to continuously process frames from webcam.

Install dependencies:
    pip install ultralytics opencv-python threading

Usage:
    detector = WebcamDetector()
    detector.start()  # Start processing in background
    
    Then in Flask app, detector.get_current_detections() returns latest frame detections
"""

import threading
import time

class WebcamDetector:
    """Real-time webcam detection with threading."""
    
    def __init__(self, model_name='yolov8n.pt', camera_id=0):
        self.model = YOLO(model_name)
        self.camera_id = camera_id
        self.current_detections = []
        self.running = False
        self.thread = None
    
    def _process_frames(self):
        """Process webcam frames continuously."""
        cap = cv2.VideoCapture(self.camera_id)
        
        while self.running:
            ret, frame = cap.read()
            if not ret:
                continue
            
            try:
                # Run inference
                results = self.model(frame, verbose=False)
                
                # Extract class names
                detected_classes = []
                if results[0].boxes:
                    for cls in results[0].boxes.cls:
                        class_name = self.model.names[int(cls)]
                        detected_classes.append(class_name)
                
                # Update current detections
                self.current_detections = detected_classes
                
                # Optional: show annotated frame
                # annotated = results[0].plot()
                # cv2.imshow('YOLO Webcam', annotated)
                # cv2.waitKey(1)
                
            except Exception as e:
                print(f"Error processing frame: {e}")
    
    def start(self):
        """Start detection thread."""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._process_frames, daemon=True)
            self.thread.start()
            print("Detector started")
    
    def stop(self):
        """Stop detection thread."""
        self.running = False
        if self.thread:
            self.thread.join()
        print("Detector stopped")
    
    def get_current_detections(self):
        """Get latest detections."""
        return self.current_detections.copy()

"""
Usage in app.py:

# At top of file
detector = WebcamDetector()
detector.start()  # Start in background

@app.route('/data')
def get_detection_data():
    # Get detections from webcam
    detections = detector.get_current_detections()
    detection_processor.process_yolo_output(detections)
    
    # ... rest of the code
"""

# ============================================================================
# APPROACH 3: YOLO + Image Processing
# ============================================================================

"""
For static images or image batches.
"""

from pathlib import Path

def process_single_image(image_path):
    """Process a single image with YOLO."""
    model = YOLO('yolov8n.pt')
    
    # Run inference
    results = model(image_path)
    
    # Extract detections
    detected_classes = []
    if results[0].boxes:
        for cls in results[0].boxes.cls:
            class_name = model.names[int(cls)]
            detected_classes.append(class_name)
    
    return detected_classes

def process_image_folder(folder_path):
    """Process all images in a folder."""
    model = YOLO('yolov8n.pt')
    
    image_detections = {}
    
    for image_file in Path(folder_path).glob('*.jpg'):
        results = model(str(image_file))
        
        detected_classes = []
        if results[0].boxes:
            for cls in results[0].boxes.cls:
                class_name = model.names[int(cls)]
                detected_classes.append(class_name)
        
        image_detections[image_file.name] = detected_classes
    
    return image_detections

# ============================================================================
# APPROACH 4: Custom YOLO with Confidence Filtering
# ============================================================================

"""
Filter detections by confidence score for more reliable results.
"""

class AdvancedYOLODetector:
    """YOLO detector with confidence filtering and class filtering."""
    
    def __init__(self, model_name='yolov8n.pt', confidence_threshold=0.5):
        self.model = YOLO(model_name)
        self.confidence_threshold = confidence_threshold
        
        # Define which classes to track
        self.target_classes = {
            'vehicles': ['car', 'motorcycle', 'bus', 'truck', 'bicycle'],
            'animals': ['cow', 'dog', 'cat', 'bird', 'horse'],
            'traffic': ['traffic light', 'stop sign', 'parking meter']
        }
    
    def detect(self, source):
        """
        Run detection on image/video/webcam.
        
        Args:
            source: image path, video path, or webcam ID (0)
        
        Returns:
            dict with detections organized by category
        """
        results = self.model(source)
        
        detections = {
            'vehicles': [],
            'animals': [],
            'traffic': [],
            'other': [],
            'confidence_scores': []
        }
        
        if results[0].boxes:
            for box_idx, (cls, conf) in enumerate(zip(
                results[0].boxes.cls, 
                results[0].boxes.conf
            )):
                class_name = self.model.names[int(cls)]
                confidence = float(conf)
                
                # Filter by confidence
                if confidence < self.confidence_threshold:
                    continue
                
                # Categorize detection
                detected = False
                for category, classes in self.target_classes.items():
                    if class_name.lower() in classes:
                        detections[category].append({
                            'class': class_name,
                            'confidence': confidence
                        })
                        detected = True
                        break
                
                if not detected:
                    detections['other'].append({
                        'class': class_name,
                        'confidence': confidence
                    })
        
        return detections

# ============================================================================
# INTEGRATION WITH FLASK APP
# ============================================================================

"""
Here's a complete example of integrating with your Flask app:

1. Replace the import in app.py:

    from yolo_integration import WebcamDetector
    from app import DetectionProcessor
    
2. Initialize detector in app.py:

    # At module level
    webcam_detector = WebcamDetector(model_name='yolov8n.pt')
    detection_processor = DetectionProcessor()
    
    @app.before_first_request
    def startup():
        webcam_detector.start()
    
    @app.teardown_appcontext
    def shutdown(exception):
        webcam_detector.stop()

3. Update /data endpoint:

    @app.route('/data')
    def get_detection_data():
        # Get current detections from webcam
        detections = webcam_detector.get_current_detections()
        
        # Process with detector
        detection_processor.process_yolo_output(detections)
        
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
        })
"""

# ============================================================================
# PERFORMANCE TIPS
# ============================================================================

"""
1. Model Selection:
   - yolov8n (nano) - fastest, lowest accuracy
   - yolov8s (small) - balanced
   - yolov8m (medium) - good accuracy
   - yolov8l/x - best accuracy, slowest

2. Inference Speed:
   - Resize large frames: frame = cv2.resize(frame, (640, 480))
   - Use GPU if available: model = YOLO('yolov8n.pt').to('cuda')
   - Skip frames: process every Nth frame instead of every frame

3. Threading:
   - Always use threading for real-time processing
   - Separate detection thread from Flask request handling

4. Memory:
   - Clear frame buffers regularly
   - Use context managers for file operations
   - Monitor GPU/CPU usage

Example optimized detector:

import torch

class OptimizedDetector:
    def __init__(self):
        self.model = YOLO('yolov8n.pt')
        
        # Use GPU if available
        if torch.cuda.is_available():
            self.model.to('cuda')
        
        self.frame_skip = 2  # Process every 2nd frame
        self.frame_count = 0
    
    def detect(self, frame):
        self.frame_count += 1
        
        # Skip frames for performance
        if self.frame_count % self.frame_skip != 0:
            return []
        
        # Resize for faster inference
        frame = cv2.resize(frame, (640, 480))
        
        # Run inference
        results = self.model(frame, verbose=False)
        
        detected_classes = []
        if results[0].boxes:
            for cls in results[0].boxes.cls:
                detected_classes.append(self.model.names[int(cls)])
        
        return detected_classes
"""
