## AI Retail Business Monitoring System
# Overview

AI Retail Business Monitoring System is a backend analytics service built with Python that automatically processes sales data, generates business insights, creates visualizations, performs simple demand forecasting, detects anomalies, and sends reports directly to WhatsApp using the official WhatsApp Business Cloud API.

The system operates entirely from the backend without relying on WhatsApp Web, browser automation, or manual interaction. It is designed as an end to end portfolio project that demonstrates real world data analytics, automation engineering, AI integration, and backend service architecture for retail businesses.

# Key Features

Automated Sales Data Processing
The system reads uploaded CSV sales data and performs automated data transformation and analysis.

Operational Business Summary
Generates structured insights including best selling product, slow moving product, best performing branch, favorite color, and overall sales trend.

Stock Management Recommendation
Provides restock and stock reduction recommendations based on product performance.

Anomaly Detection
Detects unusual spikes or drops in revenue using statistical thresholds to identify abnormal business behavior.

Demand Forecasting
Implements a rolling average based prediction to estimate products likely to sell the next day.

AI Generated Business Narrative
Uses an AI model to convert raw analytical results into human readable business insight tailored for business owners.

Backend WhatsApp Notification
Sends structured reports directly to WhatsApp using the official WhatsApp Business Cloud API without opening WhatsApp Web or desktop applications.
---
# Technology Stack

Python
Pandas
Matplotlib
Requests
Google Gemini API
WhatsApp Business Cloud API
FastAPI (optional for API deployment)
---
# Project Structure

Personal_Project
run_service.py
business_guard.py
send_whatsapp.py
.env

cloud_ai_gemini
ai_analyst.py

processed
failed

Client_Upload
---
# System Architecture

Client uploads sales CSV file
Analytics engine processes data
Business guard module performs anomaly detection and forecasting
Final report is generated
WhatsApp Business Cloud API sends report to target number

All operations run from backend infrastructure without browser automation.
---
# Installation
1. Clone the repository
2. Create a virtual environment
python -m venv venv
venv\Scripts\activate
3. Install dependencies
pip install -r requirements.txt
4. Create a .env file
Add the following environment variables:
GEMINI_API_KEY=your_gemini_api_key
WA_TOKEN=your_whatsapp_access_token
WA_PHONE_ID=your_whatsapp_phone_id
WA_TARGET=628xxxxxxxxxx
---
# Running the Service

To start the monitoring service: python run_service.py

If deploying as an API server using FastAPI: uvicorn main:app --reload
---
# WhatsApp Cloud API Setup
1. Create a Meta Developer account
2. Create a Business App
3. Add WhatsApp product to the app
4. Generate a temporary access token
5. Obtain Phone Number ID
6. Verify the recipient phone number
Update all credentials inside the .env file.
--- 
# Sample Report Output

The system generates a structured business report containing:

Operational summary
Stock management recommendation
AI generated business analysis
Anomaly alert when detected
Next day sales prediction

The report is delivered automatically to WhatsApp.
--- 
# Use Cases

This system simulates a production ready retail monitoring solution suitable for:

Flower shops
Small retail businesses
Inventory driven SMEs
Food and beverage stores

It demonstrates integration between analytics, automation, AI narrative generation, and messaging infrastructure.
--- 
# Future Improvements

Time series forecasting using advanced models
Inventory level integration
Real time API based uploads
Web dashboard interface
Multi tenant architecture
Cloud deployment on VPS or containerized environment
--- 
# Author

Bayu Chandra Putra
Data Analyst with experience in SQL, BI dashboards, automation, and AI integration
