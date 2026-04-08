# 🚗 Smart Traffic Monitoring System

A real-time traffic monitoring dashboard built with Flask and YOLO object detection. Monitor vehicle counts, traffic density, and animal detection alerts through an intuitive web interface.

![Dashboard Preview](https://via.placeholder.com/800x400/667eea/ffffff?text=Traffic+Monitoring+Dashboard)

## ✨ Features

- **Real-Time YOLO Detection**: Live object detection using YOLOv8
- **Traffic Density Monitoring**: Color-coded traffic levels (Low/Medium/High)
- **Animal Detection Alerts**: Warning system for road hazards
- **Video Upload & Management**: Upload your own videos through the web interface
- **Dynamic Video Switching**: Switch between different uploaded videos instantly
- **Responsive Dashboard**: Works on desktop, tablet, and mobile
- **Auto-Refresh**: Updates every second with live data
- **Modular Architecture**: Easy to extend and customize

## 🎯 Dashboard Metrics

- **Vehicle Count**: Live count of detected vehicles
- **Traffic Density**: Visual status with color coding
- **Animal Alerts**: Warning when animals detected on road
- **Detection Objects**: Categorized list of all detected items
- **Last Update**: Timestamp of latest detection

## 📤 Video Upload & Management

The dashboard now supports uploading and managing your own video files:

### Upload Features
- **File Upload**: Upload MP4, AVI, MOV, MKV, WebM, M4V files (max 500MB)
- **Real-time Processing**: Videos are processed immediately after upload
- **Progress Feedback**: Visual upload progress and status messages
- **File Validation**: Automatic format and size validation

### Video Management
- **Video Library**: View all uploaded videos with file details
- **Instant Switching**: Switch between videos without restarting
- **Active Video Indicator**: See which video is currently being processed
- **File Information**: View file size and upload status for each video

### How to Use
1. Click "Choose File" in the upload section
2. Select your video file (supported formats listed above)
3. Click "Upload & Switch Video"
4. The system will automatically switch to processing your uploaded video
5. Use the video list to switch between different uploaded videos

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Webcam or video file for detection
- Trained YOLO model (included in project)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/riddhi0910/Smart_traffic_monitoring_system.git
   cd Smart_traffic_monitoring_system
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your model and video paths** (in `app.py`)
   ```python
   MODEL_PATH = r"path/to/your/model.pt"
   VIDEO_SOURCE = r"path/to/your/video.mp4"  # or 0 for webcam
   ```

5. **Run the dashboard**
   ```bash
   python app.py
   ```

6. **Open in browser**
   ```
   http://localhost:5000
   ```

## 📁 Project Structure

```
Smart_traffic_monitoring_system/
├── app.py                          # Flask backend with YOLO integration
├── requirements.txt                # Python dependencies
├── inference_video.py              # Standalone YOLO inference script
├── yolo_integration_examples.py    # Integration examples
├── templates/
│   └── index.html                  # Dashboard UI + JavaScript
├── static/
│   └── style.css                   # Dashboard styling
├── 95_e/                          # YOLO training results
│   └── cls_fix_30e/
│       └── weights/
│           └── best.pt            # Trained model weights
├── .gitignore                     # Git ignore rules
└── README.md                      # This file
```

## 🔧 Configuration

### Model Configuration

Update these paths in `app.py`:

```python
# Your trained YOLO model
MODEL_PATH = r"C:\path\to\your\model.pt"

# Video source (file path or 0 for webcam)
VIDEO_SOURCE = r"C:\path\to\your\video.mp4"

# Detection confidence threshold
CONF_THRESHOLD = 0.45
```

### Detection Classes

The system is configured for traffic monitoring with these categories:

```python
VEHICLE_CLASSES = {'car', 'motorcycle', 'bus', 'truck', 'bicycle'}
ANIMAL_CLASSES = {'cow', 'dog', 'cat', 'bird', 'horse'}
TRAFFIC_CLASSES = {'traffic_light', 'barrier', 'stop_sign'}
```

## 🎨 Dashboard Features

### Real-Time Updates
- Auto-refreshes every 1 second
- Smooth animations on data changes
- Color-coded traffic density indicators

### Responsive Design
- Mobile-friendly interface
- Card-based layout
- Emoji icons for quick recognition

### Alert System
- Red alerts for animal detection
- Traffic density warnings
- Visual and textual notifications

## 🔍 API Endpoints

### GET `/`
Serves the dashboard HTML page

### GET `/data`
Returns current detection metrics
```json
{
  "vehicle_count": 5,
  "animal_detected": true,
  "traffic_density": "Medium",
  "timestamp": "2024-04-09T15:30:45.123456",
  "detected_objects": {
    "vehicles": ["car", "car", "truck"],
    "animals": ["cow"],
    "traffic_infrastructure": ["traffic_light"]
  },
  "yolo_active": true
}
```

### GET `/health`
Health check endpoint
```json
{
  "status": "ok",
  "yolo_active": true,
  "model_loaded": true,
  "video_source": "path/to/video.mp4",
  "model_path": "path/to/model.pt"
}
```

## 🛠️ Development

### Adding New Detection Classes

1. Update class sets in `DetectionProcessor`:
```python
VEHICLE_CLASSES = {'car', 'motorcycle', 'your_new_class'}
```

2. Update emoji mapping in `templates/index.html`:
```javascript
const emojiMap = {
    'car': '🚗',
    'your_new_class': '🔧'
};
```

### Customizing Traffic Density Logic

Modify `calculate_traffic_density()` in `app.py`:

```python
def calculate_traffic_density(self) -> str:
    vehicle_count = self.get_vehicle_count()

    if vehicle_count <= 3:      # Custom threshold
        return "Low"
    elif vehicle_count <= 7:    # Custom threshold
        return "Medium"
    else:
        return "High"
```

## 🚀 Deployment on Render

### Quick Deploy

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Deploy on Render**
   - Go to [render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - Configure:
     - **Runtime**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT app:app`

3. **Set Environment Variables**
   ```
   FLASK_ENV=production
   MODEL_PATH=./95_e/cls_fix_30e/weights/best.pt
   VIDEO_SOURCE=./sample_video.mp4
   CONFIDENCE_THRESHOLD=0.45
   FRAME_SKIP_RATE=5
   ```

4. **Upload Video File**
   - In Render dashboard → Your service → Settings → Disk
   - Upload your traffic video as `sample_video.mp4`

### Detailed Guide

Run the deployment script for step-by-step instructions:
```bash
chmod +x deploy.sh
./deploy.sh
```

### Production Considerations

- **Free Tier Limits**: 750 hours/month, may sleep after inactivity
- **Performance**: Set `FRAME_SKIP_RATE=5-10` for production
- **Model Size**: YOLOv8n recommended for faster inference
- **Video Upload**: Use Render's disk storage for video files

### Troubleshooting Deployment

**Build Fails**
- Check logs in Render dashboard
- Ensure all dependencies are in `requirements.txt`
- Verify Python version compatibility

**Model Not Found**
- Ensure model file is committed to Git
- Check `MODEL_PATH` environment variable
- Verify file path in repository

**Video Not Loading**
- Upload video to Render disk storage
- Update `VIDEO_SOURCE` environment variable
- Use shorter video clips for testing

**Memory Issues**
- Increase `FRAME_SKIP_RATE`
- Use smaller YOLO model
- Reduce video resolution

## 📊 Performance Optimization

- **Frame Skipping**: Processes every 3rd frame for better performance
- **Threading**: YOLO detection runs in background thread
- **Model Selection**: Use YOLOv8n for fastest inference
- **GPU Support**: Enable CUDA for GPU acceleration

## 🐛 Troubleshooting

### Dashboard Not Loading
```bash
# Check Flask server
python app.py

# Check API endpoint
curl http://localhost:5000/health
```

### YOLO Model Not Found
- Verify model path in `app.py`
- Check file permissions
- Ensure model is compatible with ultralytics

### Video Not Playing
- Check video file path
- Verify video codec compatibility
- Use webcam: `VIDEO_SOURCE = 0`

### Low Performance
- Reduce frame processing frequency
- Use smaller YOLO model (yolov8n)
- Enable GPU acceleration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Ultralytics YOLO](https://github.com/ultralytics/ultralytics) for object detection
- [Flask](https://flask.palletsprojects.com/) for web framework
- [OpenCV](https://opencv.org/) for computer vision

## 📞 Support

For questions or issues:
- Open an issue on GitHub
- Check the troubleshooting section
- Review the API documentation

---

**Made with ❤️ for safer roads**#   S m a r t _ t r a f f i c _ m o n i t o r i n g _ s y s t e m 
 
 