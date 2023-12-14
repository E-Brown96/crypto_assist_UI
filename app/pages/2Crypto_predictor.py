import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import requests
import os
import plotly.express as px

st.markdown('<h1 style="color:#FFB81C;text-align: center;font-size: 72px;">Crypto Predictor</h1>', unsafe_allow_html=True)

route_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

df = pd.read_csv(os.path.join(route_path, 'raw_data/BTC.csv'))

df['time'] = pd.to_datetime(df['time'])

df = df[['time','close']]

tail_df = df.tail(5)

#st.markdown('<p style="color:#CCCCCC;text-align: center;font-size: 24px;">\
#    Explore the dynamic world of cryptocurrency with our advanced AI model. Witness the forecasted trends as our crypto assistant predicts Bitcoin prices over the past five days.</p>', unsafe_allow_html=True)

st.markdown('<p style="color:#CCCCCC;text-align: center;font-size: 24px;">\
    Click the buttons below to unveil your personalized insights into the crypto market! 🚀💰</p>', unsafe_allow_html=True)

@st.cache(show_spinner=False,suppress_st_warning=True)
def fetch_api_data(api_url):
    response = requests.get(api_url)
    print(response.status_code)
    return response.json()

historical_predictions_pressed = st.button('Check Historical Predictions vs Real Price')

if historical_predictions_pressed:
    # Example API URL, replace it with your actual API endpoint
    api_url = 'https://crypto-assist-gxpggkqnmq-ew.a.run.app/predict'

    # Parse API response (assuming it's a JSON response)
    api_data = fetch_api_data(api_url)

    # Assuming the API returns a DataFrame-like structure with 'time' and 'close' columns
    hist_pred = np.array(api_data['historical_prediction'])

    hist_actual = np.array(api_data['validation'])

    #Extracting the dates
    existing_dates = df['time']

    desired_length = len(existing_dates)

    # Trim arrays to the desired length
    trimmed_hist_actual = hist_actual[:desired_length]
    trimmed_hist_pred = hist_pred.flatten()[:desired_length]

    # Create DataFrame with aligned arrays
    api_df = pd.DataFrame(data={'time': existing_dates, 'historical_actual': trimmed_hist_actual, 'hist_prediction': trimmed_hist_pred})

    combined_df = pd.concat([df, api_df], ignore_index=True)

    # Plotly Express line chart with dots
    fig = px.line(combined_df, x='time', y=['historical_actual', 'hist_prediction'], line_shape='linear', title='Price Over Time')
    fig.update_traces(mode='lines', hovertemplate='%{y:.2f}',
                  line=dict(color='dodgerblue'))
    fig.update_traces(selector=dict(name='hist_prediction'), line=dict(color='lightcoral'))

    fig.update_layout(yaxis_range=[0, 50000])

    # Streamlit display
    st.plotly_chart(fig, use_container_width=True)

last_predictions_pressed = st.button('Check Predictions vs Real Price')

future_predictions_pressed = st.button('Check Future Predictions')

st.markdown(
    """
    <style>
        div.stButton > button {
            display: block;
            margin: 0 auto;
        }
    </style>
    """,
    unsafe_allow_html=True
)

if future_predictions_pressed:
    # Example API URL, replace it with your actual API endpoint
    api_url = 'https://crypto-assist-gxpggkqnmq-ew.a.run.app/predict'

    # Parse API response (assuming it's a JSON response)
    api_data = fetch_api_data(api_url)

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
    fig.update_traces(mode='markers+lines', hovertemplate='%{y:.2f}', marker=dict(size=10), line=dict(color='dodgerblue'))
    fig.update_traces(selector=dict(name='pred'), line=dict(color='lightcoral'))
    fig.update_traces(selector=dict(name='pred_future'), line=dict(color='lightgreen'))


    # Streamlit display
    st.plotly_chart(fig, use_container_width=True)
elif last_predictions_pressed:
    # Example API URL, replace it with your actual API endpoint
    api_url = 'https://crypto-assist-gxpggkqnmq-ew.a.run.app/predict'

    # Parse API response (assuming it's a JSON response)
    api_data = fetch_api_data(api_url)

    # Assuming the API returns a DataFrame-like structure with 'time' and 'close' columns
    pred_last = np.array(api_data['predicted_price_last_5_days'])

    #Extracting the dates
    existing_dates = tail_df['time']

    api_df = pd.DataFrame(data={'time': existing_dates,'pred': pred_last.flatten()})

    combined_df = pd.concat([tail_df, api_df], ignore_index=True)

    # Plotly Express line chart with dots
    fig = px.line(combined_df, x='time', y=['close', 'pred'], markers=True, line_shape='linear', title='Price Over Time')
    fig.update_traces(mode='markers+lines', hovertemplate='%{y:.2f}', marker=dict(size=10))
    fig.update_traces(mode='markers+lines', hovertemplate='%{y:.2f}', marker=dict(size=10), line=dict(color='dodgerblue'))
    fig.update_traces(selector=dict(name='pred'), line=dict(color='lightcoral'))

    # Streamlit display
    st.plotly_chart(fig, use_container_width=True)


alt_model_predictions = st.button('Additional Model Predictions')

if alt_model_predictions:
    # Example API URL, replace it with your actual API endpoint
    api_url = 'https://crypto-assist-gxpggkqnmq-ew.a.run.app/predict'

    # Parse API response (assuming it's a JSON response)
    api_data = fetch_api_data(api_url)

    # Assuming the API returns a DataFrame-like structure with 'time' and 'close' columns
    pred_last = np.array(api_data['DL_predict_last'][0])

    #Extracting the dates
    existing_dates = tail_df['time']

    # Assuming the API returns a DataFrame-like structure with 'time' and 'close' columns
    pred_future = np.array(api_data['DL_predict_next'][0])

    # Creating future dates
    future_dates = pd.date_range(existing_dates.max() + pd.Timedelta(days=1), periods=len(pred_future), freq='D')

    api_df_exist = pd.DataFrame(data={'time': existing_dates,'pred': pred_last.flatten()})

    api_df_future = pd.DataFrame(data={'time': future_dates, 'pred_future': pred_future.flatten()})

    combined_df = pd.concat([tail_df, api_df_exist, api_df_future], ignore_index=True)

    # Plotly Express line chart with dots
    fig = px.line(combined_df, x='time', y=['close','pred','pred_future'], markers=True, line_shape='linear', title='Price Over Time')
    fig.update_traces(mode='markers+lines', hovertemplate='%{y:.2f}', marker=dict(size=10), line=dict(color='dodgerblue'))
    fig.update_traces(selector=dict(name='pred'), line=dict(color='lightcoral'))
    fig.update_traces(selector=dict(name='pred_future'), line=dict(color='lightgreen'))

    # Streamlit display
    st.plotly_chart(fig, use_container_width=True)


if st.button('Reset'):

    st.markdown('<p style="color:#CCCCCC;text-align: center;font-size: 24px;">\
    Ready to predict! 🚀💰</p>', unsafe_allow_html=True)

#comment update
