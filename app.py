import streamlit as st
import requests

# --- BARRE LATÉRALE ---
st.sidebar.title("📚 Base documentaire TCM")

# Texte descriptif
st.sidebar.write(
    "Cette application vous permet de consulter et d'interroger la base documentaire "
    "de The Coding Machine"
)

# Exemple de documents à lister dans la sidebar
# À adapter selon la structure de vos propres documents (titres, URL, etc.)
documents_tcm = [
    # {"title": "Politique SMSI", "url": "https://docs.google.com/document/d/1FFBexxMZfdnDvhv1NHNVGiIOrxsXcv9K2ZCeasqm6gA"},
    # {"title": "Procédure de gestion des incidents", "url": "https://docs.google.com/document/d/1KrGuZ-MWoIB2CEHddV6_p2AZuNYb9rPPhMkEZ7kYYy4"},
    #{"title": "Gestion des accès physiques", "url": "https://docs.google.com/document/d/1QEWcT1_t8Uxe30LxgaURpd2vgMNG59TVFh8PolKS-KU"},
    {"title": "Charte de télétravail", "url": "https://docs.google.com/document/d/1xx2ZKhsJ0-M-wFjfgAoL4aVb8uBsLxFYZLTEF8Hp3Oc"},
    #{"title": "Charte éthique", "url": "https://docs.google.com/document/d/13TsJXppDAc0MjWDJWIDSDqMPEaRY5wxMidRSVlWYyqI"},
    #{"title": "Charte administrateur", "url": "https://docs.google.com/document/d/1POrFdzVXTPed5AWxPRO8RBhOqqqlVx5s0XEMBo_0G1s"},
    #{"title": "Politique de développement informatique sécurisé", "url": "https://docs.google.com/document/d/1hOJQbJIUt-I6wE9eprHJ3s25XaOL-7ZEFb7G9tbt8Uw"},
    #{"title": "Politique de transfert de l'information", "url": "https://docs.google.com/document/d/11RIzbEOiqwNrlE_mi2hA6ceA7CFamEnQAlfsEFtbrc4"},
    {"title": "Charte informatique", "url": "https://docs.google.com/document/d/1ti3QS5COTDktiBs6KrIQrFe_FDiQHEBV5rg31hSOMDU"},
]

st.sidebar.markdown("### Documents disponibles")
for doc in documents_tcm:
    st.sidebar.markdown(f"- [{doc['title']}]({doc['url']})")

st.sidebar.markdown("---")

# st.sidebar.write(
#     "Des informations complémentaires ont été récupérées sur le site de TCM tel que \"Ma vie à TCM\" et \"Je suis en CDI\""
#     )

# -- INITIALISATION --
if "conversation" not in st.session_state:
    st.session_state.conversation = []

st.title("📚 The Coding Machine Chatbot 🤖")
st.text("Testez le chatbot RAG en fonction des éléments présents dans les documents")

# 1) Récupérer la question AVANT l’affichage
user_input = st.chat_input("Posez votre question ici…")

if user_input:
    # On ajoute le message "user" à l'historique
    st.session_state.conversation.append({"role": "user", "content": user_input})
    
    # 2) APPEL À N8N (webhook) pour récupérer la réponse RAG
    #    Adaptez l’URL à votre configuration (webhook test vs production)
    #    Ex: http://localhost:5678/webhook/rag
    try:
        response = requests.post(
            "https://n8n.srv749429.hstgr.cloud/webhook/f5808099-158f-49c5-b664-e2a288f3bb1d",
            json={"question": user_input},
            timeout=60
        )
        if response.status_code == 200:
            data = response.json()

            # On suppose que n8n renvoie un JSON de type {"answer": "..."}
            rag_answer = data.get("answer", "Aucune réponse trouvée.")
        else:
            rag_answer = f"Erreur (code {response.status_code}) lors de la requête."
    except requests.exceptions.RequestException as e:
        rag_answer = f"Erreur de connexion à n8n: {e}"

    # On ajoute la réponse "assistant"
    st.session_state.conversation.append({"role": "assistant", "content": rag_answer})

# 3) AFFICHER TOUTE LA CONVERSATION
for msg in st.session_state.conversation:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
