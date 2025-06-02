from sys import exit
from os import getenv
from tools import tools
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv

load_dotenv()
    
# variable definitions
try:
    url = getenv("VIDEO_LINK")
except:
    print("\nPlease enter a YouTube video link in the environment.\n")
    exit(1)
try:
    api_key = getenv("API_KEY")
except:
    print("\nPlease enter your Anthropic API Key in the environment.\n")
    exit(1)

# LLM setup
llm = ChatAnthropic(
    model="claude-3-5-sonnet-20240620",
    api_key=api_key,
    verbose=True
)
llm_with_tools = llm.bind_tools(tools)
messages = []
messages.append(SystemMessage(content=f"The YouTube video to work with is: {url}"))

# functions
def exit_chat():
    print("\n\nGoodbye!\n")
    exit(0)
    
def query():
    try:
        user_input = input("Enter Query (enter 'quit' or 'exit' to quit the program, or press Ctrl+C): ")
    except KeyboardInterrupt:
        exit_chat()

    if user_input.lower() == "quit" or user_input.lower() == "exit":
        exit_chat()
    
    return user_input

def call_claude(prompt) -> AIMessage:
    """Call the LLM with the given prompt and return the response.
    returns: AIMessage
    """

    messages.append(HumanMessage(prompt))
    ai_msg: AIMessage = llm_with_tools.invoke(messages)  # type: ignore
    messages.append(ai_msg)
    return ai_msg


def select_tool(tool_name: str):
    toolMap = dict()
    for tool in tools:
        toolMap[tool.name] = tool

    return toolMap[tool_name]

def print_response(content):
    if isinstance(content, str):
        print(f"\n{content}\n")
    elif isinstance(content, list):
        print("\n" + "\n".join(
            part['text'] if part['type'] == 'text' else f"[{part['type']}: {part.get('name', '')}]" 
            for part in content
        ) + "\n")
    else:
        print(f"\n{str(content)}\n")