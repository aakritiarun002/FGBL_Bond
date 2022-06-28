# Library needed for creating app

from cProfile import label
from inspect import trace
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as data
import streamlit as st 
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Drive Analysis",layout= "wide")
st.title("German Bond Trend")

df = pd.read_csv("FGBL.csv")

# moving the "price" column after "Low" column, but before "Vol," "Change%" columns.
price_column = df.pop("Price") #for shifting Price from 1st to 4th position
df.insert(4, 'Price', price_column) #inserting the Price column after "Low" column and before "Vol" and "Change%" and column 
price_column = df.pop("Vol.") #for shifting Price from 1st to 4th position
df.insert(5, 'Vol.', price_column)

df = df.rename(columns= {"Price":"Close"}) # changing the "Price" column name to "Close"
df = df.rename(columns= {"Vol.":"Vol"})

# Finding the true value

high_low = df["High"] - df["Low"]
high_cp = np.abs(df["High"] - df["Close"].shift()) # finding the abs of "High - Previous Close Price"
low_cp = np.abs(df["Low"] - df["Close"].shift() ) # finding the abs of "Low minus Previous Close"

TR_df = pd.concat([high_low, high_cp, low_cp], axis=1) # making a new dataframe so that we can imply the np.max()
True_Range = np.max(TR_df, axis=1)


ATR = True_Range.rolling(14).mean().to_frame() #Calculating Avg True Range


df["M_std_dev_close"] = df["Close"].rolling(20).std()  #Moving Standard Deviation for Close

df["M_std_Dev_ATR"] = ATR.rolling(20).std() #Moving Standard Deviation for ATR

#ploting the graph
fig = go.Figure(data=[go.Candlestick(x=df["Date"],
                                     open=df['Open'], 
                                     high=df['High'],
                                     low=df['Low'],
                                     close=df['Close'], name='Candlestick chart'),go.Scatter(x=df["Date"], y=df["M_std_dev_close"],name="Moving Std Dev", line=dict(color='green', width=1)),
                                     go.Scatter(x=df["Date"], y=df["M_std_Dev_ATR"],name="ATR",line=dict(color='red', width=1))])
fig2 = go.Figure(data=[go.Scatter(x=df["Date"], y=df["M_std_dev_close"],name="Moving Std Dev", line=dict(color='green', width=1)),go.Scatter(x=df["Date"], y=df["M_std_Dev_ATR"],name="ATR",line=dict(color='red', width=1))])


# Create and add slider
parameters = np.arange(0, 5, 0.1)
steps = []
for i in range(len(fig.data)):
    step = dict(
        method="update",
        label=f"{parameters[i]: .2f}",
        args=[{"visible": [False] * len(fig.data)}],  
    )
    step["args"][0]["visible"][i] = True  
    steps.append(step)

sliders = [dict(
    active=0,
    pad={"t": 150},
    steps=steps
)]


#updating the layout of graphs
fig.update_layout(
    margin=dict(l=20, r=0, t=0, b=40),
    autosize=False,
    sliders=sliders,
    width=800,
    height=500,)
fig2.update_layout(
    margin=dict(l=20, r=0, t=0, b=0),
    autosize=True,
    width=1000,
    height=150,
    )

#st.plotly_chart(fig2)
st.write("When you look at X-axis, values between 0 to 5, Green Line Shows the Standard Deviation and Red Line shows the ATR")
st.write("Clicking on the slider helps in better view of the selected area \n You can see a Candlestick Chart along with ovarlaid ATR and Moving Standard Deviation")

st.plotly_chart(fig)


fig4 = make_subplots(specs=[[{"secondary_y": True}]])

st.write("Here is the magnified graph that represents the ATR and Moving Standard Deviation")
st.plotly_chart(fig2)

