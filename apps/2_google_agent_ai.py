from dotenv import load_dotenv
load_dotenv()

from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver

llm=ChatGroq(model="openai/gpt-oss-20b")
search=GoogleSerperAPIWrapper()
memorySaver=MemorySaver()

agent=create_agent(
    model=llm,
    checkpointer=memorySaver,
    tools=[search.run],
    system_prompt="You are a agent and you can search any question on google."
)

while True:
    question=input("User: ")
    if(question.lower() in ["quit","exit","e","q"]):
        print("Good Bye")
        break

    response=agent.invoke(
            {"messages":[{"role":"user","content":question}]},
            {'configurable':{"thread_id":"1"}}
        )
    print("AI: ",response['messages'])

