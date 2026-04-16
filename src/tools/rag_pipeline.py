from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings

VECTOR_PATH = "vector_store"
class RAGPipeline:
    def __init__(self):
        self.db = FAISS.load_local(
            VECTOR_PATH,
            OpenAIEmbeddings(),
            allow_dangerous_deserialization=True
        )

    def retrieve(self, query):
        docs = self.db.similarity_search(query, k=3)
        context = "\n\n".join([doc.page_content for doc in docs])
        return context

