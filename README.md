<h1>Crypto Market Assistant UI</h1>

<h3>Introduction</h3>

This repo is the frontend to the crypto market assistant backend repo which was my final project of bootcamp. The backend contains the data collection, cleaning and multiple deep learning models used to produce a crypto prediction. It also produces an API which the frontend end calls to display the crypto prediction.

<h3>Content</h3>
The repo contains three python files which are used to make up the UI on streamlit. The first file is the homepage which consists of the title and the gif. 

The second page is the current market, this displays a candlestick chart of the bitcoin price for the last six months as well as two technical indicators that can be toggled on and off. It also displays the fear and greed index for the last six months and finally a table view of the bitcoin candlestick chart. 

The final page displays four buttons that will show a variety of predictions, all made by making a call to the API of the backend. The first displays the DARTS models prediction against the actual price of bitcoin for the last six months. The second button shows a more detailed view of this for the last five days and the third button gives predictions for the next five days. The final button shows the predictions of the second deep learning LSTM model. 
