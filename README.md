# AI Multi-Agent Salesforce Service Automation

## 📌 Overview

This project implements a **multi-agent AI system** using AutoGen to automate vehicle service case handling in a closed-loop workflow.

The system:

* Detects new service cases
* Retrieves contextual knowledge using RAG
* Uses multiple AI agents for reasoning
* Generates actionable outputs
* Simulates updates and alerts

---

## 🧠 Architecture

**Agents Involved:**

* **Context Agent** → Extracts structured case data
* **RAG Agent** → Retrieves relevant knowledge from documents
* **Decision Agent** → Determines sentiment & priority
* **Action Agent** → Generates final output and actions

**Workflow:**

```
Salesforce Case → Context Agent → RAG → Decision → Action → Output
```

---

## ⚙️ Tech Stack

* Python 3.10
* FastAPI
* AutoGen (Multi-Agent Framework)
* LangChain (RAG Pipeline)
* FAISS (Vector Store)
* Uvicorn (API Server)

---

## 📁 Project Structure

```
tachyontech_assessment/
│
├── config/
│   └── settings.py
│
├── data/
│   └── manuals/
│       └── engine.txt
│
├── schemas/
│   ├── agent_output_schema.json
│   ├── case_schema.json
│   └── vehicle_history_schema.json
│
├── src/
│   ├── tools/
│   │   ├── rag_ingestion.py
│   │   ├── rag_pipeline.py
│   │   ├── salesforce_client.py
│   │   ├── notification.py
│   │   ├── state_manager.py
│   │   └── schema_validator.py
│   │
│   ├── agents.py
│   ├── orchestrator.py
│   └── main.py
│
├── vector_store/
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🚀 Installation & Setup

### 🔹 Step 1: Clone Repository

```bash
git clone <your-github-repo-link>
cd tachyontech_assessment
```

---

### 🔹 Step 2: Create Virtual Environment

```bash
python -m venv .venv
```

Activate:

**Windows:**

```bash
.venv\Scripts\activate
```

**Mac/Linux:**

```bash
source .venv/bin/activate
```

---

### 🔹 Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 🔹 Step 4: Configure Environment (Optional)

If using OpenAI:

Create `.env` (optional):

```
OPENAI_API_KEY=your_api_key
```

⚠️ For demo, system uses **local embeddings (no API needed)**

---

## 🧠 RAG Setup (IMPORTANT)

### 🔹 Step 5: Run RAG Ingestion

This converts documents into vector embeddings.

```bash
python -m src.tools.rag_ingestion
```

Expected output:

```
Loading documents...
Chunking...
Creating embeddings...
Vector store created successfully!
```

---

## ▶️ Run Application

### 🔹 Step 6: Start FastAPI Server

```bash
uvicorn src.main:app --reload
```

Server will start at:

```
http://127.0.0.1:8000
```

---

## 🧪 Testing the System

### 🔹 Step 7: Open Swagger UI

👉 Open in browser:

```
http://127.0.0.1:8000/docs
```

---

### 🔹 Step 8: Trigger Workflow

1. Select `/trigger-case`
2. Click **Try it out**
3. Enter:

```
case_id = test123
```

4. Click **Execute**

---

## 🎯 Expected Output

```json
{
  "status": "success",
  "case_id": "test123",
  "result": {
    "summary": "Engine overheating due to coolant system issue",
    "sentiment": "Critical",
    "priority": "High",
    "actions": ["update_case", "create_task", "alert_if_critical"]
  }
}
```

---

## ⚠️ Important Notes

* Salesforce integration is **mocked for demo**
* Uses **FakeEmbeddings** (no OpenAI cost)
* Multi-agent orchestration via AutoGen
* Robust fallback ensures system does not crash

---

## 🔄 State Persistence

If failure occurs:

* Error is stored using `state_manager.py`
* Enables retry/recovery logic

---

## 🔔 Notification System

* Sends alert if case is **Critical**
* Can be integrated with Slack/Teams

---


