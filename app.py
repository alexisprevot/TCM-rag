import streamlit as st
import requests

# -- INITIALISATION --
if "conversation" not in st.session_state:
    st.session_state.conversation = []

st.title("The Coding Machine RAG Chatbot")
st.text("Ce chatbot utilise le modèle RAG. Les documents utilisés sont ceux disponible sur le drive de TCM.")

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