import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import requests

url= f'https://crypto-docker-image-gxpggkqnmq-uc.a.run.app/predict'
r = requests.get(url)
data = r.json()

st.write(data)
