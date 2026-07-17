"""
aegis_engine.py
Le cerveau du bot. Il analyse les cryptos et attribue un score (Bronze, Argent, Or).
"""

import config

def analyze_coin(coin_data):
    """
    Analyse une crypto et lui donne un score.
    coin_data contient : 'symbol', 'price', 'volume_24h', 'open_24h' (prix d'il y a 24h)
    """
    score = 0
    reasons = [] # Pour expliquer pourquoi on donne ce score
    
    price = coin_data['price']
    open_24h = coin_data.get('open_24h', price) # Prix d'ouverture il y a 24h
    
    # --- CRITÈRE 1 : Tendance (Momentum) ---
    if price > open_24h:
        variation = ((price - open_24h) / open_24h) * 100
        score += 40 # Gros bonus pour la tendance
        reasons.append(f"Tendance haussière (+{variation:.2f}%)")
    else:
        variation = ((price - open_24h) / open_24h) * 100
        # Si c'est trop baissier, on pénalise
        if variation < -5:
            score -= 20
            reasons.append(f"Tendance trop baissière ({variation:.2f}%)")
        else:
            score += 10
            reasons.append(f"Tendance neutre/légère ({variation:.2f}%)")

    # --- CRITÈRE 2 : Volume (Intérêt du marché) ---
    volume = coin_data['volume_24h']
    if volume > 500_000_000: # Plus de 500 Millions
        score += 30
        reasons.append("Volume institutionnel très fort")
    elif volume > 100_000_000: # Plus de 100 Millions
        score += 20
        reasons.append("Volume fort")
    else:
        score += 10
        reasons.append("Volume modéré")

    # --- CRITÈRE 3 : Volatilité (Le mouvement) ---
    if 2 < variation < 7:
        score += 30
        reasons.append("Mouvement sain détecté (Sweet Spot)")
    elif variation > 15:
        score -= 10 # Attention au FOMO, c'est peut-être trop tard
        reasons.append("Attention : déjà trop monté (Risque de correction)")

    # On limite le score entre 0 et 100
    score = max(0, min(100, score))
    
    return score, reasons

def get_signal_level(score):
    """Définit le niveau du signal selon le score."""
    if score >= config.SCORE_OR:
        return "🥇 OR"
    elif score >= config.SCORE_ARGENT:
        return "🥈 ARGENT"
    elif score >= config.SCORE_BRONZE:
        return "🥉 BRONZE"
    else:
        return None # Pas de signal

def scan_market(filtered_coins):
    """Analyse toutes les cryptos filtrées et retourne les signaux."""
    signals = []
    
    print(f"🧠 Analyse de {len(filtered_coins)} cryptos par le moteur Aegis...")
    
    for coin in filtered_coins:
        score, reasons = analyze_coin(coin)
        level = get_signal_level(score)
        
        if level:
            signals.append({
                'symbol': coin['symbol'],
                'price': coin['price'],
                'score': score,
                'level': level,
                'reasons': reasons
            })
            
    # On trie les signaux du meilleur score au plus faible
    signals.sort(key=lambda x: x['score'], reverse=True)
    return signals
