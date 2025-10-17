import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# --- 1. Titre et upload ---
st.set_page_config(page_title="Analyse par garantie", layout="wide")
st.title("📊 Analyse automatisée des données par garantie")

uploaded_file = st.file_uploader("📂 Importez votre fichier CSV ou Excel :", type=["csv", "xlsx"])

if uploaded_file is not None:
    # --- 2. Lecture du fichier ---
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("🔍 Aperçu des données")
    st.dataframe(df.head())

    # --- 3. Sélection des colonnes pertinentes ---
    colonne_garantie = st.selectbox("Choisissez la colonne de garantie :", df.columns)
    colonne_valeur = st.selectbox("Choisissez une colonne numérique (optionnelle) :", ["Aucune"] + list(df.select_dtypes(include='number').columns))

    # --- 4. Analyse statistique ---
    st.subheader("📈 Statistiques descriptives par garantie")
    if colonne_valeur != "Aucune":
        stats = df.groupby(colonne_garantie)[colonne_valeur].agg(['count', 'mean', 'sum', 'min', 'max']).reset_index()
        stats.rename(columns={
            'count': 'Nombre',
            'mean': 'Moyenne',
            'sum': 'Total',
            'min': 'Minimum',
            'max': 'Maximum'
        }, inplace=True)
    else:
        stats = df.groupby(colonne_garantie).size().reset_index(name="Nombre")

    st.dataframe(stats)

    # --- 5. Choix du type de graphique ---
    st.subheader("📊 Visualisation")
    type_graph = st.radio("Choisissez le type de graphique :", ["Barres", "Camembert", "Histogramme (si données numériques)"])

    if type_graph == "Barres":
        fig = px.bar(stats, x=colonne_garantie, y="Nombre", color=colonne_garantie,
                     title="Répartition des enregistrements par garantie")
        st.plotly_chart(fig, use_container_width=True)

    elif type_graph == "Camembert":
        fig = px.pie(stats, names=colonne_garantie, values="Nombre",
                     title="Répartition des garanties (camembert)")
        st.plotly_chart(fig, use_container_width=True)

    elif type_graph == "Histogramme" and colonne_valeur != "Aucune":
        fig = px.histogram(df, x=colonne_valeur, color=colonne_garantie,
                           title=f"Distribution de {colonne_valeur} par garantie")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ Choisissez une colonne numérique pour l’histogramme.")

    # --- 6. Commentaires automatiques avancés ---
    st.subheader("🧠 Interprétation automatique des résultats")

    max_garantie = stats.loc[stats["Nombre"].idxmax(), colonne_garantie]
    max_val = stats["Nombre"].max()
    min_garantie = stats.loc[stats["Nombre"].idxmin(), colonne_garantie]
    min_val = stats["Nombre"].min()
    total = stats["Nombre"].sum()
    moyenne = stats["Nombre"].mean()

    st.markdown(f"""
    ### 📘 Synthèse des résultats
    - 🔝 **Garantie la plus représentée :** `{max_garantie}` avec **{max_val} enregistrements**.
    - ⚠️ **Garantie la moins représentée :** `{min_garantie}` avec **{min_val} enregistrements**.
    - 📦 **Total d’enregistrements analysés :** {total}.
    - 📊 **Nombre moyen par garantie :** {moyenne:.2f}.

    ### 💬 Analyse détaillée
    - La distribution montre que certaines garanties dominent fortement, ce qui peut indiquer une concentration de demandes ou de ventes spécifiques.
    - Si les garanties peu représentées sont stratégiquement importantes, il serait utile d’examiner les causes possibles (mauvaise communication, faible demande, etc.).
    - Les garanties les plus fréquentes peuvent refléter la **préférence client** ou la **performance des produits** associés.
    - En combinant avec une colonne numérique (par ex. montant, coût, durée), on peut dégager des **corrélations entre la garantie et la valeur économique**.
    """)

    st.info("💡 Conseil : Vous pouvez exporter ce tableau et ces graphiques pour vos rapports internes.")

else:
    st.info("⬆️ Veuillez importer un fichier CSV ou Excel pour commencer l’analyse.")
