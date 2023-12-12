import streamlit as st
import pandas as pd
import numpy as np
import pandas_ta as pta
import os
import plotly.graph_objects as go
import plotly.express as px



st.markdown('<h1 style="color:#FFB81C;text-align: center;font-size: 72px;">Bitcoin Cryptocurrency Chart</h1>', unsafe_allow_html=True)

st.markdown('<p style="color:#CCCCCC;text-align: left;">\
    The graph below shows the Bitcoin data for the last 30 days.</p>', unsafe_allow_html=True)

route_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

df = pd.read_csv(os.path.join(route_path, 'raw_data/BTC.csv'))

df['time'] = pd.to_datetime(df['time'])

st.markdown('<h5 style="color:#CCCCCC;text-align: left;">\
    Technical Indicators:</h5>', unsafe_allow_html=True)

st.markdown('<p style="color:#CCCCCC;text-align: left;">\
    If you would like to view additional technical indicators overlaid on the bitcoin graph please select from the below.</p>', unsafe_allow_html=True)

rsi_upper_BB = st.checkbox("Show Upper Bollinger Band", value=False)
rsi_middle_BB = st.checkbox("Show Middle Bollinger Band", value=False)
rsi_lower_BB = st.checkbox("Show Lower Bollinger Band", value=False)

# Calculate Bollinger Bands
bbands_df = pta.bbands(df['close'], length=20)
df['Upper_BB'] = bbands_df['BBU_20_2.0']
df['Middle_BB'] = bbands_df['BBM_20_2.0']
df['Lower_BB'] = bbands_df['BBL_20_2.0']

df = df.iloc[21:]

fig = go.Figure()

# Create a candlestick chart
candlestick_trace = go.Candlestick(x=df['time'],
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'])

fig.add_trace(candlestick_trace)


if rsi_lower_BB:
    rsi_lower_BB = go.Scatter(x=df['time'],
                           y=df['Lower_BB'],
                           mode='lines',
                           name='Lower_BB',
                           line=dict(color='purple'))
    fig.add_trace(rsi_lower_BB)

if rsi_middle_BB:
    rsi_middle_BB = go.Scatter(x=df['time'],
                           y=df['Middle_BB'],
                           mode='lines',
                           name='Middle_BB',
                           line=dict(color='orange'))
    fig.add_trace(rsi_middle_BB)

if rsi_upper_BB:
    adx_trace = go.Scatter(x=df['time'],
                           y=df['Upper_BB'],
                           mode='lines',
                           name='Upper_BB',
                           line=dict(color='blue'))
    fig.add_trace(adx_trace)

# Set the layout of the chart
fig.update_layout(
    title='Bitcoin Chart',
    xaxis_title='Date',
    yaxis_title='Price',
    height=600,  # Adjust the height
    width=1200,
)

# Display the candlestick chart using st.plotly_chart
st.plotly_chart(fig)

route_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

df_FAGI = pd.read_csv(os.path.join(route_path, 'raw_data/FearAndGreedIndex.csv'))

df_FAGI['date'] = pd.to_datetime(df_FAGI['date'])

fig_FAGI = px.line(df_FAGI, x='date', y='FAGI_score', title='FAGI Sentiment Over Time')

fig_FAGI.update_layout(
    title='Fear and Greed Chart',
    xaxis_title='Date',
    yaxis_title='Fear and Greed Score',
    height=600,  # Adjust the height
    width=1200,
)

st.plotly_chart(fig_FAGI)

df['time'] = pd.to_datetime(df['time']).dt.strftime("%Y-%m-%d")

df.set_index('time', inplace=True)

df = df.round(1).astype(int)

st.markdown('<p style="color:#CCCCCC;text-align: left;">\
    The table and slider below can be used to take a more in depth look at the last 10 days of bitcoin data.</p>', unsafe_allow_html=True)

line_count = st.slider('Select rows of bitcoin data to view', 1, 10, 3)

# and used to select the displayed lines
head_df = df.tail(line_count)

center_aligned_df = head_df.style.set_table_styles([{'selector': 'th', 'props': [('text-align', 'center')]}])
st.table(center_aligned_df)
