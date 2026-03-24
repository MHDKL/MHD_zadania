import pandas as pd

#ZADANIE 1: Wczytanie danych
url = "https://raw.githubusercontent.com/guipsamora/pandas_exercises/master/07_Visualization/Online_Retail/Online_Retail.csv"

# Wczytanie danych z odpowiednim kodowaniem
df = pd.read_csv(url, encoding="ISO-8859-1")

print("ZADANIE 1")
print(f"Liczba rekordów: {len(df)}")
print(f"Liczba kolumn: {len(df.columns)}")
print("\n5 przykładowych wierszy:")
print(df.head())

#ZADANIE 2 i 3 Identyfikacja encji i Model 3NF

# 1. Encja Produkt (Product)
# Wyciągamy unikalne kody produktów wraz z ich opisami
products = df[['StockCode', 'Description']].drop_duplicates(subset=['StockCode'], keep='first')

# 2. Encja Klient (Customer) wraz z Krajem (Country)
# W modelu 3NF Country może być osobną tabelą, ale tutaj przypisujemy go do klienta
customers = df[['CustomerID', 'Country']].dropna(subset=['CustomerID']).drop_duplicates(subset=['CustomerID'])

# 3. Encja Faktura (Invoice) - Nagłówki
# Zawiera informacje o dacie i przypisanym kliencie
invoices = df[['InvoiceNo', 'InvoiceDate', 'CustomerID']].drop_duplicates(subset=['InvoiceNo'])

# 4. Encja Pozycje Faktury (Invoice Items / Sales)
# Tabela łącząca produkty z fakturami (rozbicie relacji wiele-do-wielu)
invoice_items = df[['InvoiceNo', 'StockCode', 'Quantity', 'UnitPrice']]

print("\n ZADANIE 3: Statystyki tabel 3NF")
print(f"Liczba produktów: {len(products)}")
print(f"Liczba klientów: {len(customers)}")
print(f"Liczba faktur: {len(invoices)}")
print(f"Liczba pozycji w fakturach: {len(invoice_items)}")