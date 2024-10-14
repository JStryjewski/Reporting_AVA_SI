# main.py
import json
import pandas as pd

from datetime import date
from jinja2 import Template
from data import (
    get_all_data
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
    dict_data = get_all_data(source='file')

    template = Template(html_template)
    html_output = template.render(
        data_aktywne=dict_data[0]['AKTYWNE'],
        data_nieaktywne=dict_data[0]['NIEAKTYWNE'],
        data_nowosci=dict_data[0]['NOWOŚĆ'],
        data_wszystko=dict_data[0]['WSZYSTKO'],
        formatted_date=formatted_date, 
        klasyfikacja_data=dict_data[1],
        statusy_data=dict_data[2],
        zejscie_data=dict_data[3],
        superkatakt_data=dict_data[4]['AKTYWNE'],
        superkatnie_data=dict_data[4]['NIEAKTYWNE'],
        superkatnow_data=dict_data[4]['NOWOŚĆ'],
        superkatwsz_data=dict_data[4]['WSZYSTKO'],
        rankingakt_data=dict_data[5]['AKTYWNE'],
        rankingnie_data=dict_data[5]['NIEAKTYWNE'],
        rankingnow_data=dict_data[5]['NOWOŚĆ'],
        rankingwsz_data=dict_data[5]['WSZYSTKO'],
        table_ava=dict_data[6]['WSZYSTKO'],  # Default data
        table_ava_aktywne=dict_data[6]['AKTYWNE'],  # New data for aktywne
        table_ava_nieaktywne=dict_data[6]['NIEAKTYWNE'],  # New data for nieaktywne
        table_ava_nowosci=dict_data[6]['NOWOŚĆ']  # New data for nowości
    )

    with open('report_availability.html', 'w', encoding='utf-8') as f:
        f.write(html_output)

    print("HTML file has been generated.")

if __name__ == '__main__':
    main()
