import typer
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from bot.client import get_binance_client
from bot.orders import place_order
from bot.logging_config import logger
from bot.validators import (
    validate_symbol,
    validate_side,
    validate_order_type,
    validate_quantity,
    validate_price
)

app = typer.Typer(help="Binance Futures Testnet Trading Bot")
console = Console()

@app.command()
def trade(
    symbol: str = typer.Argument(..., help="Trading pair symbol (e.g., BTCUSDT)"),
    side: str = typer.Argument(..., help="Order side: BUY or SELL"),
    order_type: str = typer.Argument(..., help="Order type: MARKET or LIMIT"),
    quantity: float = typer.Argument(..., help="Amount to trade"),
    price: Optional[float] = typer.Option(None, "--price", "-p", help="Price (Required for LIMIT orders)")
):
    """
    Executes a trade on the Binance Futures Testnet.
    """
    try:
        valid_symbol = validate_symbol(symbol)
        valid_side = validate_side(side)
        valid_type = validate_order_type(order_type)
        valid_quantity = validate_quantity(quantity)
        valid_price = validate_price(valid_type, price)
    except ValueError as e:
        logger.error(f"Validation Error: {e}")
        console.print(f"[bold red]Validation Error:[/bold red] {e}")
        raise typer.Exit(code=1)

    summary_table = Table(title="Order Request Summary", show_header=True, header_style="bold cyan")
    summary_table.add_column("Parameter")
    summary_table.add_column("Value", style="magenta")
    
    summary_table.add_row("Symbol", valid_symbol)
    summary_table.add_row("Side", valid_side)
    summary_table.add_row("Type", valid_type)
    summary_table.add_row("Quantity", str(valid_quantity))
    if valid_price:
        summary_table.add_row("Price", str(valid_price))

    console.print(summary_table)

    try:
        with console.status("[bold yellow]Connecting to Binance Testnet...[/bold yellow]"):
            client = get_binance_client()
            response = place_order(
                client=client,
                symbol=valid_symbol,
                side=valid_side,
                order_type=valid_type,
                quantity=valid_quantity,
                price=valid_price
            )

        success_text = (
            f"Order ID: [cyan]{response.get('orderId')}[/cyan]\n"
            f"Status: [green]{response.get('status')}[/green]\n"
            f"Executed Qty: {response.get('executedQty')}\n"
            f"Avg Price: {response.get('avgPrice', 'N/A')}"
        )
        console.print(Panel.fit(success_text, title="[bold green]✓ Order Successful[/bold green]", border_style="green"))

    except Exception as e:
        console.print("[bold red]✖ Trade Execution Failed.[/bold red] Please check logs/trading.log for details.")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    try:
        app()
    except Exception as e:
        print(f"Critical Application Error: {e}")