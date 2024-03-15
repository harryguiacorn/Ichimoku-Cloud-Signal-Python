# Cloud Signal Python #

[View demo here](https://harryguiacorn.github.io/Ichimoku-Cloud-Signal-Python/ "S&P500 Cloud Scan")

<a target="_blank" href="https://colab.research.google.com/github/harryguiacorn/Cloud-Signal-Python">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

## Status Update [2024.02.06] ## 

Uncover market movers with ease! This application analyses data silently and generates web pages displaying strength scores for every stock in major indices. Dive deeper into each stock's cloud and TKx strength, calculated using powerful multi-timeframe Ichimoku analysis. Finally, see the ultimate verdict: a clear total score for each stock. Dominate the market by sorting through this scorecard, instantly identifying the champions and laggards primed for your trading moves.

![image](https://github.com/harryguiacorn/Ichimoku-Cloud-Signal-Python/assets/1398153/f6b655be-a4a3-489a-94e3-71f8ce627f5b)

![image](https://github.com/harryguiacorn/Ichimoku-Cloud-Signal-Python/assets/1398153/861cfde8-851b-4beb-80ec-c6e6625bbfc2)

![image](https://github.com/harryguiacorn/Ichimoku-Cloud-Signal-Python/assets/1398153/cb903cdf-f2f0-414e-85f0-f6576f826deb)

![image](https://github.com/harryguiacorn/Ichimoku-Cloud-Signal-Python/assets/1398153/ba8a2fde-33c2-40c2-ad7f-0a1e612e65fa)

![image](https://github.com/harryguiacorn/Ichimoku-Cloud-Signal-Python/assets/1398153/312d3ea9-c5ea-451b-8b97-31c49ffa8c87)

![image](https://github.com/harryguiacorn/Ichimoku-Cloud-Signal-Python/assets/1398153/ac38ff46-8025-4031-a94b-9daf60c69ad9)

![image](https://github.com/harryguiacorn/Ichimoku-Cloud-Signal-Python/assets/1398153/46f66f48-7f16-4434-adda-24493831d434)

![image](https://github.com/harryguiacorn/Ichimoku-Cloud-Signal-Python/assets/1398153/70c626d8-3d2f-44e6-9d84-4375035c7495)

![image](https://github.com/harryguiacorn/Ichimoku-Cloud-Signal-Python/assets/1398153/254b69e2-3caa-4030-bb09-d3de1abbef8c)

![image](https://github.com/harryguiacorn/Ichimoku-Cloud-Signal-Python/assets/1398153/c471fa6d-cd46-407c-9b0b-0f561e12dca9)


## Status Update [2023.11.14] ## 
- This project is work in progress, the intention is to produce Ichimoku Cloud signals like in the author's [Cloud Service](https://github.com/harryguiacorn/cloudservice) which is written in PHP. The back end of the coding is taking shape, see below screenshots from one of output files:
### Ichimoku Kijun-sen Signal ###
<img width="498" alt="Screenshot 2022-11-15 at 18 07 50" src="https://user-images.githubusercontent.com/1398153/201997990-165cd688-8f86-47c1-bb34-2b334a26a77a.png">

### Candlestick Kicker Signal ###
<img width="498" alt="Screenshot 2022-11-15 at 18 08 09" src="https://user-images.githubusercontent.com/1398153/201998002-d8365f05-8a34-42cb-8501-5fcd05a59ce9.png">





## Steps to get it up and running ##
- Open main.py file it contains commands for creating Ichimoku signals and candlestick kicker signals for S&P 500, Dow Jones 30, Nasdaq 100, FTSE 100, FTSE 250, Futures and Currency Futures markets.
- Comment out the commands not required to run and run this file. Note indices such as S&P 500 which has around 500 stocks therefore would take some time to download its historical data from Yahoo Finance.
