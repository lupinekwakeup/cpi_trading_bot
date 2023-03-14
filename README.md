# CPI Trading Bot

This is a Python script for a trading bot that executes long or short trades on certain cryptocurrencies based on the latest Consumer Price Index (CPI) print in the U.S.

## Dependencies

This script requires the following Python libraries to be installed:

snscrape
ccxt
You can install them using pip:

'''pip install snscrape ccxt'''

## Usage

1. Replace the API key and secret in the exchange object with your own API key and secret.
2. Adjust the create_market_order() functions in the long() and short() functions with the coins you want to long or short and how much.
3. Adjust the if inflation >= X and if inflation <= Y statements in the main loop with the expected inflation rates for long and short trades.
4. Run the script:

'''python main.py'''

The script will continuously monitor Twitter for the latest tweet from Tree News, which contains the latest CPI print. If the tweet starts with "U.S.", the script extracts the inter-year inflation rate and executes a long or short trade on the specified cryptocurrencies if the inflation rate is above or below the expected rates.
