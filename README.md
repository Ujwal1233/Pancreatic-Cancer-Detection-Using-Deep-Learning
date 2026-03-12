# Pancreatic Cancer Detection and Diagnosis Using Deep Learning

## Overview
A comprehensive Flask web application for detecting and diagnosing pancreatic cancer from CT scan images using Convolutional Neural Networks (CNN). Features user/doctor authentication, admin dashboard, real-time predictions, custom diet recommendations, and more.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Git

### Installation
```bash
git clone https://github.com/Ujwal1233/Pancreatic-Cancer-Detection-Using-Deep-Learning.git
cd Pancreatic-Cancer-Detection-Using-Deep-Learning
python -m venv venv
# Windows
venv\\Scripts\\activate
# Linux/Mac
source venv/bin/activate
pip install -r requirements.txt
```

### Run the Application
```bash
python app.py
```
Open [http://localhost:5000](http://localhost:5000)

## 📋 Features
- **User Registration/Login**: Secure authentication
- **Doctor Portal**: View patient scans, approve/reject
- **Admin Dashboard**: Manage users/doctors with charts (gender, age, predictions)
- **Image Upload & Prediction**: Upload CT scans for instant cancer detection
- **Custom Diet Plans**: Personalized recommendations
- **Responsive UI**: Bootstrap-based modern interface

## 🏗️ Project Structure
```
.
├── app.py                    # Main Flask application
├── requirements.txt          # Dependencies
├── dataset/                  # Training images (cancerous/non_cancerous)
│   ├── cancerous/            # ~400 malignant CT scans
│   └── non_cancerous/        # ~220 benign CT scans
├── templates/                # HTML templates (login, dashboard, etc.)
├── static/                   # CSS, JS, images, uploads
├── utils/                    # Utility scripts (image processing, diet)
├── train_model.py           # Model training script
├── features_dataset.csv     # Extracted image features
└── README.md
```

## 🤖 Training Your Own Model
1. Extract features: `python feature_extraction.py`
2. Train: `python train_model.py`
3. Model saved as `pancreas_model.pkl`

## 📊 Demo Screenshots
*(Add screenshots of dashboard, prediction result)*

## 🔧 Development
- Database: SQLite (SQLAlchemy)
- ML Model: CNN + Feature Extraction
- Frontend: Bootstrap 5, Chart.js

## ⚠️ Disclaimer
**This is for educational and research purposes only. Not certified for clinical use. Always consult medical professionals for diagnosis.**

## 📝 License
MIT License

## 🤝 Contributing
Fork, PR welcome!

