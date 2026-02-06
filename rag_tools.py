import os
import json
from rag import get_query_engine
from dotenv import load_dotenv

load_dotenv()

RETRIEVE_CANDIDATES_CACHE_FILE = os.getenv("RETRIEVE_CANDIDATES_CACHE_FILE")

query_engine = get_query_engine(top_k=5)

def search_knowledge_base_tool(query: str) -> str:
	"""
	Search the resume knowledge base and return relevant candidate information.

	Use this tool for queries about candidate location, skills, experience, roles, education,
	or other resume-specific details. Provide a focused, descriptive query to
	improve retrieval quality.

	Args:
		query: A detailed search query describing the candidate information needed.

	Returns:
		A string with the most relevant candidate information found.
	"""

	response = query_engine.query(query)
	
	return str(response)

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
		with open(RETRIEVE_CANDIDATES_CACHE_FILE, "r") as f:
			return json.load(f)
	
	# retrieve candidates from knowledge base
	candidates = retrieve_candidates()
	
	# Save to cache file
	with open(RETRIEVE_CANDIDATES_CACHE_FILE, "w") as f:
		json.dump(candidates, f, indent=2)
	
	return candidates

def get_candidate_details_by_identifier(identifier: str) -> str:
	response = query_engine.query(f"""
		Provide detailed information about the candidate {identifier} 
		based on the resume stored in the knowledge base.

		Retrieve:
		- Location and contact information;
		- Professional summary;
		- Skill highlights (up to 10 key skills);
		- Professional experience;
		- Education and Certifications;
		- Languages and special skills;
		- Skip name as it's already provided.

		Format:
		- Keep markdown format for better readability.
		- For headings use next example: "##### Heading example".
		- Bullet points where appropriate.
	""")

	return str(response)
