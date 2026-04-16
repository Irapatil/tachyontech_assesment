import json
from autogen_agentchat.teams import RoundRobinGroupChat
from agents import create_agents
from tools.salesforce_client import SalesforceClient
from tools.notification import send_alert
from tools.state_manager import save_failure
from tools.rag_pipeline import RAGPipeline
from tools.schema_validator import validate_json
sf = SalesforceClient()
rag = RAGPipeline()

async def run_case_workflow(case_id: str):
    try:
        # 1️⃣ Fetch case data
        case_data = sf.get_case(case_id)
        if not case_data:
            raise Exception("No case data found")

        # 2️⃣ Retrieve KB context (RAG)
        kb_context = rag.retrieve(str(case_data))
        # 3️⃣ Create agents
        context_agent, rag_agent, decision_agent, action_agent = create_agents()

        # 4️⃣ Multi-agent orchestration
        team = RoundRobinGroupChat(
            agents=[context_agent, rag_agent, decision_agent, action_agent],
            max_turns=4
        )

        # 5️⃣ Execute workflow
        result = await team.run(
            task=f"""You are part of an autonomous service workflow.INPUT:Salesforce Case:
            {json.dumps(case_data, indent=2)}
            Technical Knowledge Base Context:
            {kb_context}
            PROCESS STEPS:
            1. ContextAgent → Extract structured fields
            2. RAGAgent → Diagnose issue using KB context
            3. DecisionAgent → Identify sentiment & priority
            4. ActionAgent → Generate final summary + actions
            FINAL OUTPUT MUST BE STRICT JSON:
            {{
                "summary": "...",
                "sentiment": "...",
                "priority": "...",
                 "actions": ["update_case", "create_task", "alert_if_critical"]
            }}
            """
             )

        # 6️⃣ Extract final agent response
        final_output = result.messages[-1].content
        try:
            parsed_output = json.loads(final_output)
        except:
            parsed_output = {
                "summary": str(final_output),
                "sentiment": "Unknown",
                "priority": "Medium",
                "actions": ["update_case"]
            }

        summary = parsed_output.get("summary", "")
        validate_json(parsed_output)
        # 7️⃣ Salesforce write-back
        sf.update_case(case_id, summary)
        sf.create_task(case_id)
        # 8️⃣ Notification (if critical)
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