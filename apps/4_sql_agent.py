from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain.agents import create_agent  
from sqlalchemy import create_engine,text
from sqlalchemy.engine import URL
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langgraph.checkpoint.memory import InMemorySaver
import streamlit as st

connection_url = URL.create(
    "mssql+pyodbc",
    username="sa",
    password="admin@123",
    host="DESKTOP-NCUSFKU",
    database="my_tasks",
    query={
        "driver": "ODBC Driver 18 for SQL Server",
        "TrustServerCertificate": "yes"
    }
)
engine = create_engine(connection_url)

db = SQLDatabase(engine)
#print(db.get_usable_table_names())
db.run("""
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[tasks]') AND type in (N'U'))
BEGIN
    Create table tasks(
        id int primary key identity(1,1),
        title varchar(100) not null,
        description varchar(max),
        status varchar(100),
        created_at datetime default getdate()
    );
END
""")

model=ChatGroq(model="openai/gpt-oss-20b")
toolkit=SQLDatabaseToolkit(db=db,llm=model)
tools=toolkit.get_tools()
system_prompt="""
You are a task management assistant that interacts with a SQL database containing a tasks table

Task Rules:
1. Limit sql queries to 10 results max with order by created_at desc
2. After create/update/delete, confirm with select query
3. If the user request a list of task, present the output with a structured table format to insure that a clean and organized display in the browser

CRUD Operations:
    INSERT INTO Tasks(title,description,status) --Add in status Pending, In-Progress, complete based on task
    SELECT * FROM Tasks WHERE...LIMIT 10
    UPDATE TASKS SET Status=? Where ID=? or title=?
    DELETE from Tasks where id=? or title=?

Table Schema: id,title,description,status,created_at

"""
#for agent LLM, tools, memory,system_prompt
@st.cache_resource
def get_agent():
    agent=create_agent(
        model=model,
        tools=tools,
        checkpointer=InMemorySaver(),
        system_prompt=system_prompt
    )
    return agent

agent=get_agent()

st.subheader("TaskBot: Manage your Tasks")

if 'messages' not in st.session_state:
    st.session_state.messages=[]

for message in st.session_state.messages:
    st.chat_message(message["role"]).markdown(message["content"])


prompt=st.chat_input("Ask me to manage any task");

#This code is for connecting SQL with Langchain
if prompt:
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role":"user","content":prompt})
    with st.chat_message("ai"):
        with st.spinner("Processing....."):
            response=agent.invoke(
                {"messages":[{ "role":"user","content":prompt}]},
                {"configurable":{"thread_id":"1"}},
            )
            result=response['messages'][-1].content
            st.markdown(result)
            st.session_state.messages.append({"role":"ai","content":result}).