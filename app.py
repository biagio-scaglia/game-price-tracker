from data.fetcher import get_deals, search_games, get_game_details, get_stores
from data.parser import deals_to_dataframe, game_details_to_dataframe, search_results_to_dataframe
from data.saver import save_csv
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
    
    if not os.path.exists("exports"):
        os.makedirs("exports")
    save_csv(df, "exports/deals.csv")
    print(f"\n💾 Dati salvati in exports/deals.csv")
    
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
    else:
        print("\n❌ Nessuna offerta disponibile al momento")

def show_menu():
    print("\n" + "="*70)
    print(" " * 20 + "🎮 CHEAPSHARK ANALYZER 🎮")
    print("="*70)
    print("\n  1. 📊 Analizza tutte le offerte")
    print("  2. 🔍 Cerca un gioco")
    print("  3. ❌ Esci")
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

