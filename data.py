# data.py
import pandas as pd
import json

def get_data_aktywne():
    return [
        [90, 10],  # Top 100 SKU (Aktywne)
        [85, 15],  # Top 500 SKU (Aktywne)
        [70, 30],  # Top 1000 SKU (Aktywne)
        [80, 20],  # Top 2000 SKU (Aktywne)
        [75, 25],  # >Top 2000 SKU (Aktywne)
        [40, 60],  # A (Aktywne)
        [30, 70],  # B (Aktywne)
        [20, 80],  # C (Aktywne)
        [10, 90]   # Niesklasyfikowane (Aktywne)
    ]

def get_data_nieaktywne():
    return [
        [30, 70],  # Top 100 SKU (Nieaktywne)
        [40, 60],  # Top 500 SKU (Nieaktywne)
        [80, 20],  # Top 1000 SKU (Nieaktywne)
        [45, 55],  # Top 2000 SKU (Nieaktywne)
        [50, 50],  # >Top 2000 SKU (Nieaktywne)
        [30, 70],  # A (Nieaktywne)
        [40, 60],  # B (Nieaktywne)
        [80, 20],  # C (Nieaktywne)
        [45, 55]   # Niesklasyfikowane (Nieaktywne)
    ]

def get_data_nowosci():
    return [
        [95, 5],   # Top 100 SKU (Nowości)
        [90, 10],  # Top 500 SKU (Nowości)
        [20, 80],  # Top 1000 SKU (Nowości)
        [85, 15],  # Top 2000 SKU (Nowości)
        [80, 20],  # >Top 2000 SKU (Nowości)
        [95, 56],  # A (Nowości)
        [90, 10],  # B (Nowości)
        [20, 80],  # C (Nowości)
        [85, 15]   # Niesklasyfikowane (Nowości)
    ]

def get_data_wszystko():
    return [
        [80, 20],  # Top 100 SKU (Wszystko)
        [75, 25],  # Top 500 SKU (Wszystko)
        [90, 10],  # Top 1000 SKU (Wszystko)
        [65, 35],  # Top 2000 SKU (Wszystko)
        [50, 50],  # >Top 2000 SKU (Wszystko)
        [80, 20],  # A (Wszystko)
        [75, 25],  # B (Wszystko)
        [90, 10],  # C (Wszystko)
        [65, 35]   # Niesklasyfikowane (Wszystko)
    ]

def get_data_klasyfikacja():
    klasyfikacja = pd.read_excel(r"C:\Users\Jacek\Documents\Python\misc\klasyfikacja.xlsx")
    klasyfikacja['Data'] = klasyfikacja['Data'].dt.strftime('%Y-%m-%d')

    # Convert to a format suitable for Chart.js
    klasyfikacja_json = {
        "labels": klasyfikacja['Data'].tolist(),  # X-axis (dates)
        "datasets": [
            {
                "label": "A",
                "data": klasyfikacja['A'].tolist(),
                "borderColor": "rgba(0, 100, 0, 1)",
                "fill": False
            },
            {
                "label": "B",
                "data": klasyfikacja['B'].tolist(),
                "borderColor": "rgba(34, 139, 34, 1)",
                "fill": False
            },
            {
                "label": "C",
                "data": klasyfikacja['C'].tolist(),
                "borderColor": "rgba(50, 205, 50, 1)",
                "fill": False
            },
            {
                "label": "Niesklasyfikowane",
                "data": klasyfikacja['Niesklasyfikowane'].tolist(),
                "borderColor": "rgba(144, 238, 144, 1)",
                "fill": False
            }
        ]
    }

    klasyfikacja_data = json.dumps(klasyfikacja_json)
    return klasyfikacja_data

def get_data_statusy():
    statusy = pd.read_excel(r"C:\Users\Jacek\Documents\Python\misc\statusy.xlsx")
    statusy['Data'] = statusy['Data'].dt.strftime('%Y-%m-%d')

    statusy_json = {
        "labels": statusy['Data'].tolist(),  # X-axis (dates)
        "datasets": [
            {
                "label": "AKTYWNE",
                "data": statusy['AKTYWNE'].tolist(),
                "borderColor": "rgba(0, 100, 0, 1)",
                "fill": False
            },
            {
                "label": "NIEAKTYWNE",
                "data": statusy['NIEAKTYWNE'].tolist(),
                "borderColor": "rgba(34, 139, 34, 1)",
                "fill": False
            },
            {
                "label": "NOWOSC",
                "data": statusy['NOWOSC'].tolist(),
                "borderColor": "rgba(50, 205, 50, 1)",
                "fill": False
            }
        ]
    }
    
    statusy_data = json.dumps(statusy_json)
    return statusy_data

def get_data_zejscie():
    zejscie = pd.read_excel(r"C:\Users\Jacek\Documents\Python\misc\zejscie.xlsx")
    zejscie['Data'] = zejscie['Data'].dt.strftime('%Y-%m-%d')

    # Convert to a format suitable for Chart.js
    zejscie_json = {
        "labels": zejscie['Data'].tolist(),  # X-axis (dates)
        "datasets": [
            {
                "label": "0-7",
                "data": zejscie['0-7'].tolist(),
                "borderColor": "rgba(0, 100, 0, 1)",
                "fill": False
            },
            {
                "label": "7-14",
                "data": zejscie['7-14'].tolist(),
                "borderColor": "rgba(34, 139, 34, 1)",
                "fill": False
            },
            {
                "label": "14-21",
                "data": zejscie['14-21'].tolist(),
                "borderColor": "rgba(50, 205, 50, 1)",
                "fill": False
            },
            {
                "label": ">21",
                "data": zejscie['>21'].tolist(),
                "borderColor": "rgba(144, 238, 144, 1)",
                "fill": False
            },
            {
                "label": "Brak sprzedaży",
                "data": zejscie['Brak sprzedaży'].tolist(),
                "borderColor": "rgba(200, 255, 200, 1)",
                "fill": False
            }
        ]
    }

    # Save the data to JSON
    zejscie_data = json.dumps(zejscie_json)
    return zejscie_data

def get_data_superkat():
    superkat = pd.read_excel(r"C:\Users\Jacek\Documents\Python\misc\superkategorie.xlsx")
    superkat.sort_values('Superkategoria', inplace=True)

    # Convert to a format suitable for Chart.js
    superkat_json = {
        "labels": superkat['Superkategoria'].tolist(),  # X-axis (dates)
        "datasets": [
            {
                "label": "Dostępność",
                "data": superkat['Dostępność'].tolist(),
                "borderColor": "rgba(126, 186, 0, 1)",
                "backgroundColor": "rgba(126, 186, 0, 1)",
                "fill": True
            }
        ]
    }

    # Save the data to JSON
    superkat_data = json.dumps(superkat_json)
    return superkat_data

def get_data_ranking():
    ranking = pd.read_excel(r"C:\Users\Jacek\Documents\Python\misc\ranking.xlsx")
    ranking['label'] = ranking[['RANKING', 'CENTYL']].agg(' - '.join, axis=1)

    # Convert to a format suitable for Chart.js
    ranking_json = {
        "labels": ranking['label'].tolist(),  # X-axis (dates)
        "datasets": [
            {
                "label": "Ranking",
                "data": ranking['Dostępność'].tolist(),
                "borderColor": "rgba(126, 186, 0, 1)",
                "backgroundColor": "rgba(126, 186, 0, 1)",
                "borderWidth": 1
            }
        ]
    }

    # Save the data to JSON
    ranking_data = json.dumps(ranking_json)
    return ranking_data

def get_data_table_ava():
    table_ava = pd.read_excel(r"C:\Users\Jacek\Documents\Python\misc\tabela_dane.xlsx")
    table_ava = table_ava[:100]
    table_ava = {
        "datasets": [
            {
                "label": "DoZam",
                "data": table_ava['DoZam'].tolist()
            },
            {
                "label": "Symkar",
                "data": table_ava['Symkar'].tolist()
            },
            {
                "label": "Sprzedaz 30 dni",
                "data": table_ava['Sprzedaz 30 dni'].round(2).tolist()
            },
            {
                "label": "Dostępność",
                "data": (table_ava['Dostępność'] * 100).round(2).tolist()
            },
            {
                "label": "Schodzenie 1 szt. w dniach",
                "data": table_ava['Schodzenie 1 szt. w dniach'].round(2).tolist()
            },
            {
                "label": "Ile dni niedostepny",
                "data": table_ava['Ile dni niedostepny'].tolist()
            },
            {
                "label": "wskaźnik OOS",
                "data": (table_ava['wskaźnik OOS'] * 100).round(2).tolist()
            }
        ],
        "labels": table_ava['Symkar'].index.tolist()  # Add a list of indices or any other relevant labels
    }
    return table_ava