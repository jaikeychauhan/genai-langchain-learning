from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
import streamlit as st
llm=ChatOpenAI(model="gpt-4o")

st.title("AskBuddy Q and A app")
st.markdown("My QnA with OpenAI and LangChain!")

if "messages"  not in st.session_state:
    st.session_state.messages=[]

for message in st.session_state.messages:
    role=message["role"]
    content=message["content"]
    st.chat_message(role).markdown(content)


query=st.chat_input("Ask Anything ?")
if query:
    st.session_state.messages.append({"role":"user","content":query})
    st.chat_message("user").markdown(query)
    result=llm.invoke(query)
    st.chat_message("ai").markdown(result.content)
    st.session_state.messages.append({"role":"ai","content":result.content})








# while True:
#     query=input("User: ")
#     if query.lower() in ["quit","exit","bye","q","e"]:
#         print("Good Bye")
#         break

#     res=llm.invoke(query)
#     print("AI: ",res.content,"\n")

