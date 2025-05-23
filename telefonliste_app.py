
import difflib
import pandas as pd
import streamlit as st

# Daten laden
df = pd.read_excel("Telefonliste_-Handelskunden.xlsx", sheet_name="Tabelle1")
df = df.drop(columns=[col for col in df.columns if 'Unnamed' in col])

# Streamlit App
st.title("Intelligente Telefonliste")

suchbegriff = st.text_input("Kontakt suchen (auch mit Tippfehlern oder Teilnamen):")

if suchbegriff:
    # Ähnlichkeitssuche
    df["Ähnlichkeit"] = df["Name"].astype(str).apply(lambda x: difflib.SequenceMatcher(None, suchbegriff.lower(), x.lower()).ratio())
    treffer = df[df["Ähnlichkeit"] > 0.4].sort_values(by="Ähnlichkeit", ascending=False).drop(columns=["Ähnlichkeit"])

    if not treffer.empty:
        st.success(f"{len(treffer)} mögliche Treffer gefunden:")
        st.dataframe(treffer)
    else:
        st.warning("Kein passender Kontakt gefunden.")
else:
    st.info("Bitte gib einen Namen oder Teilnamen ein.")
