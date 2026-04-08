#!/bin/bash
# Smart Traffic Monitoring System - Deployment Script
# This script helps deploy the application to Render

echo "🚗 Smart Traffic Monitoring System - Render Deployment Guide"
echo "=========================================================="

# Check if required files exist
echo "📋 Checking deployment requirements..."

if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt not found!"
    exit 1
fi

if [ ! -f "Procfile" ]; then
    echo "❌ Procfile not found!"
    exit 1
fi

if [ ! -f "render.yaml" ]; then
    echo "❌ render.yaml not found!"
    exit 1
fi

if [ ! -f "app.py" ]; then
    echo "❌ app.py not found!"
    exit 1
fi

echo "✅ All required files present"

# Check model file
if [ ! -f "95_e/cls_fix_30e/weights/best.pt" ]; then
    echo "⚠️  Model file not found: 95_e/cls_fix_30e/weights/best.pt"
    echo "   Make sure to include your trained model in the deployment"
fi

echo ""
echo "📝 MANUAL DEPLOYMENT STEPS FOR RENDER:"
echo "======================================"
echo ""
echo "1. 📤 Push code to GitHub:"
echo "   git add ."
echo "   git commit -m 'Ready for Render deployment'"
echo "   git push origin main"
echo ""
echo "2. 🌐 Go to https://render.com and sign up/login"
echo ""
echo "3. ➕ Click 'New +' and select 'Web Service'"
echo ""
echo "4. 🔗 Connect your GitHub repository:"
echo "   - Search for: Smart_traffic_monitoring_system"
echo "   - Click 'Connect'"
echo ""
echo "5. ⚙️ Configure the web service:"
echo "   - Name: smart-traffic-monitor"
echo "   - Runtime: Python 3"
echo "   - Build Command: pip install -r requirements.txt"
echo "   - Start Command: gunicorn --bind 0.0.0.0:\$PORT app:app"
echo ""
echo "6. 🌍 Set Environment Variables:"
echo "   - FLASK_ENV: production"
echo "   - MODEL_PATH: ./95_e/cls_fix_30e/weights/best.pt"
echo "   - VIDEO_SOURCE: ./sample_video.mp4 (upload a sample video)"
echo "   - CONFIDENCE_THRESHOLD: 0.45"
echo "   - FRAME_SKIP_RATE: 5"
echo ""
echo "7. 💾 Upload your video file:"
echo "   - Go to Render dashboard"
echo "   - Your service → Settings → Disk"
echo "   - Upload your traffic video as 'sample_video.mp4'"
echo ""
echo "8. 🚀 Click 'Create Web Service'"
echo ""
echo "9. ⏳ Wait for deployment (5-15 minutes)"
echo ""
echo "10. 🌐 Access your dashboard at the provided URL"
echo ""

echo "🔧 TROUBLESHOOTING:"
echo "==================="
echo ""
echo "• If build fails: Check the logs in Render dashboard"
echo "• If model not found: Ensure model file is committed to Git"
echo "• If video not found: Upload video file to Render disk"
echo "• If memory issues: Increase FRAME_SKIP_RATE to 10"
echo "• If timeout: Reduce video resolution or use shorter clips"
echo ""

echo "💡 PRODUCTION TIPS:"
echo "==================="
echo ""
echo "• Use YOLOv8n model for faster inference"
echo "• Set FRAME_SKIP_RATE=5-10 to reduce CPU usage"
echo "• Monitor usage on Render free tier (750 hours/month)"
echo "• Consider upgrading to paid plan for 24/7 operation"
echo ""

echo "🎯 Your app will be live at: https://your-app-name.onrender.com"
echo ""
echo "Happy deploying! 🚗📊"