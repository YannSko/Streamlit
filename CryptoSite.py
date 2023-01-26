import streamlit as st
from PIL import Image
import pandas as pd
import base64
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import resquests
import time
import json


st.set_page_config(layout="wide")

logo = Image.open('logo.jpg')

st.image(logo, width=500)

st.title('Site Crytpo')
st.markdown("""
Site traçant l'évolution des Crypto-monnaies
""")

#Layout page

col1= st.sidebar
col2, col3 = st.beta_columns((2,1))

#SideBar Main panel

col1.header("Options")

# Side bar avec les prix

PrixActuel = col1.selectbox("Choisissez l'unité",("USD","BTC","ETH"))

# Webscrap du site coinmarket pour récupe les ressources pour "alimenter le site"
@st.cache
def load_data():
    cmc = resquests.get('https://coinmarketcap.com')
    soup = BeautifulSoup (cmc.content, 'html.parser')
    
    data = soup.find('script', id='__NEXT_DATA__', type='application/json')
    coins = {}
    coin_data = json.loads(data.content [0])
    listings = coin_data['props']['initialState']['cryptocurrency']['listingLatest']['data']
    for i in listings:
        coins[str(i['id'])] = i['slug']

    coin_name = []
    coin_symbol = []
    market_cap = []
    percent_change_1h = []
    percent_change_24h = []
    percent_change_7d = []
    price = []
    volume_24h = []

    for i in listings:
      coin_name.append(i['slug'])
      coin_symbol.append(i['symbol'])
      price.append(i['quote'][PrixActuel]['price'])
      percent_change_1h.append(i['quote'][PrixActuel]['percent_change_1h'])
      percent_change_24h.append(i['quote'][PrixActuel]['percent_change_24h'])
      percent_change_7d.append(i['quote'][PrixActuel]['percent_change_7d'])
      market_cap.append(i['quote'][PrixActuel]['market_cap'])
      volume_24h.append(i['quote'][PrixActuel]['volume_24h'])

    df = pd.DataFrame(columns=['coin_name', 'coin_symbol', 'market_cap', 'percent_change_1h', 'percent_change_24h', 'percent_change_7d', 'price', 'volume_24h'])
    df['coin_name'] = coin_name
    df['coin_symbol'] = coin_symbol
    df['price'] = price
    df['percent_change_1h'] = percent_change_1h
    df['percent_change_24h'] = percent_change_24h
    df['percent_change_7d'] = percent_change_7d
    df['market_cap'] = market_cap
    df['volume_24h'] = volume_24h
    return df

df = load_data

