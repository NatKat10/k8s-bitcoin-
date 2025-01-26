import time
import requests
import os

import sys
sys.stdout.reconfigure(line_buffering=True)
# store the prices in a list and initialize last price and latest avarge to display in the html file 
prices = []
latest_avg_price = None 
last_price = None
# fetch the current Bitcoin price - documentation - https://docs.coincap.io/
# example of data returning by the api request: 
'''{
  "data": {
    "id": "bitcoin",
    "rank": "1",
    "symbol": "BTC",
    "name": "Bitcoin",
    "supply": "17193925.0000000000000000",
    "maxSupply": "21000000.0000000000000000",
    "marketCapUsd": "119179791817.6740161068269075",
    "volumeUsd24Hr": "2928356777.6066665425687196",
    "priceUsd": "6931.5058555666618359",
    "changePercent24Hr": "-0.8101417214350335",
    "vwap24Hr": "7175.0663247679233209"
  },
  "timestamp": 1533581098863
}'''
#i only take the priceUsd from it. 
def get_bitcoin_price():
    try:
        url = "https://api.coincap.io/v2/assets/bitcoin"
        response = requests.get(url)
        response.raise_for_status()  # raise an error if the request failed
        data = response.json()
        return float(data['data']['priceUsd'])  # taking the priceUsd from the data 
    except requests.RequestException as e:
        print(f"Error fetching Bitcoin price: {e}")
        return None

def log_to_html(current_price, avg_price=None):
    global latest_avg_price, last_price
    if avg_price is not None:
        latest_avg_price = avg_price  # update the latest average

    # adding price movement arrow
    if last_price is not None:
        if current_price > last_price:
            arrow = '<span style="color:green;">&#9650;</span>'  # Green up arrow ▲
        elif current_price < last_price:
            arrow = '<span style="color:red;">&#9660;</span>'  # Red down arrow ▼
        else:
            arrow = '<span style="color:yellow;">&#9654;</span>'  # Yellow right arrow ▶
    else:
        arrow = ""  # Initial state 

    # output_path = os.path.join(os.path.dirname(__file__), "output.html")
    output_path = os.path.join(os.path.dirname(__file__), "index.html")


    last_price = current_price  #update the last price 
    with open(output_path, "w",encoding="utf-8") as f:
        f.write(f"""
        <html>
        <head>
            <title>Bitcoin Price Dashboard</title>
            <meta http-equiv="refresh" content="30;url=/service-a?{int(time.time())}">

            <style>
                body {{
                    font-family: 'Aptos', sans-serif;
                    text-align: center;
                    background-color: #f4f4f4;
                    color: #333;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                }}
                h1 {{
                    font-size: 2.5rem;
                    margin-bottom: 20px;
                }}
                p {{
                    font-size: 1.5rem;
                    margin: 10px 0;
                }}
                .bouncing-bitcoin {{
                    width: 100px;
                    animation: bounce 2s infinite;
                }}
                @keyframes bounce {{
                    0%, 100% {{ transform: translateY(0); }}
                    50% {{ transform: translateY(-20px); }}
                }}
            </style>

        </head>
        <body>
            <h1>Bitcoin Price Dashboard</h1>
            <img src="https://cryptologos.cc/logos/bitcoin-btc-logo.png" alt="Bouncing Bitcoin" class="bouncing-bitcoin">
            <p><b>Current Bitcoin Price:</b> ${current_price:.5f} {arrow}</p>
        """)
        if latest_avg_price is not None:
            f.write(f"""
            <p><b>10-Minute Average Price:</b> ${latest_avg_price:.5f}</p>
            """)
        f.write("</body></html>")


# function to calculate the avg after 10 minutes
def calculate_average(prices):
    return sum(prices) / len(prices) if prices else 0

# main loop to fetch prices and calculate the average
minute_counter = 0  # track the minutes

while True:
    price = get_bitcoin_price()
    
    if price is not None:  # continue only if price fetched correctly 
        prices.append(price)
        if len(prices) > 60:
            prices.pop(0)
        print(f"Current Bitcoin Price: ${price:.5f}")
        log_to_html(price)  # update HTML file with the current price

        # increment counter every minute 
        minute_counter += 1
        
        # every 10 minutes calculate the average of the last 10 prices
        if minute_counter == 10:
            avg_price = calculate_average(prices[-10:])
            print(f"Average Bitcoin Price over the last 10 minutes: ${avg_price:.5f}")
            log_to_html(price, avg_price)  # update HTML file with the 10-minute average

            minute_counter = 0  # reset the counter after printing the average
        # print(len(prices))
    
    # sleep for 60 seconds (1 minute)
    time.sleep(60)
