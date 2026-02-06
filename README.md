# 🗣️ VoC Intelligence Pro: AI-Powered Customer Sentiment Engine

**Transforming raw customer feedback into strategic business insights using Generative AI.**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://vighnesh-shetty-vs-voice-of-customer-intelligence-app-xwbdy9.streamlit.app/)
[![Powered by Gemini](https://img.shields.io/badge/Powered%20by-Google%20Gemini-blue)](https://ai.google.dev/)
[![Python](https://img.shields.io/badge/Built%20with-Python-yellow)](https://www.python.org/)

---

## 🚀 Overview

In the modern e-commerce landscape, businesses are drowning in customer feedback. Traditional sentiment analysis tools only tell you *if* customers are unhappy. **VoC Intelligence Pro** tells you *why*—and exactly what to do about it.

This application leverages **Google's Gemini 1.5 Flash** (Large Language Model) to perform **Aspect-Based Sentiment Analysis**. It goes beyond simple "Positive/Negative" tagging to decompose reviews into specific topics (e.g., Shipping vs. Quality), tracks sentiment trends over time, and generates actionable, strategic recommendations for business leaders.

**Key Value Proposition:**
* **Beyond Polarity:** Distinguishes between a great product and bad shipping in the same review.
* **Strategic Action Plans:** Automatically generates a "Recommended Action" for every negative review.
* **Temporal Analytics:** Visualizes how sentiment shifts over time (e.g., detecting a drop in satisfaction after a specific event).

---

## 📸 Application Walkthrough

### 1. Seamless Data Ingestion
*The interface is designed for simplicity. Users can upload raw CSV/Excel files or generate a "Mock Holiday Crisis" dataset to test the tool's capabilities immediately.*
![Data Ingestion](screenshots/run_analysis.png)

### 2. Executive Health Check
*The dashboard provides an instant pulse on customer health. It calculates a dynamic **NPS (Net Promoter Score)** proxy and visualizes the split between positive, negative, and neutral feedback.*
![Executive Dashboard](screenshots/analytics_dashborad_1.png)

### 3. Trend Analysis & Issue Detection
*Static numbers don't tell the whole story. The **Time-Series Analysis** (left) detects anomalies, such as the sharp drop in sentiment shown below. The **Top Issues** chart (right) immediately pinpoints "Shipping" and "Operations" as the culprits behind the crash.*
![Trend Analysis](screenshots/analytics_dashborad_2.png)

### 4. Strategic Recommendations & Granular Filtering
*This is where data becomes action. The AI reads every review and outputs a structured **"AI Action Plan"**. Users can use the global filters to isolate specific problems (e.g., filtering only for "Negative" reviews about "Shipping") to see exactly what needs fixing.*
![Strategic Recommendations](screenshots/analytics_dashborad_3.png)

### 5. Data Transparency
*A dedicated view allows analysts to inspect the raw data alongside the AI's predicted topics and sentiments, ensuring full transparency and trust in the system.*
![Raw Data View](screenshots/Data%20View.png)

---

## 🛠️ Technical Architecture

This project integrates **Generative AI** into a robust **Data Analytics** pipeline.

* **LLM Engine:** `Google Gemini 1.5 Flash` (via API).
* **Frontend:** `Streamlit` (Interactive Web App).
* **Data Visualization:** `Plotly Express` & `Graph Objects`.
* **Data Processing:** `Pandas` (Time-series manipulation).
* **Prompt Engineering:** Few-shot prompting with JSON enforcement to ensure structured output from the LLM.

### System Workflow
1.  **Ingest:** User uploads raw CSV/Excel data.
2.  **Process:** The app batches reviews and sends them to the Gemini API.
3.  **Analyze:** The LLM extracts Sentiment, Topics, Key Phrases, and Strategic Insights.
4.  **Visualize:** Streamlit renders interactive charts and filters based on the structured data.

---

## 💻 How to Run Locally

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/vighnesh-shetty-vs/voice_of_customer_intelligence.git](https://github.com/vighnesh-shetty-vs/voice_of_customer_intelligence.git)
    cd voice_of_customer_intelligence
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the App**
    ```bash
    streamlit run app.py
    ```

4.  **Enter API Key:** When the app launches, enter your Google Gemini API key (Get one for free [here](https://aistudio.google.com/)).

---

## 👤 Author

**Vighnesh Shetty**
*MSc Data Analytics for Business | KEDGE Business School*

Building tools that turn **Unstructured Data** into **Business Decisions**.

[LinkedIn Profile](https://www.linkedin.com/in/vighnesh-shetty/)
