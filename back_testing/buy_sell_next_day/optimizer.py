from back_testing.data import DataLoader
from .indicators import IndicatorManager
from .strategy import BuySellNextDayStrategy
from .backtester import Backtester
import numpy as np

class Optimizer:
    """Optimizes parameters for the Buy and Sell Next Day strategy."""

    def __init__(self, data):
        self.data = data
        self.indicator_manager = IndicatorManager()
        self.strategy = BuySellNextDayStrategy()
        self.backtester = Backtester()

    def optimize(self, down_days_range, exit_types=['next_day_open', 'same_day_close']):
        """Finds the best parameters (consecutive down days and exit type)."""
        results = {}
        
        # Pre-calculate returns and down day data once
        df_base = self.indicator_manager.calculate_returns(self.data)
        df_base = self.indicator_manager.calculate_down_days(df_base)
        
        # Optimize over ranges
        for down_days in down_days_range:
            for exit_type in exit_types:
                key = f'down_days{down_days}_exit_{exit_type}'
                
                df = self.strategy.generate_signals(df_base, down_days=down_days)
                df = self.strategy.calculate_strategy_returns(df, exit_type=exit_type)
                
                bnh, s_returns = self.backtester.calculate_metrics(df)
                
                results[key] = s_returns
                print(f"Checking: {key} -> Total Log Return: {np.round(s_returns, 4)}")
        
        # Result Summary
        if results:
            max_ret = max(results.values())
            opt_values = [key for key, value in results.items() if value == max_ret]
            print(f"Optimization Finished.")
            print(f"The max strategy returns (log) are {np.round(max_ret, 4)} for parameters {opt_values}.")
            return max_ret, opt_values
        else:
            return None, None
