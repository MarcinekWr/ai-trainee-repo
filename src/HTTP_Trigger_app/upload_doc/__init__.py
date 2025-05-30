import json
import logging
import os
import traceback
import uuid
from pathlib import Path
from tempfile import NamedTemporaryFile

import azure.functions as func
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import AzureSearch
from langchain_core.documents import Document
from langchain_openai import AzureOpenAIEmbeddings

from langchain.text_splitter import RecursiveCharacterTextSplitter


load_dotenv()


def split_pdf(file_path):
    loader = PyPDFLoader(file_path)
    pages = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(pages)
    return chunks


def main(req: func.HttpRequest) -> func.HttpResponse:
    trace_id = str(uuid.uuid4())
    logging.info(f"[{trace_id}] Start obsługi upload_doc")

    try:
        if req.headers.get("Content-Type", "").startswith("application/pdf"):
            temp_pdf = NamedTemporaryFile(delete=False, suffix=".pdf")
            temp_pdf.write(req.get_body())
            temp_pdf.close()
            logging.info(f"[{trace_id}]  Plik PDF zapisany tymczasowo: {temp_pdf.name}")

            chunks = split_pdf(temp_pdf.name)
            os.unlink(temp_pdf.name)
            logging.info(f"[{trace_id}]  Podzielono PDF na {len(chunks)} chunków")

        else:
            data = req.get_json()
            content = data.get("content")
            if not content:
                return func.HttpResponse("Brak treści dokumentu.", status_code=400)

            splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
            chunks = splitter.split_documents([Document(page_content=content)])
            logging.info(f"[{trace_id}] Podzielono TXT na {len(chunks)} chunków")

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

        vectorstore.add_documents(chunks, include_metadata=False)
        logging.info(f"[{trace_id}] Dokument został zaindeksowany w Azure Search")

        return func.HttpResponse(
            json.dumps(
                {
                    "message": "Dokument przetworzony i dodany do indeksu!",
                    "trace_id": trace_id,
                }
            ),
            mimetype="application/json",
        )

    except Exception as e:
        logging.error(f"[{trace_id}] Błąd w funkcji upload_doc:")
        logging.error(traceback.format_exc())
        return func.HttpResponse(
            f"Błąd serwera (trace_id: {trace_id}): {str(e)}", status_code=500
        )
