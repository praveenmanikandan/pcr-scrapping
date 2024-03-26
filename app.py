import requests
import threading
import time
from datetime import datetime
from datetime import datetime, time as dtime

def getPCR(tradingPair):
    # Define the URL for the API endpoint
    optionType="equities"
    if tradingPair=="NIFTY" or tradingPair=="BANKNIFTY":
        optionType="indices"
        
    url = f"https://www.nseindia.com/api/option-chain-{optionType}?symbol={tradingPair}"

    # Create a session object
    session = requests.Session()

    # Set headers for the initial request to obtain cookies
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept': '*/*',
        "Referer": "https://www.nseindia.com/option-chain"
    }

    # Send a GET request to the webpage to get initial cookies
    response = session.get("https://www.nseindia.com/option-chain", headers=headers)

    # Check if the initial request is successful
    if response.status_code == 200:

        # Send a GET request to fetch option chain data
        response = session.get(url, headers=headers)

        # Check if the request to fetch option chain data is successful
        if response.status_code == 200:
            # Parse response JSON
            json_data = response.json()
            
            # Desired expiry date for which you want to sum open interest
            desired_expiry_date = expiry_date[tradingPair]

            # Initialize sum of open interest for Put and Call options
            open_interest_sum_PE = 0
            open_interest_sum_CE = 0

            # Iterate over the data array
            for option_data in json_data["records"]["data"]:
                # Check if the option's expiry date matches the desired expiry date
                if option_data["expiryDate"] == desired_expiry_date:
                    # Add the open interest of Put options to the sum
                    if 'PE' in option_data:
                        open_interest_sum_PE += option_data["PE"]["openInterest"]
                    # Add the open interest of Call options to the sum
                    if 'CE' in option_data:
                        open_interest_sum_CE += option_data["CE"]["openInterest"]

            # Calculate PCR (Put-Call Ratio)
            pcr = open_interest_sum_PE / open_interest_sum_CE if open_interest_sum_CE != 0 else 0

            # Print the sum of open interest for the desired expiry date
            return pcr

        else:
            print(f"Failed to fetch option chain data. Status code: {response.status_code}")
            return 0

    else:
        print(f"Failed to fetch initial data. Status code: {response.status_code}")
        return 0


# Define a list of trading pairs
trading_pairs=["TATASTEEL","TCS","RELIANCE","SBIN","SAIL","PNB","ITC","BANKNIFTY","NIFTY"]

# Define the desired expiry date for each trading pair
expiry_date = {
    "BANKNIFTY": "27-Mar-2024",
    "NIFTY":"28-Mar-2024",
    "RELIANCE":"28-Mar-2024",
    "TCS":"28-Mar-2024",
    "TATASTEEL":"28-Mar-2024",
    "SBIN":"28-Mar-2024",
    "SAIL":"28-Mar-2024",
    "PNB":"28-Mar-2024",
    "ITC":"28-Mar-2024",
}

# Define a function to scrap PCR data for a trading pair
def scrapPCR(trading_pair):
    start_time = dtime(6, 30)
    end_time = dtime(15, 20)
    while True:
        current_time = datetime.now().time()
        if start_time <= current_time <= end_time:
            pcr = getPCR(trading_pair)
            print(f"PCR for {trading_pair}: {pcr}")
        time.sleep(60)  # Wait for 1 minute before scraping again

# Create a thread for each trading pair and start scraping
threads = []
for trading_pair in trading_pairs:
    thread = threading.Thread(target=scrapPCR, args=(trading_pair,))
    thread.start()
    threads.append(thread)

# Wait for all threads to finish
for thread in threads:
    thread.join()
