
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Una catena di negozi di elettronica vuole analizzare i dati delle vendite 
# per migliorare la gestione e capire l’andamento del mercato. 
# I dati vengono raccolti giornalmente e comprendono informazioni su prodotti, 
# quantità vendute, prezzo, incassi e negozi.
# Si richiede di sviluppare un programma in Python che utilizzi:
# NumPy per elaborazioni numeriche veloci, Pandas per la gestione e 
# analisi di dataset, Matplotlib per la visualizzazione dei dati in grafici.
#
# ==========================
# Creazione Dati Sintetici
# ==========================

np.random.seed(42)   # seed per riproducibilità
n = 100              # numero righe

lista_negozi = ["Milano", "Roma", "Napoli", "Torino", "Bologna", "Firenze"]

# Dizionario range prezzi per keys:"categoria", values:(media, deviazione standard)
dizionario_prodotti = {
    "Smartphone": (300, 120),
    "Laptop": (1200, 250),
    "TV": (550, 180),
    "Tablet": (350, 80),
    "Cuffie": (60, 30),
    "Monitor": (250, 60),
    "Stampante": (150, 40),
}

# Date: 12 mesi a partire da gennaio 2025
date_range = pd.date_range("2025-01-01", periods=12, freq="ME")

# Dati generati con NumPy
negozi_random = np.random.choice(lista_negozi, size=n)
date_random = np.random.choice(date_range, size=n)
quantita = np.random.randint(1, 11, size=n)
# Estrae 100 prodotti casuali dalle categorie definite nel dizionario
prodotti_random = np.random.choice(list(dizionario_prodotti.keys()), size=n)

# Loop creazione prezzi - applica 'media' e 'dev' impostati in dizionario_prodotti
# Per ogni categoria applica la sua distribuzione (media, dev)
prezzi = np.zeros(n)
for prodotto, (media, dev) in dizionario_prodotti.items():
    # mask True/False: seleziona le righe dove il prodotto è quello corrente
    mask = prodotti_random == prodotto
    # assegna prezzi solo alle righe selezionate
    prezzi[mask] = np.random.normal(loc=media, scale=dev, size=mask.sum())

# ==========================
# CREAZIONE DATAFRAME
# ==========================

df = pd.DataFrame({
    "Data": date_random,
    "Negozio": negozi_random,
    "Prodotto": prodotti_random,
    "Quantità": quantita,
    "Prezzo_unitario": prezzi.round(2),
})

# Pulizia "Prezzo_unitario" da valori negativi:
df["Prezzo_unitario"] = df["Prezzo_unitario"].abs()

# Salvataggio in CSV:
df.to_csv("vendite.csv", index=False, encoding="utf-8-sig")

# Import CSV - diventa il nuovo DataFrame:
DATA = pd.read_csv("vendite.csv", sep=',')

# Check DATA structure
print(DATA.head())
DATA.info()

# ==========================
# PANDAS MANIPOLAZIONE DATI
# ==========================

# Aggiugere colonna Incasso = Quantità * Prezzo_unitario
DATA["Incasso"] = (DATA["Quantità"] * DATA["Prezzo_unitario"]).round(2)

# Incasso totale catena - somma vettoriale :
incasso_totale = DATA["Incasso"].sum()
# Incasso medio per negozio :
incasso_medio_negozi = DATA.groupby("Negozio")["Incasso"].mean().round(2)
# Top3 Best Sellers - per quantità :
top3_quantity = DATA["Prodotto"].value_counts().head(3)
# Incasso medio dei prodotti :
incasso_medio_prodotti = DATA.groupby(["Negozio", "Prodotto"])["Incasso"].mean().round(2)


print(DATA.head())

print("\n----Incasso Totale Catena----\n", incasso_totale,"€")
print("\n----Incasso Medio Negozi in € :\n", incasso_medio_negozi)
print("\n----Prodotti Best Sellers :\n", top3_quantity)
print("\n----Incasso Medio prodotti in € :\n", incasso_medio_prodotti)


# ==========================
# Iterare array con NumPy
# ==========================

# Estraggo colonna Quantità come array:
arr_quantity = DATA["Quantità"].to_numpy()

# Statistiche su quantità vendute:
media = np.mean(arr_quantity).round(1)
min = np.min(arr_quantity)
max = np.max(arr_quantity)
# Percentuale vendite sopra la media 
percentuale_sopra_media = (arr_quantity > media).mean() * 100

print("\n media quanità vendute:", media, "unità")
print("minime vendute:", min, "unità")
print("massime vendute:", max, "unità")
print("% vendite sopra la media:", percentuale_sopra_media,"%")

# Aggiornare array 2D aggiungendo "Prezzo_Unitario"
arr_quantity = DATA[["Quantità","Prezzo_unitario"]].to_numpy()

# Calcolo Incasso (Quantità * Prezzo)
incasso_numpy = arr_quantity[:, 0] * arr_quantity[:, 1]

#Confronto dati con colonna originale del DataFrame 'DATA'
df_incassi = DATA["Incasso"]

print("Match dei Dati (True/False):", np.allclose(incasso_numpy, df_incassi)) # True = data match / False = mismatch

# =======================
# Analisi Avanzata Pandas
# =======================

# Mappare la colonna prodotti aggiungendo una "Categoria"
mappa_categorie = {
    "Smartphone": "Informatica",
    "Laptop": "Informatica",
    "Tablet": "Informatica",
    "Monitor": "Informatica",

    "TV": "Elettrodomestici",
    "Stampante": "Elettrodomestici",

    "Cuffie": "Accessori"
}

# Creazione nuova colonna Categoria
DATA["Categoria"] = DATA["Prodotto"].map(mappa_categorie)

# Calcoli per categoria
# incasso totale per categoria
incasso_categoria = DATA.groupby("Categoria")["Incasso"].sum()
# media giornaliera unità vendute
media_categoria = DATA.groupby("Categoria")["Quantità"].mean().round(1)
# totale quantità vendute (per categoria)
item_sold_categoria = DATA.groupby("Categoria")["Quantità"].sum().round(1)

print("\n=== ANALISI PER CATEGORIA ===\n")
print("Incassi per categoria in €\n", incasso_categoria)
print("\nQuantità media vendite per categoria:\n", media_categoria)

# Salvataggio DataFrame aggiornato
DATA.to_csv("vendite_analizzate.csv", index=False, encoding="utf-8-sig")
print("\nFile salvato: vendite_analizzate.csv")

# ==========================
# Creazione grafici vendite
# ==========================

# 1) Grafico a barre: incasso totale per ogni negozio
incasso_per_negozio = DATA.groupby("Negozio")["Incasso"].sum().sort_values(ascending=False)

plt.figure(figsize=(8,5))
incasso_per_negozio.plot(kind="bar", color='blue')
plt.title("Incasso totale per negozio")
plt.ylabel("Incasso (€)")
plt.xlabel("Negozio")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
plt.close()

# 2) Grafico a torta: percentuale di incassi per ciascun prodotto
incasso_per_prodotto = DATA.groupby("Prodotto")["Incasso"].sum()
# Ordina per valore per una torta più leggibile
incasso_per_prodotto = incasso_per_prodotto.sort_values(ascending=False)

plt.figure(figsize=(7,7))
colori = plt.cm.tab20.colors #palette colori fette
plt.pie(incasso_per_prodotto, labels=incasso_per_prodotto.index, autopct='%1.1f%%',
        startangle=140, colors=colori)
plt.title("Percentuale incassi per prodotto")
plt.tight_layout()
plt.show()
plt.close()

# 3) Grafico a linee: andamento temporale degli incassi totali della catena
incasso_giornaliero = DATA.groupby("Data")["Incasso"].sum().sort_index()

plt.figure(figsize=(10,5))
plt.plot(incasso_giornaliero.index, incasso_giornaliero.values, marker='o', linestyle='-',
         color='C1')
plt.title("Andamento incassi totali della catena")
plt.xlabel("Data")
plt.ylabel("Incasso totale (€)")
plt.grid(alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
plt.close()

# ===========
# ESTENSIONI
# ===========

# Grafico combinato vendite:
fig, ax1 = plt.subplots(figsize=(10, 6))
categorie = incasso_categoria.index

# --- BARRE: Incasso totale per categoria ---
ax1.bar(
    categorie,
    incasso_categoria.values,
    color="C0",
    alpha=0.7,
    label="Incasso totale"
)

ax1.set_xlabel("Categoria")
ax1.set_ylabel("Incasso totale (€)", color="C0")
ax1.tick_params(axis="y", labelcolor="C0")
ax1.set_title("Incasso totale e quantità media giornaliera venduta")

# --- LINEA: Quantità media venduta ---
ax2 = ax1.twinx()

ax2.plot(
    categorie,
    media_categoria.values,
    color="C1",
    marker="o",
    linewidth=2,
    label="Quantità giornaliera venduta"
)

ax2.set_ylabel("Media Quantità Giornaliera Venduta", color="C1")
ax2.tick_params(axis="y", labelcolor="C1")
fig.tight_layout()
plt.show()
plt.close()

# Prodotti Best seller:

def get_best_sellers(DATA: pd.DataFrame, N: int = 5):
    """
    Restituisce un classifica di N prodotti con il maggior incasso.
    """
    best_sellers = DATA.groupby("Prodotto")["Incasso"].sum().sort_values(ascending=False).head(N)
    print(f"\n--- Top {N} Prodotti più Venduti ---\n")
    print(f"incasso totale in €:")
    print(best_sellers)
    return best_sellers

get_best_sellers(DATA, 5)