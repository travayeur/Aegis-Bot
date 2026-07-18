"""
Configuration du bot Aegis Trading Bot
Tous les paramètres sont ici pour faciliter les modifications
"""

import os

# ==================== FILTRAGE DES CRYPTOS ====================
# Volume minimum en 24h (en dollars) pour qu'une crypto soit analysée
MIN_VOLUME_24H = 5_000_000  # 5 millions de dollars (au lieu de 10M)

# ==================== SYSTÈME DE SCORING ====================
# Seuils pour les différents niveaux de signaux
SCORE_BRONZE = 60    # Signal basique
SCORE_ARGENT = 75    # Bon signal
SCORE_OR = 85        # Signal exceptionnel

# ==================== TIMEFRAMES (Unités de temps) ====================
TIMEFRAMES = ['1h', '4h', '1d']  # 1 heure, 4 heures, 1 jour

# ==================== CRYPTOS À EXCLURE ====================
EXCLUDED_COINS = [
    'USDT', 'USDC', 'BUSD', 'DAI',
    'BTCUP', 'BTCDOWN', 'ETHUP', 'ETHDOWN',
    'TUSD', 'PAX', 'USDP',
]

# ==================== PAIRES À EXCLURE ====================
QUOTE_ASSET = 'USDT'

# ==================== PARAMÈTRES DU BOT ====================
SCAN_INTERVAL = 3600  # 1 heure = 3600 secondes
MAX_COINS_TO_ANALYZE = 500  # 500 cryptos (au lieu de 300)

# ==================== PARAMÈTRES DE RISQUE ====================
MAX_RISK_PER_TRADE = 2
MIN_RISK_REWARD_RATIO = 2

# ==================== TELEGRAM ====================
# Ces valeurs seront lues depuis le "coffre-fort" (Secrets) de GitHub
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# ==================== BINANCE ====================
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY", "")
BINANCE_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY", "")
USE_TESTNET = True
