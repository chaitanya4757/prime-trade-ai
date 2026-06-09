import os
from binance.client import Client
from dotenv import load_dotenv
from bot.logging_config import logger

# Load the keys from the .env file
load_dotenv()

def get_binance_client() -> Client:
    """
    Initializes and returns the Binance client configured for the Futures Testnet.
    """
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        logger.error("API keys not found. Please check your .env file.")
        raise ValueError("Missing BINANCE_API_KEY or BINANCE_API_SECRET in .env file.")

    try:
        # The testnet=True flag points the client to the correct Binance Testnet URLs
        client = Client(api_key, api_secret, testnet=True)
        
        # Send a quick ping to the futures testnet to verify our connection works
        client.futures_ping()
        logger.info("Successfully authenticated and connected to Binance Futures Testnet.")
        
        return client
    
    except Exception as e:
        logger.error(f"Failed to connect to Binance API: {e}")
        raise