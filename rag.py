import os
import chromadb
from chromadb import PersistentClient, Collection
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.base.base_query_engine import BaseQueryEngine
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_BASE = os.getenv("API_BASE")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
MODEL = os.getenv("MODEL")

CHROMA_PATH = os.getenv("CHROMA_PATH")
CHROMA_COLLECTION = os.getenv("CHROMA_COLLECTION")

def get_collection() ->Collection:
	chroma_client = PersistentClient(path=CHROMA_PATH)
	chroma_collection = chroma_client.get_or_create_collection(name=CHROMA_COLLECTION)
	
	return chroma_collection

def get_vector_store() -> ChromaVectorStore:
	chroma_collection = get_collection()
	vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
	
	return vector_store	

def get_store_context() -> StorageContext:
	vector_store = get_vector_store()
	storage_context = StorageContext.from_defaults(vector_store=vector_store)
	
	return storage_context

def get_embed_model() -> OpenAIEmbedding:
	embed_model = OpenAIEmbedding(
		model=EMBEDDING_MODEL,
		api_key=OPENAI_API_KEY,
		# api_base=API_BASE,
		# embed_batch_size=1
	)

	return embed_model

def populate():
	print("Populating knowledge base...")
	
	reader = SimpleDirectoryReader(input_dir=".resumes", required_exts=[".txt"], exclude_hidden=False)
	documents = reader.load_data()

	print(f"Loaded {len(documents)} documents.")

	splitter = SentenceSplitter(chunk_size=1024, chunk_overlap=100)
	nodes = splitter.get_nodes_from_documents(documents, show_progress=True)
	
	storage_context = get_store_context()
	embed_model = get_embed_model()
	
	index = VectorStoreIndex(
			nodes=nodes,
			storage_context=storage_context,
			embed_model=embed_model
	)

	print(f"Knowledge base populated. {index.index_id} created with {len(nodes)} nodes.")

def get_query_engine(top_k=5) -> BaseQueryEngine:
	vector_store = get_vector_store()
	embed_model = get_embed_model()
	index = VectorStoreIndex.from_vector_store(
			vector_store=vector_store,
			embed_model=embed_model,
	)
	llm = OpenAI(
		model=MODEL,
		api_key=OPENAI_API_KEY,
		temperature=0
	)
	query_engine = index.as_query_engine(
		llm=llm,
		similarity_top_k=top_k,
		response_mode="compact",
	)

	return query_engine

if __name__ == "__main__":
	populate()
