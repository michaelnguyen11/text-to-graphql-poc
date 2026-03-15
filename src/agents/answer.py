"""Answer generation module — converts data into Vietnamese business answers."""

import json
import logging

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from src.agents.prompts import ANSWER_SYSTEM_PROMPT, ANSWER_USER_TEMPLATE
from src.config import settings

logger = logging.getLogger(__name__)


def generate_answer(
    user_message: str,
    customer_context: str,
    result_data: str,
) -> str:
    """Generate a Vietnamese business answer from query results.

    Args:
        user_message: The original user question.
        customer_context: JSON string of customer info.
        result_data: JSON string of query results.

    Returns:
        Vietnamese answer text.
    """
    model = ChatOpenAI(
        model=settings.openai_model,
        temperature=settings.answer_temperature,
        api_key=settings.openai_api_key,
    )

    user_prompt = ANSWER_USER_TEMPLATE.format(
        user_message=user_message,
        customer_context=customer_context,
        result_data=result_data,
    )

    messages = [
        SystemMessage(content=ANSWER_SYSTEM_PROMPT),
        HumanMessage(content=user_prompt),
    ]

    response = model.invoke(messages)
    return response.content
