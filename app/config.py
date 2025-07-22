import os
from dotenv import load_dotenv

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL", "http://http://host.docker.internal:6333")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "pdf_knowledge")
EMBEDDING_METHOD = os.getenv("EMBEDDING_METHOD", "nomic")
EMBEDDING_DIM = int(os.getenv("EMBEDDING_DIM", 768))  # 需和实际API返回一致

# 新增 Ollama 服务地址
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://host.docker.internal:11434")
