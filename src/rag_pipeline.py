def retrieve_solution(query, vector_store):
results = vector_store.similarity_search(query, k=3)
context = " ".join([r.page_content for r in results])
return context