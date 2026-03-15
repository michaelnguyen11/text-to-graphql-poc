"""Planner agent — interprets Vietnamese questions and creates query plans."""

import json
import logging

from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from src.agents.prompts import PLANNER_SYSTEM_PROMPT
from src.config import settings
from src.tools.customer_resolver import resolve_customer
from src.tools.context_retrieval import retrieve_context

logger = logging.getLogger(__name__)


def create_planner_agent():
    """Create the planner agent using LangGraph create_react_agent.

    The planner:
    1. Resolves the customer using resolve_customer tool
    2. Retrieves relevant context using retrieve_context tool
    3. Outputs a structured JSON query plan
    """
    model = ChatOpenAI(
        model=settings.openai_model,
        temperature=settings.planner_temperature,
        api_key=settings.openai_api_key,
    )

    tools = [resolve_customer, retrieve_context]

    agent = create_react_agent(
        model=model,
        tools=tools,
        name="planner",
        prompt=PLANNER_SYSTEM_PROMPT,
    )

    return agent
