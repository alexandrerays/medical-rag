import httpx

from app.config import get_settings


def _get_client():
    from supabase import create_client

    settings = get_settings()
    return create_client(settings.supabase_url, settings.supabase_key)


def upsert_documents(documents: list[dict]) -> None:
    client = _get_client()
    batch_size = 50
    for i in range(0, len(documents), batch_size):
        batch = documents[i : i + batch_size]
        client.table("documents").insert(batch).execute()


def search(query_embedding: list[float], top_k: int = 5, filter_metadata: dict | None = None) -> list[dict]:
    import json as json_mod

    import numpy as np

    client = _get_client()
    result = client.table("documents").select("id, content, metadata, embedding").execute()

    query_vec = np.array(query_embedding)
    scored = []
    for row in result.data:
        stored_vec = np.array(json_mod.loads(row["embedding"]))
        similarity = float(np.dot(query_vec, stored_vec) / (np.linalg.norm(query_vec) * np.linalg.norm(stored_vec)))
        scored.append({
            "id": row["id"],
            "content": row["content"],
            "metadata": row["metadata"],
            "similarity": similarity,
        })

    scored.sort(key=lambda x: x["similarity"], reverse=True)
    return scored[:top_k]
