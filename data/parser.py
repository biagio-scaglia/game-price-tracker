import pandas as pd

def deals_to_dataframe(deals):
    if not deals:
        return pd.DataFrame()
    
    rows = []
    
    for deal in deals:
        titolo = deal.get("title", "")
        prezzo_scontato = deal.get("salePrice", "0")
        prezzo_normale = deal.get("normalPrice", "0")
        risparmio = deal.get("savings", "0")
        rating = deal.get("steamRatingText", "N/A")
        store_id = deal.get("storeID", "")
        game_id = deal.get("gameID", "")
        thumb = deal.get("thumb", "")
        
        row = {
            "title": titolo,
            "salePrice": prezzo_scontato,
            "normalPrice": prezzo_normale,
            "savings": risparmio,
            "steamRating": rating,
            "storeID": store_id,
            "gameID": game_id,
            "thumb": thumb
        }
        rows.append(row)
    
    df = pd.DataFrame(rows)
    
    df["salePrice"] = pd.to_numeric(df["salePrice"], errors="coerce")
    df["normalPrice"] = pd.to_numeric(df["normalPrice"], errors="coerce")
    df["savings"] = pd.to_numeric(df["savings"], errors="coerce")
    
    return df

def game_details_to_dataframe(game_data):
    if not game_data:
        return pd.DataFrame()
    
    if "deals" not in game_data:
        return pd.DataFrame()
    
    rows = []
    
    for deal in game_data["deals"]:
        store_id = deal.get("storeID", "")
        prezzo = deal.get("price", "0")
        prezzo_originale = deal.get("retailPrice", "0")
        risparmio = deal.get("savings", "0")
        deal_id = deal.get("dealID", "")
        
        row = {
            "storeID": store_id,
            "price": prezzo,
            "retailPrice": prezzo_originale,
            "savings": risparmio,
            "dealID": deal_id
        }
        rows.append(row)
    
    df = pd.DataFrame(rows)
    
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["retailPrice"] = pd.to_numeric(df["retailPrice"], errors="coerce")
    df["savings"] = pd.to_numeric(df["savings"], errors="coerce")
    
    return df

def search_results_to_dataframe(search_results):
    if not search_results:
        return pd.DataFrame()
    
    rows = []
    
    for game in search_results:
        game_id = game.get("gameID", "")
        titolo = game.get("external", "")
        prezzo_migliore = game.get("cheapest", "0")
        steam_id = game.get("steamAppID", "")
        
        row = {
            "gameID": game_id,
            "title": titolo,
            "cheapest": prezzo_migliore,
            "steamAppID": steam_id
        }
        rows.append(row)
    
    df = pd.DataFrame(rows)
    df["cheapest"] = pd.to_numeric(df["cheapest"], errors="coerce")
    
    return df
