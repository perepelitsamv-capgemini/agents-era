import os
import json
from dotenv import load_dotenv
import streamlit as st
from rag import get_query_engine, get_collection

load_dotenv()

RETRIEVE_CANDIDATES_CACHE_FILE = os.getenv("RETRIEVE_CANDIDATES_CACHE_FILE")	

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
	if os.path.exists(RETRIEVE_CANDIDATES_CACHE_FILE):
		print(f"Loading candidates from cache: {RETRIEVE_CANDIDATES_CACHE_FILE}...")
		
		with open(RETRIEVE_CANDIDATES_CACHE_FILE, "r") as f:
			return json.load(f)
	
	candidates = retrieve_candidates()
	
	# Save to cache file
	with open(RETRIEVE_CANDIDATES_CACHE_FILE, "w") as f:
		json.dump(candidates, f, indent=2)
	
	return candidates

def render_candidates():
	query_engine = get_query_engine()

	with st.spinner("Fetching candidates..."):
		candidates = get_candidates()

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
							Provide detailed information about the candidate {candidate['name']} based on the resumes stored in the knowledge base.
							Focus on key achievements, skills, and experiences that highlight their qualifications for potential job opportunities.
							Skip name as it is already provided.
							Keep markdown format for better readability.
							Use smallest headings and bullet points where appropriate.
						""")
						st.session_state[expander_data_key] = data
				st.markdown(st.session_state[expander_data_key])

def main():
	st.set_page_config(page_title="🚀 Candidates Resume Explorer", layout="wide")

	render_candidates()
	

	with st.sidebar:
		st.header("Candidates")
		st.markdown("This application showcases candidate resumes extracted from a knowledge base using RAG architecture.")

		

if __name__ == "__main__":
    main()
