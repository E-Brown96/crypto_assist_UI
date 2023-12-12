import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import requests
import os
import plotly.express as px

st.markdown('<h1 style="color:#FFB81C;text-align: center;font-size: 72px;">Crypto Predictor</h1>', unsafe_allow_html=True)

st.markdown('<p style="color:#CCCCCC;text-align: left;">\
    The graph below shows how the current model predicts against the actual values of bitcoin for the last 5 days.</p>', unsafe_allow_html=True)

route_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

df = pd.read_csv(os.path.join(route_path, 'raw_data/BTC.csv'))

df['time'] = pd.to_datetime(df['time'])

df = df[['time','close']]

tail_df = df.tail(5)

st.markdown('<p style="color:#CCCCCC;text-align: left;">\
    Please press the button below to display your crypto AI assistants predicted bitcoin price for the past five days!</p>', unsafe_allow_html=True)
last_predictions_pressed = st.button('Check last Predictions')
st.markdown('<p style="color:#CCCCCC;text-align: left;">\
    Please press the button below to get your crypto AI assistants predicted bitcoin price for the next five days!</p>', unsafe_allow_html=True)
future_predictions_pressed = st.button('Check future Predictions')

if future_predictions_pressed:
    # Example API URL, replace it with your actual API endpoint
    api_url = 'https://crypto-assist-gxpggkqnmq-ew.a.run.app/predict'

    # Fetch data from the API
    response = requests.get(api_url)
    print(response.status_code)

    # Parse API response (assuming it's a JSON response)
    api_data = response.json()

    # Assuming the API returns a DataFrame-like structure with 'time' and 'close' columns
    pred_last = np.array(api_data['predicted_price_last_5_days'])

    #Extracting the dates
    existing_dates = tail_df['time']

    # Assuming the API returns a DataFrame-like structure with 'time' and 'close' columns
    pred_future = np.array(api_data['predicted_price_for_next_5_days'])

    # Creating future dates
    future_dates = pd.date_range(existing_dates.max() + pd.Timedelta(days=1), periods=len(pred_future), freq='D')

    api_df_exist = pd.DataFrame(data={'time': existing_dates,'pred': pred_last.flatten()})

    api_df_future = pd.DataFrame(data={'time': future_dates, 'pred_future': pred_future.flatten()})

    combined_df = pd.concat([tail_df, api_df_exist, api_df_future], ignore_index=True)

    # Plotly Express line chart with dots
    fig = px.line(combined_df, x='time', y=['close','pred','pred_future'], markers=True, line_shape='linear', title='Price Over Time')
    fig.update_traces(mode='markers+lines', hovertemplate='%{y:.2f}', marker=dict(size=10))

    # Streamlit display
    st.plotly_chart(fig, use_container_width=True)
elif last_predictions_pressed:
    # Example API URL, replace it with your actual API endpoint
    api_url = 'https://crypto-assist-gxpggkqnmq-ew.a.run.app/predict'

    # Fetch data from the API
    response = requests.get(api_url)
    print(response.status_code)

    # Parse API response (assuming it's a JSON response)
    api_data = response.json()

    # Assuming the API returns a DataFrame-like structure with 'time' and 'close' columns
    pred_last = np.array(api_data['predicted_price_last_5_days'])

    #Extracting the dates
    existing_dates = tail_df['time']

    api_df = pd.DataFrame(data={'time': existing_dates,'pred': pred_last.flatten()})

    combined_df = pd.concat([tail_df, api_df], ignore_index=True)

    # Plotly Express line chart with dots
    fig = px.line(combined_df, x='time', y=['close', 'pred'], markers=True, line_shape='linear', title='Price Over Time')
    fig.update_traces(mode='markers+lines', hovertemplate='%{y:.2f}', marker=dict(size=10))

    # Streamlit display
    st.plotly_chart(fig, use_container_width=True)
else:
    fig = px.line(tail_df, x='time', y='close', markers=True, line_shape='linear', title='Price Over Time')
    fig.update_traces(mode='markers+lines', hovertemplate='%{y:.2f}', marker=dict(size=10))
    st.plotly_chart(fig, use_container_width=True)

if st.button('Test'):

    api_url = 'https://crypto-assist-gxpggkqnmq-ew.a.run.app/predict'

    # Fetch data from the API
    response = requests.get(api_url)
    print(response.status_code)

    # Parse API response (assuming it's a JSON response)
    api_data = response.json()

    st.write(api_data)
