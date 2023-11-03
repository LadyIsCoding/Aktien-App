import yfinance as yf
import streamlit as st

def diagram(stock,button: str,x:int):
    stock = yf.Ticker(stock)
    button = st.radio("Zeitwahl", ["10 Jahre", "1 Jahr", "1 Monat", "1 Tag"], key=x, horizontal=True)
    if button == "10 Jahre":
        data = stock.history("10y", "3mo")
    elif button == "1 Jahr":
        data = stock.history("1y", "1mo")
    elif button == "1 Monat":
        data = stock.history("1mo", "1d")
    elif button == "1 Tag":
        data = stock.history("1d", "60m")

    df = data["Close"]
    st.line_chart(df)


