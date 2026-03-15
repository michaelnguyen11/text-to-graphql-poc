"""Supervisor agent — orchestrates the Text-to-GraphQL pipeline using LangGraph."""

import json
import logging
from typing import Any

from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph_supervisor import create_supervisor

from src.agents.planner import create_planner_agent
from src.agents.prompts import SUPERVISOR_SYSTEM_PROMPT
from src.config import settings
from src.tools.graphql_executor import execute_graphql_query
from src.tools.validator import validate_plan

logger = logging.getLogger(__name__)


def create_banking_assistant():
    """Create the full banking assistant supervisor agent.

    Architecture:
    - Supervisor (GPT-4o-mini) coordinates the workflow
    - Planner sub-agent: resolves customers, retrieves context, creates query plans
    - Tools on supervisor: validate_plan, execute_graphql_query

    Returns:
        Compiled LangGraph workflow.
    """
    # Create the planner sub-agent
    planner_agent = create_planner_agent()

    # Create the supervisor with tools
    supervisor_model = ChatOpenAI(
        model=settings.openai_model,
        temperature=0.1,
        api_key=settings.openai_api_key,
    )

    # Build supervisor workflow
    workflow = create_supervisor(
        agents=[planner_agent],
        model=supervisor_model,
        tools=[validate_plan, execute_graphql_query],
        prompt=SUPERVISOR_SYSTEM_PROMPT,
        supervisor_name="banking_assistant",
        output_mode="last_message",
    )

    # Compile with memory
    app = workflow.compile()
    return app


# Module-level singleton
_app = None


def get_assistant():
    """Get or create the banking assistant singleton."""
    global _app
    if _app is None:
        _app = create_banking_assistant()
    return _app


def chat(message: str, session_id: str = "default") -> str:
    """Send a message to the banking assistant and get a response.

    Args:
        message: User message in Vietnamese or English.
        session_id: Session ID for conversation context.

    Returns:
        The assistant's response text.
    """
    app = get_assistant()

    result = app.invoke(
        {"messages": [{"role": "user", "content": message}]},
        config={"configurable": {"thread_id": session_id}},
    )

    # Extract the last AI message
    messages = result.get("messages", [])
    for msg in reversed(messages):
        if hasattr(msg, "content") and msg.content:
            # Skip tool messages
            if hasattr(msg, "type") and msg.type == "tool":
                continue
            return msg.content

    return "Xin lỗi, tôi không thể xử lý yêu cầu này. Vui lòng thử lại."
