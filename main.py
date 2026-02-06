import asyncio
import streamlit as st
from rag_tools import get_candidates, get_candidate_details_by_identifier
from chat_agent import chat_agent, memory, CHAT_STORE_KEY

async def render_candidates() -> None:
	with st.spinner("Fetching candidates..."):
		candidates = get_candidates()

	# display candidates
	for idx, candidate in enumerate(candidates):
		with st.container(border=True):
			st.subheader(f"{candidate['name']} — {candidate['profession']}")
			st.caption(f"Experience: {candidate['experience_in_years']} years")
			st.markdown(candidate['summary'])
			
			# use unique key for each candidate
			expander_key = f"details_{idx}"
			expander_data_key = f"details_data_{idx}"
			
			# initialize session state for this expander
			if expander_key not in st.session_state:
				st.session_state[expander_key] = False
			
			if expander_data_key not in st.session_state:
				st.session_state[expander_data_key] = None
			
			# button to toggle details
			if st.button(f"Toggle Details", key=f"btn_{idx}"):
				st.session_state[expander_key] = not st.session_state[expander_key]
			
			# only execute query if details are shown
			if st.session_state[expander_key]:
				if st.session_state[expander_data_key] is None:
					with st.spinner("Fetching details..."):
						response = get_candidate_details_by_identifier(candidate['name'])
						st.session_state[expander_data_key] = response
				st.markdown(st.session_state[expander_data_key])

async def render_chat() -> None:
	with st.sidebar:
		st.title("🤖 AI Chatbot")

		chat_container = st.container(height=100)
		messages = memory.chat_store.get_messages(CHAT_STORE_KEY)
		
		# render chat history
		for msg in messages:
			chat_container.chat_message(msg.role.value).write(msg.content)
		
		user_message = st.chat_input()

		# render user message
		if user_message:
			chat_container.chat_message("user").write(user_message)

			# render assistant response message
			with chat_container.chat_message("assistant"):
				with st.spinner("Thinking..."):
						response = await chat_agent.run(user_message, memory=memory)
						assistant_message = str(response)
						st.write(assistant_message)

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
	st.set_page_config(layout="wide")
	st.title("Resume Analyzer")

	await render_chat()
	await render_candidates()
	
if __name__ == "__main__":
	asyncio.run(main())
