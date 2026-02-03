import os
import json
from dotenv import load_dotenv
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

def main():
	candidates = get_candidates()

	print(f"Response: {candidates}")

if __name__ == "__main__":
    main()
