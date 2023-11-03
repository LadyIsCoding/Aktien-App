import yfinance as yf
import streamlit as st
import pandas as pd
import time, json
import api_queries as apiq
import log_in
import save_load as s_l

#microsoft = yfinance.Ticker('MSF.DE')
#print(json.dumps(microsoft.info, indent=4))

#daten = microsoft.basic_info
#print(f'{daten.last_price:.2f} {daten["currency"]}')

#print(microsoft.history(period='1d', interval='5m'))

#df_list = pd.read_html('https://finance.yahoo.com/world-indices/')
#majorStockIdx = df_list[0]
#st.write(majorStockIdx)

#tickerDAX = yfinance.Ticker("")
#daten = tickerDAX.history(period='1y', interval='5d')
#st.write(daten)
#st.line_chart(daten["Open"])

dax = pd.read_csv("DAX 40.csv")
dax_symbol = [symbol + ".DE" for symbol in dax["Ticker / Symbol"]]
dow_jones = pd.read_csv("dow jones.csv")
dj_symbol = list(dow_jones["Symbol"])

stock_index = {"DOW JONES":"^DJI", "DAX":"^GDAXI"}

if "portfolio" not in st.session_state:
    try:
        with open("portfolio.json", "r", encoding="UTF-8")as file:
            st.session_state["portfolio"] = json.load(file)
    except:
        st.session_state["portfolio"] = {}

if "current_user" not in st.session_state:
    st.session_state["current_user"] = None


@st.cache_data
def test():
    for symbol in dax_symbol:
        get = yf.Ticker(symbol)
        st.write(get)
        st.write(symbol, get.info["longName"])
        st.write(get.history(period='1d', interval='1h'))
        time.sleep(1)

@st.cache_data
def test2():
    for symbol in dax_symbol:
        get = yf.Ticker(symbol)
        with st.expander(symbol):
            st.write(get.info)
        time.sleep(1)

@st.cache_resource
def get_index(index):
    get = yf.Ticker(stock_index[index])
    time.sleep(1)
    return get

@st.cache_resource
def metric(symbol):
    stock = yf.Ticker(symbol)
    st.metric(stock.info["longName"],
          f"{stock.basic_info.last_price:.2f} {stock.basic_info.currency}",
          f"{stock.basic_info.last_price - stock.basic_info.previous_close:.2f}  \
          ({((stock.basic_info.last_price-stock.basic_info.previous_close)/stock.basic_info.previous_close)* 100:.2f} %)")


def buy_stock(symbol: str, amount: int):
    stock = yf.Ticker(symbol)
    
    if stock.basic_info.currency != "EUR":
        ex_rate = apiq.get_av_fx(stock.basic_info.currency, "EUR")
        price = stock.basic_info.last_price * ex_rate
    else:
        price = stock.basic_info.last_price
    
    buyer = st.session_state["current_user"]
    for i in range(amount):
        s_l.save_data(buyer, symbol, price)
    
    #if symbol not in st.session_state["portfolio"]:
    #    st.session_state["portfolio"].update({symbol:{"amount": amount,
    #                                                  "spend": price * amount,
    #                                                  "country": stock.info["country"],
    #                                                  "industry": stock.info["industry"],
    #                                                  "last purchase": datetime.date.today().isoformat()}})
    #else:
    #    st.session_state["portfolio"][symbol]["amount"] += amount
    #    st.session_state["portfolio"][symbol]["spend"] += price * amount
    #    st.session_state["portfolio"][symbol]["last purchase"] = datetime.date.today().isoformat()

    #with open("portfolio.json", "w", encoding="UTF-8") as file:
    #    json.dump(st.session_state["portfolio"], file, indent=4)


def sell_stock(symbol, amount):
    if symbol not in st.session_state["portfolio"]:
        return st.warning("ERROR")
    if amount > st.session_state["portfolio"][symbol]["amount"]:
        return st.warning("ERROR")
    
    st.session_state["portfolio"][symbol]["amount"] -= amount

    if st.session_state["portfolio"][symbol]["amount"] == 0:
        del st.session_state["portfolio"][symbol]

    with open("portfolio.json", "w", encoding="UTF-8") as file:
        json.dump(st.session_state["portfolio"], file, indent=4)


##############################################################################

st.set_page_config(initial_sidebar_state="collapsed")
st.title("Aktien-App")
st.write(st.session_state)

with st.sidebar:
    st.subheader("Menu")
    if st.session_state["current_user"] == None:
        st.session_state["current_user"] = log_in.login()
        log_in.signup()
        if st.session_state["current_user"] is not None:
            st.experimental_rerun()
    else:
        st.write("Hallo", st.session_state["current_user"])
        st.session_state["current_user"] = log_in.logout()




tab_main, tab_search = st.tabs(["Menu", "Search"])


with tab_main:
    st.metric("EUR/USD", f"{apiq.get_av_fx('EUR', 'USD'):.2f}")

    select = st.radio("Stock Index", ["DAX", "DOW JONES"], horizontal=True)

    metric(stock_index[select])

    #index = get_index(select)
    #index_history = index.history(period="5d", interval='1h')
    #st.line_chart(index_history["Open"])

    st.write("---")
    if select == "DAX":
        drop_select =  st.selectbox("choose Stock", dax_symbol)
    elif select == "DOW JONES":
        drop_select =  st.selectbox("choose Stock", dj_symbol)

    
    col_metric, col_buy = st.columns([2, 1])
    with col_metric:
        metric(drop_select)

    
    with col_buy:
        amount = int(st.number_input("Amount", value=1, step=1))

        if st.button("BUY"):
            buy_stock(drop_select, amount)

    
    if st.button("SELL"):
        sell_stock(drop_select, amount)

    #wert = 0
    #for stock in st.session_state["portfolio"].items():

    #    wert += stock[1]["amount"] * yf.Ticker(stock[0]).basic_info.last_price

    #st.write(f"Gesamtwert des Portfolios {wert:.2f} EUR")
    #st.write(st.session_state["portfolio"])

    #portfolio = pd.DataFrame(st.session_state["portfolio"]).T
    #st.write(portfolio)


    #get = yf.
    #st.write(get.info)

st.write(s_l.load_data(st.session_state["current_user"]))


with tab_search:
    search = st.text_input("Stocksymbol")
    if search:
        try:
            result = yf.Ticker(search)
            metric(search)
            st.write(result.info)
        except:
            st.warning("Stock not found")

