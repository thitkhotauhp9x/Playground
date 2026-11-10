from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from app.libs.playground.tools.python.tool import execute_python


def test_python_tool():
    chat = ChatOpenAI(model="gpt-4o-mini")
    agent = create_agent(chat, tools=[execute_python])
    response = agent.invoke({"messages": "Kết quả của việc cộng 2 và 3 using python tool."})
    message = response["messages"][-1]
    print(message)
