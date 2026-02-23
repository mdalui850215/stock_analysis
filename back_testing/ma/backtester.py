import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Backtester:
    """Backtesting engine for the strategy."""
    
    def calculate_metrics(self, data):
        """Calculates buy-and-hold returns versus strategy returns."""
        # Check if the dataframe is empty
        if data.empty:
            return 0.0, 0.0
        
        # Calculate returns
        bnh = (data['p_returns'] + 1).cumprod().iloc[-1]
        s_returns = (data['strategy_returns'] + 1).cumprod().iloc[-1]
        
        return bnh, s_returns

    def plot_results(self, data, start=50, end=130):
        """Plots the signal, moving averages, and closing price."""
        data[['signal', 'sma', 'mma', 'lma', 'Close']].iloc[start:end].plot(
            figsize=(10, 6), secondary_y='signal')
        plt.show()
