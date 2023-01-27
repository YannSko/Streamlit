import streamlit as st
from PIL import Image
import pandas as pd
import base64
import matplotlib.pyplot as plt
import time

st.set_page_config(layout="wide")

logo = Image.open('solutions-dassurance.jpg')

st.image(logo, width=500)

st.title('Site Assurance')
st.markdown("""
Quels sont les facteurs modifiant les charges d'assurances ? Comment impactent-ils ?
""")




st.sidebar.radio('Pick your gender',['Male','Female'])
st.slider('Pick a BMI', 15.96,49.41)
st.slider('Pick your age', 18,64)
st.multiselect('choose a origin',['northeast', 'northwest', 'southeast', 'southwest'])
st.markdown("""
Your population  smoke ?
""")
st.checkbox('Yi')
st.checkbox('Ni')
st.slider('Pick a number of children from the customer', 0,5)
