# 🎮 CheapShark Analyzer

> Analizzatore completo e modulare per offerte e prezzi dei giochi usando CheapShark API

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Progetto Python modulare per analizzare offerte e prezzi dei giochi in tempo reale utilizzando l'API pubblica di CheapShark. Include analisi statistiche, confronto tra store, grafici professionali e ricerca avanzata.

## ✨ Funzionalità

- 📊 **Analisi completa offerte**: statistiche dettagliate su tutte le offerte disponibili
- 🔍 **Ricerca giochi**: cerca un gioco specifico e confronta prezzi tra store diversi
- 🏪 **Confronto store**: analizza quale store offre i migliori prezzi e sconti
- 📈 **Grafici avanzati**: visualizzazioni professionali con thumbnail dei giochi
- 💾 **Export multipli**: salvataggio automatico in CSV, JSON e Excel con organizzazione in cartelle separate
- 🎯 **Statistiche dettagliate**: risparmi medi, top offerte, analisi per fascia di sconto
- 📌 **Wishlist con alert prezzi**: salva i tuoi giochi preferiti e ricevi notifiche quando scendono sotto il prezzo target
- 🔧 **Filtri avanzati**: filtra le offerte per prezzo, sconto, store e altri criteri
- 🔔 **Verifica alert**: controlla automaticamente se i giochi nella wishlist hanno raggiunto il prezzo target

## 🚀 Quick Start

### Installazione

```bash
# Clona il repository
git clone https://github.com/biagio-scaglia/game-price-tracker.git
cd game-price-tracker

# Installa le dipendenze
pip install -r requirements.txt
```

### Utilizzo

```bash
python app.py
```

Il programma mostrerà un menu interattivo con le seguenti opzioni:

1. **📊 Analizza tutte le offerte**: analisi completa con statistiche, top offerte, confronto store e grafici
2. **🔍 Cerca un gioco**: ricerca un gioco specifico, visualizza dettagli e confronta prezzi tra store
3. **🔧 Analizza con filtri avanzati**: filtra le offerte per prezzo, sconto minimo, store specifico e altro
4. **📌 Gestisci wishlist**: visualizza, aggiungi o rimuovi giochi dalla tua wishlist
5. **🔔 Verifica alert prezzi**: controlla se i giochi nella wishlist hanno raggiunto il prezzo target
6. **📋 Visualizza tutti gli store disponibili**: mostra la lista completa di store supportati (CheapShark + store aggiuntivi)
7. **🧹 Pulisci schermo**: pulisce l'output della console per una migliore leggibilità
8. **❌ Esci**: esce dal programma

## 📁 Struttura Progetto

```
game-price-tracker/
├── data/                  # Moduli per fetch, parsing e salvataggio
│   ├── fetcher.py         # Funzioni API (get_deals, search_games, etc.)
│   ├── parser.py          # Conversione dati JSON in DataFrame pandas
│   ├── saver.py           # Salvataggio dati in CSV, JSON, Excel
│   ├── filters.py         # Filtri avanzati per le offerte
│   ├── wishlist.py        # Gestione wishlist e alert prezzi
│   └── custom_stores.py   # Gestione store aggiuntivi non in CheapShark
├── analytics/             # Moduli per analisi e visualizzazione
│   ├── analyzer.py        # Statistiche e analisi (media, top, confronto store)
│   └── chart.py           # Generazione grafici con matplotlib
├── charts/                # Cartella per i grafici generati (auto-creata)
├── exports/               # Cartella per i file esportati (auto-creata)
│   ├── csv/               # File CSV esportati
│   ├── json/              # File JSON esportati
│   └── xlsx/              # File Excel esportati
├── wishlist.json          # File wishlist (auto-creato)
├── app.py                 # Entrypoint principale con menu interattivo
├── requirements.txt       # Dipendenze Python
└── README.md             # Questo file
```

## 📊 File Generati

Il programma genera automaticamente:

- `exports/csv/deals.csv` - Tutte le offerte in formato CSV
- `exports/json/deals.json` - Esportazione in formato JSON (opzionale)
- `exports/xlsx/deals.xlsx` - Esportazione in formato Excel (opzionale)
- `charts/savings_trend.png` - Grafico top 20 offerte per risparmio (con thumbnail)
- `charts/store_comparison.png` - Confronto tra store (risparmio medio e numero offerte)
- `charts/game_prices_[nome].png` - Confronto prezzi per gioco specifico (con cover)
- `wishlist.json` - Lista dei giochi da monitorare con prezzi target

## 🎯 Caratteristiche Tecniche

- ✅ **Codice modulare**: struttura pulita e organizzata per principianti
- ✅ **Sintassi semplice**: codice leggibile senza costrutti avanzati
- ✅ **Output formattato**: interfaccia chiara con emoji e separatori
- ✅ **Grafici professionali**: visualizzazioni con matplotlib e thumbnail
- ✅ **Gestione errori**: gestione completa di errori e interruzioni
- ✅ **API pubblica**: utilizza CheapShark API gratuita e legale

## 📦 Dipendenze

- `requests` - Per le chiamate API
- `pandas` - Per la gestione e analisi dei dati
- `matplotlib` - Per la generazione dei grafici
- `Pillow` - Per il caricamento delle immagini
- `openpyxl` - Per l'export in formato Excel

## 📝 Esempio di Utilizzo

```python
# Analisi completa offerte
python app.py
# Scegli opzione 1

# Ricerca gioco specifico e aggiunta alla wishlist
python app.py
# Scegli opzione 2
# Inserisci nome gioco (es: "Red Dead Redemption")
# Visualizza dettagli e aggiungi alla wishlist con prezzo target

# Filtri avanzati
python app.py
# Scegli opzione 3
# Filtra per prezzo, sconto, store

# Verifica alert prezzi
python app.py
# Scegli opzione 5 per vedere se i giochi hanno raggiunto il prezzo target
```

## 🔧 Sviluppo

Il progetto è strutturato per essere facilmente estendibile:

- Aggiungi nuove funzioni di analisi in `analytics/analyzer.py`
- Crea nuovi grafici in `analytics/chart.py`
- Estendi le funzionalità API in `data/fetcher.py`

## 📄 Licenza

Questo progetto è rilasciato sotto licenza MIT. Vedi il file `LICENSE` per i dettagli.

## 🙏 Ringraziamenti

- [CheapShark](https://www.cheapshark.com/) per l'API pubblica gratuita
- Tutti i contributori che hanno migliorato questo progetto

## 📞 Contatti

Per domande, suggerimenti o problemi, apri una [Issue](https://github.com/biagio-scaglia/game-price-tracker/issues) su GitHub.

---

⭐ Se questo progetto ti è utile, considera di lasciare una stella su GitHub!
