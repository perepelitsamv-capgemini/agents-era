import asyncio
from pathlib import Path
from llama_index.core import SimpleDirectoryReader
from agent import ask_agent

async def main():
	base_dir = Path(__file__).resolve().parent
	file_path = f"{base_dir}/project_transkript_file.pdf"
	reader = SimpleDirectoryReader(input_files=[file_path])
	documents = reader.load_data()
	project_transcript = "\n".join([doc.text for doc in documents])

	prompt = f"""
		**Role**: You are a meeting analyst.

		**Project Transcript**:
		{project_transcript}

		**Task**:
		Create a concise project description covering:
		- What the project is about
		- What technologies are used (frontend, backend, data storage, etc.)
		- What problems the project has and what is planned for the near future

		**Constraints**:
		- Base the description strictly on the transcript content.
		- If a detail is not mentioned, state it as "not specified in the transcript".
		- Keep the total description under 200 words.

		**Output Format**:
		Return JSON with the following structure:
		{{
		  "project_overview": "1-3 sentences about what the project is about.",
		  "technologies": {{
		    "frontend": "...",
		    "backend": "...",
		    "data_storage": "...",
		    "other": "..."
		  }},
		  "problems": ["..."],
		  "near_future_plans": ["..."]
		}}
	"""

	response = await ask_agent(prompt)
	
	print(f"Agent response: \n {response}")

if __name__ == "__main__":
	asyncio.run(main())
