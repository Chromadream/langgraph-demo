# LangGraph demo

Basic repo demoing LangChain + LangGraph + LangServe integration

## Requirements

* [uv](https://docs.astral.sh/uv/)
* An OpenAI API key
* A Tavily API key: https://tavily.com/

## Installation and running

* run `uv sync` to install dependencies
* copy `.env.sample` to `.env` and add the correct API keys
* run `uv run fastapi dev` for a dev server

## TODO

* [] memory stuff
* [] more complex tools