## Resume Analyzer (LlamaIndex + Streamlit)

A lightweight resume analysis app 
that builds a vector knowledge base from resume files and provides:

- A candidate list with summaries with ability to get detailed information.
- AI chat assistant that can answer questions about candidates stored in the db and use web search.

### Features

- LlamaIndex-based retrieval with ChromaDB vector store (RAG).
- Streamlit UI with candidate list + details.
- AI chat assistant powered by `FunctionAgent` that uses RAG and Tavily web search.
- Caching of candidate list for faster UI loading.

### Project Structure

- [main.py](main.py) — Streamlit UI (candidates list + chat sidebar).
- [rag.py](rag.py) — Vector store setup and knowledge base population.
- [rag_tools.py](rag_tools.py) — Retrieval tools for candidates and details.
- [chat_agent.py](chat_agent.py) — Chat agent configuration.

### Requirements

- Python 3.12+
- OpenAI API key
- Tavily API key

### Installation

Install uv, sync deps, and activate the venv:

```
uv sync
source .venv/bin/activate
```

### Environment Variables

Create a `.env` file in the project root:
Use `.env_example` as template

### Build the Knowledge Base

Run the population script to index resumes into ChromaDB:

```
python rag.py
```

### Run the App

```
streamlit run main.py
```

### How It Works

- `rag.py` builds a vector index from resumes in `.resumes/`.
- `rag_tools.py` provides:
	- `search_knowledge_base_tool` for candidate queries.
	- `get_candidates()` for the list view.
	- `get_candidate_details_by_identifier()` for detailed profile sections.
- `chat_agent.py` wires a `FunctionAgent` with the retrieval tool and Tavily search.

### Notes

- If you update resumes, rerun `python rag.py` to rebuild embeddings.
- The candidate list is cached at `RETRIEVE_CANDIDATES_CACHE_FILE` for faster load.

### License

MIT
