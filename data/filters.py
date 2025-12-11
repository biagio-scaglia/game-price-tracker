import pandas as pd

def filter_deals(df, min_price=None, max_price=None, min_savings=None, 
                 store_id=None, min_rating=None):
    """
    Filtra le offerte in base a vari criteri
    
    Args:
        df: DataFrame con le offerte
        min_price: Prezzo minimo
        max_price: Prezzo massimo
        min_savings: Sconto minimo in percentuale
        store_id: ID dello store (può essere lista)
        min_rating: Rating minimo (se disponibile)
    
    Returns:
        DataFrame filtrato
    """
    if df.empty:
        return df
    
    filtered_df = df.copy()
    
    # Filtro per prezzo minimo
    if min_price is not None:
        if "salePrice" in filtered_df.columns:
            filtered_df = filtered_df[filtered_df["salePrice"] >= min_price]
    
    # Filtro per prezzo massimo
    if max_price is not None:
        if "salePrice" in filtered_df.columns:
            filtered_df = filtered_df[filtered_df["salePrice"] <= max_price]
    
    # Filtro per sconto minimo
    if min_savings is not None:
        if "savings" in filtered_df.columns:
            filtered_df = filtered_df[filtered_df["savings"] >= min_savings]
    
    # Filtro per store
    if store_id is not None:
        if isinstance(store_id, list):
            if "storeID" in filtered_df.columns:
                filtered_df = filtered_df[filtered_df["storeID"].isin(store_id)]
        else:
            if "storeID" in filtered_df.columns:
                filtered_df = filtered_df[filtered_df["storeID"] == store_id]
    
    return filtered_df.reset_index(drop=True)

def apply_advanced_filters(df, filters_dict):
    """
    Applica filtri avanzati da un dizionario
    
    Args:
        df: DataFrame con le offerte
        filters_dict: Dizionario con i filtri da applicare
            Esempio: {
                'min_price': 10,
                'max_price': 50,
                'min_savings': 50,
                'store_ids': [1, 2, 3]
            }
    
    Returns:
        DataFrame filtrato
    """
    return filter_deals(
        df,
        min_price=filters_dict.get('min_price'),
        max_price=filters_dict.get('max_price'),
        min_savings=filters_dict.get('min_savings'),
        store_id=filters_dict.get('store_ids')
    )

