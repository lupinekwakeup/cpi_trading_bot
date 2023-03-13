import snscrape.modules.twitter as twitter
import time
import re
import ccxt

# Longujeme v pripade, ze CPI je pozitivni
def long():
    try:
        exchange.create_market_order("BTCUSDT", "buy", 0.5) # Zadejte, jake coiny chcete longnout a kolik
        exchange.create_market_order("ETHUSDT", "buy", 1) # Tento kod by longnul pul BTC a 1 ETH, tedy cca za $12k
        print("CPI came in positive - LONGED.")
    except Exception as e:
        print(f"Error during order creation: {e}")

# Shortujeme v pripade, ze je CPI negativni
def short():
    try:
        exchange.create_market_order("BTCUSDT", "sell", 0.5) # To same, akorat se shortuje
        exchange.create_market_order("ETHUSDT", "sell", 1) # Tzn. upravte si quantity a pripadne coiny. Muzete si je pridat i odebrat
        print("CPI came in negative - SHORTED.")
    except Exception as e:
        print(f"Error during order creation: {e}")

exchange = ccxt.bybit({
    'apiKey': 'xxxxx', # Zadejte do uvozovek vas API a secret key misto x
    'secret': 'xxxxx'
})

is_newest_tweet = "Not"

while True:
    time.sleep(0.01)
    # Vezmeme nejnovejsi Tweet od Tree News
    tweet = next(twitter.TwitterSearchScraper('from:News_Of_Alpha').get_items())
    latest_tweet = tweet.rawContent
    # Pokud nenalezneme novy Tweet, hledame znovu
    if latest_tweet == is_newest_tweet:
        continue
    is_newest_tweet = latest_tweet
    # Hledame prvni cislo v Tweetu, ktere dle formatu ma byt mezirocni inflace
    match = re.search(r'\d+\.?\d*', is_newest_tweet)
    if match:
        inflation = float(match.group())
        print(inflation)
    else:
        print("No number found in the tweet")
    # Zprava musi zacinat s U.S., jinak se take nejedna o CPI print
    if is_newest_tweet.startswith("U.S."):
        print(f"This is a CPI print. Inflation is: {inflation}")

        if inflation >= 6.4: # Zde upravime cislo podle ocekavane inflace
            short()
            break

        if inflation <= 6: # Zde upravime cislo podle ocekavane inflace
            long()
            break

        print("Wasnt worth trading.")
    print("Tweet isnt CPI print. Waiting...")







