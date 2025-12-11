import json
import os
from datetime import datetime
from .fetcher import get_game_details

WISHLIST_FILE = "wishlist.json"

def load_wishlist():
    """Carica la wishlist dal file JSON"""
    if not os.path.exists(WISHLIST_FILE):
        return []
    
    try:
        with open(WISHLIST_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_wishlist(wishlist):
    """Salva la wishlist su file JSON"""
    with open(WISHLIST_FILE, 'w', encoding='utf-8') as f:
        json.dump(wishlist, f, ensure_ascii=False, indent=2)

def add_to_wishlist(game_id, game_title, target_price=None):
    """Aggiunge un gioco alla wishlist"""
    wishlist = load_wishlist()
    
    # Controlla se il gioco è già presente
    for item in wishlist:
        if item.get("gameID") == game_id:
            return False, "Gioco già presente nella wishlist"
    
    new_item = {
        "gameID": game_id,
        "title": game_title,
        "targetPrice": target_price,
        "addedDate": datetime.now().isoformat(),
        "lastChecked": None,
        "lowestPriceSeen": None
    }
    
    wishlist.append(new_item)
    save_wishlist(wishlist)
    return True, "Gioco aggiunto alla wishlist"

def remove_from_wishlist(game_id):
    """Rimuove un gioco dalla wishlist"""
    wishlist = load_wishlist()
    wishlist = [item for item in wishlist if item.get("gameID") != game_id]
    save_wishlist(wishlist)
    return True

def get_wishlist():
    """Restituisce la wishlist completa"""
    return load_wishlist()

def check_wishlist_prices():
    """Verifica i prezzi dei giochi nella wishlist e restituisce gli alert"""
    wishlist = load_wishlist()
    if not wishlist:
        return []
    
    alerts = []
    
    for item in wishlist:
        game_id = item.get("gameID")
        game_title = item.get("title")
        target_price = item.get("targetPrice")
        
        if not target_price:
            continue
        
        try:
            game_data = get_game_details(game_id)
            if not game_data or "deals" not in game_data:
                continue
            
            # Trova il prezzo più basso tra tutte le offerte
            deals = game_data.get("deals", [])
            if not deals:
                continue
            
            current_price = float(deals[0].get("price", 999999))
            best_store_id = deals[0].get("storeID")
            best_deal_id = deals[0].get("dealID", "")
            for deal in deals:
                price = float(deal.get("price", 999999))
                if price < current_price:
                    current_price = price
                    best_store_id = deal.get("storeID")
                    best_deal_id = deal.get("dealID", "")
            
            # Aggiorna il prezzo più basso visto
            lowest_seen = item.get("lowestPriceSeen")
            if not lowest_seen or current_price < float(lowest_seen):
                item["lowestPriceSeen"] = current_price
            
            item["lastChecked"] = datetime.now().isoformat()
            
            # Controlla se il prezzo è sceso sotto la soglia
            if current_price <= float(target_price):
                alerts.append({
                    "gameID": game_id,
                    "title": game_title,
                    "targetPrice": target_price,
                    "currentPrice": current_price,
                    "storeID": best_store_id,
                    "dealID": best_deal_id
                })
        
        except Exception as e:
            continue
    
    # Salva le modifiche alla wishlist
    save_wishlist(wishlist)
    return alerts

