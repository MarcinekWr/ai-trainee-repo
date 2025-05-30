import os

import requests
import streamlit as st
from dotenv import load_dotenv


load_dotenv()

AZURE_FUNCTION_URL = os.getenv("AZURE_FUNCTION_URL")
AZURE_FUNCTION_KEY = os.getenv("AZURE_FUNCTION_KEY")
UPLOAD_FUNCTION_URL = os.getenv("UPLOAD_FUNCTION_URL")
UPLOAD_FUNCTION_KEY = os.getenv("UPLOAD_FUNCTION_KEY")
RAISE_ERROR_URL = os.getenv("RAISE_ERROR_URL")
RAISE_ERROR_KEY = os.getenv("RAISE_ERROR_KEY")


st.set_page_config(page_title="RAG Chat", page_icon="🤖")
st.title("💬 Chat z RAG")

query = st.text_input("Zadaj pytanie:")

if st.button("Wyślij"):
    if query:
        response = requests.get(
            AZURE_FUNCTION_URL, params={"query": query, "code": AZURE_FUNCTION_KEY}
        )
        if response.status_code == 200:
            answer = response.json()["data"]["answer"]
            context = response.json()["data"]["source_context"]
            st.success(f"**Odpowiedź:** {answer}")
            with st.expander("🔍 Zastosowany kontekst"):
                st.write(context)
        else:
            st.error(f"❌ Błąd: {response.status_code} — {response.text}")
    else:
        st.warning("Wpisz pytanie przed wysłaniem.")

st.markdown("---")

st.subheader("📄 Dodaj nowy dokument do systemu")

uploaded_file = st.file_uploader("Wybierz plik tekstowy (TXT,PDF)", type=["txt", "pdf"])
if uploaded_file is not None:
    file_bytes = uploaded_file.read()

    if uploaded_file.type != "application/pdf":
        try:
            file_content = file_bytes.decode("utf-8")
        except UnicodeDecodeError:
            file_content = "Nie udało się zdekodować pliku jako tekst UTF-8."
    else:
        file_content = "Plik PDF – nie wyświetlono podglądu."

    st.text_area("Podgląd pliku:", value=file_content, height=200)

    if st.button("📥 Prześlij dokument"):
        if uploaded_file:
            if uploaded_file.type == "application/pdf":
                response = requests.post(
                    UPLOAD_FUNCTION_URL,
                    params={"code": UPLOAD_FUNCTION_KEY},
                    headers={"Content-Type": "application/pdf"},
                    data=file_bytes,
                )
            else:
                response = requests.post(
                    UPLOAD_FUNCTION_URL,
                    params={"code": UPLOAD_FUNCTION_KEY},
                    headers={"Content-Type": "application/json"},
                    json={"content": file_content},
                )

            if response.status_code == 200:
                st.success("✅ Dokument został pomyślnie przesłany i zaindeksowany!")
                with st.expander("ℹ️ Szczegóły odpowiedzi serwera"):
                    st.json(response.json())
            else:
                st.error(f"❌ Błąd przesyłania: {response.status_code}")
                st.text(response.text)

st.markdown("---")
st.subheader("Test błędów i logowania")

if st.button("Wygeneruj testowy błąd"):
    try:
        response = requests.get(RAISE_ERROR_URL, params={"code": RAISE_ERROR_KEY})
        st.success("✅ Testowy błąd został wywołany – sprawdź Application Insights.")
    except Exception as e:
        st.error(f"❌ Wystąpił wyjątek: {str(e)}")
