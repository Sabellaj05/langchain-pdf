#!usr/bin/env python
from typing import List
from dotenv import load_dotenv

from fastapi import FastAPI
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.tools.retriever import create_retriever_tool
from langchain.agents import create_openai_tools_agent
from langchain.agents import AgentExecutor
from langchain.pydantic_v1 import BaseModel, Field
from langserve import add_routes

# api keys
load_dotenv()

## Load the retriever
loader = WebBaseLoader("https://www.coololdgames.com/tile-games/mahjong/japanese-riichi/")
docs = loader.load()
text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(docs)
embeddings = OpenAIEmbeddings()
vector = FAISS.from_documents(documents, embeddings)
retriever = vector.as_retriever()

## Create the tools

retriever_tool = create_retriever_tool(
    retriever,
    "mahjong_riichi_search",
    "Search for information about Mahjong Riichi, for any question about Mahjong Riichi you must use this tool!"
)

search = TavilySearchResults()

tools = [retriever_tool, search]

## Create the agent

prompt = hub.pull("hwchase17/openai-tools-agent") # look into this
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
agent = create_openai_tools_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

## Define the App

app = FastAPI(
    title="LangChain Server",
    version="0.1.0",
    description="Simple API Server to run an Agent using LangChain's Runnable iterface"
)

## Adding chain route

# the input/outputt schemas are required because the
# AgentExecutor is lacking in schemas (schemaless)

class Input(BaseModel):
    input: str
    chat_history: List[BaseMessage] = Field(
        ...,
        extra={"widget": {"type": "chat", "input": "location"}}
    )

class Output(BaseModel):
    output: str

add_routes(
    app,
    agent_executor.with_types(
        input_type=Input,
        output_type=Output
    ),
    path="/agent"
)

if __name__ == "__main__":
    try:
        import uvicorn
    except Exception as e
        print(f"Importing error: {e}")
    uvicorn.run(app, host="localhost", port=8000)
