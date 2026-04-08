# Quick Start Guide - Traffic Monitoring Dashboard

## ⚡ Start in 3 Steps

### Step 1: Install Flask

```bash
pip install -r requirements_dashboard.txt
```

Or manually:
```bash
pip install Flask
```

### Step 2: Run the Dashboard

```bash
python app.py
```

You should see:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

### Step 3: Open in Browser

Visit: **http://localhost:5000**

That's it! You should see the live dashboard with:
- ✅ Vehicle count (updating randomly)
- ✅ Traffic density (Low/Medium/High)
- ✅ Animal detection alerts
- ✅ Auto-refresh every 1 second

---

## File Overview

| File | Purpose |
|------|---------|
| `app.py` | Flask backend with detection logic |
| `templates/index.html` | Dashboard UI + JavaScript |
| `static/style.css` | Dashboard styling |
| `requirements_dashboard.txt` | Python dependencies |
| `yolo_integration_examples.py` | YOLO integration reference |
| `DASHBOARD_README.md` | Full documentation |

---

## What You'll See

### Dashboard Metrics

1. **Total Vehicles** - Count of cars, motorcycles, buses, trucks
2. **Traffic Density** - Visual status with color coding
   - 🟢 Green: Low (0-2 vehicles)
   - 🟡 Yellow: Medium (3-5 vehicles)  
   - 🔴 Red: High (6+ vehicles)
3. **Animal Alert** - Shows if any animals (cow, dog, etc.) detected
4. **Last Update** - Timestamp of last detection update
5. **Detected Objects** - Lists all detected items by category

### Mock Data

Currently using simulated data that:
- Detects 2-8 random vehicles per frame
- Has 30% chance of animal detection
- Includes traffic infrastructure (lights, barriers)
- Updates every 1 second

---

## Testing Different Scenarios

### High Traffic

Open browser console (F12 → Console) and run:
```javascript
// This will force update to show High traffic
fetch('/data').then(r => r.json()).then(d => console.log(d));
```

Refresh the page a few times to see different traffic levels.

### Manual Testing

Visit API directly: `http://localhost:5000/data`

You'll see JSON response like:
```json
{
  "vehicle_count": 5,
  "animal_detected": false,
  "traffic_density": "Medium",
  "timestamp": "2024-04-09T15:30:45.123456",
  "detected_objects": {
    "vehicles": ["car", "car", "truck"],
    "animals": [],
    "traffic_infrastructure": ["traffic_light"]
  }
}
```

---

## Integration with YOLO

When ready to connect real YOLO detections:

1. See `yolo_integration_examples.py` for reference implementations
2. Key steps:
   - Load YOLO model: `model = YOLO('yolov8n.pt')`
   - Get detections: `results = model(frame)`
   - Extract classes: `[model.names[int(cls)] for cls in results[0].boxes.cls]`
   - Pass to detector: `detector.process_yolo_output(detected_classes)`

3. Modify `/data` endpoint in `app.py` to use real detections instead of `mock_detection()`

---

## Troubleshooting

### Dashboard Not Loading?
- Make sure Flask is running: `python app.py`
- Check URL: `http://localhost:5000` (not `127.0.0.1:5000`)
- Check browser console for errors (F12 → Console)

### Port Already in Use?
Edit `app.py`, change:
```python
app.run(debug=True, host='127.0.0.1', port=5000)
```
To:
```python
app.run(debug=True, host='127.0.0.1', port=8080)
```
Then visit `http://localhost:8080`

### Data Not Updating?
- Check the `/data` endpoint: visit `http://localhost:5000/data`
- Look for JavaScript errors in browser console (F12)
- Check Flask console for errors

### Want Different Refresh Rate?
Edit `templates/index.html`, find:
```javascript
const REFRESH_INTERVAL = 1000;  // milliseconds
```
Change to:
- `500` = updates 2x per second
- `2000` = updates every 2 seconds

---

## Next Steps

1. **Test with Mock Data** ← You are here
2. Install YOLO: `pip install ultralytics opencv-python`
3. Connect video source (see `yolo_integration_examples.py`)
4. Customize detection classes and thresholds
5. Add database for historical tracking
6. Deploy to production

---

## Key Files to Modify for YOLO

### `app.py`
- Change `detector.mock_detection()` to use real YOLO output
- Update class definitions in `DetectionProcessor.__init__()`

### `templates/index.html`
- Optional: Add more metrics, charts, or alerts
- Adjust refresh rate as needed

### `static/style.css`
- Customize colors, fonts, layout
- Add your brand colors and styling

---

## API Documentation

### GET `/data`
Returns current detection metrics.

**Response:**
```json
{
  "vehicle_count": 5,
  "animal_detected": true,
  "traffic_density": "Medium",
  "timestamp": "2024-04-09T15:30:45.123456",
  "detected_objects": {
    "vehicles": ["car", "motorcycle", "truck"],
    "animals": ["cow"],
    "traffic_infrastructure": ["traffic_light", "barrier"]
  },
  "animal_types": ["cow"]
}
```

### GET `/health`
Health check endpoint.

**Response:**
```json
{"status": "ok"}
```

---

## Project Statistics

- **Python Files:** 2 (app.py, yolo_integration_examples.py)
- **Frontend:** 1 HTML + 1 CSS file
- **Lines of Code:** ~600 (backend + frontend)
- **Dependencies:** Flask only (for base installation)
- **Setup Time:** < 2 minutes

---

## Architecture

```
┌─────────────────────────────────────────┐
│      Browser / Frontend (index.html)   │
│  ────────────────────────────────────  │
│  • Dashboard UI (cards, metrics)       │
│  • JavaScript (auto-refresh, updates)  │
│  • CSS (styling, animations)           │
└──────────────┬──────────────────────────┘
               │ fetch('/data')
               ↓ (every 1 second)
┌─────────────────────────────────────────┐
│    Flask API (app.py)                  │
│  ────────────────────────────────────  │
│  • GET /data - returns JSON metrics    │
│  • GET / - serves dashboard HTML       │
│  • GET /health - health check          │
└──────────────┬──────────────────────────┘
               │ DetectionProcessor
               ↓
┌─────────────────────────────────────────┐
│  Detection Logic (app.py)              │
│  ────────────────────────────────────  │
│  • mock_detection() - test data        │
│  • process_yolo_output() - real YOLO   │
│  • calculate_traffic_density()         │
│  • get_vehicle_count()                 │
│  • has_animal_detected()               │
└─────────────────────────────────────────┘
```

---

**Happy Monitoring! 🚗📊**
