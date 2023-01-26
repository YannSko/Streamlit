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

#Side Bar: selection crypto

sorted_coin = sorted(df["coin_symbol"])

selected_coin = col1.multiselect("Cryptocurrency",sorted_coin,sorted_coin)

df_selected_coin = df [ (df['coin_symbol'].isin(selected_coin))]

#Side Bar = affichage nombre de crypto

num_coin = col1.slider('Affichage de N Crypto',1,100,100)
df_coins = df_selected_coin[:num_coin]

#Side Bar : pourcentage d'évolution par période

percent_timeframe = col1.selectbox ("Pourcentage d'évolution du bitcoin par période de ",
                                    ["7d","24h","1h"])
percent_dict = {"7d":'percent_change_7d',"24h":'percent_change_24h',"1h":'percent_change_1h'}
selected_percent_timeframe = percent_dict[percent_timeframe]


#Side Bar  Trie de valeur ?

sort_values = col1.selectbox ("Sort Values ?", ["Yes","No"])

col2.subheader("Prix de La Cripto selectionnée")
col2.write('Data Dimension: ' + str(df_selected_coin.shape[0]) + ' rows and ' + str(df_selected_coin.shape[1]) + ' columns.')


#Telechargé as csv 

def filedownload(df):
  csv = df.to_csv(index=False)
  b64 = base64.b64encode(csv.encode()).decode() # strings <-> bytes conversions
  href = f'<a href="data:file/csv;base64,{b64}" download="crypto.csv">Telecharger le csv</a>'
  return href

col2.markdown(filedownload(df_selected_coin), unsafe_allow_html=True)


#Data prepa pour Bar plot avec Pourcentage du prix ( évolution)
df_change = pd.concat([df_coins.coin_symbol, df_coins.percent_change_1h, df_coins.percent_change_24h, df_coins.percent_change_7d], axis=1)
df_change = df_change.set_index('coin_symbol')
df_change['positive_percent_change_1h'] = df_change['percent_change_1h'] > 0
df_change['positive_percent_change_24h'] = df_change['percent_change_24h'] > 0
df_change['positive_percent_change_7d'] = df_change['percent_change_7d'] > 0
col2.dataframe(df_change)

#Bar Plot

col3.subheader("Barplot avec Pourcentage d'évolution du prix ")

if percent_timeframe == '7d':
    if sort_values == 'Yes':
        df_change = df_change.sort_values(by=['percent_change_7d'])
    col3.write(' période de 7 joirs')
    plt.figure(figsize=(5,25))
    plt.subplots_adjust(top = 1, bottom = 0)
    df_change['percent_change_7d'].plot(kind='barh', color=df_change.positive_percent_change_7d.map({True: 'g', False: 'r'}))
    col3.pyplot(plt)
elif percent_timeframe == '24h':
    if sort_values == 'Yes':
        df_change = df_change.sort_values(by=['percent_change_24h'])
    col3.write("période de 24h")
    plt.figure(figsize=(5,25))
    plt.subplots_adjust(top = 1, bottom = 0)
    df_change['percent_change_24h'].plot(kind='barh', color=df_change.positive_percent_change_24h.map({True: 'g', False: 'r'}))
    col3.pyplot(plt)
else:
    if sort_values == 'Yes':
        df_change = df_change.sort_values(by=['percent_change_1h'])
    col3.write("période d'une Heure")
    plt.figure(figsize=(5,25))
    plt.subplots_adjust(top = 1, bottom = 0)
    df_change['percent_change_1h'].plot(kind='barh', color=df_change.positive_percent_change_1h.map({True: 'g', False: 'r'}))
    col3.pyplot(plt)
