from back_testing.data import DataLoader
from back_testing.strategy_on_rsi.indicators import IndicatorManager
from back_testing.strategy_on_rsi.strategy import RSIStrategy
from back_testing.strategy_on_rsi.backtester import Backtester
import numpy as np
import importlib
import back_testing.data

def run_backtest(symbol='SPY', start_date='2010-02-25', end_date='2020-02-25', 
                 rsi_period=14, rsi_lower=30, rsi_upper=70, 
                 tp_level=0.05, sl_level=0.02):
    """Orchestrates the RSI backtesting workflow."""
    
    # Force reload of modules to catch updates
    import back_testing.data
    import back_testing.strategy_on_rsi.indicators
    import back_testing.strategy_on_rsi.strategy
    import back_testing.strategy_on_rsi.backtester
    importlib.reload(back_testing.data)
    importlib.reload(back_testing.strategy_on_rsi.indicators)
    importlib.reload(back_testing.strategy_on_rsi.strategy)
    importlib.reload(back_testing.strategy_on_rsi.backtester)
    
    # Initialize components
    loader = DataLoader()
    indicator_manager = IndicatorManager()
    strategy = RSIStrategy()
    backtester = Backtester()
    
    # Load data
    data = loader.load_local_csv(ticker=symbol, start=start_date, end=end_date)
    print(f"Index type after loading: {type(data.index)}")
    
    if data.empty:
        print(f"Warning: No data loaded for {symbol}.")
        return

    print(f"--- Running RSI Strategy Backtest for {symbol} ---")
    print(f"Parameters: RSI Period: {rsi_period}, RSI Range: ({rsi_lower}, {rsi_upper})")
    print(f"Risk Management: TP: {tp_level*100}%, SL: {sl_level*100}%")
    
    # Step 1: Calculate RSI
    data_with_rsi = indicator_manager.calculate_rsi(data, period=rsi_period)
    print(f"Index type after RSI calculation: {type(data_with_rsi.index)}")
    
    # Step 2: Generate Signals and Calculate Returns
    data_backtested = strategy.generate_signals(
        data_with_rsi, 
        rsi_lower=rsi_lower, 
        rsi_upper=rsi_upper, 
        tp_level=tp_level, 
        sl_level=sl_level
    )
    print(f"Index type after Signal generation: {type(data_backtested.index)}")
    
    # Step 3: Performance Metrics
    total_ret = np.exp(data_backtested['strategy_returns'].sum())
    print(f'Total return from this strategy: {np.round(total_ret, 4)}')
    
    # Step 4: Visualizations
    backtester.plot_rsi_signals(data_backtested, rsi_lower, rsi_upper)
    backtester.plot_cumulative_returns(data_backtested)
    
    # Step 5: Quantstats Report
    # Using 'daily_log_returns' as benchmark
    backtester.generate_report(data_backtested['strategy_returns'], benchmark=data_backtested['daily_log_returns'])

if __name__ == "__main__":
    run_backtest()
