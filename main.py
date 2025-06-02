from utils import *
from langchain_core.messages import ToolMessage

while True:
    prompt = query()

    ai_msg = call_claude(prompt)

    if not ai_msg.tool_calls:
        print_response(ai_msg.content)
        continue
    else:
        for tool_call in ai_msg.tool_calls:
            selected_tool = select_tool(tool_call["name"])
            tool_output = selected_tool.invoke(tool_call["args"])
            messages.append(ToolMessage(tool_output, tool_call_id=tool_call["id"]))

        ai_msg = llm_with_tools.invoke(messages)
        print_response(ai_msg.content)
        continue