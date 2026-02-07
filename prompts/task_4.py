import asyncio
from agent import ask_agent

async def main():
	prompt = f"""
		**Role**: You are an engineering manager providing performance feedback.

		**Task**: Write a highly polite, constructive letter with negative feedback about a
		software developer’s performance. Clearly describe specific mistakes, the impact on
		the project, and the reasons for your concerns. If the draft is not sufficiently
		polite or clear, refine it through several iterations before presenting the final
		letter.

		**Constraints**:
		- Maintain a respectful, supportive tone throughout.
		- Be concrete: include at least 3 specific issues and their impacts.
		- Avoid personal attacks; focus on behavior and outcomes.
		- End with next steps and an offer of support.

		**Output Format**:
		- Provide only the final letter (no analysis).
	"""

	response = await ask_agent(prompt)
	
	print(f"Agent response: \n {response}")

if __name__ == "__main__":
	asyncio.run(main())
