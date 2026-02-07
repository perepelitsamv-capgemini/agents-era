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
		- Perform a self-assessment for each meeting in the transcript. 
		- For every meeting: 
			- identify what it was about, 
			- who participated, 
			- what decisions were made,
			- top 3 insights, 
			- top 3 challenges.

		**Constraints**:
		- Use only information from the transcript.
		- If any item is unclear, write "Unknown" and add a short rationale.
		- Keep each insight and challenge to one short sentence.

		**Output Format**:
		Return a markdown section per meeting using this template:
		### Meeting <number>
		- Topic: <one sentence>
		- Participants: <comma-separated names>
		- Decisions: <bullet list>
		- <numerical list insights>
		- <numerical list challenges>
	"""

	response = await ask_agent(prompt)
	
	print(f"Agent response: \n {response}")

if __name__ == "__main__":
	asyncio.run(main())
