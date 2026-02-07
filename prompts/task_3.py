import asyncio
from agent import ask_agent

async def main():
	LINUX_TORVALDS_STORY = """
		In the dawning age of digital creation, when the realm of machines was ruled by 
fractured kingdoms of code, there arose Linus Torvalds, a quiet architect whose hands shaped 
the fate of countless devices. With steadfast resolve, he forged the Linux kernel, a mighty 
foundation upon which servers, mobiles, and humble embedded spirits found their enduring power. 
Yet his journey was not without tempest, for he championed transparency and modular craft where 
others clung to shadowed halls. Through rigorous peer review, he summoned forth a fellowship of 
developers, their minds united in open purpose. And lo, in later years, he unveiled Git, a 
distributed marvel that broke the tyranny of tangled histories and slow collaboration. This tool, 
swift as a falcon and resilient as tempered steel, granted mortals the power to branch and weave 
their works in parallel harmony. Thus did Torvalds kindle a worldwide chorus of decentralized 
innovation, guiding artisans and great houses alike toward shared creation and noble reliability.
	"""
	prompt = f"""
		**Role**: You are a markdown formatter.

		**LINUX_TORVALDS_STORY**:
		{LINUX_TORVALDS_STORY}
		
		**Task**: 
		- Convert the text LINUX_TORVALDS_STORY to Markdown format.
		- Follow next structure:
			- About Linus Torvalds
			- Linux Kernel
			- Git.
			- Summary of his impact.

		**Constraints**:
		- Don't add any additional information, only format the provided text.
		- Use appropriate Markdown syntax for headings, paragraphs, and line breaks.
		- Ensure the output is well-structured and easy to read.

		**Output Format**: 
		- Add meaningful line breaks, so lines should not be more than 100 characters long. 
	"""

	response = await ask_agent(prompt)
	
	print(f"Agent response: \n {response}")

if __name__ == "__main__":
	asyncio.run(main())
