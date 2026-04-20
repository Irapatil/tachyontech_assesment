import os
from config.settings import OPENAI_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
#from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import FakeEmbeddings

embeddings = FakeEmbeddings(size=1536)


DATA_PATH = "data/manuals"
VECTOR_PATH = "vector_store"

def load_documents():
    documents = []
    for file in os.listdir(DATA_PATH):
        path = os.path.join(DATA_PATH, file)
        if file.endswith(".pdf"):
            loader = PyPDFLoader(path)
            documents.extend(loader.load())

        elif file.endswith(".md") or file.endswith(".txt"):
            loader = TextLoader(path)
            documents.extend(loader.load())
    return documents

def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    return splitter.split_documents(documents)


def create_vector_store(chunks):
    embeddings = FakeEmbeddings(size=1536)
    db = FAISS.from_documents(chunks, embeddings)
    db.save_local(VECTOR_PATH)
    print("✅ Vector store created successfully!")


def run_ingestion():
    print("📥 Loading documents...")
    docs = load_documents()
    print(f"Loaded {len(docs)} documents")
    print("✂️ Chunking...")
    chunks = chunk_documents(docs)
    print(f"Created {len(chunks)} chunks")
    print("🧠 Creating embeddings + FAISS index...")
    create_vector_store(chunks)


if __name__ == "__main__":
    run_ingestion()