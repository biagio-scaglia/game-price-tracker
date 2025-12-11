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
- 💾 **Export dati**: salvataggio automatico in CSV per analisi successive
- 🎯 **Statistiche dettagliate**: risparmi medi, top offerte, analisi per fascia di sconto

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
3. **❌ Esci**: esce dal programma

## 📁 Struttura Progetto

```
game-price-tracker/
├── data/                  # Moduli per fetch, parsing e salvataggio
│   ├── fetcher.py         # Funzioni API (get_deals, search_games, etc.)
│   ├── parser.py          # Conversione dati JSON in DataFrame pandas
│   └── saver.py           # Salvataggio dati in CSV
├── analytics/             # Moduli per analisi e visualizzazione
│   ├── analyzer.py        # Statistiche e analisi (media, top, confronto store)
│   └── chart.py           # Generazione grafici con matplotlib
├── charts/                # Cartella per i grafici generati (auto-creata)
├── exports/               # Cartella per i file CSV esportati (auto-creata)
├── app.py                 # Entrypoint principale con menu interattivo
├── requirements.txt       # Dipendenze Python
└── README.md             # Questo file
```

## 📊 File Generati

Il programma genera automaticamente:

- `exports/deals.csv` - Tutte le offerte in formato CSV
- `charts/savings_trend.png` - Grafico top 20 offerte per risparmio (con thumbnail)
- `charts/store_comparison.png` - Confronto tra store (risparmio medio e numero offerte)
- `charts/game_prices_[nome].png` - Confronto prezzi per gioco specifico (con cover)

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

## 📝 Esempio di Utilizzo

```python
# Analisi completa offerte
python app.py
# Scegli opzione 1

# Ricerca gioco specifico
python app.py
# Scegli opzione 2
# Inserisci nome gioco (es: "Red Dead Redemption")
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
