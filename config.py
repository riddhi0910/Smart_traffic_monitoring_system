"""
Configuration settings for Smart Traffic Monitoring System
"""

import os
from pathlib import Path

# ============================================================================
# PATH CONFIGURATION
# ============================================================================

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.absolute()

# Model and data paths
MODEL_PATH = os.getenv(
    'MODEL_PATH',
    str(PROJECT_ROOT / "95_e" / "cls_fix_30e" / "weights" / "best.pt")
)

VIDEO_SOURCE = os.getenv(
    'VIDEO_SOURCE',
    str(PROJECT_ROOT / "WhatsApp Video 2026-04-08 at 10.31.39 PM.mp4")
)

# ============================================================================
# DETECTION CONFIGURATION
# ============================================================================

# YOLO detection settings
CONFIDENCE_THRESHOLD = float(os.getenv('CONFIDENCE_THRESHOLD', '0.45'))
FRAME_SKIP_RATE = int(os.getenv('FRAME_SKIP_RATE', '3'))  # Process every Nth frame

# Detection classes
VEHICLE_CLASSES = {'car', 'motorcycle', 'bus', 'truck', 'bicycle', 'vehicle'}
ANIMAL_CLASSES = {'cow', 'dog', 'cat', 'bird', 'horse', 'animal'}
TRAFFIC_CLASSES = {'traffic_light', 'barrier', 'stop_sign', 'traffic_sign'}

# ============================================================================
# FLASK CONFIGURATION
# ============================================================================

# Flask settings
FLASK_HOST = os.getenv('FLASK_HOST', '127.0.0.1')
FLASK_PORT = int(os.getenv('FLASK_PORT', '5000'))
FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'

# ============================================================================
# TRAFFIC DENSITY THRESHOLDS
# ============================================================================

TRAFFIC_THRESHOLDS = {
    'low': int(os.getenv('TRAFFIC_LOW_THRESHOLD', '2')),
    'medium': int(os.getenv('TRAFFIC_MEDIUM_THRESHOLD', '5')),
    # High is anything above medium threshold
}

# ============================================================================
# DASHBOARD CONFIGURATION
# ============================================================================

DASHBOARD_REFRESH_INTERVAL = int(os.getenv('DASHBOARD_REFRESH_INTERVAL', '1000'))  # milliseconds

# ============================================================================
# VALIDATION
# ============================================================================

def validate_config():
    """Validate configuration settings."""
    errors = []

    # Check model file exists
    if not os.path.exists(MODEL_PATH):
        errors.append(f"Model file not found: {MODEL_PATH}")

    # Check video source exists (skip for webcam)
    if VIDEO_SOURCE != '0' and not os.path.exists(VIDEO_SOURCE):
        errors.append(f"Video source not found: {VIDEO_SOURCE}")

    # Validate thresholds
    if TRAFFIC_THRESHOLDS['low'] >= TRAFFIC_THRESHOLDS['medium']:
        errors.append("Low threshold must be less than medium threshold")

    return errors

def print_config():
    """Print current configuration."""
    print("=" * 50)
    print("SMART TRAFFIC MONITORING CONFIGURATION")
    print("=" * 50)
    print(f"Model Path: {MODEL_PATH}")
    print(f"Video Source: {VIDEO_SOURCE}")
    print(f"Confidence Threshold: {CONFIDENCE_THRESHOLD}")
    print(f"Frame Skip Rate: {FRAME_SKIP_RATE}")
    print(f"Flask Host: {FLASK_HOST}")
    print(f"Flask Port: {FLASK_PORT}")
    print(f"Debug Mode: {FLASK_DEBUG}")
    print(f"Traffic Thresholds: Low≤{TRAFFIC_THRESHOLDS['low']}, Medium≤{TRAFFIC_THRESHOLDS['medium']}")
    print("=" * 50)

if __name__ == "__main__":
    # Validate and print config when run directly
    errors = validate_config()
    if errors:
        print("Configuration Errors:")
        for error in errors:
            print(f"  - {error}")
        exit(1)
    else:
        print_config()
        print("✅ Configuration is valid!")