import anthropic

from app.config import get_settings


async def generate_answer(question: str, context: str, system_prompt: str) -> str:
    settings = get_settings()
    client = anthropic.AsyncAnthropicBedrock(
        aws_region=settings.aws_region,
        aws_access_key=settings.aws_access_key_id,
        aws_secret_key=settings.aws_secret_access_key,
    )

    message = await client.messages.create(
        model=settings.llm_model,
        max_tokens=1024,
        system=system_prompt,
        messages=[{"role": "user", "content": context}],
    )

    return message.content[0].text
