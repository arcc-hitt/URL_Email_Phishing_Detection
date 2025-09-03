# URL & Email Phishing Detection

## Overview
This repository contains the implementation of a **real-time phishing detection system** designed to analyze **emails and URLs** for potential phishing threats. The system leverages **machine learning models**, integrates with **Gmail API**, and provides a user-friendly interface.

## System Architecture
The system consists of the following major components:

### 1. Backend API
- **Technology**: Flask-based backend
- **Functions**:
  - Handles requests and integrates with machine learning models.
  - Communicates with the frontend to deliver real-time phishing detection results.

### 2. Machine Learning Models
#### **Email Analysis**
- **LightGBM** for phishing classification.
- **Autoencoder** for anomaly detection in email features.

#### **URL Analysis**
- **XGBoost** for phishing classification.
- **Autoencoder** for detecting anomalous URL features.

### 3. Frontend
- **Technology**: Angular-based interface.
- **Features**:
  - Manual email and URL phishing checks.
  - Real-time email analysis using Gmail API.
  - Visual indicators and detailed insights on phishing threats.

### 4. Gmail Integration
- **Technology**: Gmail API
- **Functions**:
  - Fetches emails in real-time.
  - Extracts key features and sends them for phishing analysis.
  - Displays results with phishing probability and anomaly scores.

## Methodology
### 1. Data Preprocessing
#### **Email Data**
- Feature extraction: sender, receiver, subject, body.
- NLP techniques: tokenization, stopword removal, stemming/lemmatization.
- Text vectorization: TF-IDF or BERT-based embeddings.

#### **URL Data**
- Feature extraction: domain, URL length, lexical analysis.
- Handling missing values and normalizing features.

### 2. Model Training
#### **Email Phishing Detection**
- **LightGBM**: Trained on labeled email data for classification.
- **Autoencoder**: Learns normal email patterns and detects anomalies.

#### **URL Phishing Detection**
- **XGBoost**: Trained on labeled URL data for phishing probability prediction.
- **Autoencoder**: Detects anomalous URL patterns.

### 3. Model Integration
For both **email** and **URL** analysis:
- Combine classification model score and autoencoder anomaly score.
- Final decision is based on a **weighted combination** of both scores.

### 4. API Development
- **Flask-based REST API**
- **Endpoints**:
  - **Email Analysis**: Accepts email payload and returns phishing predictions.
  - **URL Analysis**: Accepts a URL and returns a phishing probability score.
- Handles preprocessing, model inference, and result aggregation.

### 5. Frontend Development
- **Angular-based UI**
- Features:
  - Email input form for manual checks.
  - URL input form for phishing detection.
  - Gmail integration for real-time email analysis.
  - Displays phishing probability, anomaly scores, and alerts.

### 6. Real-Time Gmail Integration
- Uses Gmail API for email fetching and analysis.
- Implements OAuth 2.0 for authentication.
- Processes emails and extracts features for phishing detection.
- Sends results back to the frontend with detailed insights.

## Installation & Setup
### 1. Clone the Repository
```sh
git clone https://github.com/arcc-hitt/URL_Email_Phishing_Detection.git
cd URL_Email_Phishing_Detection
```

### 2. Setup Backend (Flask API)
#### **Install Dependencies**
```sh
pip install -r requirements.txt
```
#### **Run the API Server**
```sh
python app.py
```

### 3. Setup Frontend (Angular UI)
#### **Install Dependencies**
```sh
cd frontend
npm install
```
#### **Run the Frontend Server**
```sh
ng serve
```

### 4. Gmail API Configuration
- Enable **Gmail API** in Google Cloud Console.
- Configure OAuth 2.0 credentials.
- Store authentication keys securely.

## Usage
- **Manual Analysis**: Enter an email or URL in the frontend for phishing detection.
- **Gmail Integration**: Authenticate with Gmail and analyze emails in real-time.
- **View Results**: Check phishing probability scores and anomaly warnings.

## Contributing
Contributions are welcome! Feel free to submit issues or pull requests.

## Contact
For any queries or support, please open an issue in the repository.
