from typing import List, Union
from dotenv import load_dotenv
from fastapi import FastAPI
from langserve import add_routes
from pydantic import BaseModel, Field
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from src.graphs import chatbot
load_dotenv()
from src.llm import llm
app = FastAPI()

class InputChat(BaseModel):
    """Input for the chat endpoint."""

    messages: List[Union[HumanMessage, AIMessage, SystemMessage]] = Field(
        ...,
        description="The chat messages representing the current conversation.",
    )

add_routes(app, chatbot.compiled_runnable(llm).with_types(input_type=InputChat), path='/chat', playground_type="default")

from fastapi.middleware.cors import CORSMiddleware

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)