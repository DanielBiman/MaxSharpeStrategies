
import gym
import numpy as np

class TradingEnv(gym.Env):
    def __init__(self, data):
        super(TradingEnv, self).__init__()
        self.data = data
        self.current_step = 0
        self.action_space = gym.spaces.Discrete(3)  # Buy, Hold, Sell
        self.observation_space = gym.spaces.Box(low=-np.inf, high=np.inf, shape=(data.shape[1],), dtype=np.float32)
        
        # Initialize additional variables to track returns
        self.returns = []
        self.position = 0  # 1 for holding a position, 0 for no position

    def reset(self):
        self.current_step = 0
        self.returns = []
        self.position = 0
        return self.data.iloc[self.current_step].values

    def step(self, action):
        self.current_step += 1
        if self.current_step >= len(self.data):
            self.current_step = len(self.data) - 1
            done = True
        else:
            done = False

        # Calculate reward based on the Sharpe ratio
        reward = self._calculate_sharpe_reward(action)
        state = self.data.iloc[self.current_step].values

        # Ensure no NaN values in the state
        state = np.nan_to_num(state)

        return state, reward, done, {}

    def _calculate_sharpe_reward(self, action):
        # Calculate price change
        price_change = self.data['Close'].iloc[self.current_step] - self.data['Close'].iloc[self.current_step - 1]

        # Calculate return based on the action
        if action == 0:  # Buy
            self.position = 1
        elif action == 2:  # Sell
            self.position = 0
        # Hold action keeps the current position

        # Calculate return for the current step
        step_return = self.position * price_change / self.data['Close'].iloc[self.current_step - 1]
        self.returns.append(step_return)

        # Calculate the Sharpe ratio as the reward
        if len(self.returns) > 1:
            mean_return = np.mean(self.returns)
            volatility = np.std(self.returns)
            if volatility == 0:
                sharpe_ratio = 0  # Avoid division by zero
            else:
                sharpe_ratio = mean_return / volatility
        else:
            sharpe_ratio = 0

        return sharpe_ratio
