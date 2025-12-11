import requests

BASE_URL = "https://www.cheapshark.com/api/1.0"

def get_deals(store_id=None, upper_price=None):
    url = f"{BASE_URL}/deals"
    params = {}
    
    if store_id:
        params["storeID"] = store_id
    
    if upper_price:
        params["upperPrice"] = upper_price
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def search_games(title):
    url = f"{BASE_URL}/games"
    params = {"title": title}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def get_game_details(game_id):
    url = f"{BASE_URL}/games"
    params = {"id": game_id}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def get_stores():
    url = f"{BASE_URL}/stores"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
