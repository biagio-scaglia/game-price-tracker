import pandas as pd

def average_saving(df):
    if df.empty:
        return 0.0
    
    if "savings" not in df.columns:
        return 0.0
    
    return df["savings"].mean()

def top_savings(df, limit):
    if df.empty:
        return df.head(0)
    
    if "savings" not in df.columns:
        return df.head(0)
    
    return df.nlargest(limit, "savings")

def get_statistics(df):
    if df.empty:
        return {}
    
    stats = {}
    stats["total_deals"] = len(df)
    
    if "savings" in df.columns:
        stats["avg_saving"] = df["savings"].mean()
        stats["max_saving"] = df["savings"].max()
        stats["deals_over_50"] = len(df[df["savings"] >= 50])
        stats["deals_over_75"] = len(df[df["savings"] >= 75])
        stats["deals_over_90"] = len(df[df["savings"] >= 90])
    else:
        stats["avg_saving"] = 0
        stats["max_saving"] = 0
        stats["deals_over_50"] = 0
        stats["deals_over_75"] = 0
        stats["deals_over_90"] = 0
    
    if "salePrice" in df.columns:
        stats["min_price"] = df["salePrice"].min()
        stats["max_price"] = df["salePrice"].max()
        stats["avg_price"] = df["salePrice"].mean()
    else:
        stats["min_price"] = 0
        stats["max_price"] = 0
        stats["avg_price"] = 0
    
    return stats

def best_store_for_game(df, stores_dict):
    if df.empty:
        return None
    
    if "storeID" not in df.columns:
        return None
    
    if "price" not in df.columns:
        return None
    
    prezzo_minimo = df["price"].min()
    indice_migliore = df["price"].idxmin()
    best_deal = df.loc[indice_migliore]
    
    store_id = str(best_deal["storeID"])
    if store_id in stores_dict:
        store_name = stores_dict[store_id]
    else:
        store_name = f"Store {store_id}"
    
    risultato = {
        "store": store_name,
        "price": best_deal["price"],
        "savings": best_deal["savings"],
        "retailPrice": best_deal["retailPrice"]
    }
    
    return risultato

def store_analysis(df, stores_dict):
    if df.empty:
        return pd.DataFrame()
    
    if "storeID" not in df.columns:
        return pd.DataFrame()
    
    store_stats = []
    for store_id, store_name in stores_dict.items():
        store_deals = df[df["storeID"] == store_id]
        
        if store_deals.empty:
            continue
        
        numero_offerte = len(store_deals)
        risparmio_medio = store_deals["savings"].mean()
        prezzo_medio = store_deals["salePrice"].mean()
        prezzo_minimo = store_deals["salePrice"].min()
        prezzo_massimo = store_deals["salePrice"].max()
        
        stat = {
            "storeID": store_id,
            "storeName": store_name,
            "numDeals": numero_offerte,
            "avgSavings": risparmio_medio,
            "avgPrice": prezzo_medio,
            "minPrice": prezzo_minimo,
            "maxPrice": prezzo_massimo
        }
        store_stats.append(stat)
    
    return pd.DataFrame(store_stats)
