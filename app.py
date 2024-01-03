import yfinance as yf
import streamlit as st
import plotly.express as px
from datetime import datetime as dt

st.set_page_config(layout="wide")

st.header('Stock Market Analyser')
st.divider()

tickers = st.text_input('Enter stock tickers seperated by commas, e.g, GOOG,NKE,AAPL', 'NKE')

col1, col2 = st.columns(2)

with col1:
    start_date = st.date_input('Enter Start Date', dt.fromisoformat('2013-01-01'))

with col2:
    end_date = st.date_input('Enter End Date', dt.today())

data = []

tickers = list(set(tickers.split(',')))

for ticker in tickers:
    data.append(yf.download(ticker, start_date, end_date, auto_adjust=True))

tabs = st.tabs(tickers)

for i in range(len(tickers)):
    with tabs[i]:
        st.subheader('Stock Data')
        st.dataframe(data[i], use_container_width=True)

        st.divider()

        st.subheader('Stock Data vs Time')
        fig = px.line(data[i], x=data[i].index, y=data[i].columns)
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)

        ma_50_days = data[i].Close.rolling(50).mean()
        ma_100_days = data[i].Close.rolling(100).mean()
        ma_200_days = data[i].Close.rolling(200).mean()

        st.subheader('Price vs MA50 vs MA100 vs MA200')

        fig = px.line(data[i], x=data[i].index, y=[data[i].Close, ma_50_days, ma_100_days, ma_200_days])

        fig['data'][1]['line']['color'] = '#00ff00'
        fig['data'][1]['name'] = 'MA50'

        fig['data'][2]['line']['color'] = '#ff0000'
        fig['data'][2]['name'] = 'MA100'

        fig['data'][3]['line']['color'] = '#ffa500'
        fig['data'][3]['name'] = 'MA200'

        st.plotly_chart(fig, theme="streamlit", use_container_width=True)

if len(tickers) > 1:
    st.divider()
    st.subheader('Comparisson')

    fig = px.line(data[0], x=data[0].index, y=[d.Close for d in data])

    for i in range(len(tickers)):
        fig['data'][i]['name'] = tickers[i]

    st.plotly_chart(fig, theme="streamlit", use_container_width=True)