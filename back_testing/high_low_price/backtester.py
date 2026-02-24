import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import quantstats as qs

class Backtester:
    """Performance analysis for High/Low strategy."""

    def plot_results(self, data, symbol):
        """Plots cumulative returns and signal state."""
        # Ensure DatetimeIndex for plotting
        if not isinstance(data.index, pd.DatetimeIndex):
            data.index = pd.to_datetime(data.index)

        # Compute cumulative returns
        data['strat_cum_ret'] = (1 + data['trade_ret']).cumprod()
        
        close_col = 'Close' if 'Close' in data.columns else 'close'
        data['bh_cum_ret'] = (1 + data[close_col].pct_change()).cumprod()
        
        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(15, 10))
        
        ax1.plot(data.index, data['strat_cum_ret'], label='Strategy returns')
        ax1.plot(data.index, data['bh_cum_ret'], label='Buy and Hold Returns')
        ax1.set_ylabel('Cumulative Returns')
        ax1.set_title(f'High/Low Price Strategy - {symbol}')
        ax1.legend()
        
        ax2.plot(data.index, data['signal'], color='green')
        ax2.set_ylabel('Signal (0 or 1)')
        ax2.set_xlabel('Date')
        
        plt.tight_layout()
        plt.show()

    def generate_report(self, returns, benchmark=None):
        """Generates performance report using quantstats."""
        if not isinstance(returns.index, pd.DatetimeIndex):
            returns.index = pd.to_datetime(returns.index)
        
        if benchmark is not None and not isinstance(benchmark.index, pd.DatetimeIndex):
            benchmark.index = pd.to_datetime(benchmark.index)

        qs.reports.full(returns, benchmark=benchmark)
