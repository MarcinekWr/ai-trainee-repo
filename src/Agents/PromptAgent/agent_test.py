from dotenv import load_dotenv


load_dotenv()

import os
from typing import TypedDict

from langchain_openai import AzureChatOpenAI
from langgraph.graph import StateGraph


class AgentState(TypedDict):
    input: str
    output: str


llm = AzureChatOpenAI(
    deployment_name=os.getenv("DEPLOYMENT_NAME"),
    model="gpt-4o",
    api_key=os.getenv("API_KEY"),
    azure_endpoint=os.getenv("API_BASE"),
    api_version=os.getenv("API_VERSION"),
    temperature=0,
)


def agent_node(state: AgentState) -> AgentState:
    prompt = state["input"]
    result = llm.invoke(prompt)
    return {"input": prompt, "output": result.content}


graph = StateGraph(AgentState)
graph.add_node("agent", agent_node)
graph.set_entry_point("agent")
graph.set_finish_point("agent")

graph = graph.compile()
