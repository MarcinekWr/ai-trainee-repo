import os
from typing import TypedDict

from dotenv import load_dotenv
from langchain_community.vectorstores import AzureSearch
from langchain_core.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langgraph.graph import StateGraph

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


class RagState(TypedDict):
    input: str
    output: str


def rag_node(state: RagState) -> RagState:
    result = qa_chain.invoke({"query": state["input"]})
    return {"input": state["input"], "output": result["result"]}


def translate_node(state: RagState) -> RagState:
    translation_prompt = (
        f"Translate the following answer to English:\n\n{state['output']}"
    )
    result = llm.invoke(translation_prompt)
    return {"input": state["input"], "output": result.content}


graph = StateGraph(RagState)
graph.add_node("rag", rag_node)
# graph.add_node("translate", translate_node)

graph.set_entry_point("rag")
# graph.add_edge("rag", "translate")
# graph.set_finish_point("translate")
graph.set_finish_point("rag")

graph = graph.compile()
