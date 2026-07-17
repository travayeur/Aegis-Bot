"""
binance_client.py
Ce fichier gère la connexion avec Binance pour récupérer les prix.
"""

import ccxt

# On initialise la connexion à Binance
# 'defaultType': 'spot' force le bot à utiliser le marché classique (Spot)
exchange = ccxt.binance({
    'enableRateLimit': True, 
    'options': {
        'defaultType': 'spot', 
    }
})

def get_price(symbol):
    """Récupère le prix actuel d'une crypto (ex: 'BTC/USDT')"""
    try:
        ticker = exchange.fetch_ticker(symbol)
        return ticker['last']
    except Exception as e:
        print(f"❌ Erreur prix {symbol} : {e}")
        return None

def get_all_tickers():
    """Récupère les données de TOUTES les cryptos"""
    try:
        print(" Récupération des données sur Binance (Marché Spot)...")
        tickers = exchange.fetch_tickers()
        print(f"✅ {len(tickers)} cryptos récupérées avec succès !")
        return tickers
    except Exception as e:
        print(f"❌ Erreur de connexion à Binance : {e}")
        return None
