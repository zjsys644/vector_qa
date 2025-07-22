from pydantic import BaseModel
from typing import List, Dict

class SearchRequest(BaseModel):
    query: str
    top_k: int = 30

class SearchResult(BaseModel):
    text: str
    score: float
    meta: Dict

class SearchResponse(BaseModel):
    results: List[SearchResult]

