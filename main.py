import asyncio
from market_scanner import get_filtered_coins
from aegis_engine import scan_market
from telegram_bot import send_signal, BOT_IS_READY

async def main():
    print("🤖 Démarrage...")
    print(f" Telegram Ready: {BOT_IS_READY}")
    
    # Un seul cycle d'analyse
    filtered_coins = get_filtered_coins()
    print(f"✅ {len(filtered_coins)} cryptos trouvées")
    
    if len(filtered_coins) > 0:
        print(f"📊 Première crypto: {filtered_coins[0]['symbol']}")
    
    signals = scan_market(filtered_coins)
    print(f"✅ {len(signals)} signaux détectés")
    
    if signals:
        print("📡 Envoi des signaux...")
        for signal in signals:
            print(f"  → {signal['symbol']} (Score: {signal['score']})")
            send_signal(signal)
    
    print("✅ Terminé")

if __name__ == "__main__":
    asyncio.run(main())
