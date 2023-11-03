import streamlit as st
import yfinance as yf
import pandas as pd
import api_queries as apiq
import save_load as s_l
import diagrams as dg

dax = pd.read_csv("assets/DAX 40.csv")
dax_symbol = [symbol + ".DE" for symbol in dax["Ticker / Symbol"]]
dow_jones = pd.read_csv("assets/dow jones.csv")
dj_symbol = list(dow_jones["Symbol"])

stock_index = {"DOW JONES":"^DJI", "DAX":"^GDAXI"}


@st.cache_resource
def metric(symbol):
    stock = yf.Ticker(symbol)
    last_price = stock.basic_info.last_price
    previous_close = stock.basic_info.previous_close
    
    st.metric(stock.info["longName"],
          f"{last_price:.2f} {stock.basic_info.currency}",
          f"{last_price - previous_close:.2f}  \
          ({((last_price-previous_close)/previous_close)* 100:.2f} %)")


def winners_loser():
    winners = apiq.get_av_TOP_GAINERS_LOSERS()["top_gainers"]
    loser = apiq.get_av_TOP_GAINERS_LOSERS()["top_losers"]

    col_winner, col_loser = st.columns(2)
    
    with col_winner:
        st.subheader("Top 5 Winner")

        for i in range(5):
            st.metric(winners[i]["ticker"],
                    winners[i]["price"] + " USD",
                    winners[i]["change_amount"] + f" {winners[i]['change_percentage']}")
            
    with col_loser:
        st.subheader("Top 5 Loser")

        for i in range(5):
            st.metric(loser[i]["ticker"],
                    loser[i]["price"] + " USD",
                    loser[i]["change_amount"] + f" {loser[i]['change_percentage']}")


def get_last_price_EUR(symbol):
    stock = yf.Ticker(symbol)
    
    if stock.basic_info.currency != "EUR":
        ex_rate = apiq.get_av_fx(stock.basic_info.currency, "EUR")
        price = stock.basic_info.last_price * ex_rate
    else:
        price = stock.basic_info.last_price

    return price

def buy_stock(symbol: str, amount: int):
    price = get_last_price_EUR(symbol)
    
    user = st.session_state["current_user"]
    for i in range(amount):
        s_l.save_data(user, symbol, price)


def sell_stock(symbol, amount):
    user = st.session_state["current_user"]
    owning = s_l.get_amount(user, symbol)

    price = get_last_price_EUR(symbol)
    
    
    if amount > owning[0][0]:
        st.warning("Yout try to sell more Stocks then you own!")
    else:
        for i in range(amount):
            s_l.sell(user, symbol, price)


def display_info(stock):
    result = yf.Ticker(stock)

    info = result.info

    st.subheader("General Information")
    st.write("Address:", info["address1"])
    st.write("City:", info["city"], ",", info["state"])
    st.write("Zip:", info["zip"])
    st.write("Country:", info["country"])
    st.write("Website:", info["website"])
    st.write("Industry:", info["industry"])
    st.write("Sector:", info["sector"])
    st.write("CEO:", info["companyOfficers"][0]["name"])
    
    st.write("---")
    with st.expander("Business Summary"):
        st.write(info["longBusinessSummary"])

    with st.expander("History"):
        pass

    st.write("---")

    st.write("Marked Cap:", info["marketCap"], info["currency"])
    st.write("Current Price:", info["currentPrice"], info["currency"])
    st.write("Previous Close:", info["previousClose"], info["currency"])




###################################################################################

def main_page():

    select = st.radio("Stock Index", ["DAX", "DOW JONES"], horizontal=True)

    metric(stock_index[select])

    dg.diagram(stock_index[select],"select2",1)

    st.write("---")
    with st.expander("Top Winners and Loser"):
        winners_loser()

    with st.expander("Currency Exchange Rates"):
        col_1 , col_2 = st.columns(2)
        with col_1:
            st.metric("EUR/USD", f"{apiq.get_av_fx('EUR', 'USD'):.2f}")
        with col_2:
            st.metric("EUR/GBP", f"{apiq.get_av_fx('EUR', 'GBP'):.2f}")
    
    st.write("---")
    if select == "DAX":
        drop_select =  st.selectbox("choose Stock", dax_symbol)
    elif select == "DOW JONES":
        drop_select =  st.selectbox("choose Stock", dj_symbol)



    col_metric, col_buy = st.columns([2, 1])
    with col_metric:
        metric(drop_select)
    with col_buy:
        amount = int(st.number_input("Amount_alt", value=1, step=1))


        if st.button("BUY_alt"):
            buy_stock(drop_select, amount)

    dg.diagram(drop_select, "select3",2)
    st.write(s_l.load_data(st.session_state["current_user"]))


def tab_search():
    search = st.text_input("Stocksymbol")
    if search:
        
        try:
            result = yf.Ticker(search)
            
            if st.session_state["current_user"] is None:
                metric(search)
            else:
                col_1, col_2 = st.columns(2)

                with col_1:
                    metric(search)

                with col_2:
                    amount = int(st.number_input("Amount",key="aalt2", value=1, step=1))
                
                    if st.button("BUY", key="buyalt2"):
                         buy_stock(search, amount)

            st.write("---")
            display_info(search)
            
            st.write(result.info)

        except:
            st.warning("Stock not found")

        
    
def tab_port():
    data = s_l.load_data(st.session_state["current_user"])
    

    for i, line in enumerate(data):
        col_1 , col_2, col_3 = st.columns(3)
        spend = s_l.spend(st.session_state["current_user"], line[0])
        with col_1:
            metric(line[0])

        with col_2:
            st.write("Owning:", f"{line[1]}", "Shares")
            st.write("Overall spend:", f"{spend[0][0]:.2f}", "EUR")
            
            value = get_last_price_EUR(line[0]) * line[1]
            st.write("Overall Value:", f"{value:.2f}", "EUR")

        with col_3:
            amount = int(st.number_input("Amount",key=f"ni{i}", value=1, step=1))
            col_buy, col_sell = st.columns([2, 4])
                    
            with col_buy:
                if st.button("BUY", key=f"buy{i}"):
                        buy_stock(line[0], amount)

                with col_sell:
                    if st.button("SELL", key=f"sell{i}"):
                        sell_stock(line[0], amount)

        st.write("---")

    with st.expander("All Transactions"):
        st.table(s_l.get_all_transactions(st.session_state["current_user"]))
        