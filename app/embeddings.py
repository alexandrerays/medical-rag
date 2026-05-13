import json

import boto3

from app.config import get_settings


def _get_client():
    settings = get_settings()
    kwargs = {"region_name": settings.aws_region}
    if settings.aws_access_key_id and settings.aws_secret_access_key:
        kwargs["aws_access_key_id"] = settings.aws_access_key_id
        kwargs["aws_secret_access_key"] = settings.aws_secret_access_key
    return boto3.client("bedrock-runtime", **kwargs)


def get_embedding(text: str) -> list[float]:
    settings = get_settings()
    client = _get_client()
    body = {"inputText": text}
    if "v2" in settings.embedding_model:
        body["dimensions"] = settings.embedding_dimensions
    response = client.invoke_model(
        modelId=settings.embedding_model,
        contentType="application/json",
        accept="application/json",
        body=json.dumps(body),
    )
    result = json.loads(response["body"].read())
    return result["embedding"]


def get_embeddings(texts: list[str], input_type: str = "document") -> list[list[float]]:
    all_embeddings = []
    for text in texts:
        all_embeddings.append(get_embedding(text))
    return all_embeddings
