import requests
from datetime import datetime
import config

BOT_IS_READY = True

def send_signal(signal):
    """Envoie un signal sur Telegram"""
    
    # Récupération des infos
    crypto = signal.get('symbol', 'Inconnu')
    score = signal.get('score', 0)
    price = signal.get('price', 0.0)
    level = signal.get('level', 'INCONNU')
    reasons = signal.get('reasons', [])
    
    raisons_texte = "\n".join([f"✅ {r}" for r in reasons]) if reasons else "✅ Analyse standard"
    
    message = f"""
{level} <b>SIGNAL AEGIS</b> {level}

💎 <b>Crypto:</b> {crypto}
💰 <b>Prix:</b> ${price:,.2f}
📊 <b>Score:</b> {score}/100

📌 <b>ANALYSE:</b>
{raisons_texte}

⏰ <b>Heure:</b> {datetime.now().strftime('%H:%M:%S')}
    """.strip()

    # Récupération des secrets
    token = config.TELEGRAM_BOT_TOKEN
    chat_id = config.TELEGRAM_CHAT_ID

    print(f" Token: {token[:20]}..." if token else "❌ Token manquant")
    print(f"🔍 Chat ID: {chat_id}" if chat_id else "❌ Chat ID manquant")

    if not token or not chat_id:
        print("❌ ERREUR: Token ou Chat ID manquant !")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    params = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }
    
    try:
        print(f"📤 Envoi vers Telegram...")
        reponse = requests.post(url, params=params, timeout=10)
        
        if reponse.status_code == 200:
            print(f"✅ Signal envoyé : {crypto}")
            return True
        else:
            print(f"❌ Erreur Telegram ({reponse.status_code}): {reponse.text}")
            return False
    except Exception as e:
        print(f"❌ Exception Telegram: {e}")
        return False
