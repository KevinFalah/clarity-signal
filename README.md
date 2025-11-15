📈 Clarity Signal For U

ClaritySignal is a powerful, minimalist web app for cryptocurrency traders who believe in confirmation.

Instead of relying on a single noisy indicator, this dashboard validates potential trading signals using a confluence of four distinct factors: Technical Indicators, Price Action, Trend, and Market Sentiment.

🚀 Try the Live App!

The application is deployed on Streamlit Community Cloud and is publicly accessible:

➡️ Access the Live Dashboard here [claritySignal](https://clarity-signal-for-u.streamlit.app/)

📊 Dashboard Preview
<img width="1919" height="946" alt="image" src="https://github.com/user-attachments/assets/ee847467-8e3b-46f1-b5ee-0c8f601e1dd2" />


✅ The Validation Checklist

This tool doesn't just give you a signal; it shows you why the signal is valid by checking it against a predefined ruleset.

For a BUY Signal (Long):

A BUY signal is only considered valid if all four of these conditions are met:

[RSI] Is the asset oversold? (RSI < 30)

[Bollinger Bands] Is the price at an extreme low? (Price < Lower Band)

[Trend] Are we in a long-term uptrend? (Price > 200-day EMA)

[Sentiment] Is the market fearful? (Fear & Greed Index < 40)

For a SELL Signal (Short/Take Profit):

A SELL signal is only considered valid if all three of these conditions are met:

[RSI] Is the asset overbought? (RSI > 70)

[Bollinger Bands] Is the price at an extreme high? (Price > Upper Band)

[Sentiment] Is the market greedy? (Fear & Greed Index > 75)

🛠️ Tech Stack

This app is built entirely in Python using the following libraries:

Streamlit: For the web application UI and deployment.

yfinance: For fetching historical OHLCV price data.

Plotly: For generating interactive price charts.

Requests: For fetching the Fear & Greed Index from the alternative.me API.

Pandas: For all data manipulation and indicator calculations.

⚠️ Disclaimer

This application is for educational and informational purposes only. The signals and data provided are not financial advice. All trading involves significant risk, and you should always Do Your Own Research (DYOR) before making any investment decisions.

Wait for a bigger and more informative on chain data application to come.
