# main.py
import json
import pandas as pd

from datetime import datetime
from jinja2 import Template
from data import (
    get_data_aktywne,
    get_data_nieaktywne,
    get_data_nowosci,
    get_data_wszystko
)
from template import html_template

def format_date():
    date = datetime(2024, 9, 12)  # Set a static date
    options = { 'weekday': 'long' }
    year = date.year
    month = str(date.month).zfill(2)
    day = str(date.day).zfill(2)
    weekday = date.strftime('%A')

    # Translate the weekday to Polish
    polish_weekdays = {
        'Monday': 'Poniedziałek',
        'Tuesday': 'Wtorek',
        'Wednesday': 'Środa',
        'Thursday': 'Czwartek',
        'Friday': 'Piątek',
        'Saturday': 'Sobota',
        'Sunday': 'Niedziela'
    }
    
    weekday_pl = polish_weekdays[weekday]
    return f"{year}-{month}-{day} ({weekday_pl})"

def main():
    formatted_date = format_date()
    data_aktywne = get_data_aktywne()
    data_nieaktywne = get_data_nieaktywne()
    data_nowosci = get_data_nowosci()
    data_wszystko = get_data_wszystko()


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

    # Save the data to JSON
    klasyfikacja_data = json.dumps(klasyfikacja_json)

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

    # Rendering the template with data
    template = Template(html_template)
    html_output = template.render(
        data_aktywne=data_aktywne,
        data_nieaktywne=data_nieaktywne,
        data_nowosci=data_nowosci,
        data_wszystko=data_wszystko,
        formatted_date=formatted_date,  # Pass the static date to the template
        klasyfikacja_data=klasyfikacja_data,
        statusy_data=statusy_data,
        zejscie_data=zejscie_data,
        superkat_data=superkat_data,
        ranking_data=ranking_data,
        table_ava=table_ava
    )

    # Save the HTML output to a file with UTF-8 encoding
    with open('report_availability.html', 'w', encoding='utf-8') as f:
        f.write(html_output)

    print("HTML file with filters has been generated.")

if __name__ == '__main__':
    main()
