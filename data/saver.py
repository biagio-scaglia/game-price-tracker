import pandas as pd
import json
import os

# Cartelle per i vari formati
EXPORTS_BASE = "exports"
CSV_DIR = os.path.join(EXPORTS_BASE, "csv")
JSON_DIR = os.path.join(EXPORTS_BASE, "json")
XLSX_DIR = os.path.join(EXPORTS_BASE, "xlsx")

def ensure_export_dirs():
    """Crea le cartelle per i vari formati se non esistono"""
    os.makedirs(CSV_DIR, exist_ok=True)
    os.makedirs(JSON_DIR, exist_ok=True)
    os.makedirs(XLSX_DIR, exist_ok=True)

def save_csv(df, path):
    """Salva DataFrame in formato CSV"""
    if df.empty:
        return False
    ensure_export_dirs()
    df.to_csv(path, index=False)
    return True

def save_json(df, path):
    """Salva DataFrame in formato JSON"""
    if df.empty:
        return False
    ensure_export_dirs()
    df.to_json(path, orient='records', indent=2, force_ascii=False)
    return True

def save_excel(df, path):
    """Salva DataFrame in formato Excel"""
    if df.empty:
        return False
    ensure_export_dirs()
    try:
        df.to_excel(path, index=False, engine='openpyxl')
        return True
    except ImportError:
        return False

def save_data(df, filename, format='csv'):
    """
    Salva DataFrame nel formato specificato nella cartella appropriata
    
    Args:
        df: DataFrame da salvare
        filename: Nome del file (senza estensione e senza percorso)
        format: Formato ('csv', 'json', 'excel')
    
    Returns:
        Percorso completo del file salvato, o None se errore
    """
    ensure_export_dirs()
    
    # Rimuovi estensione se presente e path se presente
    filename = os.path.basename(filename)
    if filename.endswith(('.csv', '.json', '.xlsx')):
        filename = os.path.splitext(filename)[0]
    
    if format.lower() == 'csv':
        full_path = os.path.join(CSV_DIR, f"{filename}.csv")
        if save_csv(df, full_path):
            return full_path
    elif format.lower() == 'json':
        full_path = os.path.join(JSON_DIR, f"{filename}.json")
        if save_json(df, full_path):
            return full_path
    elif format.lower() in ['excel', 'xlsx']:
        full_path = os.path.join(XLSX_DIR, f"{filename}.xlsx")
        if save_excel(df, full_path):
            return full_path
    
    return None
