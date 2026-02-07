import asyncio
from agent import ask_agent

async def main():
	prompt = f"""
		**Role**: You are a technical quiz author.

		**Task**:
		Using the Wikipedia article about Go (https://en.wikipedia.org/wiki/Go_(programming_language)), 
		create a comprehensive English-language quiz about the Go programming language.
		The quiz should contain 10 questions total and include a mix of:
		- Questions with one correct answer
		- Questions with multiple correct answers
		Questions must cover a variety of topics from the article, including Go’s history, features, design goals, syntax, and typical use cases.

		**Constraints**:
		- Base all questions and answers strictly on the Wikipedia article.
		- Provide exactly 4 answer options for each question.
		- Clearly indicate the correct answer(s) for each question.
		- Ensure at least 3 questions are multiple-correct.
		- Avoid ambiguous or trick questions.

		**Output Format**:
		Return JSON with the following structure:
		{{
		  "questions": [
		    {{
		      "id": N,
		      "type": "single | multiple",
		      "question": "...",
		      "options": ["A", "B", "C", "D"],
		      "correct_answers": ["A"]
		    }}
		  ]
		}}
	"""

	response = await ask_agent(prompt)
	
	print(f"Agent response: \n {response}")

if __name__ == "__main__":
	asyncio.run(main())
