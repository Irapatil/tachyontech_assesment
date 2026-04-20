import json
from autogen_agentchat.teams import RoundRobinGroupChat

from src.agents import create_agents
from src.tools.salesforce_client import SalesforceClient
from src.tools.notification import send_alert
from src.tools.state_mananger import save_failure
from src.tools.rag_pipeline import RAGPipeline

# Initialize clients
sf = SalesforceClient()
rag = RAGPipeline()


async def run_case_workflow(case_id: str):
    try:
        # 1️⃣ Mock Case (demo-safe)
        case_data = {
            "Subject": "Engine overheating frequently",
            "Description": "Vehicle shuts down after 20 minutes. Urgent issue.",
            "Vehicle": "Toyota Camry 2018",
        }

        # 2️⃣ RAG context
        kb_context = rag.retrieve(str(case_data))

        # 3️⃣ Create agents
        context_agent, rag_agent, decision_agent, action_agent = create_agents()

        # 4️⃣ Create team
        team = RoundRobinGroupChat([
            context_agent,
            rag_agent,
            decision_agent,
            action_agent
        ])

        # 5️⃣ Run workflow (NO await here)
        result_stream = team.run_stream(
            task=f"""
You are a team of AI agents solving an automotive service case.

INPUT:
Case:
{json.dumps(case_data, indent=2)}

Context:
{kb_context}

INSTRUCTIONS:
- Collaborate step by step
- Final response MUST be clean and structured

FINAL OUTPUT FORMAT (STRICT JSON):
{{
    "summary": "short technical explanation",
    "sentiment": "Critical or Normal",
    "priority": "High, Medium, or Low",
    "actions": ["update_case", "create_task", "alert_if_critical"]
}}

IMPORTANT:
- DO NOT include explanation
- DO NOT include markdown
- RETURN ONLY JSON
"""
        )

        # 6️⃣ Collect final output
        final_output = ""

        async for msg in result_stream:
            try:
                if hasattr(msg, "content") and msg.content:
                    final_output = str(msg.content)
            except:
                continue

        print("RAW OUTPUT:", final_output)

        # 7️⃣ SAFE JSON PARSING
        try:
            parsed_output = json.loads(final_output)
        except:
            # 🔥 fallback ensures JSON always returned
            parsed_output = {
                "summary": final_output[:200],
                "sentiment": "Critical" if "critical" in final_output.lower() else "Normal",
                "priority": "High" if "high" in final_output.lower() else "Medium",
                "actions": ["update_case"]
            }

        print("FINAL OUTPUT:", parsed_output)

        # 🚫 Skip Salesforce (demo safe)
        # sf.update_case(case_id, parsed_output.get("summary", ""))
        # sf.create_task(case_id)

        # 8️⃣ Alert if critical
        if parsed_output.get("sentiment") == "Critical":
            send_alert(f"🚨 Critical Case Detected: {case_id}")

        return {
            "status": "success",
            "case_id": case_id,
            "result": parsed_output
        }

    except Exception as e:
        save_failure(case_id, str(e))

        return {
            "status": "failed",
            "case_id": case_id,
            "error": str(e)
        }