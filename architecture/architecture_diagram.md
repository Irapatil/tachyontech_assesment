## Architecture Overview

Trigger → FastAPI → Agent Layer → RAG → Decision → Action → Salesforce + Notifications

Components:
- Ingress: FastAPI / Azure Function
- Orchestration: AutoGen / LangGraph
- RAG: Azure AI Search + Blob Storage
- State: Cosmos DB / Service Bus
- Integration: Salesforce REST API