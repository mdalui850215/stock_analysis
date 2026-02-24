from .strategy import RSIStrategy
from .indicators import IndicatorManager
from ..data import DataLoader
import numpy as np

class Optimizer:
    """Optimizes parameters for the RSI strategy."""

    def __init__(self, data):
        self.data = data
        self.indicator_manager = IndicatorManager()
        self.strategy = RSIStrategy()

    def optimize(self, rsi_lower_range, tp_range, sl_range):
        """Iterates through parameters to find maximum return."""
        results = {}
        
        # Calculate RSI once for the default period
        df_base = self.indicator_manager.calculate_rsi(self.data)
        
        for rl in rsi_lower_range:
            for tp in tp_range:
                for sl in sl_range:
                    key = f"rsi_low_{rl}_tp_{tp}_sl_{sl}"
                    
                    df = self.strategy.generate_signals(
                        df_base, 
                        rsi_lower=rl, 
                        tp_level=tp, 
                        sl_level=sl
                    )
                    
                    total_ret = np.exp(df['strategy_returns'].sum())
                    results[key] = total_ret
                    print(f"Checking: {key} -> Return: {np.round(total_ret, 4)}")
        
        if results:
            best_key = max(results, key=results.get)
            print(f"Optimization Results:")
            print(f"Best Parameters: {best_key}")
            print(f"Best Return: {np.round(results[best_key], 4)}")
            return results[best_key], best_key
        return None, None
