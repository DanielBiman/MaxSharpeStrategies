# MaxSharpeStrategies
An attempt to create a fully autonomous trading system using AI. The goal is to increase the sharpe value and have an automatic system predict prices and execute orders.

main.py contains the downloading of the data, the loading of the model, the prediction, executing the prediction in Alpaca and sending a message in Telegram.

RL_model_X contains the class TradingEnvironment for Model X. The training was made in RL_algorithm.ipynb and it saved the trained model in XXX_trading_model.zip

utils.py contains usefull functions.

.github/workflows contains schedule.yml which is a cron job which gets executed currently every 4 hours.

Under Actions you can run the workflow manually for testing.
