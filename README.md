# Cloud Signal Python #

[View demo here](https://harryguiacorn.github.io/Ichimoku-Cloud-Signal-Python/ "S&P500 Cloud and TKx score page")

<a target="_blank" href="https://colab.research.google.com/github/harryguiacorn/Cloud-Signal-Python">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

## Status Update ## 
- This project is work in progress, the intention is to produce Ichimoku Cloud signals like in the author's [Cloud Service](https://github.com/harryguiacorn/cloudservice) which is written in PHP. The back end of the coding is taking shape, see below screenshots from one of output files:
### Ichimoku Kijun-sen Signal ###
<img width="498" alt="Screenshot 2022-11-15 at 18 07 50" src="https://user-images.githubusercontent.com/1398153/201997990-165cd688-8f86-47c1-bb34-2b334a26a77a.png">

### Candlestick Kicker Signal ###
<img width="498" alt="Screenshot 2022-11-15 at 18 08 09" src="https://user-images.githubusercontent.com/1398153/201998002-d8365f05-8a34-42cb-8501-5fcd05a59ce9.png">





## Steps to get it up and running ##
- Open main.py file it contains commands for creating Ichimoku signals and candlestick kicker signals for S&P 500, Dow Jones 30, Nasdaq 100, FTSE 100, FTSE 250, Futures and Currency Futures markets.
- Comment out the commands not required to run and run this file. Note indices such as S&P 500 which has around 500 stocks therefore would take some time to download its historical data from Yahoo Finance.
