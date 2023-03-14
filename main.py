import snscrape.modules.twitter as twitter
import time
import re
import ccxt

# We long if CPI is positive
def long():
    try:
        exchange.create_market_order("BTCUSDT", "buy", 0.5) # Enter which coins you want to long and how much
        exchange.create_market_order("ETHUSDT", "buy", 1) # This code would long half BTC and 1 ETH, roughly for $12k
        print("CPI came in positive - LONGED.")
    except Exception as e:
        print(f"Error during order creation: {e}")

# We short if CPI is negative
def short():
    try:
        exchange.create_market_order("BTCUSDT", "sell", 0.5) # Same thing, just shorting
        exchange.create_market_order("ETHUSDT", "sell", 1) # So adjust the quantity and coins as necessary. You can add or remove them
        print("CPI came in negative - SHORTED.")
    except Exception as e:
        print(f"Error during order creation: {e}")

exchange = ccxt.bybit({
    'apiKey': 'xxxxx', # Enter your API and secret key in quotes instead of x
    'secret': 'xxxxx'
})

is_newest_tweet = "Not"

while True:
    time.sleep(0.01)
    # We take the newest tweet from Tree News
    tweet = next(twitter.TwitterSearchScraper('from:News_Of_Alpha').get_items())
    latest_tweet = tweet.rawContent
    # If we don't find a new tweet, we look again
    if latest_tweet == is_newest_tweet:
        continue
    is_newest_tweet = latest_tweet
    # We search for the first number in the tweet, which should be inter-year inflation according to the format
    match = re.search(r'\d+\.?\d*', is_newest_tweet)
    if match:
        inflation = float(match.group())
        print(inflation)
    else:
        print("No number found in the tweet")
    # The message must start with U.S., otherwise it's not a CPI print
    if is_newest_tweet.startswith("U.S."):
        print(f"This is a CPI print. Inflation is: {inflation}")

        if inflation >= 6.4: # Here we adjust the number based on expected inflation
            short()
            break

        if inflation <= 6: # Here we adjust the number based on expected inflation
            long()
            break

        print("Wasn't worth trading.")
    print("Tweet isn't CPI print. Waiting...")
