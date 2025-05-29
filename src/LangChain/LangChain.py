import os

from dotenv import load_dotenv
from langchain_community.vectorstores import AzureSearch
from langchain_core.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings

from langchain.chains import RetrievalQA


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

vectorstore = AzureSearch(
    azure_search_endpoint=os.getenv("URL_RAG"),
    azure_search_key=os.getenv("API_KEY_SEARCH"),
    index_name=os.getenv("INDEX_NAME"),
    embedding_function=embeddings,
    fields={"content": "content", "vector": "content_vector"},
)

retriever = vectorstore.as_retriever()

prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template="""Odpowiadaj na pytania wyłącznie na podstawie dostarczonego kontekstu.

Kontekst:
{context}

Pytanie: {question}

Odpowiedź:""",
)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff",
    chain_type_kwargs={"prompt": prompt_template},
)


def ask_rag(query: str):
    """Zadaje pytanie do systemu RAG i zwraca odpowiedź"""
    result = qa_chain.invoke({"query": query})

    print(f"Pytanie: {query}")
    print(f"Odpowiedź: {result['result']}")
    return result


if __name__ == "__main__":
    query = "O czym jest ten dokument?"
    result = ask_rag(query)
