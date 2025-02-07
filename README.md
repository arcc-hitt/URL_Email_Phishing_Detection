# URL and Email Phishing Detection System

This repository contains the implementation of a real-time phishing detection system designed to identify phishing attempts in email content and URLs. The system integrates machine learning models with a user-friendly interface for seamless interaction.

## Table of Contents
- [Problem Statement](#problem-statement)
- [System Architecture](#system-architecture)
- [Methodology](#methodology)
  - [Data Preprocessing](#data-preprocessing)
  - [Model Training](#model-training)
  - [Model Integration](#model-integration)
  - [API Development](#api-development)
  - [Frontend Development](#frontend-development)
  - [Real-Time Gmail Integration](#real-time-gmail-integration)
- [Deployment](#deployment)
- [Evaluation](#evaluation)

## Problem Statement
The goal of this project is to develop a real-time phishing detection system that can identify phishing attempts in email content and URLs. The system will integrate machine learning models and provide a user-friendly interface for seamless interaction.

## System Architecture
The system consists of the following major components:

- **Backend API**: A Flask-based backend to handle requests, integrate with ML models, and communicate with the frontend.
- **Machine Learning Models**:
  - **Email Analysis**: Combines LightGBM for classification and an autoencoder for anomaly detection.
  - **URL Analysis**: Utilizes XGBoost for classification and an autoencoder for detecting anomalous URL features.
- **Frontend**: An Angular-based interface for user interaction.
- **Integration with Gmail**: Real-time email access and analysis using Gmail API.

## Methodology

### Data Preprocessing

#### Email Data:
- Extract features such as sender, receiver, subject, and body.
- Clean and preprocess text using natural language processing (NLP) techniques like tokenization, stopword removal, and stemming/lemmatization.
- Encode categorical features and vectorize text using TF-IDF or embeddings (e.g., BERT-based features).

#### URL Data:
- Extract features such as domain, URL length, and lexical analysis of the URL.
- Handle missing values and normalize features to standardize inputs for models.

### Model Training

#### Email Phishing Detection:
- Train a LightGBM model on labeled email data to classify emails as phishing or safe.
- Train an autoencoder to learn normal patterns in email features and detect anomalies.

#### URL Phishing Detection:
- Train an XGBoost model on labeled URL data for phishing probability prediction.
- Train an autoencoder to detect anomalous patterns in URL features.

### Model Integration
Combine outputs of both models for each component:

#### Email Analysis:
- LightGBM provides a classification score.
- Autoencoder computes an anomaly score for email content.
- Final decision: A weighted combination of classification and anomaly scores.

#### URL Analysis:
- XGBoost provides a phishing probability score.
- Autoencoder computes an anomaly score for URL features.
- Final decision: A weighted combination of classification and anomaly scores.

### API Development
Use Flask to create RESTful endpoints for real-time predictions:

- **Email Analysis Endpoint**: Accepts email payloads (sender, receiver, date, subject, body, URLs) and returns phishing predictions.
- **URL Analysis Endpoint**: Accepts a URL and returns a phishing probability score.

Implement preprocessing, model inference, and result aggregation within Flask services.

### Frontend Development
Use Angular for building a user-friendly interface:

- Email input form for manual phishing checks.
- Integration with Gmail API for real-time email fetching and analysis.
- URL input form for phishing detection.
- Display results with detailed insights:
  - Email phishing probability, anomaly score, and decision.
  - URL phishing probability, anomaly score, and decision.
- Implement notification systems and visual cues for phishing warnings.

### Real-Time Gmail Integration
- Use the Gmail API to fetch user emails in real time.
- Provide user authentication via OAuth 2.0.
- Process fetched emails:
  - Extract features (sender, receiver, date, subject, body, URLs).
  - Send data to the backend API for analysis.
  - Return phishing detection results to the frontend.

## Deployment

- **Backend**: Deploy Flask APIs on a cloud platform (e.g., AWS, Azure, or Heroku).
- **Frontend**: Host the Angular application on a web server or cloud hosting service.
- **Database**: Use a database (e.g., MongoDB or MySQL) for logging phishing results, user feedback, and other metrics.

## Evaluation
Measure the performance of individual models using metrics like accuracy, precision, recall, F1-score, and AUC-ROC.

Evaluate the combined model's effectiveness in terms of:

- Overall detection accuracy.
- False positive and false negative rates.
- Response time for real-time requests.


This methodology outlines a robust and scalable approach to real-time phishing detection using LightGBM, XGBoost, and autoencoder models, ensuring effective backend integration and a seamless frontend experience.
