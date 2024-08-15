import directories
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

openai_embedding = OpenAIEmbeddings(model="text-embedding-3-small")

mydata_api_docs_chroma = Chroma(
    persist_directory=str(directories.mydata_api_docs_chromadb),
    embedding_function=openai_embedding,
    collection_metadata={"hnsw:space": "cosine"},
)

mydata_guideline_docs_chroma = Chroma(
    persist_directory=str(directories.mydata_guideline_docs_chromadb),
    embedding_function=openai_embedding,
    collection_metadata={"hnsw:space": "cosine"},
)

mydata_other_docs_chroma = Chroma(
    persist_directory=str(directories.mydata_other_docs_chromadb),
    embedding_function=openai_embedding,
    collection_metadata={"hnsw:space": "cosine"},
)
