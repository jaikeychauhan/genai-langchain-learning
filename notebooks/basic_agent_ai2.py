from dotenv import load_dotenv
load_dotenv()                           

from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

@tool
def add_numbers(a:int, b:int):
    """
        it will return the sum of two nubers
        Args:
            a: Number one
            b: Number two
    """
    return a+b

@tool
def multiply_numbers(a:int, b:int):
    """
        it will return the product of two nubers
        Args:
            a: Number one
            b: Number two
    """
    return a*b

llm=ChatOpenAI(model="gpt-4o-mini")
agent=create_agent(
    model=llm,
    tools=[add_numbers, multiply_numbers],
    system_prompt="""
                You are a math teacher.

                IMPORTANT:
                - You MUST use the appropriate tool for every mathematical calculation.
                - Never calculate addition or multiplication yourself.
                - For addition, ALWAYS call add_numbers.
                - For multiplication, ALWAYS call multiply_numbers.
                """
)
response=agent.invoke({"messages":[
            {"role":"user","content":"what is 2 + 3 * 5?"}]}
        )

# for res in response['messages']:
#     print(res)
#     print("\n")

print(response['messages'][-1].content)