-- Enable pgvector extension
create extension if not exists vector;

-- Documents table for storing chunked content with embeddings
create table if not exists documents (
  id uuid primary key default gen_random_uuid(),
  content text not null,
  metadata jsonb not null default '{}',
  embedding vector(1536)
);

-- Index for fast cosine similarity search (HNSW works with any number of rows)
create index if not exists documents_embedding_idx
  on documents using hnsw (embedding vector_cosine_ops);

-- RPC function for similarity search
create or replace function match_documents(
  query_embedding vector(1536),
  match_count int default 5,
  filter jsonb default '{}'
)
returns table (
  id uuid,
  content text,
  metadata jsonb,
  similarity float
)
language plpgsql
as $$
begin
  return query
  select
    d.id,
    d.content,
    d.metadata,
    1 - (d.embedding <=> query_embedding) as similarity
  from documents d
  where case
    when filter = '{}'::jsonb then true
    else d.metadata @> filter
  end
  order by d.embedding <=> query_embedding
  limit match_count;
end;
$$;
