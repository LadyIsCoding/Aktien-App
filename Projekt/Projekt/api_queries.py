import requests
import string
import random
import time
import pandas as pd
import streamlit as st


def key_generator(size=16, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def api_timing(sleeptime=1):
    time.sleep(sleeptime)

def get_demo(url):
    my_response = requests.get(url)
    if (my_response.ok):
        j_data = my_response.json()
    api_timing()
    return j_data


def get_av_overview(symbol):
    apikey = key_generator()
    apiurl = 'https://www.alphavantage.co/query?'
    apifunction = 'OVERVIEW'
    payload = {'function': apifunction,
               'symbol': symbol,
               'apikey': apikey}
    my_response = requests.get(apiurl, params=payload)
    if (my_response.ok):
        j_data = my_response.json()
    api_timing()
    return j_data

def get_av_quote(symbol):
    apikey = key_generator()
    apiurl = 'https://www.alphavantage.co/query?'
    apifunction = 'GLOBAL_QUOTE'
    payload = {'function': apifunction,
               'symbol': symbol,
               'apikey': apikey}
    my_response = requests.get(apiurl, params=payload)
    quote = False
    if (my_response.ok):
        j_data = my_response.json()
        if 'Global Quote' in j_data:
            quote = float(j_data['Global Quote']['05. price'])
    api_timing()
    return quote

@st.cache_data
def get_av_fx(from_currency, to_currency):
    apikey = key_generator()
    apiurl = 'https://www.alphavantage.co/query?'
    apifunction = 'CURRENCY_EXCHANGE_RATE'
    payload = {'function': apifunction,
               'from_currency': from_currency,
               'to_currency': to_currency,
               'apikey': apikey}
    my_response = requests.get(apiurl, params=payload)
    fx_rate = False
    if (my_response.ok):
        j_data = my_response.json()
        if 'Realtime Currency Exchange Rate' in j_data:
            fx_rate = float(
                j_data['Realtime Currency Exchange Rate']['5. Exchange Rate'])
    api_timing()
    return fx_rate


def get_symbols(keyword):
    apikey = key_generator()
    apiurl = 'https://www.alphavantage.co/query?'
    apifunction = "SYMBOL_SEARCH"
    datatype = ""
    payload = {"function": apifunction,
               "keywords": keyword,
               "datatype": datatype,
               "apikey": apikey}
    my_response = requests.get(apiurl, params=payload)
    if (my_response.ok):
        j_data = my_response.json()
    api_timing()
    return j_data

def get_av_TIME_SERIES_DAILY(symbol):
    apikey = key_generator()
    apiurl = 'https://www.alphavantage.co/query?'
    apifunction = 'TIME_SERIES_DAILY'
    payload = {'function': apifunction,
               'symbol': symbol,
               'apikey': apikey}
    my_response = requests.get(apiurl, params=payload)
    if (my_response.ok):
        j_data = pd.DataFrame(my_response.json())
    api_timing()
    return j_data

@st.cache_data
def get_av_TOP_GAINERS_LOSERS():
    apikey = key_generator()
    apiurl = 'https://www.alphavantage.co/query?'
    apifunction = 'TOP_GAINERS_LOSERS'
    payload = {'function': apifunction,
               'apikey': apikey}
    my_response = requests.get(apiurl, params=payload)
    if (my_response.ok):
        j_data = my_response.json()
    api_timing()
    return j_data


@st.cache_data
def get_av_NEWS_SENTIMENT(topics):
    apikey = key_generator()
    apiurl = 'https://www.alphavantage.co/query?'
    apifunction = 'NEWS_SENTIMENT'
    payload = {'function': apifunction,
               'topics':topics,
               'apikey': apikey}
    my_response = requests.get(apiurl, params=payload)
    if (my_response.ok):
        j_data = my_response.json()
    api_timing()
    return j_data


#print(get_av_NEWS_SENTIMENT("finance"))