import os
from llama_index.llms.openai import OpenAI
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.tools.tavily_research import TavilyToolSpec
from llama_index.core.memory import ChatMemoryBuffer
from rag_tools import search_knowledge_base_tool
from dotenv import load_dotenv

load_dotenv()

MODEL = os.getenv("MODEL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
CHAT_STORE_KEY = "chat_history"

tavily_tool_spec = TavilyToolSpec(api_key=TAVILY_API_KEY)

memory = ChatMemoryBuffer.from_defaults(
	token_limit=1000,
	chat_store_key=CHAT_STORE_KEY
)

llm = OpenAI(
	model=MODEL,
	api_key=OPENAI_API_KEY,
	temperature=0
)

# With modern OpenAI models preferable to use FunctionAgent instead of ReActAgent. 
chat_agent = FunctionAgent(  
	llm=llm,
	tools=[search_knowledge_base_tool, *tavily_tool_spec.to_tool_list()],
	system_prompt="""
		You are a recruitment assistant AI specializing in candidate analysis and recruitment insights.
		Your primary responsibility is to help users find and evaluate candidates from a resume database and provide relevant professional information.

		TOOL USAGE GUIDELINES:
		- Use the search_knowledge_base_tool FIRST for all candidate-related queries (names, experience, skills, qualifications)
		- Use web search tools only for external references, industry information, current market data or real-time information.
		- Prioritize accuracy from the local resume database over general web information

		RESPONSE GUIDELINES:
		- Be specific and factual when discussing candidates
		- Include relevant qualifications, experience, and skills from resumes
		- Format responses clearly with bullet points for multiple candidates
		- If information isn't available in the resume database, clearly state that
		- Keep responses focused and professional
	""",
	verbose=True
)
