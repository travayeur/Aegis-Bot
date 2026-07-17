import requests
from datetime import datetime
import config

# Indique au main.py que le module est bien chargé
BOT_IS_READY = True

def send_signal(signal):
    """
    Envoie un signal de trading formaté proprement sur Telegram.
    """
    # On récupère les infos
    crypto = signal.get('symbol', 'Inconnu')
    score = signal.get('score', 0)
    price = signal.get('price', 0.0)
    level = signal.get('level', 'INCONNU')
    reasons = signal.get('reasons', [])
    
    # On met en forme les raisons avec des puces
    raisons_texte = "\n".join([f"✅ {r}" for r in reasons]) if reasons else "✅ Analyse standard"
    
    # Le design du message
    message = f"""
{level} <b>SIGNAL AEGIS</b> {level}

💎 <b>Crypto:</b> {crypto}
💰 <b>Prix:</b> ${price:,.2f}
📊 <b>Score:</b> {score}/100

📌 <b>ANALYSE:</b>
{raisons_texte}

⏰ <b>Heure:</b> {datetime.now().strftime('%H:%M:%S')}
📅 <b>Date:</b> {datetime.now().strftime('%Y-%m-%d')}
    """.strip()

    # Récupération des secrets depuis config.py (qui lit le coffre-fort GitHub)
    token = config.TELEGRAM_BOT_TOKEN
    chat_id = config.TELEGRAM_CHAT_ID

    if not token or not chat_id:
        print("❌ Erreur: Token ou Chat ID manquant dans la configuration !")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    params = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }
    
    try:
        reponse = requests.post(url, params=params, timeout=10)
        if reponse.status_code == 200:
            print(f"✅ Signal envoyé sur Telegram : {crypto} ({level})")
            return True
        else:
            print(f" Erreur Telegram : {reponse.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Problème de connexion Telegram : {e}")
        return False
