from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import FakeEmbeddings

VECTOR_PATH = "vector_store"

class RAGPipeline:

    def __init__(self):
        self.db = FAISS.load_local(
            VECTOR_PATH,
            FakeEmbeddings(size=1536),
            allow_dangerous_deserialization=True
        )

    def retrieve(self, query):
        docs = self.db.similarity_search(query, k=3)
        return "\n".join([doc.page_content for doc in docs])