import streamlit as st
from PIL import Image
import pandas as pd
import base64
import matplotlib.pyplot as plt
import time

st.set_page_config(layout="wide",
                   page_title ="AssuranceStat"
                   

                            )

# Import le csv
file_path="./insurance.csv"
df = pd.read_csv(file_path)
df['bmi'] = df['bmi'].astype(int)

### Filtre ( disposition = sidebaar)

S_bar = st.sidebar

S_bar.header ("Choose your input")

#Gender
Gender = S_bar.multiselect('Pick your gender',
                     options = df["sex"].unique(),
                     default = df["sex"].unique())
Separation= st.sidebar.markdown("""
------
""")
#BMI
Bmi = S_bar.slider('Pick a BMI',  
                    min_value=df['bmi'].min(), max_value=df['bmi'].max()
                    #default= df['bmi'].min()
                    )
Separation= st.sidebar.markdown("""
------
""")
#Age
Age = S_bar.slider('Pick your Age', 
                    min_value=df['age'].min(), max_value=df['age'].max(),
                    #default= df['age'].min()
                    )
Separation= st.sidebar.markdown("""
------
""")
#Region
Region = S_bar.multiselect('Choose a origin',
                            options = df["region"].unique(),
                            default = df["region"].unique())
Separation= st.sidebar.markdown("""
------
""")
#Smoker
Smoker = S_bar.multiselect('Your population  smoke ?',
                            options = df["smoker"].unique(),
                            default = df["smoker"].unique())
Separation= st.sidebar.markdown("""
------
""")
#Children number 
Children = S_bar.slider('Pick a number of children from the customer', 
                        min_value=df['children'].min(), max_value=df['children'].max(),
                       # default= df['children'].min()
                        )

#Application du filtre sur la dataframe

df_select = df.query(
    " sex ==@Gender & bmi <=@Bmi & age <=@Age & region== @Region & smoker = =@Smoker & children  <=@Children "
)



# --- Main ---


logo = Image.open('solutions-dassurance.jpg')


st.title('Assurance ')
st.markdown("""
What are the factors modifying the insurance costs? How do they impact?
""")

# Stat Charges
Total_Charges = int(df_select["charges"].sum())
Average_Charges = round(df_select["charges"].mean(),1)

LeftCol, MidCol, RightCol = st.columns(3)

with LeftCol:
    st.image(logo, width=250)
with MidCol:
    st.subheader("Total Charges:")
    st.subheader(f"${Total_Charges} ")
   

with RightCol:
    st.subheader('Average Charges:')
    st.subheader(f"${Average_Charges}")

st.markdown("---")
st.header("Data frame depedent of the filter you took")
st.dataframe(df_select)#à placer dans le main

def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="crypto.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_select), unsafe_allow_html=True)
