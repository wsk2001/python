from binance_api_python.common.constants import INTERVAL_1MINUTE
from binance_api_python.common.functions import get_historical_klines

# Import the Binance API client
from binance_api_python.binance import Binance

# Create a Binance client
client = Binance()

# Set the asset and time interval for the volume data
asset = 'BTC'
interval = INTERVAL_1MINUTE

# Retrieve the volume data
volume_data = client.futures_klines(symbol=asset, interval=interval)

# Print the volume data
print(volume_data)
