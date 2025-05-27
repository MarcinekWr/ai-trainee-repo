import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import AzureSearch
from langchain_openai import AzureOpenAIEmbeddings

from langchain.text_splitter import RecursiveCharacterTextSplitter


def load_and_split_pdfs(directory: str):
    all_docs = []
    for pdf_path in Path(directory).rglob("*.pdf"):
        loader = PyPDFLoader(str(pdf_path))
        docs = loader.load()
        all_docs.extend(docs)

    print(f"Załadowano dokumentów: {len(all_docs)}")

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(all_docs)
    print(f"Podzielono na chunków: {len(chunks)}")
    return chunks


def embed_and_upload_to_azure(chunks):
    embeddings = AzureOpenAIEmbeddings(
        azure_deployment=os.getenv("DEPLOYMENT_NAME_FOR_EMBEDDING"),
        azure_endpoint=os.getenv("API_BASE"),
        api_key=os.getenv("API_KEY"),
        api_version=os.getenv("API_VERSION"),
    )
    vectorstore = AzureSearch(
        azure_search_endpoint=os.getenv("URL_RAG"),
        azure_search_key=os.getenv("API_KEY_SEARCH"),
        index_name=os.getenv("INDEX_NAME"),
        embedding_function=embeddings.embed_query,
    )

    print("Wgrywanie danych do Azure Cognitive Search...")
    vectorstore.add_documents(chunks, include_metadata=False)
    print("Zakończono wgrywanie.")


def main():
    load_dotenv()
    chunks = load_and_split_pdfs(Path(os.getenv("DATA_DIR")))
    embed_and_upload_to_azure(chunks)


if __name__ == "__main__":
    main()
