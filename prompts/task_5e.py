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
		Based on the results of the three meetings, write a single letter addressed to all participants. 
		The tone should be optimistic and businesslike. The letter must:
		- Summarize the meetings
		- State the next steps to be taken
		- Thank each participant by name and specify for what they should be thanked 
			(e.g., "Thank you, Alice, for your insightful analysis of the data.", 
			"Appreciate your support, Bob, in moving the project forward.", 
			"Charlie, your critical feedback was invaluable, thank you.")
		- Indicate the date of the next meeting after two weeks from the last meeting.

		**Constraints**:
		- Base the letter strictly on the transcript content.
		- If the next meeting date is not mentioned, state "not specified in the transcript".
		- Keep the letter between 300 and 500 words.
		- Use complete sentences and a professional sign-off.

		**Output Format**:
		Use bullets list format for thanks block.
		Use the following markdown format for the letter:
		Subject: <letter subject>
		<full letter text>
	"""

	response = await ask_agent(prompt)
	
	print(f"Agent response: \n {response}")

if __name__ == "__main__":
	asyncio.run(main())
