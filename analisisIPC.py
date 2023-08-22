#analizando IPC index

import yfinance as yf
from pandas_datareader import data as pdr
import sys
import numpy as np
from plotly.offline import download_plotlyjs,plot,iplot,init_notebook_mode
import plotly.graph_objs as go

msft=yf.Ticker("^MXX")
hist = msft.history(period="max")
hist

columns_to_remove = ['Open', 'High','Dividends','Low','Stock Splits','Volume']
df = hist.drop(columns=columns_to_remove)

df.dtypes

df.Close.plot(kind='line')
#calculo de medias moviles

def sma(df,d):
  c=df.rolling(d).mean()
  return c.dropna()


df["mv50"]=sma(df.Close,50)
df["mv100"]=sma(df.Close,100)


columnas=["Close","mv50","mv100"]
fig=go.Figure()
for columna in columnas:
  fig.add_trace(go.Scatter(x=df.index,y=df[columna],mode="lines",name=columna))

fig.update_layout(template='plotly_dark')
iplot(fig)

#strategy
df["alpha"]=df["mv50"]-df["mv100"]
df["alpha"]

df["alpha"].plot()
df["alpha_bin"]=df["alpha"].apply(np.sign)
df["alpha_bin"]
df["alpha_bin"].value_counts()

df["alpha_trade_long"]=((df["alpha_bin"]== 1) & (df["alpha_bin"].shift(1)==-1) & (df["alpha_bin"].shift(2)==-1) & (df["alpha_bin"].shift(3)==-1))
df["alpha_trade_short"]=((df["alpha_bin"]== -1) & (df["alpha_bin"].shift(1)==1) & (df["alpha_bin"].shift(2)==1) & (df["alpha_bin"].shift(3)==1))
df["alpha_trade_long"].value_counts()
df["alpha_trade_short"].value_counts()
df["alpha_trade_compra"]=np.where(df["alpha_trade_long"]==True,df['mv50'],np.nan)
df["alpha_trade_venta"]=np.where(df["alpha_trade_short"]==True,df['mv50'],np.nan)
columnas=["mv50","mv100","alpha_trade_compra","alpha_trade_venta"]
fig=go.Figure()
for columna in columnas:
  if columna=="alpha_trade_compra":
    fig.add_trace(go.Scatter(x=df.index,y=df[columna],mode="markers",name=columna,marker=dict(color="green")))
  if columna=="alpha_trade_venta":
    fig.add_trace(go.Scatter(x=df.index,y=df[columna],mode="markers",name=columna,marker=dict(color="red")))
  else:
    fig.add_trace(go.Scatter(x=df.index,y=df[columna],mode="lines",name=columna))

fig.update_layout(template="plotly_dark")

iplot(fig)
