import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Configuration
st.set_page_config(page_title="Mon Coach Richesse", page_icon="💰")

# --- FONCTION POUR SAUVEGARDER ---
def sauvegarder_donnee(montant, categorie, commentaire):
    nom_fichier = 'finances.csv'
    nouvelle_ligne = pd.DataFrame({
        'Date': [datetime.now().strftime("%Y-%m-%d %H:%M")],
        'Montant': [montant],
        'Categorie': [categorie],
        'Commentaire': [commentaire]
    })
    
    if not os.path.isfile(nom_fichier):
        nouvelle_ligne.to_csv(nom_fichier, index=False)
    else:
        nouvelle_ligne.to_csv(nom_fichier, mode='a', header=False, index=False)

# --- INTERFACE ---
st.title("🚀 Objectif : Indépendance Financière")

# Formulaire de saisie
with st.expander("➕ Enregistrer une nouvelle dépense", expanded=True):
    montant = st.number_input("Montant (FCFA)", min_value=0, step=500)
    categorie = st.selectbox("Catégorie", ["Besoins", "Loisirs", "Investissement", "Business"])
    commentaire = st.text_input("Détails (ex: Restaurant, Carburant...)")
    
    if st.button("Valider la dépense"):
        sauvegarder_donnee(montant, categorie, commentaire)
        st.success("Donnée enregistrée dans votre coffre-fort financier !")
        if categorie == "Loisirs" and montant > 5000:
            st.warning("⚠️ Ce plaisir immédiat retarde votre liberté. Était-ce nécessaire ?")

# --- AFFICHAGE DES RÉSULTATS ---
st.divider()
st.header("📊 Vos Statistiques")

if os.path.isfile('finances.csv'):
    df = pd.read_csv('finances.csv')
    
    # Calculs rapides
    total_depense = df['Montant'].sum()
    st.metric("Total Dépensé", f"{total_depense:,} FCFA".replace(',', ' '))
    
    # Graphique
    st.subheader("Répartition par catégorie")
    stats_cat = df.groupby('Categorie')['Montant'].sum()
    st.bar_chart(stats_cat)
    
    # Historique
    with st.expander("Voir l'historique complet"):
        st.dataframe(df.sort_index(ascending=False))
else:
    st.info("Aucune donnée enregistrée pour le moment. Commencez par saisir une dépense.")
