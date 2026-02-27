# AI Retail Business Monitoring System

## Overview

AI Retail Business Monitoring System is a backend analytics service built with Python that automatically processes sales data, generates business insights, creates visualizations, performs demand forecasting, detects anomalies, and sends reports directly to WhatsApp using the official WhatsApp Business Cloud API.

The system operates entirely from the backend without using WhatsApp Web, browser automation, or manual interaction. It demonstrates an end-to-end analytics pipeline combined with AI integration and messaging infrastructure, similar to a lightweight SaaS solution for retail businesses.

---

## Key Features

### Automated Sales Data Processing
Reads uploaded CSV sales data and performs automatic transformation and analysis.

### Operational Business Summary
Generates insights including:
- Best selling product
- Slow moving product
- Best performing branch
- Favorite color
- Overall sales trend

### Stock Management Recommendation
Provides restock and stock reduction suggestions based on product performance.

### Anomaly Detection
Detects abnormal spikes or drops in revenue using statistical thresholds.

### Demand Forecasting
Implements rolling average logic to predict products likely to sell the next day.

### AI Generated Business Insight
Uses an AI model to convert analytical results into structured business narrative.

### Backend WhatsApp Notification
Sends reports directly through WhatsApp Business Cloud API without opening WhatsApp Web or Desktop.

---

## Tech Stack

- Python
- Pandas
- Matplotlib
- Requests
- Google Gemini API
- WhatsApp Business Cloud API
- FastAPI (optional for API deployment)

---

## Project Structure

Personal_Project/

│

├── run_service.py

├── business_guard.py

├── send_whatsapp.py

├── .env

│

├── cloud_ai_gemini/

│ └── ai_analyst.py

│

├── processed/

├── failed/

└── Client_Upload/


---

## System Architecture

Client Upload CSV

↓

AI Analytics Engine

↓

Business Guard Module

↓

Report Generation

↓

WhatsApp Business Cloud API

↓

Business Owner Notification

All processes run fully on backend infrastructure.

---

## Installation

### 1. Clone Repository

git clone <your-repo-url>
cd Personal_Project

### 2. Create Virtual Environment

python -m venv venv
venv\Scripts\activate

### 3. Install Dependencies

pip install -r requirements.txt

### 4. Create `.env` File

Add the following environment variables:

GEMINI_API_KEY=your_gemini_api_key

WA_TOKEN=your_whatsapp_access_token

WA_PHONE_ID=your_whatsapp_phone_id

WA_TARGET=628xxxxxxxxxx

---

## Running the Service

### Local Monitoring Service

python run_service.py

### Optional: Run as API Server

uvicorn main:app --reload


---

## WhatsApp Cloud API Setup

1. Create Meta Developer account  
2. Create a Business App  
3. Add WhatsApp product  
4. Generate temporary access token  
5. Get Phone Number ID  
6. Verify recipient number  

Update credentials in the `.env` file.

---

## Sample Report Output

The system generates a structured business report containing:

- Operational summary
- Stock management recommendation
- AI generated business analysis
- Anomaly alert (if detected)
- Next day sales prediction

The report is automatically delivered to WhatsApp.

---

## Use Cases

This system is suitable for:

- Flower shops
- Small retail businesses
- Inventory driven SMEs
- Food and beverage stores

It demonstrates integration between data analytics, automation, AI narrative generation, and messaging infrastructure.

---

## Future Improvements

- Advanced time series forecasting
- Inventory level integration
- Real time API based upload
- Web dashboard frontend
- Multi tenant architecture
- Cloud deployment on VPS or container platform

---

## Author

**Bayu Chandra Putra**  
Data Analyst | linkedin.com/in/bayuchandraputra
