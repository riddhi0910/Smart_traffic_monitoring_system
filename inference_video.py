import cv2
from ultralytics import YOLO
import os

# CONFIGURATION
MODEL_PATH = r"C:\Users\VICUTUS\OneDrive\文档\Desktop\DL LAB PROJECT 59 61\95_e\cls_fix_30e\weights\best.pt"
VIDEO_SOURCE = r"C:\Users\VICUTUS\OneDrive\文档\Desktop\DL LAB PROJECT 59 61\WhatsApp Video 2026-04-08 at 10.31.39 PM.mp4" # Use 0 for Webcam, or r"path\to\video.mp4" for file
CONF_THRESHOLD = 0.45

def run_inference():
    # 1. Load Model
    if not os.path.exists(MODEL_PATH):
        print(f"Error: Model not found at {MODEL_PATH}")
        # Try finding the latest run if best.pt isn't in that specific folder
        return

    print(f"Loading model: {MODEL_PATH}")
    model = YOLO(MODEL_PATH)

    # 2. Open Video Source
    cap = cv2.VideoCapture(VIDEO_SOURCE)
    if not cap.isOpened():
        print(f"Error: Could not open video source {VIDEO_SOURCE}")
        return

    print(f"Starting inference on {VIDEO_SOURCE}...")
    print("Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("End of video stream or error.")
            break

        # 3. Run YOLO Inference
        # imgsz should match training (640)
        results = model.predict(frame, conf=CONF_THRESHOLD, imgsz=640, verbose=False)

        # 4. Visualize Results
        annotated_frame = results[0].plot()

        # Display Result
        cv2.imshow("YOLOv8 Inference", annotated_frame)

        # Break on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Cleanup
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_inference()
