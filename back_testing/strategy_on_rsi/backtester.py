import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import quantstats as qs

class Backtester:
    """Performance analysis and visualization for RSI strategy."""

    def plot_rsi_signals(self, data, rsi_lower=30, rsi_upper=70):
        """Visualizes the strategy with position overlaid on RSI."""
        n = data.shape[0]
        plt.figure(figsize=(15, 7))
        y = data['RSI'].plot()
        
        # Draw thresholds
        plt.axhline(y=rsi_lower, color='r', linestyle='--')
        plt.axhline(y=rsi_upper, color='g', linestyle='--')
        
        # Plot position
        data['RSI_signal'].plot(ax=y, secondary_y='position', alpha=0.3, label='Position')
        
        plt.title('RSI Strategy: RSI and Signal Positions')
        plt.show()

    def plot_cumulative_returns(self, data):
        """Plots cumulative returns of the strategy."""
        # Using simple exp(cumsum) for log returns
        cum_ret = data['strategy_returns'].cumsum().apply(np.exp)
        
        plt.figure(figsize=(10, 6))
        cum_ret.plot()
        plt.title('Cumulative Strategy Returns (Exp)')
        plt.ylabel('Growth')
        plt.show()

    def generate_report(self, returns, benchmark=None):
        """Generates full quantstats report."""
        # Ensure returns is a Series and has a DatetimeIndex for quantstats
        if not isinstance(returns.index, pd.DatetimeIndex):
            returns.index = pd.to_datetime(returns.index)
            
        # quantstats works best with simple returns
        # converting log returns back to simple returns for report
        simple_returns = np.exp(returns) - 1
        
        simple_benchmark = None
        if benchmark is not None:
            if not isinstance(benchmark.index, pd.DatetimeIndex):
                benchmark.index = pd.to_datetime(benchmark.index)
            simple_benchmark = np.exp(benchmark) - 1
            
        qs.reports.full(simple_returns, benchmark=simple_benchmark)
