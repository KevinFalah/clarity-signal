import streamlit as st
import pandas as pd
import yfinance as yf
import requests
from datetime import datetime, timedelta
import plotly.graph_objects as go
import warnings

warnings.filterwarnings('ignore', category=FutureWarning, module='yfinance')

# ==========================================================
# WEB APPLICATION CONFIGURATION
# ==========================================================

st.set_page_config(layout="wide", page_title="Dashboard Sinyal Kripto")

# ==========================================================
# BACKEND FUNCTIONS
# add @st.cache_data so that Streamlit "remembers" # the API call results and doesn't download them every time.
# ttl=600 means the cache will expire after 600 seconds (10 minutes).
# ==========================================================

@st.cache_data(ttl=600)
def get_fear_and_greed_index():
    """Mengambil data Fear & Greed Index terbaru dari alternative.me"""
    try:
        response = requests.get("https://api.alternative.me/fng/?limit=2")
        response.raise_for_status()
        data = response.json()['data']
        # Gunakan data kemarin (index 1) untuk sinyal harian yang reliable
        fng_value = int(data[1]['value'])
        fng_classification = data[1]['value_classification']
        return fng_value, fng_classification
    except Exception as e:
        st.error(f"Error mengambil F&G Index: {e}")
        return None, None

@st.cache_data(ttl=600)
def get_latest_data(ticker, days_back):
    """Mengambil data historis untuk 'days_back' terakhir."""
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        data = yf.download(ticker, start=start_date, end=end_date, auto_adjust=False)
        
        if hasattr(data.columns, 'levels'):
            data.columns = data.columns.droplevel(1)
            
        data.columns = [col.lower().replace(' ', '_') for col in data.columns]
        
        if data.empty:
            st.error(f"Tidak ada data untuk {ticker}")
            return None
        return data
    except Exception as e:
        st.error(f"Error mengambil data harga: {e}")
        return None

def add_indicators(df):
    """Menambahkan Bollinger Bands, RSI, dan EMA 200."""
    # Bollinger Bands (window 20)
    df['bb_middle'] = df['close'].rolling(window=20).mean()
    rolling_std = df['close'].rolling(window=20).std()
    df['bb_upper'] = df['bb_middle'] + (rolling_std * 2)
    df['bb_lower'] = df['bb_middle'] - (rolling_std * 2)
    
    # RSI (window 14)
    price_change = df['close'].diff()
    gains = price_change.where(price_change > 0, 0)
    losses = -price_change.where(price_change < 0, 0)
    avg_gains = gains.rolling(window=14).mean()
    avg_losses = losses.rolling(window=14).mean()
    rs = avg_gains / avg_losses
    df['rsi'] = 100 - (100 / (1 + rs))
    
    # Filter Tren (window 200)
    df['ema_200'] = df['close'].ewm(span=200, adjust=False).mean()
    
    return df

def create_price_chart(df, ticker):
    """Membuat grafik harga interaktif dengan Plotly."""
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df.index, y=df['close'],
                             mode='lines', name='Harga Close',
                             line=dict(color='black', width=2)))

    fig.add_trace(go.Scatter(x=df.index, y=df['ema_200'],
                             mode='lines', name='EMA 200',
                             line=dict(color='purple', width=1.5)))

    fig.add_trace(go.Scatter(x=df.index, y=df['bb_upper'],
                             mode='lines', name='BB Upper',
                             line=dict(color='red', width=1, dash='dash')))
    
    fig.add_trace(go.Scatter(x=df.index, y=df['bb_lower'],
                             mode='lines', name='BB Lower',
                             line=dict(color='green', width=1, dash='dash'),
                             fill='tonexty',
                             fillcolor='rgba(0,100,80,0.1)'))

    fig.update_layout(
        title=f"Grafik Harga {ticker} (180 Hari Terakhir)",
        yaxis_title="Harga (USD)",
        xaxis_title="Tanggal",
        legend_title="Indikator",
        hovermode="x unified"
    )
    return fig

# ==========================================================
# INTERFACE WEB APPLICATION
# ==========================================================

st.title("📊 Clarity Signal")
st.markdown("Sebuah alat untuk memvalidasi sinyal trading menggunakan konfluensi teknikal dan sentimen.")

st.sidebar.header("⚙️ Kontrol Input")
ticker = st.sidebar.text_input("Masukkan Ticker (cth: BTC-USD, ETH-USD):", "BTC-USD")
analyze_button = st.sidebar.button("🚀 Analisis Sekarang", type="primary")

if analyze_button:
    with st.spinner(f"Menganalisis {ticker}... Mengambil data F&G dan 300 hari data harga..."):
        
        fng_value, fng_classification = get_fear_and_greed_index()
        df_raw = get_latest_data(ticker.upper(), days_back=300)
        
        if df_raw is None or fng_value is None:
            st.error("Gagal mengambil data. Pastikan ticker valid atau coba lagi.")
            st.stop() # Hentikan eksekusi jika data tidak ada


        df = add_indicators(df_raw.copy())
        last_valid_data = df.dropna().iloc[-1]
        
        price = last_valid_data['close']
        rsi = last_valid_data['rsi']
        bb_upper = last_valid_data['bb_upper']
        bb_lower = last_valid_data['bb_lower']
        ema_200 = last_valid_data['ema_200']
        date = last_valid_data.name

    st.success(f"Analisis Selesai untuk {date.strftime('%Y-%m-%d')}")

    RSI_OVERSOLD = rsi < 30
    PRICE_BELOW_BB = price < bb_lower
    TREND_IS_UP = price > ema_200
    SENTIMENT_IS_FEAR = fng_value < 40
    
    RSI_OVERBOUGHT = rsi > 70
    PRICE_ABOVE_BB = price > bb_upper
    SENTIMENT_IS_GREED = fng_value > 75

    buy_signal = (RSI_OVERSOLD and PRICE_BELOW_BB and TREND_IS_UP and SENTIMENT_IS_FEAR)
    sell_signal = (RSI_OVERBOUGHT and PRICE_ABOVE_BB and SENTIMENT_IS_GREED)

    st.header("🎯 Sinyal Utama")
    if buy_signal:
        st.success(f"🚨 SINYAL BUY VALID: {ticker} 🚨")
    elif sell_signal:
        st.error(f"🔔 SINYAL SELL VALID: {ticker} 🔔")
    else:
        st.info("⏳ TIDAK ADA SINYAL (HOLD / NEUTRAL) ⏳")

    st.header("📋 Checklist Validasi Sinyal")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("✅ Kriteria BUY")
        st.markdown(f"**{'✅' if RSI_OVERSOLD else '❌'} 1. RSI Oversold (< 30):** `{rsi:.2f}`")
        st.markdown(f"**{'✅' if PRICE_BELOW_BB else '❌'} 2. Harga di Bawah BB:** `${price:,.2f} < ${bb_lower:,.2f}`")
        st.markdown(f"**{'✅' if TREND_IS_UP else '❌'} 3. Tren Naik (Harga > EMA 200):** `${price:,.2f} > ${ema_200:,.2f}`")
        st.markdown(f"**{'✅' if SENTIMENT_IS_FEAR else '❌'} 4. Sentimen Fear (F&G < 40):** `{fng_value} ({fng_classification})`")
        
    with col2:
        st.subheader("❌ Kriteria SELL")
        st.markdown(f"**{'✅' if RSI_OVERBOUGHT else '❌'} 1. RSI Overbought (> 70):** `{rsi:.2f}`")
        st.markdown(f"**{'✅' if PRICE_ABOVE_BB else '❌'} 2. Harga di Atas BB:** `${price:,.2f} > ${bb_upper:,.2f}`")
        st.markdown(f"**{'✅' if SENTIMENT_IS_GREED else '❌'} 3. Sentimen Greed (F&G > 75):** `{fng_value} ({fng_classification})`")

    st.header("📈 Data Metrik Terbaru")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Harga Terakhir", f"${price:,.2f}")
    kpi2.metric("F&G Index", f"{fng_value}", f"{fng_classification}")
    kpi3.metric("RSI (14)", f"{rsi:.2f}")
    kpi4.metric("Tren (EMA 200)", f"${ema_200:,.2f}")

    st.header("📉 Grafik Harga Interaktif")
    # Hanya plot 180 hari terakhir agar tidak terlalu ramai
    fig = create_price_chart(df.tail(180), ticker)
    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Silakan masukkan ticker di sidebar kiri dan klik 'Analisis Sekarang'.")