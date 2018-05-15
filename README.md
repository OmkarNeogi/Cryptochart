# Cryptochart

Site running at https://cryptochart.azurewebsites.net (Site takes time to display graph.)
REST API accessible at https://cryptochart.herokuapp.com/chart/btc

Write once read many behavior, GET request returns prices and analyses (Smoothed moving average and Relative Strength index) for the last 31 days. The deployed code is stored in a private repository.

In progress: 
1. D3.JS visualizaton - adding RSI. Button to remove SMMA on clicking double
2. cron based scheduler

<img width="1440" alt="cryptochart-smma-screenshot" src="https://user-images.githubusercontent.com/13189478/40057770-3883c862-581d-11e8-8eba-99a433385c8b.png">
