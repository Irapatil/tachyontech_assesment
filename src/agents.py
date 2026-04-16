from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from config.settings import OPENAI_API_KEY


def create_agents():
    model_client = OpenAIChatCompletionClient(
        model="gpt-4o-mini",
        api_key=OPENAI_API_KEY
    )

    context_agent = AssistantAgent(
        name="ContextAgent",
        model_client=model_client,
        system_message="""
You are a Context Extraction Agent.
Input: Salesforce Case JSON
Output strictly in JSON:
{
 "issue": "...",
 "description": "...",
 "vehicle_context": "..."
}
"""
    )

    rag_agent = AssistantAgent(
        name="RAGAgent",
        model_client=model_client,
        system_message="""
You are a Technical Diagnosis Agent.
Use context to identify:
- root cause
- recommended fix
Output JSON:
{
 "root_cause": "...",
 "recommended_fix": "...",
 "confidence": "high/medium/low"
}
"""
    )

    decision_agent = AssistantAgent(
        name="DecisionAgent",
        model_client=model_client,
        system_message="""
        You are a Decision Agent.
        Classify:
        - sentiment (Critical / Normal)
        - priority (High / Medium / Low)
        Rules:- urgent, failure, safety → Critical Output JSON:
        {
        "sentiment": "...",
        "priority": "..." }"""
    )
    action_agent = AssistantAgent(
        name="ActionAgent",
        model_client=model_client,
        system_message=system_message="""You are an Action Agent.
        STRICT RULES:
        - Output MUST follow this JSON schema exactly
        - Do NOT add extra text
        - Do NOT explain 
        schema:
        {
        "summary": "...",
        "sentiment": "Critical or Normal",
        "priority": "High/Medium/Low",
        "actions": ["update_case", "create_task", "alert_if_critical"]
        }
        """
    )

    return context_agent, rag_agent, decision_agent, action_agent