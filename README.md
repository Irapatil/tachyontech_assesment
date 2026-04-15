Production-ready Agentic AI architecture for enterprise automation.
# Closed-Loop Salesforce Service Agent

## Overview
This project implements an agentic AI system that automates handling of high-priority Salesforce cases using RAG and multi-agent orchestration.

## Features
- Salesforce API integration (OAuth2)
- Multi-agent system (AutoGen/LangGraph ready)
- RAG-based knowledge retrieval
- Automated case updates
- Slack/Teams notifications
- Fault-tolerant state management

## Tech Stack
- Python (FastAPI)
- Azure OpenAI
- Azure AI Search
- Salesforce REST API

## Flow
1. Detect new case
2. Fetch context
3. Query knowledge base
4. Generate solution
5. Update Salesforce
6. Notify stakeholders
