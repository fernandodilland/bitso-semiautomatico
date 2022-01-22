import bitso
api = bitso.Api('API_KEY', 'API_SECRET')

# Libros de pedidos disponibles en Bitso
libros = api.available_books()
print("Libros disponibles:", libros) #.books / .books[0]

# Ticker
tick = api.ticker('btc_mxn')
print("\nTicker:", tick) #.last / .created_at

# Libro de pedidos
ob = api.order_book('btc_mxn')
print("\nLibro de pedidos:", ob) #.updated_at / .bids / .asks

# Trades
trades = api.trades('btc_mxn')
print("\nTrades:", trades)