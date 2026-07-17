"""
main.py
Le chef d'orchestre du bot Aegis.
"""

import asyncio
from market_scanner import get_filtered_coins
from aegis_engine import scan_market
from telegram_bot import send_signal, BOT_IS_READY
import config

async def run_bot_cycle():
    """Exécute un cycle complet : Scan -> Filtre -> Analyse -> Envoi"""
    
    print("\n" + "="*50)
    print("🔄 DÉMARRAGE D'UN NOUVEAU CYCLE D'ANALYSE")
    print("="*50)

    try:
        # 1. Filtrer les cryptos
        print("1️⃣ Récupération et filtrage des cryptos sérieuses...")
        filtered_coins = get_filtered_coins()
        print(f"✅ {len(filtered_coins)} cryptos sérieuses trouvées.")

        if len(filtered_coins) == 0:
            print("⚠️ Aucune crypto ne respecte les critères.")
            return

        # 2. Analyser avec Aegis
        print("2️⃣ Analyse par le moteur Aegis...")
        signals = scan_market(filtered_coins)
        print(f"✅ {len(signals)} signaux détectés.")

        # 3. Envoyer les signaux
        print("3️⃣ Traitement des signaux...")
        if not signals:
            print("ℹ️ Aucun signal de qualité pour le moment.")
        else:
            for signal in signals:
                # On envoie le signal (fonction synchrone, pas de "await" ici)
                send_signal(signal)
                await asyncio.sleep(1)  # Petite pause pour ne pas spammer l'API Telegram

        print("\n✅ CYCLE TERMINÉ.")
        
    except Exception as e:
        print(f"\n❌ Erreur dans le cycle : {e}")

async def main():
    """Fonction principale"""
    print("🤖 AEGIS TRADING BOT - DÉMARRAGE...")
    print(f"🌐 Mode: {'TESTNET (Simulation)' if config.USE_TESTNET else 'RÉEL'}")
    
    # Vérification que Telegram est prêt
    if BOT_IS_READY:
        print("✅ Connexion Telegram : OK")
    else:
        print("⚠️ Attention : Module Telegram non chargé.")

    # Premier cycle immédiat
    await run_bot_cycle()
    
    # Boucle infinie pour tourner 24h/24
    print(f"\n🔄 Passage en mode continu (scan toutes les {config.SCAN_INTERVAL} secondes)...")
    while True:
        await run_bot_cycle()
        await asyncio.sleep(config.SCAN_INTERVAL)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Bot arrêté manuellement par l'utilisateur.")
    except Exception as e:
        print(f"\n❌ Erreur critique : {e}")
