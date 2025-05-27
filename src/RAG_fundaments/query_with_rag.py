import json
import os
from pathlib import Path

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery
from dotenv import load_dotenv
from index_pdf_to_azure_free import get_embedding
from openai import AzureOpenAI


load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("API_KEY"),
    api_version=os.getenv("API_VERSION"),
    azure_endpoint=os.getenv("API_BASE"),
)

deployment = os.getenv("DEPLOYMENT_NAME")

search_client = SearchClient(
    endpoint=os.getenv("URL_RAG"),
    index_name=os.getenv("INDEX_NAME"),
    credential=AzureKeyCredential(os.getenv("API_KEY_SEARCH")),
)


def get_rag_response(query: str, search_results):
    context = "\n".join([doc["content"] for doc in search_results])

    messages = [
        {
            "role": "system",
            "content": "Odpowiadaj na pytania wyłącznie na podstawie dostarczonego kontekstu.",
        },
        {"role": "user", "content": f"Kontekst:\n{context}\n\nPytanie: {query}"},
    ]

    response = client.chat.completions.create(
        model=deployment, messages=messages, temperature=0.7
    )

    return response.choices[0].message.content


query = "O czym jest ten dokument?"

query_vector = get_embedding(query)

results = search_client.search(
    search_text=query,
    vector_queries=[
        VectorizedQuery(
            vector=query_vector, k_nearest_neighbors=3, fields="contentVector"
        )
    ],
    select=["id", "content"],
)

results_list = list(results)
vector_results_json = [doc for doc in results_list]

answer = get_rag_response(query, results_list)

print("Odpowiedź RAG z embeddingiem:\n", answer)

output_path = Path("notebooks/queries.ipynb")
output_path.parent.mkdir(parents=True, exist_ok=True)


def append_cell_to_notebook(cell_content: str, notebook_path: str):
    notebook_file = Path(notebook_path)

    if not notebook_file.exists():
        notebook = {
            "cells": [],
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3",
                    "language": "python",
                    "name": "python3",
                },
                "language_info": {"name": "python"},
            },
            "nbformat": 4,
            "nbformat_minor": 5,
        }
    else:
        with open(notebook_file, "r", encoding="utf-8") as f:
            notebook = json.load(f)

    new_cell = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": cell_content.splitlines(),
    }

    notebook["cells"].append(new_cell)

    with open(notebook_file, "w", encoding="utf-8") as f:
        json.dump(notebook, f, ensure_ascii=False, indent=2)

    print(f"Dopisano komórkę do {notebook_path}")


cell_code = f"""# Zapytanie (embedding): {query}
vector_results = {json.dumps(vector_results_json, indent=2, ensure_ascii=False)}
print("Vector search results:", vector_results)

answer = \"\"\"{answer}\"\"\"
print("RAG answer (vector-based):", answer)
"""

append_cell_to_notebook(cell_code, str(output_path))
