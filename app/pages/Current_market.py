import streamlit as st
import pandas as pd
import numpy as np
import os
import plotly.graph_objects as go


st.markdown('<h1 style="color:#FFB81C;text-align: center;font-size: 72px;">Bitcoin Cryptocurrency Chart</h1>', unsafe_allow_html=True)

st.markdown('<h4 style="color:#CCCCCC;text-align: center;">\
    The graph below shows the Bitcoin data for the last 30 days.</h4>', unsafe_allow_html=True)

route_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

df = pd.read_csv(os.path.join(route_path, 'raw_data/BTC.csv'))

df['time'] = pd.to_datetime(df['time'])

# Create a candlestick chart
fig = go.Figure(data=[go.Candlestick(x=df['time'],
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'])])

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

df.set_index('time', inplace=True)

df = df.round(1).astype(int)

center_aligned_df = df.tail(5).style.set_table_styles([{'selector': 'th', 'props': [('text-align', 'center')]}])
st.table(center_aligned_df)
