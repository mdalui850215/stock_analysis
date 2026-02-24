import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import quantstats as qs

class Backtester:
    """Backtesting engine for the Buy/Sell Next Day strategy."""
    
    def calculate_metrics(self, data):
        """Calculates buy-and-hold returns versus strategy returns."""
        if data.empty:
            return 0.0, 0.0
        
        # Cumulative sum for log returns
        bnh = data['cc_returns'].sum()
        s_returns = data['strategy_returns'].sum()
        
        return bnh, s_returns

    def plot_results(self, data, symbol):
        """Plots the cumulative returns comparison."""
        # For plotting, convert log returns to cumulative growth
        bnh_cum = data['cc_returns'].cumsum()
        s_cum = data['strategy_returns'].cumsum()
        
        plt.figure(figsize=(10, 6))
        plt.plot(bnh_cum, label='Buy and hold returns')
        plt.plot(s_cum, label='Strategy Returns')
        plt.ylabel('Cumulative Log Returns')
        plt.xlabel('Date')
        plt.title(f'Returns Comparison - {symbol}')
        plt.legend()
        plt.show()

    def generate_report(self, returns, benchmark=None):
        """Generates a performance report using quantstats."""
        # quantstats expects simple returns for many metrics, 
        # but can work with log returns if they are daily.
        # We'll pass the strategy returns series.
        qs.reports.full(returns, benchmark=benchmark)
