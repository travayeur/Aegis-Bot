"""
main.py - VERSION GITHUB ACTIONS
"""

import asyncio
from market_scanner import get_filtered_coins
from aegis_engine import scan_market
from telegram_bot import send_signal, BOT_IS_READY
import config

async def run_bot_cycle():
    """Un seul cycle d'analyse"""
    
    print("\n" + "="*50)
    print("🔄 DÉMARRAGE DU CYCLE D'ANALYSE")
    print("="*50)

    try:
        print("1️ Récupération des cryptos...")
        filtered_coins = get_filtered_coins()
        print(f"✅ {len(filtered_coins)} cryptos trouvées.")

        if len(filtered_coins) == 0:
            print("⚠️ Aucune crypto trouvée.")
            return

        print("2️ Analyse Aegis...")
        signals = scan_market(filtered_coins)
        print(f"✅ {len(signals)} signaux détectés.")

        if signals:
            print("3️ Envoi des signaux...")
            for signal in signals:
                send_signal(signal)
                await asyncio.sleep(1)

        print("\n✅ CYCLE TERMINÉ.")
        
    except Exception as e:
        print(f"\n❌ Erreur : {e}")

async def main():
    """Fonction principale - UN SEUL CYCLE"""
    print(" AEGIS BOT - START")
    
    if BOT_IS_READY:
        print("✅ Telegram OK")
    
    await run_bot_cycle()
    
    print("\n✅ TERMINÉ")

if __name__ == "__main__":
    asyncio.run(main())
