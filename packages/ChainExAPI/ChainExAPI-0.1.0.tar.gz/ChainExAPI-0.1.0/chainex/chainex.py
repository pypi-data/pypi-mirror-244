import hashlib
import hmac
import time
import requests

class ChainExAPI:
    """
    A Python client for interacting with the ChainEx cryptocurrency exchange API.

    Attributes:
        base_url (str): The base URL of the ChainEx API.
        public_key (str): The user's public API key.
        private_key (str): The user's private API key.
        session (requests.Session): A session object for persistent connections.
    """

    def __init__(self, public_key, private_key):
        """
        Initializes the ChainExAPI client with the provided public and private keys.

        Args:
            public_key (str): The user's public API key.
            private_key (str): The user's private API key.
        """
        self.base_url = "https://api.chainex.io"
        self.public_key = public_key
        self.private_key = private_key
        self.session = requests.Session()

    def _generate_hash(self, url, params):
        """
        Generate HMAC-SHA-256 hash for authentication.

        Args:
            url (str): The URL to be hashed.
            params (dict): The parameters to be included in the hash.

        Returns:
            str: The generated HMAC-SHA-256 hash.
        """
        url = url + "?"
        encoded_url = url.encode('ascii')
        encoded_data = ''.join([f'{key}={value}&' for key, value in params.items()]).rstrip('&').encode('ascii')
        message = encoded_url + encoded_data
        signature = hmac.new(self.private_key.encode('ascii'), message, hashlib.sha256).hexdigest()
        return signature

    def _get_server_time(self):
        """
        Get the current server time from ChainEx.

        Returns:
            str: The current server time as a string.
        """
        response = self.session.get(f"{self.base_url}/timestamp")
        return str(int(response.json()['data']))

    def _make_request(self, endpoint, params={}, method='GET'):
        """
        Make a request to the ChainEx API.

        Args:
            endpoint (str): The API endpoint to make the request to.
            params (dict, optional): The parameters to include in the request. Defaults to {}.
            method (str, optional): The HTTP method to use for the request. Defaults to 'GET'.

        Returns:
            dict: The JSON response from the API.

        Raises:
            ValueError: If an unsupported HTTP method is provided.
        """
        url = f"{self.base_url}/{endpoint}/"
        params['key'] = self.public_key
        params['time'] = int(time.time())
        params['hash'] = self._generate_hash(url, params)

        if method == 'GET':
            response = self.session.get(url, params=params)
        elif method == 'POST':
            print(params)
            response = self.session.post(url, data=params)
        elif method == 'DELETE':
            response = self.session.delete(url, params=params)
        else:
            raise ValueError("Unsupported HTTP method")

        return response.json()

    # Market Methods
    def get_market_summary(self, exchange):
        """
        Fetches market summary for a given exchange.

        Args:
            exchange (str): The exchange identifier (e.g., "BTC_ETH").

        Returns:
            dict: A dictionary containing the market summary data.
        """
        return self._make_request(f"market/summary/{exchange}")

    def get_market_stats(self, coin, exchange):
        """
        Fetches market statistics for a given coin and exchange.

        Args:
            coin (str): The coin identifier (e.g., "BTC").
            exchange (str): The exchange identifier (e.g., "BTC_ETH").

        Returns:
            dict: A dictionary containing market statistics data.
        """
        return self._make_request(f"market/stats/{exchange}/{coin}")

    def get_market_trades(self, coin, exchange, limit=None):
        """
        Fetches market trades for a given coin and exchange with an optional limit.

        Args:
            coin (str): The coin identifier (e.g., "BTC").
            exchange (str): The exchange identifier (e.g., "BTC_ETH").
            limit (int, optional): The maximum number of trades to fetch. Defaults to None.

        Returns:
            dict: A dictionary containing market trades data.
        """
        endpoint = f"market/trades/{exchange}/{coin}"
        params = {}
        if limit is not None:
            params['limit'] = min(limit, 200)  # Ensure limit does not exceed 200
        return self._make_request(endpoint, params)

    def get_market_orders(self, coin, exchange, order_type="ALL", limit=None):
        """
        Fetches market orders for a given coin, exchange, and order type.
        'ALL' can be used for order_type to fetch both buys and sells.

        Args:
            coin (str): The coin identifier (e.g., "BTC").
            exchange (str): The exchange identifier (e.g., "BTC_ETH").
            order_type (str): The type of order ("BUY", "SELL", or "ALL").
            limit (int, optional): The maximum number of orders to fetch. Defaults to None.

        Returns:
            dict: A dictionary containing market orders data.

        Raises:
            ValueError: If order_type is not one of 'BUY', 'SELL', or 'ALL'.
        """
        if order_type not in ["BUY", "SELL", "ALL"]:
            raise ValueError("order_type must be 'BUY', 'SELL', or 'ALL'")

        endpoint = f"market/orders/{coin}/{exchange}/{order_type}"
        params = {}
        if limit is not None:
            params['limit'] = min(limit, 200)  # Ensure limit does not exceed 200
        return self._make_request(endpoint, params)

    def get_market_chart_data(self, coin, exchange, period='6hh'):
        """
        Fetches market chart data for a given coin, exchange, and period.
        :param coin: The coin identifier (string).
        :param exchange: The exchange identifier (string).
        :param period: The period for the chart data ('6hh', '1DD', '3DD', '7DD', 'MAX'). Defaults to '6hh'.
        """
        valid_periods = ['6hh', '1DD', '3DD', '7DD', 'MAX']
        if period not in valid_periods:
            raise ValueError(f"Invalid period. Must be one of {valid_periods}")

        endpoint = f"market/chartdata/{exchange}/{coin}/{period}"
        return self._make_request(endpoint)

    # Wallet Methods
    def get_wallet_balances(self, coin=None):
        """
        Fetches wallet balances, optionally for a specific coin.
        :param coin: Optional. The coin identifier (string). If not provided, fetches all balances.
        """
        endpoint = "wallet/balances"
        params = {}
        if coin is not None:
            endpoint += f"/{coin}"
        return self._make_request(endpoint, params)

    def get_wallet_deposits(self, coin="ALL", start=0, limit=25):
        """
        Fetches wallet deposits, optionally filtered by coin, start, and limit.
        :param coin: The coin identifier (string) or "ALL". Defaults to "ALL".
        :param start: The starting index for fetching deposits (int). Defaults to 0.
        :param limit: The number of deposits to fetch (int, max 200). Defaults to 25.
        """
        limit = min(limit, 200)  # Ensure limit does not exceed 200
        endpoint = f"wallet/deposits/{coin}/{start}/{limit}"
        return self._make_request(endpoint)

    def get_wallet_deposit_address(self, coin):
        """
        Fetches the deposit address for a specific coin.
        :param coin: The coin identifier (string).
        """
        endpoint = f"wallet/depositaddress/{coin}"
        return self._make_request(endpoint)

    def generate_new_deposit_address(self, coin):
        """
        Generates a new deposit address for a specific coin.
        :param coin: The coin identifier (string).
        """
        endpoint = f"wallet/newdepositaddress/{coin}"
        return self._make_request(endpoint)

    def get_wallet_withdrawals(self, coin="ALL", start=0, limit=25):
        """
        Fetches wallet withdrawals, optionally filtered by coin, start, and limit.
        :param coin: The coin identifier (string) or "ALL". Defaults to "ALL".
        :param start: The starting index for fetching withdrawals (int). Defaults to 0.
        :param limit: The number of withdrawals to fetch (int, max 200). Defaults to 25.
        """
        limit = min(limit, 200)  # Ensure limit does not exceed 200
        endpoint = f"wallet/withdrawals/{coin}/{start}/{limit}"
        return self._make_request(endpoint)

    def get_single_withdrawal(self, withdrawal_id):
        """
        Fetches details for a single withdrawal by its ID.

        Args:
            withdrawal_id (str): The unique identifier for the withdrawal.

        Returns:
            dict: A dictionary containing details of the specified withdrawal.
        """
        return self._make_request(f"wallet/withdrawal/{withdrawal_id}")

    def request_withdrawal(self, coin, address, amount, payment_id=None):
        """
        Requests a withdrawal to a specified address.
        :param coin: The coin identifier (string).
        :param address: The address to withdraw to (string).
        :param amount: The amount to withdraw (decimal, up to 8 decimals).
        :param payment_id: Optional. Payment ID for coins based on the CryptoNote protocol (string).
        """
        endpoint = f"wallet/withdrawal"
        params = {
            'coin': coin,
            'address': address,
            'amount': amount
        }
        if payment_id:
            params['payment_id'] = payment_id

        return self._make_request(endpoint, params, method='POST')

    def cancel_withdrawal(self, withdrawal_id):
        """
        Cancels a specified withdrawal.
        :param withdrawal_id: The ID of the withdrawal to cancel (string).
        """
        endpoint = f"wallet/withdrawal/{withdrawal_id}"
        return self._make_request(endpoint, method='DELETE')

    # Trading Methods
    def get_trading_orders(self, coin="ALL", start=0, limit=25):
        """
        Fetches trading orders, optionally filtered by coin, start, and limit.
        :param coin: The coin identifier (string) or "ALL". Defaults to "ALL".
        :param start: The starting index for fetching orders (int). Defaults to 0.
        :param limit: The number of orders to fetch (int, max 200). Defaults to 25.
        """
        limit = min(limit, 200)  # Ensure limit does not exceed 200
        endpoint = f"trading/orders/{coin}/{start}/{limit}"
        return self._make_request(endpoint)

    def get_single_order(self, order_id):
        """
        Fetches details for a single trading order by its ID.

        Args:
            order_id (str): The unique identifier for the trading order.

        Returns:
            dict: A dictionary containing details of the specified trading order.
        """
        return self._make_request(f"trading/order/{order_id}")

    def add_order(self, coin, exchange, price, amount, order_type, post_only=False):
        """
        Adds an order to a specified market.
        :param coin: The first half of the market (string), e.g., "LTC" for LTC/BTC.
        :param exchange: The second half of the market (string), e.g., "BTC" for LTC/BTC.
        :param price: The price of the order (decimal, up to 8 decimals).
        :param amount: The amount of coins to purchase or sell (decimal, up to 8 decimals).
        :param order_type: Integer indicating if the order is a BUY (0) or a SELL (1).
        :param post_only: Boolean indicating if the order should be post-only (default: False).
        """
        endpoint = f"trading/order"
        params = {
            'coin': coin,
            'exchange': exchange,
            'price': price,
            'amount': amount,
            'type': order_type,
            # 'post_only': post_only
        }
        # print(params)

        return self._make_request(endpoint, params, method='POST')

    def cancel_order(self, order_id):
        """
               Cancels a specified order.
               :param order_id: The ID of the withdrawal to cancel (string).
               """
        endpoint = f"trading/order/{order_id}"
        return self._make_request(endpoint, method='DELETE')

    def get_trading_trades(self, coin="ALL", start=0, limit=25):
        """
               Fetches trading trades, optionally filtered by coin, start, and limit.
               :param coin: The coin identifier (string) or "ALL". Defaults to "ALL".
               :param start: The starting index for fetching orders (int). Defaults to 0.
               :param limit: The number of orders to fetch (int, max 200). Defaults to 25.
               """
        limit = min(limit, 200)  # Ensure limit does not exceed 200
        endpoint = f"trading/trades/{coin}/{start}/{limit}"
        return self._make_request(endpoint)

    def get_single_trade(self, trade_id):
        """
        Fetches details for a single trade by its ID.

        Args:
            trade_id (str): The unique identifier for the trade.

        Returns:
            dict: A dictionary containing details of the specified trade.
        """
        return self._make_request(f"trading/trade/{trade_id}")
