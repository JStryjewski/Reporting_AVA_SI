# main.py
import json
import pandas as pd

from datetime import date
from jinja2 import Template
from data import (
    get_data_aktywne,
    get_data_nieaktywne,
    get_data_nowosci,
    get_data_wszystko,
    get_data_klasyfikacja,
    get_data_ranking,
    get_data_statusy,
    get_data_superkat,
    get_data_table_ava,
    get_data_zejscie
)
from template import html_template

def format_date():
    today = date.today()
    year = today.year
    month = str(today.month).zfill(2)
    day = str(today.day).zfill(2)
    weekday = today.strftime('%A')

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
    klasyfikacja_data = get_data_klasyfikacja()
    statusy_data = get_data_statusy()
    zejscie_data = get_data_zejscie()
    superkat_data = get_data_superkat()
    ranking_data = get_data_ranking()
    table_ava = get_data_table_ava()

    template = Template(html_template)
    html_output = template.render(
        data_aktywne=data_aktywne,
        data_nieaktywne=data_nieaktywne,
        data_nowosci=data_nowosci,
        data_wszystko=data_wszystko,
        formatted_date=formatted_date, 
        klasyfikacja_data=klasyfikacja_data,
        statusy_data=statusy_data,
        zejscie_data=zejscie_data,
        superkat_data=superkat_data,
        ranking_data=ranking_data,
        table_ava=table_ava
    )

    with open('report_availability.html', 'w', encoding='utf-8') as f:
        f.write(html_output)

    print("HTML file has been generated.")

if __name__ == '__main__':
    main()
