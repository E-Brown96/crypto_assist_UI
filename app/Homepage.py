import streamlit as st
import pandas as pd
import numpy as np
import requests
import io
import base64

#001119

st.markdown('<h1 style="color:#FFB81C;text-align: center;font-size: 72px;">Crypto Market Assistant</h1>', unsafe_allow_html=True)

st.markdown('<h3 style="color: #CCCCCC;text-align: center;">Introducing your cutting-edge AI companion, designed to guide you skillfully through the dynamic world of cryptocurrencies!</h3>', unsafe_allow_html=True)

file_path = "raw_data/bitcoin.gif"

with open(file_path, "rb") as file:
    contents = file.read()

# Convert the contents to base64
data_url = base64.b64encode(contents).decode("utf-8")

# Set the desired width and height
width = 625
height = 500

# Display the image with specified size using st.markdown
st.markdown(
    f'<div style="text-align: center">'
    f'<img src="data:image/gif;base64,{data_url}" alt="Bitcoin GIF" width="{width}" height="{height}">'
    '</div>',
    unsafe_allow_html=True,
)
