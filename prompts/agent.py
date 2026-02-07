import os
import asyncio
from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

MODEL = os.getenv("MODEL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm = OpenAI(
	model=MODEL,
	api_key=OPENAI_API_KEY,
)

agent = ReActAgent(
		llm=llm,
		verbose=True
)

async def ask_agent(user_prompt: str) -> str:
	response = await agent.run(user_prompt)
	
	return str(response)
