## Data Mapping

Salesforce Case → Internal Model

- CaseId → case_id
- Description → issue_description
- Priority → priority
- CustomerId → customer_id

Vehicle History → vehicle_context

RAG Input:
"Issue: {description} | Vehicle: {model} | History: {history}"
