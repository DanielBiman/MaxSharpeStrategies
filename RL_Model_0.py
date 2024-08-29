import gym
import numpy as np

# Define a custom trading environment
class TradingEnv(gym.Env):
    def __init__(self, data):
        super(TradingEnv, self).__init__()
        self.data = data
        self.current_step = 0
        self.action_space = gym.spaces.Discrete(3)  # Buy, Hold, Sell
        self.observation_space = gym.spaces.Box(low=-np.inf, high=np.inf, shape=(data.shape[1],), dtype=np.float32)

    def reset(self):
        self.current_step = 0
        return self.data.iloc[self.current_step].values

    def step(self, action):
        self.current_step += 1
        if self.current_step >= len(self.data):
            self.current_step = len(self.data) - 1
            done = True
        else:
            done = False

        reward = self._calculate_reward(action)
        state = self.data.iloc[self.current_step].values

        # Ensure no NaN values in the state
        state = np.nan_to_num(state)

        return state, reward, done, {}

    def _calculate_reward(self, action):
        # Simplified reward calculation
        price_change = self.data['Close'].iloc[self.current_step] - self.data['Close'].iloc[self.current_step - 1]
        if action == 0:  # Buy
            return price_change
        elif action == 2:  # Sell
            return -price_change
        else:  # Hold this should be position size times price change
            return 0
