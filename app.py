import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Mon Coach Richesse", page_icon="💰", layout="centered")

# --- FONCTION DE SAUVEGARDE ---
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

# --- INTERFACE PRINCIPALE ---
st.title("🚀 Objectif : Indépendance Financière")
st.write("Votre centre de commandement pour bâtir votre fortune.")

# --- SECTION 1 : SAISIE ---
with st.expander("➕ Enregistrer une opération", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        montant = st.number_input("Montant (FCFA)", min_value=0, step=500)
    with col2:
        # AJOUT DE LA CATÉGORIE 'CHARGES' ICI
        categorie = st.selectbox("Catégorie", ["Investissement", "Business", "Charges", "Besoins", "Loisirs"])
    
    commentaire = st.text_input("Détails (ex: Loyer, Senelec, Restaurant, Matériel...)")
    
    if st.button("Valider l'opération"):
        sauvegarder_donnee(montant, categorie, commentaire)
        
        # --- LOGIQUE DU COACH (RECADRAGE) ---
        if categorie == "Investissement":
            st.balloons()
            st.success("🔥 EXCELLENT ! C'est ainsi qu'on devient riche. Cet argent travaille pour vous.")
        
        elif categorie == "Business":
            st.info("📈 Investir dans votre business, c'est investir dans votre futur.")
            
        elif categorie == "Charges":
            st.info("🏠 Charges enregistrées. Essayez de les réduire au minimum pour libérer plus d'argent pour l'investissement.")
            
        elif categorie == "Loisirs":
            if montant > 15000:
                st.error(f"🚨 RECADRAGE : {montant} FCFA en loisirs ? Posez-vous la question : cet achat vaut-il vraiment de retarder votre liberté ?")
            else:
                st.warning("⚠️ Attention : Chaque plaisir immédiat a un coût sur votre futur patrimoine.")
        
        else:
            st.success("Donnée enregistrée avec succès.")

# --- SECTION 2 : ANALYSE & PROGRESSION ---
st.divider()

if os.path.isfile('finances.csv'):
    df = pd.read_csv('finances.csv')
    
    # 1. Barre de Progression vers le 1er Million
    st.subheader("🎯 Objectif : Premier Million (Investissement)")
    epargne_actuelle = df[df['Categorie'] == 'Investissement']['Montant'].sum()
    objectif = 1000000
    progression = min(epargne_actuelle / objectif, 1.0)
    
    st.progress(progression)
    st.write(f"Progression : **{epargne_actuelle:,} FCFA** sur **1 000 000 FCFA**.".replace(',', ' '))

    # 2. Statistiques Globales
    col_a, col_b = st.columns(2)
    with col_a:
        total_depense = df['Montant'].sum()
        st.metric("Total Dépensé", f"{total_depense:,} FCFA".replace(',', ' '))
    with col_b:
        # Calcul du taux d'investissement (La clé de la richesse)
        ratio = (epargne_actuelle / total_depense * 100) if total_depense > 0 else 0
        st.metric("Taux d'Investissement", f"{ratio:.1f}%")

    # 3. Focus sur les Charges
    total_charges = df[df['Categorie'] == 'Charges']['Montant'].sum()
    if total_charges > 0:
        st.write(f"🏠 Vos charges fixes représentent **{total_charges:,} FCFA** ce mois-ci.".replace(',', ' '))

    # 4. Graphique de Répartition
    st.subheader("📊 Où part votre argent ?")
    stats_cat = df.groupby('Categorie')['Montant'].sum()
    st.bar_chart(stats_cat)

    # 5. Historique
    with st.expander("📖 Historique des transactions"):
        st.dataframe(df.sort_index(ascending=False), use_container_width=True)

else:
    st.info("Votre base de données est vide. Commencez par enregistrer une dépense ou un investissement !")
