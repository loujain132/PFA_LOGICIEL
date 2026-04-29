import pandas as pd

import matplotlib.pyplot as plt

import matplotlib 

matplotlib.use('TkAgg')

import os

print (os.getcwd())


# ==============================
# LOAD DATA
# ==============================
def load_data(file_path):
    if not os.path.exists(file_path):
        print(" Fichier introuvable")
        exit()

    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    elif file_path.endswith(".xlsx"):
        df = pd.read_excel(file_path)
    else:
        print(" Format non supporté")
        exit()

    return df


# ==============================
# DATA VALIDATION
# ==============================
def validate_data(df):
    required_columns = ["ID", "Prix", "Quantite", "Remise"]

    for col in required_columns:
        if col not in df.columns:
            print(f" Colonne manquante: {col}")
            exit()

    if df.isnull().sum().any():
        print(" Valeurs manquantes détectées")

    if (df["Prix"] < 0).any() or (df["Quantite"] < 0).any():
        print(" Valeurs négatives détectées")


# ==============================
#  CALCULATIONS
# ==============================
def compute_metrics(df):
    df["CA_Brut"] = df["Prix"] * df["Quantite"]
    df["CA_Net"] = df["CA_Brut"] - (df["CA_Brut"] * df["Remise"] / 100)
    df["TVA"] = df["CA_Net"] * 0.2
    return df


# ==============================
#  ANALYSIS
# ==============================
def analyze(df):
    total = df["CA_Net"].sum()
    mean = df["CA_Net"].mean()
    best = df.loc[df["CA_Net"].idxmax()]
    worst = df.loc[df["CA_Net"].idxmin()]
    top3 = df.sort_values(by="CA_Net", ascending=False).head(3)

    print("\n ===== ANALYSE =====")
    print(f" CA Total: {total:.2f}")
    print(f" CA Moyen: {mean:.2f}")
    print(f" Meilleur Produit ID: {best['ID']}")
    print(f" Moins bon Produit ID: {worst['ID']}")

    print("\n Top 3 Produits:")
    print(top3[["ID", "CA_Net"]])


# ==============================
#  EXPORT
# ==============================
def export(df):
    df.to_csv("resultats_final.csv", index=False)
    df.to_excel("resultats_final.xlsx", index=False)
    print("\n Fichiers exportés avec succès")


# ==============================
#  VISUALIZATION
# ==============================
def create_graphs(df):
    plt.style.use("ggplot")

    print(" création des graphes...")

    colors = ["#FF5733", "#33FF57", "#3357FF", "#F39C12", "#8E44AD"]

    top = df.sort_values(by="CA_Net", ascending=False).head(10)

    # BAR
    plt.figure()
    plt.bar(top["ID"], top["CA_Net"], color=colors)
    plt.title("Top 10 Produits (CA Net)")
    plt.xlabel("Produit ID")
    plt.ylabel("CA Net")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("graph_bar.png")

    # LINE
    plt.figure()
    plt.plot(top["ID"], top["CA_Net"], marker='o', color="#2ECC71")
    plt.title("Evolution CA (Top 10)")
    plt.xlabel("Produit ID")
    plt.ylabel("CA Net")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("graph_line.png")

    # PIE
    plt.figure()
    plt.pie(top["CA_Net"], labels=top["ID"], autopct="%1.1f%%")
    plt.title("Répartition CA (Top 10)")
    plt.tight_layout()
    plt.savefig("graph_pie.png")

    # HIST
    plt.figure()
    plt.hist(df["CA_Net"], bins=10, color="#3498DB")
    plt.title("Distribution CA Net")
    plt.tight_layout()
    plt.savefig("graph_hist.png")

    # BOX
    plt.figure()
    plt.boxplot(df["CA_Net"])
    plt.title("Boxplot CA Net")
    plt.tight_layout()
    plt.savefig("graph_box.png")

    print(" Graphiques générés avec succès")
    plt.show()


# ==============================
#  MAIN
# ==============================
def main():
    print(" Dossier courant:", os.getcwd())

    file_path = "ventes.csv"

    df = load_data(file_path)
    validate_data(df)
    df = compute_metrics(df)

    analyze(df)
    export(df)
    create_graphs(df)

    files = [
        "graph_bar.png",
        "graph_line.png",
        "graph_pie.png",
        "graph_hist.png",
        "graph_box.png",
        "resultats_final.xlsx"
    ]

    for f in files:
        if os.path.exists(f):
            os.startfile(f)



if __name__ == "__main__":
    main()
