This assessment will validate the learner's ability apply LlamaIndex

Loading CV Files: This involves reading CV files from
https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset
You can choose up to 20-30 CVs.

---------------------------------------------------
Bad quality of resumes in the dataset, let's generate it

Generate Chef resume include:

Title: for example CHEF, EXECUTIVE CHEF, CHEF INSTRUCTOR
Name
Summary - up to 500 words
Skill Highlights - up to 20
Experience - 3 -5 companies

save to txt file and put to .resume folder

------------------------------------------------------

- Split CV into small meaningful chunks.

- Generating Embeddings: Convert the parsed data into numerical representations
(embeddings) that can be easily processed by machine learning algorithms. This typically
involves using techniques like word embeddings or sentence embeddings.
Storing Embeddings in a Vector Database: Save the generated embeddings into a vector
database. As a vector store, you can choose PostgreSQL, ChromaDB, FAISS, etc,

- Retrieving Candidate Details: Extract and display specific information about each
candidate, such as name, profession, and years of commercial experience.

- Generating Experience Summary: Based on the parsed data and embeddings, generate a
summary of each candidate’s strongest skills and professional highlights.

- Important note:
The task should be done using LlamaIndex.

- Expected outcome:
The repository contains a straightforward web application that lists candidates. Users can click on
any candidate to view detailed information and a summary of their profile.

------------------------------------------------------------------

Enhancing the Resume Analysis System with a ReAct Agent
Extend your existing resume analysis system (from LlamaIndex first practical task) by integrating
a ReAct (Reasoning and Acting) agent using LlamaIndex. This agent will interact with multiple tools,
including a retrieval tool powered by pgvector, to answer user queries about candidates and engage
in broader conversations.
Instructions:

Implement the Retrieval Tool:
a. Develop a tool that connects to your vector database and retrieves relevant candidate
information based on user queries.
b. Ensure the tool returns concise summaries or key information from the retrieved data.
Develop Additional Tools:
a. Create at least two more tools to enhance the agent's capabilities.
Examples include:
• General Knowledge Tool: Allows the agent to answer general questions
unrelated to the resumes, enabling broader conversations.
• One of Pre-Build tools:
https://docs.llamaindex.ai/en/stable/community/integrations/
Integrate the ReAct Agent:
a. Utilize LlamaIndex to build an agent that processes user inputs, determines which
tool(s) to use, and formulates appropriate responses.
b. Incorporate all developed tools into the agent's toolkit, allowing it to fetch
information and perform analyses as needed





