import os

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings


load_dotenv()

llm = AzureChatOpenAI(
    azure_endpoint=os.getenv("API_BASE"),
    api_key=os.getenv("API_KEY"),
    api_version=os.getenv("API_VERSION"),
    deployment_name=os.getenv("DEPLOYMENT_NAME"),
    temperature=0.7,
)

embeddings = AzureOpenAIEmbeddings(
    azure_endpoint=os.getenv("API_BASE"),
    api_key=os.getenv("API_KEY"),
    api_version=os.getenv("API_VERSION"),
    deployment=os.getenv("DEPLOYMENT_NAME_FOR_EMBLEDDING"),
)

search_client = SearchClient(
    endpoint=os.getenv("URL_RAG"),
    index_name=os.getenv("INDEX_NAME"),
    credential=AzureKeyCredential(os.getenv("API_KEY_SEARCH")),
)

prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template="""Odpowiadaj na pytania wyłącznie na podstawie dostarczonego kontekstu.

Kontekst:
{context}

Pytanie: {question}

Odpowiedź:""",
)


def ask_rag(query: str):
    """Main RAG function that takes query and returns answer"""

    query_vector = embeddings.embed_query(query)

    results = search_client.search(
        search_text=query,
        vector_queries=[
            VectorizedQuery(
                vector=query_vector, k_nearest_neighbors=3, fields="content_vector"
            )
        ],
        select=["id", "content"],
    )

    context = "\n".join([doc["content"] for doc in results])

    prompt = prompt_template.format(context=context, question=query)

    response = llm.invoke(prompt)

    print(f"Pytanie: {query}")
    print(f"Odpowiedź: {response.content}")

    return {"question": query, "answer": response.content, "context": context}
