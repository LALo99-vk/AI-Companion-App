# AI-Companion-App
# Medy-Dobby: AI-Driven Medical Assistant

## 🚀 Overview
Medy-Dobby is an AI-driven healthcare mobile application built using **Ionic Capacitor**. The app predicts diseases based on user symptoms using a **Machine Learning model** and provides related information such as **medications, diets, workouts, precautions**, and more. It also includes emergency call functionality and medication reminders.

## 🏆 Features
- **Speech Recognition:** Accepts symptoms via speech input.
- **Disease Prediction:** Uses a **Flask-based API** to predict diseases from symptoms.
- **Text-to-Speech Output:** Speaks out the diagnosis and recommended treatments.
- **Image Analysis:** Analyzes medical images (e.g., wound detection) using an AI model.
- **Emergency Call System:** Detects trigger words (e.g., "Help") to call emergency contacts.
- **Medication Alerts:** Sends notifications to remind users to take medicine on time.
- **User Authentication:** Sign up and log in using Firebase authentication.

## 📌 Tech Stack
- **Frontend:** Ionic Capacitor, Angular
- **Backend:** Flask, FastAPI (for ML model integration)
- **Database:** Firebase
- **Machine Learning:** Python (Scikit-Learn, TensorFlow for Image Analysis)
- **Speech Recognition:** Web Speech API, Speech-to-Text API
- **Deployment:** Firebase Hosting (Frontend), Flask (Backend)

## 📂 Folder Structure
```
medy-dobby/
│── src/
│   ├── app/
│   │   ├── home/
│   │   ├── login/
│   │   ├── signup/
│   │   ├── tab1/ (Symptoms Input)
│   │   ├── tab2/ (Image Analysis)
│   │   ├── tab3/ (Emergency Calls)
│   │   ├── tabs/
│   ├── assets/
│   ├── environments/
│── backend/
│   ├── app.py  (Flask API for ML Model)
│   ├── model/
│── README.md
```

## 🔧 Installation & Setup
### Prerequisites
- Node.js & npm
- Ionic CLI (`npm install -g @ionic/cli`)
- Python (for backend)

### Frontend Setup
```bash
git clone https://github.com/yourusername/medy-dobby.git
cd medy-dobby
npm install
ionic serve
```

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python app.py
```

## 📱 Usage
1. Open the app and log in.
2. Navigate to the **Symptoms Tab** and enter symptoms via speech or text.
3. The app predicts the disease and speaks out the result.
4. Use the **Image Analysis** page to upload medical images for AI-based analysis.
5. The **Emergency Call System** will trigger calls when it detects danger words.

## 🚀 Deployment
### Deploy Frontend (Firebase Hosting)
```bash
ionic build
firebase deploy
```

### Deploy Backend (Flask)
Use any cloud provider (e.g., Heroku, Render, AWS):
```bash
git push heroku main
```

## 📜 License
This project is **open-source** and available under the MIT License.


## 🤝 Contributing
Pull requests are welcome! Open an issue for discussions.

---
✉️ **Contact:** [jharshav442@gmail.com] | 
