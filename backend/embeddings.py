import chromadb
from sentence_transformers import SentenceTransformer 
from backend import config

_model = SentenceTransformer(config.EMBEDDING_MODEL_NAME)
_client = chromadb.Client()
_collection = _client.get_or_create_collection(config.CHROMA_COLLECTION_NAME)


def embed_transactions(df) -> None:
    existing_ids = _collection.get(include=[])["ids"]
    if existing_ids:
        _collection.delete(ids=existing_ids)
    # embeds each transaction description and stores it with light metadata
    documents = df["description"].tolist()
    embeddings = _model.encode(documents).tolist()

    metadatas = [
        {
            "date": str(row["date"].date()),
            "category": row["category"],
            "debit": float(row["debit"]),
            "credit": float(row["credit"]),
        }
        for _, row in df.iterrows()
    ]
    ids = [f"txn_{i}" for i in range(len(df))]
    
    _collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )


def query_similar(question: str, n_results: int = 10) -> list[dict]:
    # semantic search over transaction descriptions for the chat router
    query_embedding = _model.encode([question]).tolist()
    results = _collection.query(query_embeddings=query_embedding, n_results=n_results)

    matches = []
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        matches.append({"description": doc, **meta})
    return matches