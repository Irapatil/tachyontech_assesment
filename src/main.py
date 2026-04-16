from fastapi import FastAPI, HTTPException
from orchestrator import run_case_workflow

app = FastAPI(
    title="Salesforce Multi-Agent Service Automation",
    description="Closed-loop AI Agent System using AutoGen + RAG",
    version="1.0"
)


@app.get("/")
def root():
    return {"message": "🚀 AI Multi-Agent System Running"}


@app.post("/trigger-case")
async def trigger_case(case_id: str):
    if not case_id:
        raise HTTPException(status_code=400, detail="case_id is required")

    result = await run_case_workflow(case_id)

    if result["status"] == "failed":
        raise HTTPException(status_code=500, detail=result["error"])
    return result