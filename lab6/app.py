import pandas as pd

# WCZYTANIE I PRZYGOTOWANIE DANYCH
try:
    print("Wczytywanie i przygotowanie danych...")
    df1 = pd.read_csv('Online_Retail.csv', encoding='ISO-8859-1', on_bad_lines='skip', low_memory=False)
    df2 = pd.read_csv('online_retail_II.csv', encoding='ISO-8859-1', on_bad_lines='skip', low_memory=False)
    df = pd.concat([df1, df2])
    
    # Czyszczenie
    df = df.dropna(subset=['CustomerID'])
    df = df[df['Quantity'] > 0]
    
    # Zgodnie z wytycznymi Lab 6, używamy nazwy 'Revenue'
    df['Revenue'] = df['Quantity'] * df['UnitPrice']
    
    # Przygotowanie wymiaru czasu
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df['Month'] = df['InvoiceDate'].dt.month
    
    print("Dane gotowe!\n")
    print("-" * 40)

    # ZADANIE 1: Tabela pivot
    # Utworzenie tabeli pivot (wiersze: Country, kolumny: Month, wartości: suma Revenue)
    pivot = df.pivot_table(
        values='Revenue',
        index='Country',
        columns='Month',
        aggfunc='sum'
    )
    print("--- ZADANIE 1: Tabela pivot (fragment) ---")
    print(pivot.head())
    
    # Sprawdzenie, które miesiące mają najwyższą sprzedaż
    mies_sprzedaz = df.groupby('Month')['Revenue'].sum().sort_values(ascending=False)
    print("\nMiesiące z najwyższą sprzedażą:")
    print(mies_sprzedaz.head())

    # ZADANIE 2: Ranking krajów
    # Obliczenie całkowitego przychodu, sortowanie malejąco i wyświetlenie TOP 10
    ranking = df.groupby('Country')['Revenue'].sum().sort_values(ascending=False)
    top10 = ranking.head(10)
    print("\n--- ZADANIE 2: TOP 10 krajów ---")
    print(top10)

    # ZADANIE 3: Analiza klientów
    # Przychód dla każdego klienta, TOP 10 klientów i średni przychód
    customers = df.groupby('CustomerID')['Revenue'].sum()
    top_customers = customers.sort_values(ascending=False).head(10)
    avg_revenue = customers.mean()
    
    print("\n--- ZADANIE 3: Analiza klientów ---")
    print(f"TOP 10 klientów:\n{top_customers}")
    print(f"\nŚredni przychód na klienta: {avg_revenue:.2f}")

    # ZADANIE 4: Segmentacja krajów
    # Podział na 3 grupy za pomocą funkcji pd.qcut (kwantyle)
    etykiety = ['Dolne 25%', 'Środkowe 50%', 'Top 25%']
    # Ustalamy granice przedziałów: 0% -> 25% -> 75% -> 100%
    segmenty = pd.qcut(ranking, q=[0, 0.25, 0.75, 1.0], labels=etykiety)
    
    # Łączymy wyniki w czytelną tabelę DataFrame
    wynik_segmentacji = pd.DataFrame({'Revenue': ranking, 'Segment': segmenty})
    
    print("\n--- ZADANIE 4: Segmentacja krajów (Top 10 z przypisanym segmentem) ---")
    print(wynik_segmentacji.head(10))

except FileNotFoundError:
    print("Błąd: Nie znaleziono plików CSV. Upewnij się, że są w folderze.")
except Exception as e:
    print(f"Wystąpił błąd: {e}")