from data.fetcher import get_deals, search_games, get_game_details, get_stores
from data.parser import deals_to_dataframe, game_details_to_dataframe, search_results_to_dataframe
from data.saver import save_data
from data.wishlist import add_to_wishlist, remove_from_wishlist, get_wishlist, check_wishlist_prices
from data.filters import filter_deals, apply_advanced_filters
from data.custom_stores import get_all_stores_info, get_custom_stores, search_url_for_store
from analytics.analyzer import average_saving, top_savings, best_store_for_game, store_analysis, get_statistics
from analytics.chart import plot_savings_trend, plot_store_comparison, plot_game_prices
import os

def load_stores():
    stores = get_stores()
    stores_dict = {}
    
    for store in stores:
        store_id = str(store["storeID"])
        store_name = store["storeName"]
        stores_dict[store_id] = store_name
    
    return stores_dict

def analyze_all_deals():
    print("\n" + "="*70)
    print(" " * 15 + "ANALISI COMPLETA OFFERTE")
    print("="*70)
    
    print("\n📡 Recupero offerte da CheapShark...")
    deals = get_deals()
    print(f"✓ Trovate {len(deals)} offerte")
    
    df = deals_to_dataframe(deals)
    
    if df.empty:
        print("❌ Nessun dato disponibile")
        return
    
    stats = get_statistics(df)
    
    print("\n" + "─"*70)
    print("📊 STATISTICHE GENERALI")
    print("─"*70)
    print(f"  • Totale offerte: {stats['total_deals']}")
    print(f"  • Risparmio medio: {stats['avg_saving']:.2f}%")
    print(f"  • Risparmio massimo: {stats['max_saving']:.2f}%")
    print(f"  • Prezzo medio: ${stats['avg_price']:.2f}")
    print(f"  • Prezzo minimo: ${stats['min_price']:.2f}")
    print(f"  • Prezzo massimo: ${stats['max_price']:.2f}")
    print(f"\n  🎯 Offerte con sconto ≥50%: {stats['deals_over_50']}")
    print(f"  🎯 Offerte con sconto ≥75%: {stats['deals_over_75']}")
    print(f"  🎯 Offerte con sconto ≥90%: {stats['deals_over_90']}")
    
    print("\n" + "─"*70)
    print("🏆 TOP 5 OFFERTE CON PIÙ RISPARMIO")
    print("─"*70)
    top_5 = top_savings(df, 5)
    numero = 1
    for idx in top_5.index:
        row = top_5.loc[idx]
        print(f"  {numero}. {row['title']}")
        print(f"     💰 Prezzo: ${row['salePrice']:.2f} | 💸 Risparmio: {row['savings']:.2f}%")
        numero += 1
    
    stores_dict = load_stores()
    store_df = store_analysis(df, stores_dict)
    
    if not store_df.empty:
        print("\n" + "─"*70)
        print("🏪 ANALISI PER STORE")
        print("─"*70)
        store_df_display = store_df[["storeName", "numDeals", "avgSavings", "avgPrice"]].copy()
        store_df_display.columns = ["Store", "N. Offerte", "Risparmio Medio (%)", "Prezzo Medio ($)"]
        store_df_display["Risparmio Medio (%)"] = store_df_display["Risparmio Medio (%)"].round(2)
        store_df_display["Prezzo Medio ($)"] = store_df_display["Prezzo Medio ($)"].round(2)
        print(store_df_display.to_string(index=False))
        plot_store_comparison(store_df)
    
    # Salvataggio in CSV
    csv_path = save_data(df, "deals", format='csv')
    if csv_path:
        print(f"\n💾 Dati salvati in {csv_path}")
    
    # Offri export multipli
    export_more = input("\n💾 Vuoi esportare anche in altri formati? (s/n): ").strip().lower()
    if export_more == 's':
        json_path = save_data(df, "deals", format='json')
        if json_path:
            print(f"✅ Export JSON completato: {json_path}")
        else:
            print("❌ Export JSON fallito")
        
        try:
            import openpyxl
            xlsx_path = save_data(df, "deals", format='excel')
            if xlsx_path:
                print(f"✅ Export Excel completato: {xlsx_path}")
            else:
                print("❌ Export Excel fallito")
        except ImportError:
            print("⚠️  Export Excel non disponibile (installa openpyxl: pip install openpyxl)")
    
    plot_savings_trend(df)
    print("\n✅ Analisi completata! Grafici salvati nella cartella 'charts/'")

def search_game():
    print("\n" + "="*70)
    print(" " * 25 + "RICERCA GIOCO")
    print("="*70)
    
    title = input("\n🔍 Inserisci il nome del gioco da cercare: ").strip()
    
    if not title:
        print("❌ Nome non valido")
        return
    
    print(f"\n🔎 Ricerca di '{title}'...")
    results = search_games(title)
    
    if not results:
        print("❌ Nessun gioco trovato")
        return
    
    df = search_results_to_dataframe(results)
    
    print(f"\n✅ Trovati {len(df)} giochi:")
    print("─"*70)
    numero = 1
    for idx in df.index:
        row = df.loc[idx]
        if row['steamAppID']:
            steam_info = f"Steam ID: {row['steamAppID']}"
        else:
            steam_info = "Non su Steam"
        print(f"  {numero}. {row['title']}")
        print(f"     💰 Prezzo migliore: ${row['cheapest']:.2f} | {steam_info}")
        numero += 1
    
    choice = input("\n📝 Inserisci il numero del gioco per vedere i dettagli (0 per annullare): ").strip()
    
    if choice == "0":
        return
    
    try:
        idx = int(choice) - 1
        
        if idx < 0:
            print("❌ Scelta non valida")
            return
        
        if idx >= len(df):
            print("❌ Scelta non valida")
            return
        
        game_id = df.iloc[idx]["gameID"]
        game_title = df.iloc[idx]["title"]
        show_game_details(game_id, game_title)
        
    except ValueError:
        print("❌ Inserisci un numero valido")

def show_game_details(game_id, game_title):
    print("\n" + "="*70)
    print(f" " * 20 + f"DETTAGLI: {game_title}")
    print("="*70)
    
    print("\n📡 Recupero dettagli...")
    game_data = get_game_details(game_id)
    
    if not game_data:
        print("❌ Dettagli non disponibili")
        return
    
    info = game_data.get("info", {})
    cheapest_ever = game_data.get("cheapestPriceEver", {})
    
    print("\n" + "─"*70)
    print("📋 INFORMAZIONI GIOCO")
    print("─"*70)
    print(f"  • Titolo: {info.get('title', 'N/A')}")
    steam_id = info.get('steamAppID', 'N/A')
    if steam_id != 'N/A':
        print(f"  • Steam App ID: {steam_id}")
        print(f"  • Link Steam: https://store.steampowered.com/app/{steam_id}/")
    else:
        print(f"  • Steam App ID: Non disponibile")
    
    if cheapest_ever:
        price = cheapest_ever.get('price', 'N/A')
        date = cheapest_ever.get('date', 'N/A')
        print(f"\n  📉 Prezzo più basso mai registrato: ${price}")
        if date != 'N/A':
            from datetime import datetime
            try:
                date_str = datetime.fromtimestamp(date).strftime("%d/%m/%Y")
                print(f"  📅 Data: {date_str}")
            except:
                pass
    
    deals_df = game_details_to_dataframe(game_data)
    
    if not deals_df.empty:
        stores_dict = load_stores()
        deals_df["storeName"] = deals_df["storeID"].astype(str).map(stores_dict)
        deals_df_sorted = deals_df.sort_values("price")
        
        print("\n" + "─"*70)
        print(f"💰 OFFERTE DISPONIBILI ({len(deals_df)})")
        print("─"*70)
        
        display_df = deals_df_sorted[["storeName", "price", "retailPrice", "savings"]].copy()
        display_df.columns = ["Store", "Prezzo ($)", "Prezzo Originale ($)", "Risparmio (%)"]
        display_df["Prezzo ($)"] = display_df["Prezzo ($)"].round(2)
        display_df["Prezzo Originale ($)"] = display_df["Prezzo Originale ($)"].round(2)
        display_df["Risparmio (%)"] = display_df["Risparmio (%)"].round(2)
        print(display_df.to_string(index=False))
        
        best = best_store_for_game(deals_df, stores_dict)
        if best:
            print("\n" + "─"*70)
            print("🏆 MIGLIORE OFFERTA")
            print("─"*70)
            print(f"  • Store: {best['store']}")
            print(f"  • Prezzo: ${best['price']:.2f}")
            print(f"  • Prezzo originale: ${best['retailPrice']:.2f}")
            print(f"  • Risparmio: {best['savings']:.2f}%")
            saved = best['retailPrice'] - best['price']
            print(f"  • Risparmi: ${saved:.2f}")
        
        thumb_url = info.get("thumb", "")
        plot_game_prices(deals_df, game_title, stores_dict, thumb_url)
        print(f"\n✅ Grafico salvato nella cartella 'charts/'")
        
        # Mostra link per ricerca su store aggiuntivi
        show_additional_stores_links(game_title)
        
        # Offri opzione per aggiungere alla wishlist
        wishlist_choice = input("\n📌 Vuoi aggiungere questo gioco alla wishlist? (s/n): ").strip().lower()
        if wishlist_choice == 's':
            target_price_input = input("💰 Inserisci il prezzo target (lascia vuoto per nessun target): ").strip()
            target_price = None
            if target_price_input:
                try:
                    target_price = float(target_price_input)
                except ValueError:
                    print("❌ Prezzo non valido, aggiunto senza target")
            success, message = add_to_wishlist(game_id, game_title, target_price)
            print(f"✅ {message}")
    else:
        print("\n❌ Nessuna offerta disponibile al momento")

def analyze_with_filters():
    """Analizza le offerte con filtri avanzati"""
    print("\n" + "="*70)
    print(" " * 15 + "ANALISI OFFERTE CON FILTRI")
    print("="*70)
    
    print("\n📡 Recupero offerte da CheapShark...")
    deals = get_deals()
    print(f"✓ Trovate {len(deals)} offerte")
    
    df = deals_to_dataframe(deals)
    
    if df.empty:
        print("❌ Nessun dato disponibile")
        return
    
    print("\n🔧 Configura i filtri (lascia vuoto per saltare):")
    
    # Prezzo minimo
    min_price_input = input("  💵 Prezzo minimo ($): ").strip()
    min_price = float(min_price_input) if min_price_input else None
    
    # Prezzo massimo
    max_price_input = input("  💵 Prezzo massimo ($): ").strip()
    max_price = float(max_price_input) if max_price_input else None
    
    # Sconto minimo
    min_savings_input = input("  🎯 Sconto minimo (%): ").strip()
    min_savings = float(min_savings_input) if min_savings_input else None
    
    # Store
    stores_dict = load_stores()
    print("\n  🏪 Store disponibili:")
    store_list = list(stores_dict.items())[:10]  # Mostra i primi 10
    for store_id, store_name in store_list:
        print(f"    {store_id}: {store_name}")
    store_id_input = input("  🏪 ID Store (lascia vuoto per tutti, multipli separati da virgola): ").strip()
    store_ids = None
    if store_id_input:
        try:
            store_ids = [int(s.strip()) for s in store_id_input.split(',')]
        except:
            print("  ⚠️  Formato non valido, verranno mostrati tutti gli store")
    
    # Applica filtri
    filtered_df = filter_deals(df, min_price=min_price, max_price=max_price, 
                               min_savings=min_savings, store_id=store_ids)
    
    if filtered_df.empty:
        print("\n❌ Nessuna offerta corrisponde ai filtri selezionati")
        return
    
    print(f"\n✅ Trovate {len(filtered_df)} offerte corrispondenti ai filtri")
    
    stats = get_statistics(filtered_df)
    
    print("\n" + "─"*70)
    print("📊 STATISTICHE OFFERTE FILTRATE")
    print("─"*70)
    print(f"  • Totale offerte: {stats['total_deals']}")
    print(f"  • Risparmio medio: {stats['avg_saving']:.2f}%")
    print(f"  • Prezzo medio: ${stats['avg_price']:.2f}")
    print(f"  • Prezzo minimo: ${stats['min_price']:.2f}")
    print(f"  • Prezzo massimo: ${stats['max_price']:.2f}")
    
    print("\n" + "─"*70)
    print("🏆 TOP 10 OFFERTE FILTRATE")
    print("─"*70)
    top_10 = top_savings(filtered_df, 10)
    for i, (idx, row) in enumerate(top_10.iterrows(), 1):
        print(f"  {i}. {row['title']}")
        print(f"     💰 ${row['salePrice']:.2f} | 💸 {row['savings']:.2f}%")
    
    # Export
    export_format = input("\n💾 Formato export (csv/json/excel, default: csv): ").strip().lower() or 'csv'
    if export_format not in ['csv', 'json', 'excel']:
        export_format = 'csv'
    
    saved_path = save_data(filtered_df, "filtered_deals", format=export_format)
    if saved_path:
        print(f"✅ Dati salvati in {saved_path}")
    else:
        print("❌ Errore nel salvataggio dei dati")

def manage_wishlist():
    """Gestisce la wishlist"""
    print("\n" + "="*70)
    print(" " * 25 + "WISHLIST")
    print("="*70)
    
    wishlist = get_wishlist()
    
    if not wishlist:
        print("\n📭 La tua wishlist è vuota")
        print("\n💡 Suggerimento: Aggiungi giochi dalla ricerca per monitorare i prezzi!")
        return
    
    print(f"\n📋 Giochi nella wishlist ({len(wishlist)}):")
    print("─"*70)
    
    for i, item in enumerate(wishlist, 1):
        game_id = item.get("gameID")
        title = item.get("title")
        target_price = item.get("targetPrice")
        lowest_seen = item.get("lowestPriceSeen")
        
        print(f"  {i}. {title}")
        if target_price:
            print(f"     🎯 Prezzo target: ${target_price:.2f}")
        if lowest_seen:
            print(f"     📉 Prezzo più basso visto: ${lowest_seen:.2f}")
        else:
            print(f"     📉 Prezzo più basso visto: Non ancora controllato")
        print()
    
    print("\nOpzioni:")
    print("  1. Verifica prezzi e mostra alert")
    print("  2. Rimuovi un gioco")
    print("  3. Torna al menu principale")
    
    choice = input("\nScegli un'opzione: ").strip()
    
    if choice == "1":
        check_price_alerts()
    elif choice == "2":
        remove_game_from_wishlist(wishlist)
    else:
        return

def check_price_alerts():
    """Verifica i prezzi della wishlist e mostra gli alert"""
    wishlist = get_wishlist()
    
    if not wishlist:
        print("\n📭 La tua wishlist è vuota")
        print("💡 Aggiungi giochi dalla ricerca per monitorare i prezzi!")
        return
    
    games_with_target = [item for item in wishlist if item.get("targetPrice")]
    if not games_with_target:
        print("\n⚠️  Nessun gioco nella wishlist ha un prezzo target impostato")
        print("💡 Modifica i giochi nella wishlist per impostare un prezzo target")
        return
    
    print(f"\n📡 Verifica prezzi per {len(games_with_target)} giochi in corso...")
    alerts = check_wishlist_prices()
    
    if not alerts:
        print("✅ Nessun alert: nessun gioco ha raggiunto il prezzo target")
        return
    
    print("\n" + "="*70)
    print(" " * 25 + "🎉 ALERT PREZZI!")
    print("="*70)
    stores_dict = load_stores()
    
    for alert in alerts:
        store_id = str(alert.get("storeID", ""))
        store_name = stores_dict.get(store_id, f"Store {store_id}")
        
        print(f"\n🎮 {alert['title']}")
        print(f"   🎯 Prezzo target: ${alert['targetPrice']:.2f}")
        print(f"   💰 Prezzo attuale: ${alert['currentPrice']:.2f}")
        print(f"   🏪 Store: {store_name}")
        risparmio = float(alert['targetPrice']) - alert['currentPrice']
        print(f"   💸 Risparmi rispetto al target: ${risparmio:.2f}")
        print(f"   🔗 https://www.cheapshark.com/redirect?dealID={alert.get('dealID', '')}")

def clear_screen():
    """Pulisce lo schermo della console"""
    import platform
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def show_additional_stores_links(game_title):
    """Mostra link per cercare su store aggiuntivi non supportati da CheapShark"""
    custom_stores = get_custom_stores()
    
    if not custom_stores:
        return
    
    print("\n" + "─"*70)
    print("🔗 RICERCA SU ALTRI STORE")
    print("─"*70)
    print("💡 Link per cercare manualmente su store aggiuntivi:\n")
    
    # Mostra solo i primi 10 per non appesantire l'output
    stores_list = list(custom_stores.items())[:10]
    
    for store_name, store_info in stores_list:
        search_url = search_url_for_store(store_name, game_title)
        website = store_info.get("website", "")
        print(f"  🏪 {store_name}")
        if search_url:
            print(f"     🔗 {search_url}")
        elif website:
            print(f"     🔗 {website}")
        print()
    
    if len(custom_stores) > 10:
        print(f"  ... e altri {len(custom_stores) - 10} store")
        print(f"  💡 Usa l'opzione 'Visualizza tutti gli store' dal menu per vedere tutti i link")

def list_all_stores():
    """Mostra tutti gli store disponibili (CheapShark + custom)"""
    print("\n" + "="*70)
    print(" " * 20 + "📋 TUTTI GLI STORE DISPONIBILI")
    print("="*70)
    
    # Store da CheapShark
    print("\n🏪 STORE SUPPORTATI DA CHEAPSHARK API")
    print("─"*70)
    stores_dict = load_stores()
    cheapshark_stores = list(stores_dict.values())
    
    # Ordina alfabeticamente
    cheapshark_stores_sorted = sorted(cheapshark_stores)
    
    for i, store_name in enumerate(cheapshark_stores_sorted, 1):
        print(f"  {i:2d}. {store_name}")
    
    # Store custom
    custom_stores = get_all_stores_info()
    supported_custom = {name: info for name, info in custom_stores.items() if info.get("supported", False)}
    unsupported_custom = {name: info for name, info in custom_stores.items() if not info.get("supported", False)}
    
    if unsupported_custom:
        print("\n🏪 ALTRI STORE (ricerca manuale richiesta)")
        print("─"*70)
        for i, (store_name, store_info) in enumerate(sorted(unsupported_custom.items()), 1):
            website = store_info.get("website", "")
            notes = store_info.get("notes", "")
            print(f"  {i:2d}. {store_name}")
            if website:
                print(f"      🔗 {website}")
            if notes:
                print(f"      ℹ️  {notes}")
            print()

def remove_game_from_wishlist(wishlist):
    """Rimuove un gioco dalla wishlist"""
    if not wishlist:
        return
    
    print("\nQuale gioco vuoi rimuovere?")
    try:
        choice = int(input("Numero: ").strip())
        if 1 <= choice <= len(wishlist):
            game_id = wishlist[choice - 1].get("gameID")
            remove_from_wishlist(game_id)
            print("✅ Gioco rimosso dalla wishlist")
        else:
            print("❌ Scelta non valida")
    except ValueError:
        print("❌ Inserisci un numero valido")

def show_menu():
    print("\n" + "="*70)
    print(" " * 20 + "🎮 CHEAPSHARK ANALYZER 🎮")
    print("="*70)
    print("\n  1. 📊 Analizza tutte le offerte")
    print("  2. 🔍 Cerca un gioco")
    print("  3. 🔧 Analizza con filtri avanzati")
    print("  4. 📌 Gestisci wishlist")
    print("  5. 🔔 Verifica alert prezzi")
    print("  6. 📋 Visualizza tutti gli store disponibili")
    print("  7. 🧹 Pulisci schermo")
    print("  8. ❌ Esci")
    print("="*70)

def main():
    try:
        while True:
            show_menu()
            choice = input("\nScegli un'opzione: ").strip()
            
            if choice == "1":
                analyze_all_deals()
            elif choice == "2":
                search_game()
            elif choice == "3":
                analyze_with_filters()
            elif choice == "4":
                manage_wishlist()
            elif choice == "5":
                check_price_alerts()
            elif choice == "6":
                list_all_stores()
            elif choice == "7":
                clear_screen()
            elif choice == "8":
                print("\nArrivederci!")
                break
            else:
                print("\nOpzione non valida, riprova")
    except KeyboardInterrupt:
        print("\n\n⚠️  Operazione interrotta")
        print("👋 Arrivederci!")
    except Exception as e:
        print(f"\n\n❌ Errore: {e}")
        print("👋 Arrivederci!")

if __name__ == "__main__":
    main()

