import os
import re
import uuid

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from dotenv import load_dotenv
from PyPDF2 import PdfReader


load_dotenv()

search_client = SearchClient(
    endpoint=os.getenv("URL_RAG_SEM"),
    index_name=os.getenv("INDEX_NAME_SEM"),
    credential=AzureKeyCredential(os.getenv("API_KEY_SEARCH_SEM")),
)


def main():
    def split_text_smartly(text, max_chunk_size=500):
        sentences = re.split(r"[.!?]+", text)
        chunks = []
        current_chunk = ""

        for sentence in sentences:
            if len(current_chunk + sentence) < max_chunk_size:
                current_chunk += sentence + ". "
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + ". "

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

    reader = PdfReader(r"src\RAG_fundaments\data\NewYorkBrochure.pdf")
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    chunks = split_text_smartly(text)

    documents = []
    for i, chunk in enumerate(chunks):
        documents.append({"id": str(uuid.uuid4()), "content": chunk})

    result = search_client.upload_documents(documents)
    print(f"Wysłano {len(documents)} dokumentów. Status: {result}")

    for r in result:
        print(f"Dokument ID: {r.key}, Sukces: {r.succeeded}, Błąd: {r.error_message}")


if __name__ == "__main__":
    main()
