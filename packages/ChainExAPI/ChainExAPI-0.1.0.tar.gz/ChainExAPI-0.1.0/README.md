# ChainExAPI Python Client

## Overview

ChainExAPI is a Python client library for interacting with the ChainEx cryptocurrency exchange API. It provides a convenient way to integrate ChainEx's services into your Python applications.

## Features

- Easy to use methods for market, wallet, and trading operations.
- HMAC-SHA-256 authentication for secure API calls.
- Fetch market summaries, statistics, trades, and orders.
- Manage wallet balances, deposits, withdrawals, and addresses.
- Execute and manage trading orders and trades.

## Installation

You can install the ChainExAPI library via pip:

```bash
pip install chainexapi
```

## Quick Start

Here's a quick example to get you started:

```python
from chainex import ChainExAPI

# Initialize the API client
client = ChainExAPI('your_public_key', 'your_private_key')

# Fetch market summary
market_summary = client.get_market_summary('BTC_ETH')
print(market_summary)

# Fetch wallet balances
wallet_balances = client.get_wallet_balances()
print(wallet_balances)
```

## Usage

### Initializing the Client

First, import the `ChainExAPI` class and initialize it with your public and private API keys:

```python
from chainex import ChainExAPI

client = ChainExAPI('your_public_key', 'your_private_key')
```

### Market Methods

- `get_market_summary(exchange)`: Fetches market summary for a given exchange.
- `get_market_stats(coin, exchange)`: Fetches market statistics for a given coin and exchange.
- ... (and so on for other market methods)

### Wallet Methods

- `get_wallet_balances(coin=None)`: Fetches wallet balances.
- `get_wallet_deposits(coin="ALL", start=0, limit=25)`: Fetches wallet deposits.
- ... (and so on for other wallet methods)

### Trading Methods

- `get_trading_orders(coin="ALL", start=0, limit=25)`: Fetches trading orders.
- `add_order(coin, exchange, price, amount, order_type)`: Adds an order to a specified market.
- ... (and so on for other trading methods)

## Contributing

Contributions to the ChainExAPI library are welcome! Please feel free to submit issues and pull requests to the repository.

## License

This project is licensed under the [MIT License](LICENSE).
