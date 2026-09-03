# 🛡️ SentinelAI

## AI-Powered Network Intrusion Detection System

SentinelAI is a machine-learning based Network Intrusion Detection System (NIDS) designed to analyze network traffic and identify potentially malicious activity.

The system uses a Random Forest classifier to classify network traffic into:

- BENIGN
- ATTACK

SentinelAI also provides threat assessment, risk scoring, confidence analysis, attack details, visual analytics, scan history, and downloadable prediction results.

---

## 🎯 Problem Statement

Modern networks generate a large amount of traffic, making manual identification of malicious activity difficult.

SentinelAI aims to automatically analyze network traffic and identify suspicious patterns using machine learning.

---

## 🚀 Objectives

- Detect potentially malicious network traffic.
- Classify traffic as BENIGN or ATTACK.
- Provide confidence scores for predictions.
- Calculate a threat percentage and risk score.
- Display detected attack records.
- Provide visual network traffic analytics.
- Maintain scan history.
- Generate downloadable prediction results.

---

## 🧠 Machine Learning Model

SentinelAI uses:

**Algorithm:** Random Forest Classifier

Random Forest is an ensemble machine-learning algorithm that combines multiple decision trees to make predictions.

The model is trained using network traffic features and learns patterns associated with benign and malicious traffic.

---

## 📊 Dataset

The project uses network traffic data containing multiple network-flow features.

The training dataset contains:

- Training Records: 225,711
- Features: 78
- BENIGN Records: 97,686
- DDoS Records: 128,025

The target label is converted into two classes:

```text
BENIGN → 0
ATTACK → 1