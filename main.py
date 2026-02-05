import os
import json
import asyncio
import streamlit as st
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.llms.openai import OpenAI
from llama_index.tools.tavily_research import TavilyToolSpec
from dotenv import load_dotenv
from rag import get_query_engine

load_dotenv()

RETRIEVE_CANDIDATES_CACHE_FILE = os.getenv("RETRIEVE_CANDIDATES_CACHE_FILE")
MODEL = os.getenv("MODEL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

tavily_tool = TavilyToolSpec(api_key=TAVILY_API_KEY)
search_tools = tavily_tool.to_tool_list()

def retrieve_candidates() -> list[dict]:
	response = get_query_engine(top_k=30).query("""
		You are an AI assistant helping to extract information from resumes stored in a knowledge base.
		Provide list of candidates in JSON format with next structure:
		{
			"candidates": [
				{
					"name": "Candidate Name",
					"profession": "Candidate Profession",
					"experience_in_years": "Number of years of experience from the beginning of the career.",
					"summary": "Brief summary of the candidate's strongest skills and professional highlights",	
				},
				...
			]
		}
		Ensure the information is accurate and based solely on the data available in the resumes.
	""")

	data: dict = json.loads(str(response))	

	return data.get("candidates", [])


def get_candidates() -> list[dict]:
	# Check if cache file exists
	if os.path.exists(RETRIEVE_CANDIDATES_CACHE_FILE):
		print(f"Loading candidates from cache: {RETRIEVE_CANDIDATES_CACHE_FILE}")
		
		with open(RETRIEVE_CANDIDATES_CACHE_FILE, "r") as f:
			return json.load(f)
	
	# retrieve candidates from knowledge base
	candidates = retrieve_candidates()
	
	# Save to cache file
	with open(RETRIEVE_CANDIDATES_CACHE_FILE, "w") as f:
		json.dump(candidates, f, indent=2)
	
	return candidates

def candidates_retrieve_data_tool(query: str) -> str:
	"""
	Retrieve information about candidates based on the query from knowledge base.

	"""
	print(f"candidates_retrieve_data_tool called with query: {query}")

	response = get_query_engine(top_k=5).query(query)

	print(f"candidates_retrieve_data_tool response: {str(response)}")	
	
	return str(response)

def get_chat_agent() -> FunctionAgent:
	llm = OpenAI(
		model=MODEL,
		api_key=OPENAI_API_KEY,
		temperature=1,
	)

	chat_agent = FunctionAgent(  
    llm=llm,
		tools=[candidates_retrieve_data_tool] + search_tools,
    system_prompt="""
			You are a recruitment assistant AI specializing in candidate analysis and recruitment insights.
			Your primary responsibility is to help users find and evaluate candidates from a resume database and provide relevant professional information.

			TOOL USAGE GUIDELINES:
			- Use the candidates_retrieve_data_tool FIRST for all candidate-related queries (names, experience, skills, qualifications)
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

	return chat_agent

def get_contexual_chat_input(chat_input: str, N = 10) -> str:
	# Build context from last N messages (e.g., last 10 messages)
	N = 10
	recent_messages = st.session_state.messages[-(N+1):-1] if len(st.session_state.messages) > 1 else []
	
	contexual_chat_input = ""
	if recent_messages:
		contexual_chat_input = "Previous conversation:\n"
		for msg in recent_messages:
			contexual_chat_input += f"{msg['role'].capitalize()}: {msg['content']}\n"
		contexual_chat_input += f"\nCurrent message: {chat_input}"
	else:
		contexual_chat_input = chat_input
	
	return contexual_chat_input

async def render_candidates() -> None:
	query_engine = get_query_engine()

	with st.spinner("Fetching candidates..."):
		candidates = get_candidates()

	# Display candidates
	for idx, candidate in enumerate(candidates):
		with st.container(border=True):
			st.subheader(f"{candidate['name']} — {candidate['profession']}")
			st.caption(f"Experience: {candidate['experience_in_years']} years")
			st.markdown(candidate['summary'])
			
			# Use unique key for each candidate
			expander_key = f"details_{idx}"
			expander_data_key = f"details_data_{idx}"
			
			# Initialize session state for this expander
			if expander_key not in st.session_state:
				st.session_state[expander_key] = False
			
			if expander_data_key not in st.session_state:
				st.session_state[expander_data_key] = None
			
			# Button to toggle details
			if st.button(f"Toggle Details", key=f"btn_{idx}"):
				st.session_state[expander_key] = not st.session_state[expander_key]
			
			# Only execute query if details are shown
			if st.session_state[expander_key]:
				if st.session_state[expander_data_key] is None:
					with st.spinner("Fetching details..."):
						data = query_engine.query(f"""
							Provide detailed information about the candidate {candidate['name']} 
							based on the resumes stored in the knowledge base.
							Focus on key achievements, skills, and experiences that highlight their qualifications 
							for potential job opportunities.
							Skip name as it is already provided.
							Keep markdown format for better readability.
							Use smallest headings and bullet points where appropriate.
						""")
						st.session_state[expander_data_key] = data
				st.markdown(st.session_state[expander_data_key])

async def render_chat() -> None:
	chat_agent = get_chat_agent()

	with st.sidebar:
		st.title("🤖 AI Chatbot")

		if "messages" not in st.session_state:
			st.session_state.messages = []
		
		chat_container = st.container(height=100)

		for msg in st.session_state.messages:
			chat_container.chat_message(msg["role"]).write(msg["content"])
		
		chat_input = st.chat_input()

		if chat_input:
			chat_container.chat_message("user").write(chat_input)
			st.session_state.messages.append({"role": "user", "content": chat_input})

			with chat_container.chat_message("assistant"):
				with st.spinner("Thinking..."):
						# Get the response from the chat agent
						contexual_chat_input = get_contexual_chat_input(chat_input=chat_input)
						response = await chat_agent.run(contexual_chat_input)
						response_str = str(response)
						# Show the final response
						st.write(response_str)
						st.session_state.messages.append({"role": "assistant", "content": response_str})

		# Custom CSS to adjust sidebar
		st.markdown(
			"""
			<style>
				[data-testid="stSidebar"] {
            width: 400px;
        }
				[data-testid="stSidebarCollapseButton"] {
            display: none;
        }
				[data-testid="stSidebarHeader"] {
            display: none;
        }
				[data-testid="stSidebarContent"] {
					display: flex;
					flex-direction: column;
				}
				[data-testid="stSidebarUserContent"] {
					display: flex;
					flex-direction: column;
					flex: 1;
					padding: 0 0 10px 0;
				}
				[data-testid="stSidebarUserContent"] > 
				div {
					height: 100%;
				}
				[data-testid="stSidebarUserContent"] > 
				div > 
				[data-testid="stVerticalBlock"] {
					height: 100%;
				}
				[data-testid="stSidebarUserContent"] > 
				div > 
				[data-testid="stVerticalBlock"] > 
				[data-testid="stLayoutWrapper"] {
					flex: 1 0 auto;
					overflow-y: auto;
				}
				.stMainBlockContainer  {
					padding-top: 0;
				}
				.stAppHeader {
					display: none;
				}
			</style>
			""",
			unsafe_allow_html=True,
		)
	
async def main():
	print("Starting Resume Analyzer app...")

	st.set_page_config(layout="wide")
	st.title("Resume Analyzer")

	await render_candidates()
	await render_chat()

	print("Resume Analyzer app rendered.")
	
if __name__ == "__main__":
	asyncio.run(main())
