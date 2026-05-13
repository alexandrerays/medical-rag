from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    supabase_url: str
    supabase_key: str

    # AWS Bedrock configuration
    aws_region: str = "us-east-1"
    aws_access_key_id: str | None = None
    aws_secret_access_key: str | None = None

    embedding_model: str = "amazon.titan-embed-text-v1"
    embedding_dimensions: int = 1536
    llm_model: str = "us.anthropic.claude-opus-4-6-v1"

    chunk_size: int = 800
    chunk_overlap: int = 100
    top_k: int = 5

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8", "extra": "ignore"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
