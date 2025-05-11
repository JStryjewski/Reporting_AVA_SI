# data.py
import pandas as pd
import json
from sqlalchemy import create_engine
import urllib

def get_data(table, column_str, condition, agg_list, agg_by_dict):
    table_tmp = table[table[column_str]==condition].groupby(agg_list[0]).agg(agg_by_dict)
    sorter = ['TOP_100','TOP_500','TOP_1000','TOP_2000','> TOP_2000']
    table_tmp = table_tmp.reindex(sorter)
    table_tmp[table_tmp.columns[1]] = table_tmp[table_tmp.columns[1]] - table_tmp[table_tmp.columns[0]]
    list1 = [list(pair) for pair in zip(table_tmp[table_tmp.columns[0]], table_tmp[table_tmp.columns[1]])]
    table_tmp = table[table[column_str]==condition].groupby(agg_list[1]).agg(agg_by_dict)
    sorter = ['A','B','C','']
    table_tmp = table_tmp.reindex(sorter)
    table_tmp[table_tmp.columns[1]] = table_tmp[table_tmp.columns[1]] - table_tmp[table_tmp.columns[0]]
    list2 = [list(pair) for pair in zip(table_tmp[table_tmp.columns[0]], table_tmp[table_tmp.columns[1]])]
    list1.extend(list2)
    return list1

def get_data_klasyfikacja(table):
    table['Data'] = table['Data'].dt.strftime('%Y-%m-%d')

    # Convert to a format suitable for Chart.js
    klasyfikacja_json = {
        "labels": table['Data'].tolist(),  # X-axis (dates)
        "datasets": [
            {
                "label": "A",
                "data": table['A'].tolist(),
                "borderColor": "rgba(0, 100, 0, 1)",
                "fill": False
            },
            {
                "label": "B",
                "data": table['B'].tolist(),
                "borderColor": "rgba(34, 139, 34, 1)",
                "fill": False
            },
            {
                "label": "C",
                "data": table['C'].tolist(),
                "borderColor": "rgba(50, 205, 50, 1)",
                "fill": False
            },
            {
                "label": "Niesklasyfikowane",
                "data": table['Niesklasyfikowane'].tolist(),
                "borderColor": "rgba(144, 238, 144, 1)",
                "fill": False
            }
        ]
    }

    klasyfikacja_data = json.dumps(klasyfikacja_json)
    return klasyfikacja_data

def get_data_statusy(table):
    table['Data'] = table['Data'].dt.strftime('%Y-%m-%d')

    statusy_json = {
        "labels": table['Data'].tolist(),  # X-axis (dates)
        "datasets": [
            {
                "label": "AKTYWNE",
                "data": table['AKTYWNE'].tolist(),
                "borderColor": "rgba(0, 100, 0, 1)",
                "fill": False
            },
            {
                "label": "NIEAKTYWNE",
                "data": table['NIEAKTYWNE'].tolist(),
                "borderColor": "rgba(34, 139, 34, 1)",
                "fill": False
            },
            {
                "label": "NOWOŚĆ",
                "data": table['NOWOŚĆ'].tolist(),
                "borderColor": "rgba(50, 205, 50, 1)",
                "fill": False
            }
        ]
    }
    
    statusy_data = json.dumps(statusy_json)
    return statusy_data

def get_data_zejscie(table):
    table['Data'] = table['Data'].dt.strftime('%Y-%m-%d')

    zejscie_json = {
        "labels": table['Data'].tolist(),
        "datasets": [
            {
                "label": "0-7",
                "data": table['0-7'].tolist(),
                "borderColor": "rgba(0, 100, 0, 1)",
                "fill": False
            },
            {
                "label": "7-14",
                "data": table['7-14'].tolist(),
                "borderColor": "rgba(34, 139, 34, 1)",
                "fill": False
            },
            {
                "label": "14-21",
                "data": table['14-21'].tolist(),
                "borderColor": "rgba(50, 205, 50, 1)",
                "fill": False
            },
            {
                "label": ">21",
                "data": table['>21'].tolist(),
                "borderColor": "rgba(144, 238, 144, 1)",
                "fill": False
            },
            {
                "label": "Brak sprzedaży",
                "data": table['Brak sprzedaży'].tolist(),
                "borderColor": "rgba(200, 255, 200, 1)",
                "fill": False
            }
        ]
    }

    zejscie_data = json.dumps(zejscie_json)
    return zejscie_data

def get_data_superkat(table):
    table = table.sort_values('super_kategoria')

    superkat_json = {
        "labels": table['super_kategoria'].tolist(),
        "datasets": [
            {
                "label": "Dostępność",
                "data": table['Dostępność'].tolist(),
                "borderColor": "rgba(126, 186, 0, 1)",
                "backgroundColor": "rgba(126, 186, 0, 1)",
                "fill": True
            }
        ]
    }

    superkat_data = json.dumps(superkat_json)
    return superkat_data

def get_data_ranking(table):
    table = table.copy()
    table['label'] = table[['RANKING', 'CENTYL']].agg(' - '.join, axis=1)
    table.set_index('label', inplace=True)
    table = table.reindex(['TOP_100 - 5%','TOP_100 - 10%','TOP_100 - 20%','TOP_100 - 50%','TOP_100 - 100%','TOP_100 - Brak sprzedaży','TOP_500 - 5%','TOP_500 - 10%','TOP_500 - 20%','TOP_500 - 50%','TOP_500 - 100%','TOP_500 - Brak sprzedaży','TOP_1000 - 5%','TOP_1000 - 10%','TOP_1000 - 20%','TOP_1000 - 50%','TOP_1000 - 100%','TOP_1000 - Brak sprzedaży','TOP_2000 - 5%','TOP_2000 - 10%','TOP_2000 - 20%','TOP_2000 - 50%','TOP_2000 - 100%','TOP_2000 - Brak sprzedaży','> TOP_2000 - 5%','> TOP_2000 - 10%','> TOP_2000 - 20%','> TOP_2000 - 50%','> TOP_2000 - 100%','> TOP_2000 - Brak sprzedaży'])
    table = table.dropna()
    table.reset_index(inplace=True)

    ranking_json = {
        "labels": table['label'].tolist(),
        "datasets": [
            {
                "label": "Ranking",
                "data": table['Dostępność'].tolist(),
                "borderColor": "rgba(126, 186, 0, 1)",
                "backgroundColor": "rgba(126, 186, 0, 1)",
                "borderWidth": 1
            }
        ]
    }

    ranking_data = json.dumps(ranking_json)
    return ranking_data

def get_data_table_ava(table):
    table = table.copy()
    table['suma_si_ilosc_30'] = pd.to_numeric(table['suma_si_ilosc_30'], errors='coerce').fillna(0)
    table['dostepnosc'] = pd.to_numeric(table['dostepnosc'], errors='coerce').fillna(0)
    table['schodzenie'] = pd.to_numeric(table['schodzenie'], errors='coerce').fillna(0)
    table['Niedostepny'] = pd.to_numeric(table['Niedostepny'], errors='coerce').fillna(0)

    table = {
        "datasets": [
            {
                "label": "Status zamówień",
                "data": table['StatusZam'].tolist()
            },
            {
                "label": "Symkar",
                "data": table['SymKar'].tolist()
            },
            {
                "label": "Sprzedaz 30 dni",
                "data": table['suma_si_ilosc_30'].round(2).tolist()
            },
            {
                "label": "Dostępność",
                "data": (table['dostepnosc'] * 100).round(2).tolist()
            },
            {
                "label": "Schodzenie 1 szt. w dniach",
                "data": table['schodzenie'].round(2).tolist()
            },
            {
                "label": "Ile dni niedostepny",
                "data": table['Niedostepny'].tolist()
            },
            {
                "label": "wskaźnik OOS",
                "data": ((1-table['dostepnosc']) * 100).round(2).tolist()
            }
        ],
        "labels": table['SymKar'].index.tolist()
    }
    return table

def compute_availability(df, group_cols, agg_by_dict):
    """Compute availability for given grouped DataFrame."""
    availability_df = df.groupby(group_cols).agg(agg_by_dict)
    availability_df['availability'] = availability_df['Dostepny'] / availability_df['CNT']
    availability_df.drop(columns=['Dostepny', 'CNT'], inplace=True)
    return pd.pivot(availability_df.reset_index(), values='availability', columns=group_cols[-1], index='Data').reset_index()


def get_all_data(source='sql'):
    if source == 'sql':
        # SQL connection string and queries
        conn_str = (
            r'Driver={ODBC Driver 17 for SQL Server};'
            r'Server=hd;'
            r'Database=CF;'
            r'Trusted_Connection=yes;'
        )

        conn_str_encoded = urllib.parse.quote_plus(conn_str)
        engine = create_engine(f'mssql+pyodbc:///?odbc_connect={conn_str_encoded}')

        sql_filename = "ecom_query.sql"
        df_sql_query_group = """   
            select * from cf.dbo.ecom_ava_group 
        """

        df_sql_query_daily = """   
            select * from cf.dbo.ecom_ava_daily 
        """

        df_sql_query_monthly = """   
            select * from ecom_ava_monthly 
        """

        # Execute custom SQL file if needed
        with open(sql_filename, encoding='UTF-8') as f:
            query = f.read()

        with engine.connect() as connection:
            connection.execute(query)

        # Load data from SQL queries
        df_group = pd.read_sql(df_sql_query_group.replace('\n', ""), engine)
        df_daily = pd.read_sql(df_sql_query_daily.replace('\n', ""), engine)
        df_monthly = pd.read_sql(df_sql_query_monthly.replace('\n', ""), engine)
    
    elif source == 'file':
        # Load data from local Excel files
        df_group = pd.read_excel('df_group.xlsx')
        df_daily = pd.read_excel('df_daily.xlsx')
        df_monthly = pd.read_excel('df_monthly.xlsx')

    else:
        raise ValueError("Source must be 'sql' or 'file'")

    # Clean up the data
    for col in df_group.select_dtypes(include=['object']).columns:
        df_group[col].fillna("", inplace=True)

    for col in df_daily.select_dtypes(include=['object']).columns:
        df_daily[col].fillna("", inplace=True)

    for col in df_monthly.select_dtypes(include=['object']).columns:
        df_monthly[col].fillna("", inplace=True)

    agg_by_dict = {'Dostepny':'sum','CNT':'sum'}

    # Get active, non-active, and new data
    statuses = ['AKTYWNE', 'NIEAKTYWNE', 'NOWOŚĆ']
    data_frames = {status: get_data(df_daily, 'StatusZam', status, ['RANKING', 'ABC_class'], agg_by_dict) for status in statuses}
    all_index = [[a + b + c for a, b, c in zip(sublist1, sublist2, sublist3)] for sublist1, sublist2, sublist3 in zip(*data_frames.values())]
    data_frames.update({'WSZYSTKO': all_index})

    # Fill NA values in ABC_class
    df_monthly['ABC_class'].fillna('Niesklasyfikowane', inplace=True)

    # Classification DataFrame
    klasyfikacja = compute_availability(df_monthly, ['Data', 'ABC_class'], agg_by_dict)
    klasyfikacja = get_data_klasyfikacja(klasyfikacja)

    # Statuses DataFrame
    statusy = compute_availability(df_monthly, ['Data', 'StatusZam'], agg_by_dict)
    statusy = get_data_statusy(statusy)

    # Zejscie DataFrame
    zejscie = compute_availability(df_monthly, ['Data', 'schodzenie'], agg_by_dict)
    zejscie = get_data_zejscie(zejscie)

    # Superkat DataFrame
    superkat = df_daily.groupby(['StatusZam', 'super_kategoria']).agg(agg_by_dict)
    superkat_tot = df_daily.groupby(['super_kategoria']).agg(agg_by_dict).reset_index()
    superkat_tot['StatusZam'] = 'WSZYSTKO'
    superkat_tot.set_index(['StatusZam', 'super_kategoria'], inplace=True)
    superkat = pd.concat([superkat, superkat_tot])
    superkat['Dostępność'] = superkat['Dostepny'] / superkat['CNT']
    superkat.drop(columns=['Dostepny', 'CNT'], inplace=True)
    superkat.reset_index(inplace=True)

    # Get super category data
    superkat_data = {status: get_data_superkat(superkat[superkat['StatusZam'] == status]) for status in statuses + ['WSZYSTKO']}

    # Ranking DataFrame
    ranking = df_daily.groupby(['StatusZam', 'RANKING', 'CENTYL']).agg(agg_by_dict)
    ranking_tot = df_daily.groupby(['RANKING', 'CENTYL']).agg(agg_by_dict).reset_index()
    ranking_tot['StatusZam'] = 'WSZYSTKO'
    ranking_tot.set_index(['StatusZam', 'RANKING', 'CENTYL'], inplace=True)
    ranking = pd.concat([ranking, ranking_tot])
    ranking['Dostępność'] = ranking['Dostepny'] / ranking['CNT']
    ranking.drop(columns=['Dostepny', 'CNT'], inplace=True)
    ranking.reset_index(inplace=True)
    ranking['CENTYL'] = ranking['CENTYL'].replace(r'^\s*$', 'Brak sprzedaży', regex=True)

    # Get ranking data
    ranking_data = {status: get_data_ranking(ranking[ranking['StatusZam'] == status]) for status in statuses + ['WSZYSTKO']}

    df_group.sort_values('suma_si_ilosc_30', ascending=False, inplace=True)
    df_group=df_group[:1000]
    df_group_tot = df_group.copy()
    df_group_tot['StatusZamowien'] = 'WSZYSTKO'
    df_group['StatusZamowien'] = df_group['StatusZam']
    df_group = pd.concat([df_group,df_group_tot])
    tabela = {status: get_data_table_ava(df_group[df_group['StatusZamowien'] == status]) for status in statuses + ['WSZYSTKO']}

    return [data_frames,klasyfikacja,statusy,zejscie,superkat_data,ranking_data,tabela]
