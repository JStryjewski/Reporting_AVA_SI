# data.py
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
