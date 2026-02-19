import ccxt
import logging
from typing import Dict, Any
import os

class APIHandler:
    def __init__(self):
        self.exchanges = []
        self._initialize_exchanges()
    
    def _initialize_exchanges(self):
        """Initialize supported exchanges with their respective keys."""
        try:
            # Load exchange credentials from environment variables
            exchange_keys = {
                'binance': {'key': os.getenv('BINANCE_API_KEY'), 'secret': os.getenv('BINANCE_SECRET_KEY')},
                'kucoin': {'key': os.getenv('KUCOIN_API_KEY'), 'secret': os.getenv('KUCOIN_SECRET_KEY')},
                # Add more exchanges as needed
            }
            
            for exchange, config in exchange_keys.items():
                if config['key'] and config['secret']:
                    if exchange == 'binance':
                        self.exchanges.append(ccxt.binance({
                            'apiKey': config['key'],
                            'secretKey': config['secret']
                        }))
                    elif exchange == 'kucoin':
                        self.exchanges.append(ccxt.kucoin({
                            'apiKey': config['key'],
                            'secretKey': config['secret']
                        }))
            logging.info("Initialized exchanges: %s", list(exchange_keys.keys()))
        except Exception as e:
            logging.error("Failed to initialize exchanges: %s", str(e))
    
    async def fetch_market_data(self, symbol: str, exchange_list: list = None) -> Dict[str, Any]:
        """Fetch market data from specified exchanges."""
        if not exchange_list:
            exchange_list = self.exchanges
        market_data = {}
        
        try:
            for exchange in exchange_list:
                if isinstance(exchange, ccxt.Exchange):
                    market_data[exchange.name] = await exchange.fetch_ticker(symbol)
            return market_data
        except Exception as e:
            logging.error("Failed to fetch market data: %s", str(e))
            return None
    
    def get_valid_exchanges(self) -> list:
        """Return list of initialized exchanges."""
        return [e.name for e in self.exchanges]