import pandas as pd
import numpy as np
from typing import Dict, Any
import logging

class DataProcessor:
    def __init__(self):
        pass
    
    @staticmethod
    def clean_data(data: Dict[str, Any]) -> pd.DataFrame:
        """Convert raw market data into a DataFrame for analysis."""
        try:
            df = pd.DataFrame([{
                'exchange': e,
                'bid': d['bid'],
                'ask': d['ask'],
                'timestamp': d['timestamp']
            } for e, d in data.items()])
            
            # Convert to decimal type for accurate calculations
            df[['bid', 'ask']] = df[['bid', 'ask']].astype('float')
            return df
        except Exception as e:
            logging.error("Data cleaning failed: %s", str(e))
            return None
    
    def calculate_spread(self, df: pd.DataFrame) -> pd.Series:
        """Calculate bid-ask spread for each exchange."""
        try:
            df['spread'] = np.abs(df['bid'] - df['ask'])
            return df[['exchange', 'spread']]
        except Exception as e:
            logging.error("Failed to calculate spreads: %s", str(e))
            return None