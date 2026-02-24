from .strategy import HighLowStrategy
from .indicators import IndicatorManager
import numpy as np

class Optimizer:
    """Optimizes parameters for the High/Low Price strategy."""

    def __init__(self, data):
        self.data = data
        self.indicator_manager = IndicatorManager()
        self.strategy = HighLowStrategy()

    def optimize(self, high_range, low_range):
        """Finds the best combination of entry and exit periods."""
        results = {}
        
        for h in high_range:
            for l in low_range:
                key = f"high{h}_low{l}"
                
                # Apply indicators for these periods
                df_ind = self.indicator_manager.calculate_channels(self.data, ndays_high=h, ndays_low=l)
                
                # Run strategy
                df = self.strategy.generate_signals(df_ind)
                
                # Compute cumulative return
                total_ret = (1 + df['trade_ret']).prod()
                results[key] = total_ret
                print(f"Testing: {key} -> Return: {np.round(total_ret, 4)}")
                
        if results:
            best_key = max(results, key=results.get)
            print(f"Optimization Results:")
            print(f"Best Parameters: {best_key}")
            print(f"Best Return: {np.round(results[best_key], 4)}")
            return results[best_key], best_key
        return None, None
