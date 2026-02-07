import asyncio
from agent import ask_agent

async def main():
	prompt = """
		**Role**: You are a technical historian and software engineering writer.
		
		**Tone**: Clear, factual, and professional.
		
		**Task**: Generate a paragraph in English about Linus Torvalds 
		contributions to software development and technology innovation.

		**Constraints**:
		- Avoid excessive biographical details (birthplace, early life)
		- Stick to his technical and cultural impact on industry standards.
		- Focus on Linux kernel, Git, and open-source collaboration.

		**Output Format**: 
		- A single cohesive paragraph of text in English, 4–6 sentences, 120-150 words.
		- Add meaningful line breaks, so lines should not be more than 100 characters long. 
	"""

	response = await ask_agent(prompt)
	
	print(f"Agent response: \n {response}")

if __name__ == "__main__":
	asyncio.run(main())
