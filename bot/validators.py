def validate_symbol(symbol: str) -> str:
    """Ensures the symbol is a valid format and returns it in uppercase."""
    if not symbol or not symbol.isalnum():
        raise ValueError("Invalid symbol. It must be alphanumeric (e.g., BTCUSDT).")
    return symbol.upper()

def validate_side(side: str) -> str:
    """Ensures the side is strictly BUY or SELL."""
    side = side.upper()
    if side not in ["BUY", "SELL"]:
        raise ValueError("Invalid side. Must be exactly 'BUY' or 'SELL'.")
    return side

def validate_order_type(order_type: str) -> str:
    """Ensures the order type is supported."""
    order_type = order_type.upper()
    if order_type not in ["MARKET", "LIMIT"]:
        raise ValueError("Invalid order type. Must be 'MARKET' or 'LIMIT'.")
    return order_type

def validate_quantity(quantity: float) -> float:
    """Ensures the user is trying to buy a positive amount."""
    if quantity <= 0:
        raise ValueError("Quantity must be greater than 0.")
    return quantity

def validate_price(order_type: str, price: float = None):
    """Ensures a price is provided if the order is a LIMIT order."""
    if order_type.upper() == "LIMIT":
        if price is None or price <= 0:
            raise ValueError("A valid positive price is REQUIRED for LIMIT orders.")
    return price