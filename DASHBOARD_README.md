# Real-Time Traffic Monitoring Dashboard

A simple yet powerful Flask-based web dashboard for real-time traffic monitoring using YOLO object detection.

## Features

✅ **Real-Time Vehicle Counting** - Live count of detected vehicles  
✅ **Traffic Density Monitoring** - Color-coded traffic levels (Low/Medium/High)  
✅ **Animal Detection Alerts** - Warning system when animals (e.g., cows) are detected  
✅ **Live Object Detection Display** - Lists all detected vehicles, animals, and traffic infrastructure  
✅ **Auto-Refresh Dashboard** - Updates every 1 second via JavaScript fetch  
✅ **Responsive Design** - Works on desktop, tablet, and mobile devices  
✅ **Modular Architecture** - Easy YOLO integration  

## Project Structure

```
├── app.py                          # Flask backend with detection logic
├── requirements_dashboard.txt       # Python dependencies
├── templates/
│   └── index.html                  # Dashboard HTML + JavaScript
└── static/
    └── style.css                   # Dashboard styling
```

## Installation & Setup

### 1. Install Dependencies

```bash
pip install -r requirements_dashboard.txt
```

Or install manually:
```bash
pip install Flask==2.3.3 Werkzeug==2.3.7
```

### 2. Run the Dashboard

```bash
python app.py
```

The dashboard will be available at: `http://localhost:5000`

### 3. Open in Browser

Navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000) to view the live dashboard.

## How It Works

### Backend (`app.py`)

**DetectionProcessor Class** - Handles all detection logic:
- `mock_detection()` - Generates simulated detection data (for testing)
- `process_yolo_output(detections)` - Accepts real YOLO detection results
- Calculates vehicle count, animal detection status, and traffic density
- Returns organized object categories

**API Endpoints:**
- `GET /` - Serves the dashboard HTML
- `GET /data` - Returns JSON with current detection metrics
- `GET /health` - Health check endpoint

### Frontend (`index.html` + `style.css`)

**Auto-Refresh System:**
- Fetches `/data` every 1 second
- Updates all metrics in real-time
- Smooth animations for data changes

**Display Elements:**
1. **Vehicle Count Card** - Shows total vehicles detected
2. **Traffic Density Card** - Color-coded (Green/Yellow/Red)
3. **Animal Alert Card** - Warning when animals detected
4. **Timestamp Card** - Last update time
5. **Objects List** - Categorized detected objects with counts

## Integration with YOLO

### Step 1: Modify `DetectionProcessor.process_yolo_output()`

In `app.py`, after running YOLO inference:

```python
# Example with YOLOv8
from ultralytics import YOLO

model = YOLO('yolov8n.pt')

@app.route('/data')
def get_detection_data():
    # Read frame or video
    frame = ... # your frame source
    
    # Run YOLO inference
    results = model(frame)
    
    # Extract class names
    detected_classes = [model.names[int(cls)] for cls in results[0].boxes.cls]
    
    # Process with detector
    detector.process_yolo_output(detected_classes)
    
    # Return results
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
```

### Step 2: Update Detection Classes

Edit the class definitions in `DetectionProcessor`:

```python
VEHICLE_CLASSES = {'car', 'motorcycle', 'bus', 'truck', 'your_class'}
ANIMAL_CLASSES = {'cow', 'dog', 'cat', 'bird', 'your_animal'}
TRAFFIC_CLASSES = {'traffic_light', 'barrier', 'stop_sign', 'your_infrastructure'}
```

### Step 3: Connect Your Video Source

Replace `mock_detection()` call or add video processing:

```python
@app.route('/data')
def get_detection_data():
    # Option 1: Use mock data (current - for testing)
    detector.mock_detection()
    
    # Option 2: Process actual video frames
    # frame = capture_next_frame()  # From your video source
    # results = yolo_model.detect(frame)
    # detector.process_yolo_output(results.class_names)
    
    ...
```

## Configuration

### Adjust Refresh Rate

In `templates/index.html`, change `REFRESH_INTERVAL`:

```javascript
const REFRESH_INTERVAL = 1000;  // 1 second (change this)
// 500 = 0.5 seconds (more frequent)
// 2000 = 2 seconds (less frequent)
```

### Adjust Traffic Density Thresholds

In `app.py`, modify `calculate_traffic_density()`:

```python
def calculate_traffic_density(self) -> str:
    vehicle_count = self.get_vehicle_count()
    
    if vehicle_count <= 2:      # Change threshold
        return "Low"
    elif vehicle_count <= 5:    # Change threshold
        return "Medium"
    else:
        return "High"
```

### Change Detection Classes

Modify class sets in `DetectionProcessor.__init__()`:

```python
VEHICLE_CLASSES = {'car', 'motorcycle', ...}
ANIMAL_CLASSES = {'cow', 'dog', ...}
TRAFFIC_CLASSES = {'traffic_light', 'barrier', ...}
```

## API Response Example

```json
{
  "vehicle_count": 5,
  "animal_detected": true,
  "traffic_density": "Medium",
  "timestamp": "2024-04-09T15:30:45.123456",
  "detected_objects": {
    "vehicles": ["car", "car", "motorcycle", "truck", "bus"],
    "animals": ["cow"],
    "traffic_infrastructure": ["traffic_light", "barrier"]
  },
  "animal_types": ["cow"]
}
```

## Customization Ideas

- **Add confidence scores** - Display detection confidence in object list
- **Add historical data** - Store metrics in database for trend analysis
- **Add alerts** - Send notifications on high traffic or animal detection
- **Add multiple camera support** - Display multiple feeds on dashboard
- **Add filters** - Filter by detection type in the dashboard
- **Add export** - Download detection data as CSV/JSON
- **Add threshold settings** - Configure density thresholds via UI

## Performance Tips

1. **Handle video source efficiently** - Process frames at appropriate FPS
2. **Cache YOLO model** - Load model once, reuse for multiple frames
3. **Optimize detection frequency** - Adjust refresh rate based on needs
4. **Use lighter YOLO models** - For real-time performance (yolov8n, yolov8s)

## Troubleshooting

**Issue: Dashboard not updating**
- Check browser console (F12) for JavaScript errors
- Verify Flask server is running: `python app.py`
- Check API endpoint: visit `http://localhost:5000/data`

**Issue: Port 5000 already in use**
- Change in `app.py`: `app.run(port=8080)`
- Or kill process using port 5000

**Issue: YOLO integration not working**
- Verify YOLO model outputs correct class names
- Check detection class names match `VEHICLE_CLASSES`, etc.
- Print detected objects for debugging

## License

MIT License - Feel free to use and modify!

## Next Steps

1. Connect actual YOLO video source
2. Add database for historical tracking
3. Build admin panel for settings
4. Add email/SMS alerts
5. Deploy to production server
