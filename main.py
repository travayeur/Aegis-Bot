import asyncio
from market_scanner import get_filtered_coins
from aegis_engine import scan_market
from telegram_bot import send_signal

async def main():
    print("🤖 Démarrage...")
    
    filtered_coins = get_filtered_coins()
    print(f"✅ {len(filtered_coins)} cryptos trouvées")
    
    signals = scan_market(filtered_coins)
    print(f"✅ {len(signals)} signaux détectés")
    
    for signal in signals:
        send_signal(signal)
    
    print("✅ Terminé")

if __name__ == "__main__":
    asyncio.run(main())
