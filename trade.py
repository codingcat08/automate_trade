import upstox_client
import pandas as pd
from upstox_client.rest import ApiException
import json
import time 
configuration = upstox_client.Configuration()
configuration.access_token = 'eyJ0eXAiOiJKV1QiLCJrZXlfaWQiOiJza192MS4wIiwiYWxnIjoiSFMyNTYifQ.eyJzdWIiOiI1TEE3TksiLCJqdGkiOiI2NzViZjc3ZjJjMDQyZDYzNzZjMTI1MGEiLCJpc011bHRpQ2xpZW50IjpmYWxzZSwiaWF0IjoxNzM0MDgwMzgzLCJpc3MiOiJ1ZGFwaS1nYXRld2F5LXNlcnZpY2UiLCJleHAiOjE3MzQxMjcyMDB9.L1BPll9D2qD1ClwP1cj_I8uB6zbpJZOuP6FYkmWOJeU'
api_version = '2.0'
history_api_instance = upstox_client.HistoryApi(upstox_client.ApiClient(configuration))
market_quote_api_instance = upstox_client.MarketQuoteApi(upstox_client.ApiClient(configuration))
instrument_key = 'NSE_EQ|INE839G01010'
interval = 'month'
to_date = '2023-11-13'
def fetch_historical_data(instrument_key, interval, to_date, api_version):
    try:
        api_response = history_api_instance.get_historical_candle_data(instrument_key, interval, to_date, api_version)
        string = str(api_response)  # Convert the api response to string
        string = string.replace("'", "\"")  # Replace single quotes with double quotes to make it a valid JSON string
        json_dict = json.loads(string)  # convert the string to python dictionary
        df = pd.DataFrame(json_dict['data']['candles'],columns=['time_stamp', 'open', 'high', 'low', 'close', 'volume', 'open_interest'])
        print(df.describe())
        return df
    except ApiException as e:
        print(f"Exception when calling HistoryApi->get_historical_candle_data for {interval}: {e}")
        return None
data_1D = fetch_historical_data(instrument_key, 'day', to_date, api_version)
data_1W = fetch_historical_data(instrument_key, 'week', to_date, api_version)
data_1M = fetch_historical_data(instrument_key, 'month', to_date, api_version)

# Calculate EMAs for all time frames
def calculate_ema(data, window):
    data[f'EMA_{window}'] = data['close'].ewm(span=window, adjust=False).mean()
    return data

data_1D = calculate_ema(data_1D, 20)
data_1D = calculate_ema(data_1D, 50)
data_1D = calculate_ema(data_1D, 100)
data_1D = calculate_ema(data_1D, 200)

data_1W = calculate_ema(data_1W, 20)
data_1W = calculate_ema(data_1W, 50)
data_1W = calculate_ema(data_1W, 100)
data_1W = calculate_ema(data_1W, 200)

data_1M = calculate_ema(data_1M, 20)
data_1M = calculate_ema(data_1M, 50)
data_1M = calculate_ema(data_1M, 100)
data_1M = calculate_ema(data_1M, 200)
symbol = 'NSE_EQ:JOCIL'
api_instance = upstox_client.MarketQuoteApi(upstox_client.ApiClient(configuration))
def fetch_live_data(symbol , api_version):
    try:
        api_response = market_quote_api_instance.ltp(symbol, api_version)
        print(api_response)
        # Convert the response to a string
        response_str = str(api_response)
        # Replace single quotes with double quotes to make it a valid JSON string
        response_str = response_str.replace("'", "\"")
        # Parse the JSON string into a dictionary
        json_dict = json.loads(response_str)
        # Extract the relevant data for the symbol
        live_data = json_dict['data']['NSE_EQ:JOCIL']
        # Convert the data to a DataFrame
        live_data_df = pd.DataFrame([live_data], columns=['instrument_token', 'last_price'])
        return live_data_df
    except ApiException as e:
        print(f"Exception when calling MarketQuoteApi->ltp: {e}")
        return None
live_data_df = fetch_live_data(instrument_key, api_version)
print(live_data_df)
print(data_1D['volume'].iloc[-1])
print(data_1D['volume'].iloc[-2])
if live_data_df is not None:
    # Extract live price from the DataFrame
    live_price = live_data_df['last_price'].iloc[0]
    print(f"Live Price: {live_price}")

    # Check selection criteria
    def check_selection_criteria(live_price, data_1D):
        # Ensure the stock is above the 20 EMA on the 1D time frame
        if data_1D is not None and live_price > data_1D['EMA_20'].iloc[-1]:
            
            #consolidation of candles slightly above or on the 20 EMA on the 1D time frame
            if data_1D is not None and all(data_1D['close'].iloc[-5:].between(data_1D['EMA_20'].iloc[-5:], data_1D['EMA_20'].iloc[-5:] * 1.01)):
                
                # a strong candle breakout with significant buying volume on the 1D time frame
                if data_1D is not None and data_1D['volume'].iloc[-1] > data_1D['volume'].iloc[-2] * 1.5:
                    print("Entry condition met. Strong candle breakout with significant buying volume.")
                    
                    #stop loss at the previous swing low
                    stop_loss = data_1D['low'].iloc[-2]
                    print(f"Stop loss set at: {stop_loss}")
                    
                    # target based on risk-reward ratio of 1:2
                    risk = live_price - stop_loss
                    target = live_price + (risk * 2)
                    print(f"Target set at: {target} (Risk-Reward 1:2)")
                    execute_trade(live_price, stop_loss, target)
                    return True
        return False

    # Assuming data_1D is already fetched and calculated
    data_1D = None  # Replace with actual historical data

    if check_selection_criteria(live_price, data_1D):
        print("Trade criteria met. Execute the trade.")
    else:
        print("Trade criteria not met.")
else:
    print("Failed to fetch live data.")


def execute_trade(entry_price, stop_loss, target):
    print(f"Executing trade: Entry Price = {entry_price}, Stop Loss = {stop_loss}, Target = {target}")
    # Add your trade execution logic here (e.g., placing an order via the Upstox API)
# Main live monitoring loop
def live_monitoring(instrument_key, api_version, data_1D):
    print("Starting live monitoring...")
    while True:
        try:
            # Fetch live data
            live_data_df = fetch_live_data(instrument_key, api_version)
            if live_data_df is not None:
                live_price = live_data_df['last_price'].iloc[0]
                print(f"Live Price: {live_price}")
                
                # Check and execute trade if conditions are met
                if check_selection_criteria(live_price, data_1D):
                    print("Trade executed successfully.")
                else:
                    print("Trade criteria not met.")
            
            # Wait for a few seconds before fetching live data again
            time.sleep(5)  # Adjust the sleep time as needed
        
        except KeyboardInterrupt:
            print("Live monitoring stopped by user.")
            break
        except Exception as e:
            print(f"Error during live monitoring: {e}")
            time.sleep(5)  # Wait before retrying


#live_monitoring(symbol, api_version, data_1D)