from flask import Flask, render_template, jsonify
from datetime import datetime
import random
from typing import List, Dict, Tuple

app = Flask(__name__)

# ============================================================================
# DETECTION DATA MODULE - Structure for easy YOLO integration
# ============================================================================

class DetectionProcessor:
    """
    Processes raw detection data from YOLO or mock sources.
    Easy to replace mock_detection() with actual YOLO output later.
    """
    
    VEHICLE_CLASSES = {'car', 'motorcycle', 'bus', 'truck'}
    ANIMAL_CLASSES = {'cow', 'dog', 'cat', 'bird'}
    TRAFFIC_CLASSES = {'traffic_light', 'barrier', 'stop_sign'}
    
    def __init__(self):
        self.current_detections = []
    
    def mock_detection(self) -> List[str]:
        """
        Simulates YOLO detection output.
        Replace this with actual YOLO inference output.
        
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
# GLOBAL DETECTOR INSTANCE
# ============================================================================

detector = DetectionProcessor()


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
        - timestamp: str (ISO format)
        - detected_objects: dict (optional, for frontend display)
    """
    # Get mock or real detection data
    detector.mock_detection()
    # For YOLO integration, comment out mock_detection() and use:
    # detector.process_yolo_output(your_yolo_results)
    
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


@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({'status': 'ok'})


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    # Run Flask in debug mode for development
    # Set debug=False for production
    app.run(debug=True, host='127.0.0.1', port=5000)
