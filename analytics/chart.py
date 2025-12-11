import matplotlib.pyplot as plt
import pandas as pd
import os
from PIL import Image
import requests
from io import BytesIO
import numpy as np

CHARTS_DIR = "charts"

def load_image_from_url(url, max_size=(100, 100)):
    if not url:
        return None
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            return np.array(img)
    except:
        pass
    return None

def ensure_charts_dir():
    if not os.path.exists(CHARTS_DIR):
        os.makedirs(CHARTS_DIR)

def plot_savings_trend(df):
    if df.empty or "savings" not in df.columns:
        print("Nessun dato disponibile per il grafico")
        return
    
    ensure_charts_dir()
    df_sorted = df.sort_values("savings", ascending=False).head(20)
    
    fig, ax = plt.subplots(figsize=(16, 10))
    colors = plt.cm.viridis(df_sorted["savings"] / df_sorted["savings"].max())
    bars = ax.barh(range(len(df_sorted)), df_sorted["savings"], color=colors, alpha=0.8, edgecolor="black", linewidth=0.5)
    
    print("📥 Caricamento thumbnail dei giochi...")
    for i, (idx, row) in enumerate(df_sorted.iterrows()):
        thumb_url = row.get("thumb", "")
        if thumb_url:
            img = load_image_from_url(thumb_url, max_size=(80, 80))
            if img is not None:
                ax.imshow(img, extent=[-8, -1, i-0.4, i+0.4], aspect="auto", zorder=3)
        
        ax.text(row["savings"], i, f"{row['savings']:.1f}%", va="center", ha="left", fontweight="bold", fontsize=9)
        ax.text(-9, i, f"${row['salePrice']:.2f}", va="center", ha="right", fontsize=8, color="gray")
    
    ax.set_yticks(range(len(df_sorted)))
    ax.set_yticklabels(df_sorted["title"], fontsize=9)
    ax.set_xlabel("Risparmio (%)", fontsize=12, fontweight="bold")
    ax.set_title("Top 20 Offerte per Risparmio", fontsize=16, fontweight="bold", pad=20)
    ax.grid(True, alpha=0.3, axis="x", linestyle="--")
    ax.set_xlim(left=-10)
    ax.invert_yaxis()
    plt.tight_layout()
    
    filepath = os.path.join(CHARTS_DIR, "savings_trend.png")
    plt.savefig(filepath, dpi=300, bbox_inches="tight", facecolor="white")
    print(f"✓ Grafico salvato: {filepath}")
    plt.close()

def plot_store_comparison(store_df):
    if store_df.empty:
        print("Nessun dato disponibile per il confronto store")
        return
    
    ensure_charts_dir()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))
    
    store_df_sorted = store_df.sort_values("avgSavings", ascending=False).head(10)
    
    colors1 = plt.cm.Reds(store_df_sorted["avgSavings"] / store_df_sorted["avgSavings"].max())
    bars1 = ax1.barh(store_df_sorted["storeName"], store_df_sorted["avgSavings"], color=colors1, alpha=0.8, edgecolor="black", linewidth=0.5)
    for i, val in enumerate(store_df_sorted["avgSavings"]):
        ax1.text(val, i, f"{val:.1f}%", va="center", ha="left", fontweight="bold", fontsize=9)
    ax1.set_xlabel("Risparmio Medio (%)", fontsize=12, fontweight="bold")
    ax1.set_title("Risparmio Medio per Store", fontsize=14, fontweight="bold", pad=15)
    ax1.grid(True, alpha=0.3, axis="x", linestyle="--")
    ax1.invert_yaxis()
    
    colors2 = plt.cm.Greens(store_df_sorted["numDeals"] / store_df_sorted["numDeals"].max())
    bars2 = ax2.barh(store_df_sorted["storeName"], store_df_sorted["numDeals"], color=colors2, alpha=0.8, edgecolor="black", linewidth=0.5)
    for i, val in enumerate(store_df_sorted["numDeals"]):
        ax2.text(val, i, f"{int(val)}", va="center", ha="left", fontweight="bold", fontsize=9)
    ax2.set_xlabel("Numero di Offerte", fontsize=12, fontweight="bold")
    ax2.set_title("Numero di Offerte per Store", fontsize=14, fontweight="bold", pad=15)
    ax2.grid(True, alpha=0.3, axis="x", linestyle="--")
    ax2.invert_yaxis()
    
    plt.tight_layout()
    filepath = os.path.join(CHARTS_DIR, "store_comparison.png")
    plt.savefig(filepath, dpi=300, bbox_inches="tight", facecolor="white")
    print(f"✓ Grafico salvato: {filepath}")
    plt.close()

def plot_game_prices(game_df, game_title, stores_dict, thumb_url=None):
    if game_df.empty or "price" not in game_df.columns:
        print("Nessun dato disponibile per il grafico prezzi")
        return
    
    ensure_charts_dir()
    game_df_sorted = game_df.sort_values("price")
    game_df_sorted["storeName"] = game_df_sorted["storeID"].astype(str).map(stores_dict)
    
    fig = plt.figure(figsize=(18, max(8, len(game_df_sorted) * 0.8)))
    
    if thumb_url:
        ax_main = plt.subplot2grid((1, 6), (0, 0), colspan=5)
        ax_thumb = plt.subplot2grid((1, 6), (0, 5))
    else:
        ax_main = fig.add_subplot(111)
    
    max_price = game_df_sorted["retailPrice"].max() if "retailPrice" in game_df_sorted.columns else game_df_sorted["price"].max()
    
    for i, (idx, row) in enumerate(game_df_sorted.iterrows()):
        price = row["price"]
        retail = row["retailPrice"]
        savings = row["savings"]
        
        if retail > price and savings > 0:
            ax_main.barh(i, retail, color="lightgray", alpha=0.4, height=0.6, label="Prezzo Originale" if i == 0 else "")
            ax_main.barh(i, price, color="steelblue", alpha=0.8, height=0.6, edgecolor="navy", linewidth=1.5, label="Prezzo Scontato" if i == 0 else "")
            
            ax_main.text(price / 2, i, f"${price:.2f}", va="center", ha="center", 
                        fontweight="bold", fontsize=11, color="white", 
                        bbox=dict(boxstyle="round,pad=0.3", facecolor="steelblue", alpha=0.8))
            
            discount_width = retail - price
            if discount_width > max_price * 0.05:
                ax_main.text(price + discount_width / 2, i, f"-{savings:.1f}%", 
                           va="center", ha="center", fontsize=10, color="darkred", 
                           fontweight="bold", 
                           bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow", alpha=0.9, edgecolor="darkred", linewidth=1))
            
            ax_main.text(retail + max_price * 0.02, i, f"${retail:.2f}", 
                        va="center", ha="left", fontsize=9, color="gray", style="italic")
        else:
            ax_main.barh(i, price, color="gray", alpha=0.6, height=0.6, edgecolor="black", linewidth=1)
            ax_main.text(price / 2, i, f"${price:.2f}", va="center", ha="center", 
                        fontweight="bold", fontsize=11, color="white",
                        bbox=dict(boxstyle="round,pad=0.3", facecolor="gray", alpha=0.8))
    
    ax_main.set_xlabel("Prezzo ($)", fontsize=13, fontweight="bold")
    ax_main.set_title(f"Confronto Prezzi: {game_title}", fontsize=18, fontweight="bold", pad=25)
    ax_main.set_yticks(range(len(game_df_sorted)))
    ax_main.set_yticklabels(game_df_sorted["storeName"], fontsize=11)
    ax_main.grid(True, alpha=0.3, axis="x", linestyle="--", linewidth=0.8)
    ax_main.set_xlim(left=0, right=max_price * 1.15)
    ax_main.invert_yaxis()
    
    handles, labels = ax_main.get_legend_handles_labels()
    if handles:
        by_label = {}
        for label, handle in zip(labels, handles):
            if label not in by_label:
                by_label[label] = handle
        if by_label:
            ax_main.legend(by_label.values(), by_label.keys(), loc="lower right", fontsize=10, framealpha=0.9)
    
    if thumb_url:
        print("📥 Caricamento thumbnail del gioco...")
        img = load_image_from_url(thumb_url, max_size=(250, 250))
        if img is not None:
            ax_thumb.imshow(img)
            ax_thumb.axis("off")
            ax_thumb.set_title("Cover", fontsize=12, fontweight="bold", pad=10)
    
    plt.tight_layout()
    safe_title = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in game_title)[:30]
    filepath = os.path.join(CHARTS_DIR, f"game_prices_{safe_title.replace(' ', '_')}.png")
    plt.savefig(filepath, dpi=300, bbox_inches="tight", facecolor="white")
    print(f"✓ Grafico salvato: {filepath}")
    plt.close()

