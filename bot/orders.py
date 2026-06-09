from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
from bot.logging_config import logger

def place_order(client: Client, symbol: str, side: str, order_type: str, quantity: float, price: float = None):
    """
    Places a MARKET or LIMIT order on the Binance Futures Testnet.
    """
    try:
        # 1. Construct the base payload required for all orders
        order_params = {
            "symbol": symbol.upper(),
            "side": side.upper(),
            "type": order_type.upper(),
            "quantity": quantity,
        }

        # 2. Add extra parameters required specifically for LIMIT orders
        if order_type.upper() == "LIMIT":
            if not price:
                raise ValueError("A specific price must be provided for LIMIT orders.")
            order_params["price"] = price
            order_params["timeInForce"] = "GTC"  # 'Good Till Canceled' (required for limit orders)

        logger.info(f"Attempting to place {order_type.upper()} {side.upper()} order for {quantity} {symbol.upper()}...")
        
        # 3. Execute the payload against the Futures API
        # Using **order_params unpacks our dictionary directly into the function arguments
        response = client.futures_create_order(**order_params)
        
        logger.info(f"Order Success! Order ID: {response.get('orderId')} | Status: {response.get('status')}")
        return response

    except BinanceAPIException as e:
        # Catches issues like invalid API keys or insufficient testnet funds
        logger.error(f"Binance API Error: {e.status_code} - {e.message}")
        raise
    except BinanceOrderException as e:
        # Catches issues with the order itself (e.g., price is too far from market)
        logger.error(f"Binance Order Error: {e.message}")
        raise
    except Exception as e:
        # Catch-all for any other unexpected crashes
        logger.error(f"Unexpected error while placing order: {e}")
        raise