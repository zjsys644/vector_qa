from .config import EMBEDDING_METHOD, OLLAMA_HOST
import ollama
import time

class Embedder:
    def __init__(self):
        self.method = EMBEDDING_METHOD.lower()
        if self.method == "nomic":
            self.client = ollama.Client(host=OLLAMA_HOST)
        else:
            raise ValueError(f"不支持的 EMBEDDING_METHOD: {self.method}")

    def embed(self, texts: list[str]) -> list[list[float]]:
        if self.method != "nomic":
            raise ValueError(f"不支持的方法: {self.method}")
        results = []
        for t in texts:
            for attempt in range(3):
                try:
                    resp = self.client.embeddings(model="nomic-embed-text:latest", prompt=t)
                    vec = resp.get("embedding") or resp.get("embeddings")
                    if vec is None:
                        # Ollama 0.1.34 之后返回 embedding，兼容 embeddings
                        raise RuntimeError("Ollama 返回缺少 embeddings 字段")
                    results.append(vec)
                    print(f"[Ollama] embedding success for segment (len={len(t)})")
                    break
                except Exception as e:
                    print(f"Ollama embedding失败: {e}, 内容片段: {t[:100]}")
                    time.sleep(1)
            else:
                # embedding失败时放入全零向量
                results.append([0.0]*1024)
        return results

