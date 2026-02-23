import pandas as pd
import numpy as np
from ..data import DataLoader
from .indicators import IndicatorManager
from .strategy import MovingAverageStrategy
from .backtester import Backtester

class Optimizer:
    """Optimizes the moving average periods for the strategy."""

    def __init__(self, data):
        self.data = data
        self.loader = DataLoader()
        self.indicator_manager = IndicatorManager()
        self.strategy = MovingAverageStrategy()
        self.backtester = Backtester()

    def optimize(self, sma_range, mma_range, lma_range):
        """Finds the best moving average parameters for maximum strategy returns."""
        ma_dict = {}
        
        # Optimize the strategy
        for sma in sma_range:
            for mma in mma_range:
                for lma in lma_range:
                    key = f'sma{sma}_mma{mma}_lma{lma}'
                    print(f'\nChecking for SMA: {sma}, MMA: {mma}, LMA: {lma}')
                    
                    df = self.data.copy()
                    df = self.loader.generate_returns(df)
                    df = self.indicator_manager.apply_mas(df, sma, mma, lma)
                    df = self.strategy.generate_signals(df)
                    bnh, s_returns = self.backtester.calculate_metrics(df)
                    
                    print(f'Buy and hold returns: {np.round(bnh, 2)}')
                    print(f'Strategy returns: {np.round(s_returns, 2)}')
                    ma_dict[key] = s_returns
        
        # Result Summary
        if ma_dict:
            max_ret = max(ma_dict.values())
            opt_values = [key for key, value in ma_dict.items() if value == max_ret]
            print(f"The max strategy returns are {max_ret} for the values {opt_values}.")
            return max_ret, opt_values
        else:
            return None, None
