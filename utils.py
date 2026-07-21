def preprocess(data):
    import numpy as np
    short_window = 20
    long_window = 50
    
    data['Returns'] = data['Close'].pct_change()
    data['Short_MA'] = data['Close'].rolling(window=short_window).mean()
    data['Long_MA'] = data['Close'].rolling(window=long_window).mean()
    data['Price_Diff'] = data['Close'].diff()
    
    data.dropna(inplace=True)

    # Check for NaN values
    data = data.replace([np.inf, -np.inf], np.nan)
    data = data.dropna()

    return data


# Executing a buy order in Alpaca
def simple_order(qty,api_key,api_secret,symbol='BTC/USD',side="buy",type='market',time_in_force='gtc'):
    from alpaca.trading.client import TradingClient
    from alpaca.trading.requests import MarketOrderRequest
    from alpaca.trading.enums import OrderSide, TimeInForce

    base_url = 'https://paper-api.alpaca.markets/v2'  # for paper trading

    trading_client = TradingClient(api_key, api_secret, paper=True)
    # Setting parameters for our buy order
    market_order_data = MarketOrderRequest(
                          symbol=symbol,
                          qty=qty,
                          side=side,
                          time_in_force=time_in_force,
                          order_class="simple",
                      )
    # Submitting the order and then printing the returned object
    market_order = trading_client.submit_order(market_order_data)


# Send message
def telegram_bot_sendtext(bot_message,token,id):
    import requests
    
    send_text = 'https://api.telegram.org/bot' + token + '/sendMessage?chat_id=' + id + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()

# Risk management
def calc_share(atr,investment,risk):
  # risk in %
  share_size = investment*risk/100/atr
  return share_size
