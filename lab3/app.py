import pandas as pd
import numpy as np

# Wczytanie danych
df = pd.read_csv("Online_Retail.csv", encoding='latin1')

print("Przykładowe dane:")
display(df.head())

print("\nInformacje o zbiorze:")
df.info()
# 1. Usunięcie wierszy bez CustomerID
df = df.dropna(subset=["CustomerID"])

# 2. Usunięcie anulowanych transakcji (InvoiceNo zaczyna się od 'C')
df = df[~df["InvoiceNo"].astype(str).str.startswith("C")]

# 3. Usunięcie Quantity <= 0 oraz UnitPrice <= 0
df = df[df["Quantity"] > 0]
df = df[df["UnitPrice"] > 0]

# 4. Konwersja daty do odpowiedniego formatu
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# 5. Usunięcie duplikatów
df = df.drop_duplicates()

# 6. Dodanie miary Revenue (Przychód)
df["Revenue"] = df["Quantity"] * df["UnitPrice"]

print(f"Liczba wierszy po czyszczeniu: {len(df)}")
# 1. DimProduct
# Pobieramy unikalne produkty. Bierzemy pierwszy opis dla danego kodu, aby uniknąć duplikatów
dim_product = df.groupby("StockCode")["Description"].first().reset_index()
dim_product["Product_SK"] = dim_product.index + 1 # Klucz sztuczny


# 2. DimDate
# Tworzymy unikalne daty na podstawie InvoiceDate
df["Date"] = df["InvoiceDate"].dt.date
dim_date = pd.DataFrame({"Date": df["Date"].unique()})
dim_date["Year"] = pd.to_datetime(dim_date["Date"]).dt.year
dim_date["Month"] = pd.to_datetime(dim_date["Date"]).dt.month
dim_date["Day"] = pd.to_datetime(dim_date["Date"]).dt.day
dim_date = dim_date.sort_values("Date").reset_index(drop=True)
dim_date["Date_SK"] = dim_date.index + 1 # Klucz sztuczny


# 3. DimCustomer (z implementacją SCD typu 2)
# Śledzimy zmianę przypisania klienta do kraju (Country) w czasie
dim_customer = df.groupby(["CustomerID", "Country"], as_index=False).agg(
    valid_from=("InvoiceDate", "min")
).sort_values(by=["CustomerID", "valid_from"]).reset_index(drop=True)

# Klucz sztuczny
dim_customer["Customer_SK"] = dim_customer.index + 1

# Ustawienie valid_to oraz current_flag dla SCD2
dim_customer["valid_to"] = dim_customer.groupby("CustomerID")["valid_from"].shift(-1)
# Jeśli nie ma nowszego rekordu, ustawiamy datę daleko w przyszłości
dim_customer["valid_to"] = dim_customer["valid_to"].fillna(pd.to_datetime("2099-12-31"))

dim_customer["current_flag"] = dim_customer["valid_to"] == pd.to_datetime("2099-12-31")
dim_customer["current_flag"] = dim_customer["current_flag"].map({True: "Y", False: "N"})

print("Przykładowy DimCustomer z SCD2:")
display(dim_customer.head())
# FactSales
# 1. Dołączamy Product_SK (łączymy po kluczu naturalnym StockCode)
fact_sales = df.merge(dim_product[["StockCode", "Product_SK"]], on="StockCode", how="left")

# 2. Dołączamy Date_SK (łączymy po kolumnie Date)
fact_sales = fact_sales.merge(dim_date[["Date", "Date_SK"]], on="Date", how="left")

# 3. Dołączamy Customer_SK
# Łączymy po CustomerID oraz Country, aby poprawnie złapać historyczną wersję klienta (zgodnie z SCD2)
fact_sales = fact_sales.merge(dim_customer[["CustomerID", "Country", "Customer_SK"]], 
                              on=["CustomerID", "Country"], how="left")

# 4. Wybieramy docelowe kolumny: wyłącznie klucze sztuczne z wymiarów, nr faktury i miary
fact_sales = fact_sales[[
    "Customer_SK", "Product_SK", "Date_SK", "InvoiceNo", "Quantity", "Revenue"
]]

print("Tabela Faktów (FactSales):")
display(fact_sales.head())