import os
from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings

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



    embeddings = OpenAIEmbeddings()



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