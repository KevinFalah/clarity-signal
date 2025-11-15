# 📊 Clarity Signal

An interactive web application built with **Streamlit** to analyze and validate cryptocurrency trading signals based on the confluence of multiple technical indicators (Bollinger Bands, RSI, EMA 200) and market sentiment (Fear & Greed Index).

This application aims to provide potential entry points (Buy Signals) or exit points (Sell Signals) based on strict, predefined criteria.



---

## ✨ Key Features

* **Confluence Analysis:** Combines multiple technical indicators and sentiment data to generate more validated trading signals.
* **Technical Indicators:** Calculates and visualizes **Bollinger Bands (BB)**, **Relative Strength Index (RSI)**, and **Exponential Moving Average 200 (EMA 200)**.
* **Market Sentiment:** Fetches the latest **Fear & Greed Index** data to gauge market psychology.
* **Interactive Visualization:** Displays an interactive price chart using **Plotly** for the last 180 days, including all indicators.
* **Smart Caching:** Utilizes Streamlit's `@st.cache_data` to speed up data retrieval (price and F&G Index) and prevent unnecessary repeated API calls.

---

## 🛠️ Signal Criteria

The application generates signals based on the following criteria:

### Valid Buy Signal

A Buy Signal is triggered when **all** the following conditions are met:

1.  **RSI Oversold:** RSI (14) **< 30**.
2.  **Price Below BB:** Closing Price **< Lower Bollinger Band**.
3.  **Uptrend:** Closing Price **> EMA 200** (Indicates the long-term trend is still bullish/uptrend).
4.  **Sentiment is Fear:** Fear & Greed Index **< 40**.

### Valid Sell Signal

A Sell Signal is triggered when **all** the following conditions are met:

1.  **RSI Overbought:** RSI (14) **> 70**.
2.  **Price Above BB:** Closing Price **> Upper Bollinger Band**.
3.  **Sentiment is Greed:** Fear & Greed Index **> 75**.

---

## 🚀 Installation and Running the Project

### Prerequisites

Ensure you have Python (3.7+) installed on your system.

### Steps

1.  **Clone the Repository:**
    ```bash
    git clone [YOUR_REPO_LINK]
    cd [PROJECT_FOLDER_NAME]
    ```

2.  **Create a Virtual Environment (Optional, but Recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    .\venv\Scripts\activate   # Windows
    ```

3.  **Install Dependencies:**
    ```bash
    pip install streamlit pandas yfinance requests plotly
    ```

4.  **Run the Streamlit Application:**
    ```bash
    streamlit run app.py  # Assuming your code file is named app.py
    ```

The application will automatically open in your web browser (usually at `http://localhost:8501`).

---

## 💻 Usage

1.  Open the application in your browser.
2.  In the left **Sidebar**, enter the **Ticker** of the cryptocurrency you wish to analyze (e.g., `BTC-USD`, `ETH-USD`).
3.  Click the **`🚀 Analyze Now`** button.
4.  The analysis results, signal validation checklist, latest metrics, and price chart will be displayed on the main dashboard.

---

## ⚠️ Disclaimer

* **Not Financial Advice:** This application is intended ONLY for analytical and educational purposes. Never consider the generated signals as financial advice or trading recommendations.
* **High Risk:** Cryptocurrency trading involves high risk and may result in the loss of funds. Always perform your own research (`Do Your Own Research - DYOR`) before making any trading decisions.
* **Data Sources:** Price data is sourced from **Yahoo Finance** via the `yfinance` library, and the Fear & Greed Index data is sourced from **alternative.me**.