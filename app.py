import yfinance as yf
import streamlit as st
import plotly.express as px
from datetime import datetime as dt
from sqlalchemy import text


def collection_from_db(conn):
    df = conn.query(
        f"SELECT TICKER FROM SAVED WHERE USERNAME = '{st.session_state.username}';"
    )
    collection = []
    for row in df.itertuples():
        collection.append(row[1])

    return collection


def app(conn) -> None:
    """Main UI"""
    st.header("Stock Market Analyser")
    st.divider()

    tickers = st.text_input(
        "Enter stock tickers seperated by commas, e.g, GOOG,NKE,AAPL", "DIS"
    )

    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input("Enter Start Date", dt.fromisoformat("2013-01-01"))

    with col2:
        end_date = st.date_input("Enter End Date", dt.today())

    data = []

    st.session_state.collection = collection_from_db(conn)

    st.session_state.tickers = list(set(tickers.split(",")))

    for ticker in st.session_state.tickers:
        data.append(yf.download(ticker, start_date, end_date, auto_adjust=True))

    with st.sidebar:
        st.header("Collections")

        if not st.session_state.collection:
            st.write("No tickers added, click on the add ticker button to save a stock")
        else:
            for i,t in enumerate(st.session_state.collection):
                if st.button(t[0], i+0x8F) and (t[0] not in tickers):
                    st.session_state.tickers.append(t[0])
                    data.append(yf.download(t[0], start_date, end_date, auto_adjust=True))

    tabs = st.tabs(st.session_state.tickers)

    for i in range(len(st.session_state.tickers)):
        with tabs[i]:
            if st.button("Add ticker to collection", key=i) and (tickers[i] not in st.session_state.collection):
                with conn.session as s:
                    s.execute(
                        text(
                            f"INSERT INTO SAVED VALUE('{st.session_state['username']}', '{st.session_state.tickers[i]}');"
                        )
                    )
                    s.commit()

            st.subheader("Stock Data")
            st.dataframe(data[i], use_container_width=True)

            st.divider()

            st.subheader("Stock Data vs Time")
            fig = px.line(data[i], x=data[i].index, y=data[i].columns)
            st.plotly_chart(fig, theme="streamlit", use_container_width=True)

            ma_50_days = data[i].Close.rolling(50).mean()
            ma_100_days = data[i].Close.rolling(100).mean()
            ma_200_days = data[i].Close.rolling(200).mean()

            st.subheader("Price vs MA50 vs MA100 vs MA200")

            fig = px.line(
                data[i],
                x=data[i].index,
                y=[data[i].Close, ma_50_days, ma_100_days, ma_200_days],
            )

            fig["data"][1]["line"]["color"] = "#00ff00"
            fig["data"][1]["name"] = "MA50"

            fig["data"][2]["line"]["color"] = "#ff0000"
            fig["data"][2]["name"] = "MA100"

            fig["data"][3]["line"]["color"] = "#ffa500"
            fig["data"][3]["name"] = "MA200"

            st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    if len(st.session_state.tickers) > 1:
        st.divider()
        st.subheader("Comparisson")

        fig = px.line(data[0], x=data[0].index, y=[d.Close for d in data])

        for i in range(len(st.session_state.tickers)):
            fig["data"][i]["name"] = st.session_state.tickers[i]

        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
