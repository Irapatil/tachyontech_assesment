from typing import Dict

# Retrieval Agent

def retrieval_agent(case_data: Dict, vector_store) -> str:
"""
Retrieves relevant knowledge from vector store (RAG)
"""
query = case_data.get("description", "")

results = vector_store.similarity_search(query, k=3)

context = " ".join([doc.page_content for doc in results])

return context



# Context Understanding Agent

def context_agent(case_data: Dict) -> str:
"""
Extracts and formats context from case + vehicle history
"""
description = case_data.get("description", "")
vehicle = case_data.get("vehicle_model", "")
history = case_data.get("vehicle_history", "")

context = f"""
Issue: {description}
Vehicle: {vehicle}
History: {history}
"""

return context


# Decision Agent

def decision_agent(context: str, llm_client) -> str:
"""
Uses LLM to generate technical summary
"""

prompt = f"""
You are an automotive technical expert.

Based on the following context, suggest a repair procedure and summary:

{context}

Provide a clear and concise technical summary.
"""

response = llm_client.chat.completions.create(
model="gpt-4o-mini",
messages=[
{"role": "system", "content": "You are a vehicle diagnostics expert."},
{"role": "user", "content": prompt}
],
temperature=0.3
)

return response.choices[0].message.content


# Sentiment Agent

def sentiment_agent(case_data: Dict, llm_client) -> str:
"""
Determines sentiment of the case (Normal / Critical)
"""

text = case_data.get("description", "")

prompt = f"""
Classify the sentiment of the following service case:
"{text}"

Output only one word: Normal or Critical
"""

response = llm_client.chat.completions.create(
model="gpt-4o-mini",
messages=[
{"role": "system", "content": "You are a sentiment classifier."},
{"role": "user", "content": prompt}
],
temperature=0
)

return response.choices[0].message.content.strip()


# Action Agent

def action_agent(case_id: str, summary: str, sf_client):
"""
Performs write-back actions to Salesforce
"""

# Update case
sf_client.update_case(case_id, summary)

# Create follow-up task
sf_client.create_task(case_id)

return "Actions completed successfully"

#Orchestrator

def orchestrator(case_data, vector_store, llm_client, sf_client):
context = context_agent(case_data)
rag_context = retrieval_agent(case_data, vector_store)

combined_context = context + "\n" + rag_context

summary = decision_agent(combined_context, llm_client)

sentiment = sentiment_agent(case_data, llm_client)

action_agent(case_data["case_id"], summary, sf_client)

return {
"summary": summary,
"sentiment": sentiment
}