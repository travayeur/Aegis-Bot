"""
market_scanner.py
Le filtre intelligent qui garde uniquement les cryptos sérieuses.
"""

import config
from binance_client import exchange

def get_filtered_coins():
    """Récupère et filtre les cryptos sérieuses selon nos règles."""
    
    try:
        # 1. On récupère toutes les données du marché
        all_tickers = exchange.fetch_tickers()
        
        # 2. On crée une liste vide pour stocker nos cryptos sélectionnées
        good_coins = []
        
        # 3. On passe chaque crypto au "tamis"
        for symbol, ticker in all_tickers.items():
            
            # Règle 1 : On ne garde que les paires en USDT (ex: BTC/USDT)
            if not symbol.endswith('/USDT'):
                continue
                
            # On extrait le nom de la crypto (ex: 'BTC' dans 'BTC/USDT')
            coin_name = symbol.split('/')[0]
            
            # Règle 2 : On exclut les stablecoins et tokens bizarres
            if coin_name in config.EXCLUDED_COINS:
                continue
                
            # Règle 3 : On vérifie le volume sur 24h (en dollars)
            volume_24h = ticker.get('quoteVolume', 0)
            
            if volume_24h < config.MIN_VOLUME_24H:
                continue
                
            # On ajoute le prix d'ouverture d'il y a 24h (très important pour le moteur Aegis !)
            open_24h = ticker.get('open', ticker['last'])
            
            # Si la crypto a passé toutes les règles, on l'ajoute à notre liste
            good_coins.append({
                'symbol': symbol,
                'price': ticker['last'],
                'volume_24h': volume_24h,
                'open_24h': open_24h
            })
            
        # 4. On trie la liste par volume (les plus gros volumes en premier)
        good_coins.sort(key=lambda x: x['volume_24h'], reverse=True)
        
        # 5. On limite au nombre max configuré
        good_coins = good_coins[:config.MAX_COINS_TO_ANALYZE]
        
        print(f"✅ {len(good_coins)} cryptos sérieuses trouvées (sur {len(all_tickers)} totales)")
        return good_coins
        
    except Exception as e:
        print(f"❌ Erreur dans le market_scanner : {e}")
        return []
