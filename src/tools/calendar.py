from langchain.tools import tool
from datetime import datetime

@tool
def date():
    """A tool to get the current time, since your training time would no longer be current"""
    return str(datetime.now())