import pandas as pd
import time
import numpy as np

# 1: ANALIZA  I WCZYTANIE DANYCH 
print("1: ANALIZA I WCZYTANIE DANYCH")
start_load = time.time()

# Wczytanie danych z kodowaniem ISO-8859-1
try:
    df = pd.read_csv('Online_Retail.csv', encoding='ISO-8859-1')
    end_load = time.time()
    print(f"Czas wczytywania danych: {end_load - start_load:.4f} s")
except FileNotFoundError:
    print("Błąd: Nie znaleziono pliku Online_Retail.csv")
    exit()

# Wyświetlenie podstawowych informacji
print(f"Liczba rekordów: {len(df)}")
print("\nLiczba brakujących wartości:")
print(df.isnull().sum())
print("\nTypy danych kolumn przed optymalizacją:")
print(df.dtypes)

# Pomiar zajętości pamięci
mem_before = df.memory_usage(deep=True).sum()
print(f"\nZużycie pamięci przed optymalizacją: {mem_before / 1024**2:.2f} MB")


# 2: OPTYMALIZACJA PAMIĘCI
print("\n2: OPTYMALIZACJA PAMIĘCI")
df_opt = df.copy()

# 1. Zmiana kolumn tekstowych na typ category (np. Country, StockCode)
# Typ category jest znacznie wydajniejszy dla danych o dużej liczbie powtórzeń
cols_to_category = ['Country', 'StockCode']
for col in cols_to_category:
    df_opt[col] = df_opt[col].astype('category')

# 2. Zmniejszenie rozmiaru typów liczbowych (downcasting)
# Quantity: int64 -> int16/int32
df_opt['Quantity'] = pd.to_numeric(df_opt['Quantity'], downcast='integer')

# UnitPrice: float64 -> float32
df_opt['UnitPrice'] = pd.to_numeric(df_opt['UnitPrice'], downcast='float')

# Pomiar zajętości pamięci po zmianach
mem_after = df_opt.memory_usage(deep=True).sum()
print(f"Zużycie pamięci po optymalizacji: {mem_after / 1024**2:.2f} MB")
print(f"Zaoszczędzono: {100 * (1 - mem_after/mem_before):.2f}% pamięci")


# 3: ANALIZA WYDAJNOŚCI OPERACJI
print("\n3: ANALIZA WYDAJNOŚCI OPERACJI")

def run_benchmarks(data, label):
    print(f"\n>>> Testy dla: {label}")
    
    # Operacja 1: Grupowanie - suma sprzedaży według kraju
    start = time.time()
    # observed=False zapobiega ostrzeżeniom przy typie category
    res_group = data.groupby('Country', observed=False)['Quantity'].sum()
    print(f"Czas grupowania (Country): {time.time() - start:.6f} s")
    
    # Operacja 2: Sortowanie - TOP 10 zakupów pod względem ilości
    start = time.time()
    res_sort = data.sort_values(by='Quantity', ascending=False).head(10)
    print(f"Czas sortowania (TOP 10):  {time.time() - start:.6f} s")
    
    # Operacja 3: Filtrowanie - sprzedaż w Wielkiej Brytanii
    start = time.time()
    res_filter = data[data['Country'] == 'United Kingdom']
    print(f"Czas filtrowania (UK):     {time.time() - start:.6f} s")

# Pomiary przed optymalizacją
run_benchmarks(df, "DANE PRZED OPTYMALIZACJĄ")

# Pomiary po optymalizacji
run_benchmarks(df_opt, "DANE PO OPTYMALIZACJI")


# 4: WNIOSKI: Na podstawie dzisiejszego laboratorium należy wziąć pod uwagę kilka kluczowych wniosków. Po pierwsze zmiana typów obiektowych (string) na 'category' drastycznie redukuje zużycie RAM.
#Następnym jest to, iż operacje grupowe i filtrowanie na kategoriach są zazwyczaj szybsze niż na tekstach. Następnie downcasting typów numerycznych pozwala na szybsze ładowanie danych do cache procesora.
#Samo zadanie było bardzo edukujące i pomogło mi w zrozumieniu jak bardzo ważna jest optymalizacja zbiorów danych i jaki impakt ma na wydajność przy pracy na nich.