import asyncio
from agent import ask_agent

async def main():
	LINUX_TORVALDS_STORY = """
		Linus Torvalds has played a defining role in modern software development through his creation 
of the Linux kernel, a foundational technology that underpins countless servers, mobile devices, 
and embedded systems worldwide. His engineering approach emphasized transparency, modularity, 
and rigorous peer review, helping establish practices that shaped open-source development at scale. 
Torvalds later introduced Git, a distributed version-control system that revolutionized how 
developers collaborate by enabling fast branching, parallel experimentation, and resilient code 
management. Together, Linux and Git fostered a global culture of decentralized innovation, 
empowering individuals and organizations to contribute to shared infrastructure while maintaining 
high standards of code quality. His influence continues to guide industry norms around 
collaboration, reliability, and open technical ecosystems.
	"""
	prompt = f"""
		**Role**: You are a technical historian and software engineering writer.
		**Tone**: Dramatic, suspenseful, and Shakespearean.

		**LINUX_TORVALDS_STORY**:
		{LINUX_TORVALDS_STORY}
		
		**Task**: 
		- Modify the text LINUX_TORVALDS_STORY to infuse a tone reminiscent of William Shakespeare 's style, 
		emphasizing dramatic and suspenseful elements in Torvalds's journey through the tech industry. 

		**Constraints**:
		- Use archaic language and poetic devices to enhance the dramatic effect.
		- Highlight the challenges and triumphs in Torvalds's career with a sense of grandeur and tension.
		- Maintain the factual accuracy of his contributions while elevating the narrative style.

		**Output Format**: 
		- A single cohesive paragraph of text in English, 8–10 sentences, 180-200 words.
		- Add meaningful line breaks, so lines should not be more than 100 characters long. 
	"""

	response = await ask_agent(prompt)
	
	print(f"Agent response: \n {response}")

if __name__ == "__main__":
	asyncio.run(main())
