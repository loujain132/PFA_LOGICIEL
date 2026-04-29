import pandas as pd

def process_file(file):
    try:
        df = pd.read_csv(file)

        df["CA_Net"] = df["Prix"] * df["Quantite"] * (1 - df["Remise"] / 100)

        total = df["CA_Net"].sum()
        best = df.loc[df["CA_Net"].idxmax()]

        return df, total, best.to_dict()

    except Exception as e:
        print("Erreur:", e)
        return None