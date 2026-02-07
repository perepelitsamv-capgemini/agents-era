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
		Create a general summary of all meetings for each participant, including:
		- Participant name
		- A concise summary of what the participant said across all meetings
		- The participant's role in the discussion: idea generator, critic, supporter, or neutral

		**Constraints**:
		- Base the summary strictly on the transcript content.
		- If a role is unclear, mark it as "neutral" and state that evidence is limited.
		- Do not invent names or statements not present in the transcript.
		- Keep each participant summary to 2-4 sentences.

		**Output Format**:
		Return JSON with the following structure:
		{{
		  "participants": [
		    {{
		      "name": "<participant name>",
		      "summary": "<2-4 sentence summary of what the person said across meetings>",
		      "role": "<idea_generator | critic | supporter | neutral>",
		      "role_evidence": "<short justification based on the transcript>"
		    }}
		  ]
		}}
	"""

	response = await ask_agent(prompt)
	
	print(f"Agent response: \n {response}")

if __name__ == "__main__":
	asyncio.run(main())
