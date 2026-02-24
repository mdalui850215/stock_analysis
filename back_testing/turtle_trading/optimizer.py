from .strategy import TurtleStrategy
from .indicators import IndicatorManager
from ..data import DataLoader
import numpy as np

class Optimizer:
    """Optimizes parameters for the Turtle Trading System."""

    def __init__(self, data):
        self.data = data
        self.indicator_manager = IndicatorManager()
        self.strategy = TurtleStrategy()

    def optimize(self, ndays_range, sl_range, tp_range):
        """Iterates through parameter combinations to find best cumulative return."""
        results = {}
        
        for n in ndays_range:
            # Re-calculate indicators for each channel length
            df_ind = self.indicator_manager.calculate_atr(self.data)
            df_ind = self.indicator_manager.calculate_channels(df_ind, ndays_high=n, ndays_low=n)
            df_ind.dropna(subset=['ATR', 'ndays_high', 'ndays_low'], inplace=True)
            
            for sl in sl_range:
                for tp in tp_range:
                    key = f"n{n}_sl{sl}_tp{tp}"
                    
                    df = self.strategy.generate_signals(df_ind, sl_mult=sl, tp_mult=tp)
                    total_ret = (1 + df['trade_ret']).prod()
                    
                    results[key] = total_ret
                    print(f"Checking: {key} -> Cum Return: {np.round(total_ret, 4)}")
        
        if results:
            best_key = max(results, key=results.get)
            print(f"Optimization Results:")
            print(f"Best Parameters: {best_key}")
            print(f"Best Return: {np.round(results[best_key], 4)}")
            return results[best_key], best_key
        return None, None
