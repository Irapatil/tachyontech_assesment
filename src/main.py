from salesforce_client import SalesforceClient
from rag_pipeline import retrieve_solution
from agents import decision_agent

def process_case(case_data, sf_client, vector_store):
query = case_data["description"]

context = retrieve_solution(query, vector_store)
solution = decision_agent(context)

sf_client.update_case(case_data["case_id"], solution)
sf_client.create_task(case_data["case_id"])