import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# SETUP I WCZYTANIE DANYCH
try:
    print("Wczytywanie danych... Może to chwilę potrwać ze względu na rozmiar plików.")
    df1 = pd.read_csv('Online_Retail.csv', encoding='ISO-8859-1', on_bad_lines='skip', low_memory=False)
    df2 = pd.read_csv('online_retail_II.csv', encoding='ISO-8859-1', on_bad_lines='skip', low_memory=False)
    
    # Połączenie obu zbiorów danych w jeden obiekt DataFrame
    df = pd.concat([df1, df2])
    print("Krok 1: Dane wczytane i połączone pomyślnie.")

    # CZYSZCZENIE DANYCH
    # Usunięcie rekordów bez identyfikatora klienta (CustomerID)
    df = df.dropna(subset=['CustomerID']) 
    # Usunięcie transakcji z ilością mniejszą lub równą zero (np. zwroty lub błędy)
    df = df[df['Quantity'] > 0] 
    # Obliczenie całkowitej wartości sprzedaży dla każdego wiersza (Fakt)
    df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
    print("Krok 2: Czyszczenie danych zakończone.")

    # CZAS JAKO WYMIAR OLAP
    # Konwersja kolumny na format daty i czasu
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    # Ekstrakcja roku i miesiąca (Wymiary czasu)
    df['Year'] = df['InvoiceDate'].dt.year
    df['Month'] = df['InvoiceDate'].dt.month
    print("Krok 3: Wymiary czasu przygotowane.")

    # --- 4. REALIZACJA ZADAŃ LABORATORYJNYCH ---

    # Zadanie 1: Top 10 krajów pod względem łącznej sprzedaży
    zadanie1 = df.groupby('Country')['TotalPrice'].sum().sort_values(ascending=False).head(10)
    print("\n--- Zadanie 1: Top 10 krajów ---")
    print(zadanie1)

    # Zadanie 2: Znalezienie miesiąca o największej sprzedaży w całym zbiorze
    zadanie2 = df.groupby('Month')['TotalPrice'].sum().idxmax()
    print(f"\n--- Zadanie 2: Miesiąc o największej sprzedaży to: {zadanie2} ---")

    # Zadanie 3: Budowa kostki danych (Pivot Table)
    # Wiersze: kraj, Kolumny: miesiąc, Wartości: suma sprzedaży
    kostka = pd.pivot_table(df, values='TotalPrice', index='Country', columns='Month', aggfunc='sum')
    print("\n--- Zadanie 3: Kostka danych (fragment) ---")
    print(kostka.head())

    # Zadanie 4: Dla każdego kraju znajdź rok z najwyższą sprzedażą
    sprzedaz_rok = df.groupby(['Country', 'Year'])['TotalPrice'].sum().reset_index()
    zadanie4 = sprzedaz_rok.loc[sprzedaz_rok.groupby('Country')['TotalPrice'].idxmax()]
    print("\n--- Zadanie 4: Najlepszy rok dla każdego kraju (fragment) ---")
    print(zadanie4.head())

    # Zadanie 5: Top 5 produktów pod względem sprzedaży w każdym kraju
    top_produkty = df.groupby(['Country', 'Description'])['TotalPrice'].sum().reset_index()
    zadanie5 = top_produkty.sort_values(['Country', 'TotalPrice'], ascending=[True, False]).groupby('Country').head(5)
    print("\n--- Zadanie 5: Top 5 produktów w każdym kraju (fragment) ---")
    print(zadanie5.head(10))

    # WIZUALIZACJA
    plt.figure(figsize=(14, 8))
    # Wyświetlamy mapę ciepła dla pierwszych 15 krajów, aby zachować czytelność
    sns.heatmap(kostka.fillna(0).head(15), cmap='YlGnBu', annot=False)
    plt.title('Analiza sprzedaży: Kraje vs Miesiące (Heatmap)')
    plt.ylabel('Kraj')
    plt.xlabel('Miesiąc')
    plt.show()

except FileNotFoundError:
    print("Błąd: Nie znaleziono plików .csv. Upewnij się, że są w tym samym folderze co skrypt.")
except Exception as e:
    print(f"Wystąpił błąd podczas przetwarzania: {e}")