import asyncio
from market_scanner import get_filtered_coins
from aegis_engine import scan_market
from telegram_bot import send_signal, BOT_IS_READY

async def main():
    print("🤖 Démarrage...")
    
    # TEST TELEGRAM
    if BOT_IS_READY:
        print("✅ Telegram est prêt")
        # Envoi d'un message de test
        test_signal = {
            'symbol': 'TEST/USDT',
            'price': 1234.56,
            'score': 99,
            'level': '🧪 TEST',
            'reasons': ['Ceci est un message de test']
        }
        send_signal(test_signal)
        print("✅ Message de test envoyé")
    else:
        print("❌ Telegram non prêt")
    
    # Un seul cycle
    filtered_coins = get_filtered_coins()
    print(f"✅ {len(filtered_coins)} cryptos trouvées")
    
    signals = scan_market(filtered_coins)
    print(f"✅ {len(signals)} signaux")
    
    for signal in signals:
        send_signal(signal)
    
    print("✅ Terminé")

if __name__ == "__main__":
    asyncio.run(main())
