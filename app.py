import yfinance as yf
import streamlit as st
import plotly.express as px
from datetime import datetime as dt
import pytz

st.set_page_config(layout="wide")

st.header('Stock Market Analyser')
st.divider()

tickers = st.text_input('Enter stock ticker, e.g, GOOG, NKE, AAPL', 'NKE')
tz = pytz.timezone('UTC')
start = tz.localize(dt(2013, 1, 1))
end = tz.localize(dt.today())

col1, col2 = st.columns(2)

with col1:
    start_date = st.date_input('Enter Start Date', start)

with col2:
    end_date = st.date_input('Enter End Date', end)


data = yf.download(tickers, start_date, end_date, auto_adjust=True) # Download data

st.divider()

st.subheader('Stock Data')
st.dataframe(data, use_container_width=True)

st.subheader('Stock Data vs Time')
fig = px.line(data, x=data.index, y=data.columns)
st.plotly_chart(fig, theme="streamlit", use_container_width=True)

ma_50_days = data.Close.rolling(50).mean()
ma_100_days = data.Close.rolling(100).mean()
ma_200_days = data.Close.rolling(200).mean()

st.subheader('Price vs MA50 vs MA100 vs MA200')

fig = px.line(data, x=data.index, y=[data.Close, ma_50_days, ma_100_days, ma_200_days])

fig['data'][1]['line']['color'] = '#00ff00'
fig['data'][1]['name'] = 'MA50'

fig['data'][2]['line']['color'] = '#ff0000'
fig['data'][2]['name'] = 'MA100'

fig['data'][3]['line']['color'] = '#ffa500'
fig['data'][3]['name'] = 'MA200'

st.plotly_chart(fig, theme="streamlit", use_container_width=True)