# 🏠 PropCast — AI Real Estate Sales Forecasting Platform

An AI-powered web platform that helps real estate businesses make smarter decisions using Machine Learning and AI.

## Features
- 📊 CSV Upload + Auto Data Analysis
- 📈 Interactive Charts (Plotly)
- 🤖 ML Price Predictor (Random Forest)
- 💡 AI Market Insights (Groq LLaMA)
- 💬 Natural Language Q&A
- 📄 PDF Report Export

## Tech Stack
Python, Django, Pandas, Scikit-learn, Plotly, Groq API, ReportLab, Bootstrap 5

## Setup Instructions
1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Create `.env` file with your `GROQ_API_KEY`
4. Run migrations: `python manage.py migrate`
5. Start server: `python manage.py runserver`
6. Open: `http://127.0.0.1:8000`

## Sample Dataset
Upload `sample_properties.csv` from the root folder to test the app.

## Built By
Rahul Achari — Final Year CSE Student