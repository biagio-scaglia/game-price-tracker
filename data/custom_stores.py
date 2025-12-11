"""
Gestione store personalizzati non supportati da CheapShark API
"""

CUSTOM_STORES = {
    # Store non in CheapShark ma popolari
    "Epic Games Store": {
        "name": "Epic Games Store",
        "website": "https://store.epicgames.com/",
        "search_url": "https://store.epicgames.com/en-US/browse",
        "supported": False,  # Non supportato da CheapShark
        "notes": "Controlla manualmente sul sito"
    },
    "Humble Store": {
        "name": "Humble Store",
        "website": "https://www.humblebundle.com/store",
        "search_url": "https://www.humblebundle.com/store/search",
        "supported": True,  # Supportato da CheapShark
        "notes": "Disponibile via CheapShark"
    },
    "Microsoft Store": {
        "name": "Microsoft Store",
        "website": "https://www.microsoft.com/store/games",
        "search_url": "https://www.microsoft.com/store/search/games",
        "supported": False,
        "notes": "Controlla manualmente sul sito"
    },
    "Ubisoft Store": {
        "name": "Ubisoft Store",
        "website": "https://store.ubisoft.com/",
        "search_url": "https://store.ubisoft.com/en-us/search",
        "supported": False,
        "notes": "Controlla manualmente sul sito"
    },
    "Battle.net": {
        "name": "Battle.net",
        "website": "https://www.battle.net/",
        "search_url": "https://www.battle.net/shop",
        "supported": False,
        "notes": "Controlla manualmente sul sito"
    },
    "Itch.io": {
        "name": "Itch.io",
        "website": "https://itch.io/",
        "search_url": "https://itch.io/games",
        "supported": False,
        "notes": "Controlla manualmente sul sito"
    },
    "Xbox Game Pass for PC": {
        "name": "Xbox Game Pass for PC",
        "website": "https://www.xbox.com/en-US/xbox-game-pass/pc-games",
        "search_url": "https://www.xbox.com/en-US/xbox-game-pass/pc-games",
        "supported": False,
        "notes": "Servizio di abbonamento - controlla disponibilità"
    },
    "Kinguin": {
        "name": "Kinguin",
        "website": "https://www.kinguin.net/",
        "search_url": "https://www.kinguin.net/catalogsearch/result",
        "supported": False,
        "notes": "Controlla manualmente sul sito"
    },
    "CDKeys": {
        "name": "CDKeys",
        "website": "https://www.cdkeys.com/",
        "search_url": "https://www.cdkeys.com/search",
        "supported": False,
        "notes": "Controlla manualmente sul sito"
    },
    "Eneba": {
        "name": "Eneba",
        "website": "https://www.eneba.com/",
        "search_url": "https://www.eneba.com/store/games",
        "supported": False,
        "notes": "Controlla manualmente sul sito"
    },
    "HRK Game": {
        "name": "HRK Game",
        "website": "https://www.hrkgame.com/",
        "search_url": "https://www.hrkgame.com/search",
        "supported": False,
        "notes": "Controlla manualmente sul sito"
    },
    "Fanatical": {
        "name": "Fanatical",
        "website": "https://www.fanatical.com/",
        "search_url": "https://www.fanatical.com/en/search",
        "supported": True,  # Supportato da CheapShark
        "notes": "Disponibile via CheapShark"
    },
    "Voidu": {
        "name": "Voidu",
        "website": "https://www.voidu.com/",
        "search_url": "https://www.voidu.com/en/search",
        "supported": False,
        "notes": "Controlla manualmente sul sito"
    },
    "IndieGala": {
        "name": "IndieGala",
        "website": "https://www.indiegala.com/store",
        "search_url": "https://www.indiegala.com/store/search",
        "supported": True,  # Supportato da CheapShark
        "notes": "Disponibile via CheapShark"
    },
    "Sila Games": {
        "name": "Sila Games",
        "website": "https://silagames.com/",
        "search_url": "https://silagames.com/search",
        "supported": False,
        "notes": "Controlla manualmente sul sito"
    },
    "AllYouPlay": {
        "name": "AllYouPlay",
        "website": "https://www.allyouplay.com/",
        "search_url": "https://www.allyouplay.com/en/search",
        "supported": False,
        "notes": "Controlla manualmente sul sito"
    },
    "Playism": {
        "name": "Playism",
        "website": "https://playism.com/",
        "search_url": "https://playism.com/games",
        "supported": False,
        "notes": "Controlla manualmente sul sito"
    },
    "GG.deals": {
        "name": "GG.deals",
        "website": "https://gg.deals/",
        "search_url": "https://gg.deals/games/",
        "supported": False,
        "notes": "Aggregatore di prezzi - controlla per confronto"
    }
}

def get_all_stores_info():
    """Restituisce informazioni su tutti gli store (CheapShark + personalizzati)"""
    return CUSTOM_STORES

def get_custom_stores():
    """Restituisce solo gli store personalizzati non supportati da CheapShark"""
    return {name: info for name, info in CUSTOM_STORES.items() if not info.get("supported", False)}

def get_store_info(store_name):
    """Restituisce informazioni su uno store specifico"""
    return CUSTOM_STORES.get(store_name)

def is_store_supported_by_cheapshark(store_name):
    """Verifica se uno store è supportato da CheapShark"""
    store_info = CUSTOM_STORES.get(store_name)
    if store_info:
        return store_info.get("supported", False)
    return None  # Store non conosciuto

def search_url_for_store(store_name, game_title=""):
    """Genera URL di ricerca per uno store dato il nome di un gioco"""
    store_info = CUSTOM_STORES.get(store_name)
    if not store_info:
        return None
    
    search_url = store_info.get("search_url", "")
    if game_title and search_url:
        # Aggiungi parametri di ricerca se supportato
        # Ogni store ha formato diverso, questo è un template base
        if "search" in search_url.lower():
            # Alcuni store usano query parameters
            if "?" in search_url:
                return f"{search_url}&q={game_title.replace(' ', '+')}"
            else:
                return f"{search_url}?q={game_title.replace(' ', '+')}"
    return search_url or store_info.get("website", "")

