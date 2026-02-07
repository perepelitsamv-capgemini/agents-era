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
		- Analysis of the meetings in the project transcript. 
		- Determine the likely specialization/role of each participant based on what they say and do. 
		- Create a list of meeting participants with their names and inferred specialization.

		**Constraints**:
		- Infer roles only from evidence in the transcript.
		- If unsure, mark specialization as "Unknown" and add a short rationale.
		- Do not invent participants not present in the transcript.

		**Output Format**:
		Return list with next structure:
		Member of the meeting:
		- <Name>: <Inferred Specialization> (short evidence)
	"""

	response = await ask_agent(prompt)
	
	print(f"Agent response: \n {response}")

if __name__ == "__main__":
	asyncio.run(main())
