from dotenv import load_dotenv
load_dotenv()           

from pydantic import BaseModel
from langgraph.graph import StateGraph,START,END
from langchain_groq import ChatGroq
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver
from typing import Annotated

class ChatState(BaseModel):
    messages:Annotated[list,add_messages]

llm=ChatGroq(model="openai/gpt-oss-20b")

def chatBotNode(state:ChatState)->ChatState:
    res=llm.invoke(state.messages)
    state.messages=[res]
    return state

memory=InMemorySaver()

graph=StateGraph(ChatState)
graph.add_node("chatbot",chatBotNode)

graph.add_edge(START,"chatbot")
graph.add_edge("chatbot",END )

graph=graph.compile(checkpointer=memory)

config={"configurable":{"thread_id":"1"}}

while True:
    question=input("User: ")
    if(question.lower() in ["quit","q","exit","e"]):
        print("Bye")
        break

    res=graph.invoke(
        {"messages":[{"role":"user","content":question}]},
        config=config
    )

    result=res["messages"][-1].content
    print("AI: ",result)