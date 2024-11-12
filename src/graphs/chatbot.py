from typing import Literal

from langgraph.graph import END, START, StateGraph, MessagesState
from langgraph.prebuilt import ToolNode
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

from src.tools import tool_list
from langchain_core.messages import AIMessage

def chatbot_graph(model):
    tool_node = ToolNode(tool_list)

    model = model.bind_tools(tool_list)

    # Define the function that determines whether to continue or not
    def should_continue(state: MessagesState) -> Literal["tools", END]:
        messages = state['messages']
        last_message = messages[-1]
        # If the LLM makes a tool call, then we route to the "tools" node
        if last_message.tool_calls:
            return "tools"
        # Otherwise, we stop (reply to the user)
        return END


    # Define the function that calls the model
    def call_model(state: MessagesState):
        messages = state['messages']
        response = model.invoke(messages)
        # We return a list, because this will get added to the existing list
        return {"messages": [response]}


    # Define a new graph
    workflow = StateGraph(MessagesState)

    # Define the two nodes we will cycle between
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", tool_node)

    # Set the entrypoint as `agent`
    # This means that this node is the first one called
    workflow.add_edge(START, "agent")

    # We now add a conditional edge
    workflow.add_conditional_edges(
        # First, we define the start node. We use `agent`.
        # This means these are the edges taken after the `agent` node is called.
        "agent",
        # Next, we pass in the function that will determine which node is called next.
        should_continue,
    )

    # We now add a normal edge from `tools` to `agent`.
    # This means that after `tools` is called, `agent` node is called next.
    workflow.add_edge("tools", 'agent')

    return workflow

def compiled_runnable(llm):
    return chatbot_graph(llm).compile() | RunnableLambda(lambda x: x['agent']['messages'][-1].content)