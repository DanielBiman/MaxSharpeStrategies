
import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv

import os
import requests
import yfinance 
import numpy as np

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

from utils import *

# Choose here the Trading Environment class
from RL_Model_0 import *

# Secrets
token = str(os.environ["TOKEN"])
user_id = str(os.environ["GROUP_ID"]) 

api_key = str(os.environ["API_KEY"]) 
api_secret = str(os.environ["API_SECRET"]) 

atr_period = 11
atr_multiplier = 3.0

investment = 100000
symbol = "BTC-USD"
#interval = "30m"

#data = yfinance.Ticker(symbol).history(period="1mo", interval="1d") # state = data.iloc[-1] issue
data = yfinance.download(tickers=[symbol],period="max")

data = preprocess(data)

# Create the trading environment TODO this is gym not gymnasium? maybe cause of the dummywrap
env = DummyVecEnv([lambda: TradingEnv(data)])

# All inputs for the model. 
# Here: Index(['Open', 'High', 'Low', 'Close', 'Volume', 'Returns', 'Short_MA',
# 'Long_MA', 'Price_Diff', 'Position'],
# dtype='object')
state = data.iloc[-1]

# Load model
model = PPO.load("sharpe_ppo_trading_model", env=env)

action, _states = model.predict(state)
print('Action: ',action)

# Initialize the Alpaca Trading Client
trading_client = TradingClient(api_key, api_secret, paper=True)

# BUY
if action == 0:
    # TODO: Doublecheck
    qty = calc_share(atr=1000,investment = 100000, risk = 5)
    
    print(f"Buy {qty} {symbol} at {state}")
    
    #if qty > 0.5:qty=0.123
    ###### For TESTING############
    qty = 0.1

    simple_order(qty,api_key,api_secret)
    message = "Buy " +  str(qty) + " " + str(symbol) + " at " + str(state['Close'])
    telegram_bot_sendtext(message,token,user_id)


# SELL - Shorting not possible
elif action == 2:
    # Get all open positions
    positions = trading_client.get_all_positions()

    # Close each position individually
    for position in positions:
        market_order_data = MarketOrderRequest(
            symbol=position.symbol,
            # qty=position.qty,
            # Reduced qty due to 200k order size limit from Alpaca
            qty = [200000/float(position.current_price) if float(position.qty)*float(position.current_price) > 200000 else float(position.qty)]

            side=OrderSide.SELL,
            time_in_force=TimeInForce.GTC
        )
        trading_client.submit_order(order_data=market_order_data)
        
    message = "Sell all at " + str(state['Close'])
    telegram_bot_sendtext(message,token,user_id)

else:
    message = "Hold." 
    telegram_bot_sendtext(message,token,user_id)


######################################################################################


print('Finished script')
