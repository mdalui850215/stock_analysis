import pandas as pd
import numpy as np
import os

class DataLoader:
    """Handles downloading and initial processing of stock data."""
    
    @staticmethod
    def load_local_csv(ticker='MSFT', start=None, end=None):
        """Reads data from a local CSV file instead of downloading."""
        print(f"\n--- Data Loading for: {ticker} ---")
        print(f"Requested Range: {start} to {end}")
        
        file_path = os.path.join("data", "historical_data13081.csv")
        try:
            # Read CSV - we'll handle the index and date parsing explicitly for robustness
            df = pd.read_csv(file_path)
            
            # Find the date column (usually 'timestamp' or column index 1)
            # In your CSV, column 0 is an empty index, column 1 is 'timestamp'
            if 'timestamp' in df.columns:
                date_col = 'timestamp'
            elif 'date' in df.columns:
                date_col = 'date'
            else:
                # Fallback to the second column
                date_col = df.columns[1]
            
            print(f"Setting index to: {date_col}")
            df[date_col] = pd.to_datetime(df[date_col])
            df.set_index(date_col, inplace=True)
            
            # Remove redundant numeric index column if it exists as a column (e.g. 'Unnamed: 0')
            for col in ['Unnamed: 0', 'unnamed: 0']:
                if col in df.columns:
                    df.drop(columns=[col], inplace=True)
            
            # FORCE CHRONOLOGICAL ORDER (Earliest to Latest)
            df.sort_index(ascending=True, inplace=True)
            
            # Clean column names (strip spaces and lowercase for matching)
            df.columns = [c.strip().lower() for c in df.columns]
            
            print(f"Columns after cleaning: {list(df.columns)}")
            
            # Standardize OHLC column names
            rename_dict = {
                'open': 'Open',
                'high': 'High',
                'low': 'Low',
                'close': 'Close',
                'volume': 'Volume'
            }
            df.rename(columns=rename_dict, inplace=True)
            print(f"Columns after rename: {list(df.columns)}")
            
            # Log available range before filtering
            print(f"File availability: {df.index.min().date()} to {df.index.max().date()}")
            
            # Filter by date range
            if start:
                df = df[df.index >= pd.to_datetime(start)]
            if end:
                df = df[df.index <= pd.to_datetime(end)]

            print(f"Final loaded range: {df.index.min().date()} to {df.index.max().date()}")
            print(f"Total rows loaded: {len(df)}")
            return df
        except Exception as e:
            print(f"Error loading data from CSV: {e}")
            return pd.DataFrame()

    @staticmethod
    def generate_returns(df):
        """Calculates percentage returns for the 'Close' column."""
        if df is None or df.empty:
            return df
        df = df.copy()
        if 'Close' in df.columns:
            df['p_returns'] = df['Close'].pct_change()
        return df
