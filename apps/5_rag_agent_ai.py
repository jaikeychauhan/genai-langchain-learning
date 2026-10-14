from dotenv import load_dotenv
load_dotenv()

from langchain_community.document_loaders import PyPDFLoader,PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_groq import ChatGroq
from langchain_community.vectorstores import InMemoryVectorStore
from langchain.agents import create_agent
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
import streamlit as st

### data in st session
if "document_uploaded" not in st.session_state:
    st.session_state.document_uploaded=False

if "agent" not in st.session_state:
    st.session_state.agent=None

if "vectordb" not in st.session_state:
    st.session_state.vectordb=None

if "messages" not in st.session_state:
    st.session_state.messages=[]

def process_docs(path:str):

    # Load the document
    loader=PyPDFDirectoryLoader(path)
    docs=loader.load()

    # -> Split the loaded document
    splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=100)
    splitted_Doc=splitter.split_documents(documents=docs)

    # -> Embedding and Vector DB store
    embeddings=OpenAIEmbeddings(model="text-embedding-3-large")
    vectordb=InMemoryVectorStore.from_documents(
        documents=splitted_Doc,
        embedding=embeddings
    )

    # Now create agent (Need: tool, LLM, Prompt)

    # 1. LLM
    llm=ChatGroq(model="openai/gpt-oss-20b")

    # 2. Tool
    @tool
    def retrival_context(query:str):
        """Retrieve documents relevant to query from the knowledge base."""
        context=""
        docs=vectordb.similarity_search(query=query,k=3)
        for doc in docs:
            context +=doc.page_content +"\n\n"

        return context

    # 3. Prompt
    system_prompt="""
        You are a helpful assistant that answers the questions using retrieved context.
        My knowledge base consists of the details from the uploaded documents.
        ALWAYS use the 'retrival_context' tool for questions requiring external knowledge.
    """

    memory=InMemorySaver()

    # Now create the agent
    agent=create_agent(
        model=llm,
        tools=[retrival_context],
        system_prompt=system_prompt,
        checkpointer=memory
    )
    st.session_state.agent=agent
    st.session_state.document_uploaded=True


### Upload Document secton or pdf files uploader
if not st.session_state.document_uploaded:
    uploaded=st.file_uploader(label="Upload PDF Files", type=["pdf"],accept_multiple_files=True)
    if(uploaded):
        with st.spinner("Processing...."):
            path="./doc_files/"
            for file in uploaded:
                with open(path+file.name,"wb") as f:
                    f.write(file.getvalue())
            process_docs(path)
            st.rerun()



### Chat UI
if st.session_state.document_uploaded and st.session_state.agent:

    for message in st.session_state.messages:
        role=message["role"]
        content=message["content"]
        st.chat_message(role).markdown(content)


    query=st.chat_input("Ask me anthing related to documents")

    if(query):
        st.session_state.messages.append({"role":"user","content":query})
        st.chat_message("user").markdown(query)
        response=st.session_state.agent.invoke(
            {"messages":[{"role":"user","content":query}]},
            {"configurable":{"thread_id":1}}
        )

        result=response["messages"][-1].content
        st.session_state.messages.append({"role":"ai","content":result})
        st.chat_message("ai").markdown(result)
