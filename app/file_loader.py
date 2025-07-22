import os
import json
import docx
import pandas as pd
import fitz  # PyMuPDF 处理 PDF

def split_file(file_path: str, max_chars: int = 500, by: str = "chars_500"):
    ext = file_path.split('.')[-1].lower()
    if ext == "pdf":
        return split_pdf(file_path, max_chars)
    if ext in ("txt", "md"):
        return split_text(file_path, max_chars)
    if ext in ("csv", "tsv"):
        return split_csv(file_path, max_chars)
    if ext == "docx":
        return split_docx(file_path, max_chars)
    if ext in ("xlsx", "xls"):
        return split_xlsx(file_path, max_chars)
    if ext == "jsonl":
        return split_jsonl(file_path, max_chars)
    if ext == "json":
        return split_json(file_path, max_chars)
    if ext in ("jpg", "jpeg", "png"):
        return [{"text": f"图片文件: {os.path.basename(file_path)}"}]
    raise ValueError("不支持的文件类型: %s" % ext)

def split_text(file_path, max_chars):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    return [{"text": content[i:i+max_chars]} for i in range(0, len(content), max_chars)]

def split_csv(file_path, max_chars):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    chunks, chunk = [], ""
    for line in lines:
        if len(chunk) + len(line) > max_chars:
            chunks.append({"text": chunk})
            chunk = ""
        chunk += line
    if chunk.strip():
        chunks.append({"text": chunk})
    return chunks

def split_docx(file_path, max_chars):
    doc = docx.Document(file_path)
    text = "\n".join([p.text for p in doc.paragraphs])
    return [{"text": text[i:i+max_chars]} for i in range(0, len(text), max_chars)]

def split_xlsx(file_path, max_chars):
    df = pd.read_excel(file_path)
    text = df.to_string(index=False)
    return [{"text": text[i:i+max_chars]} for i in range(0, len(text), max_chars)]

def split_pdf(file_path, max_chars):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return [{"text": text[i:i+max_chars]} for i in range(0, len(text), max_chars)]

def split_jsonl(file_path, max_chars):
    # 按行/分块分割 jsonl，每行可视为一个 json object
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    chunk, chunks = "", []
    for line in lines:
        if len(chunk) + len(line) > max_chars:
            chunks.append({"text": chunk})
            chunk = ""
        chunk += line
    if chunk.strip():
        chunks.append({"text": chunk})
    return chunks

def split_json(file_path, max_chars):
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            content = json.load(f)
        except Exception:
            f.seek(0)
            raw = f.read()
            # 如果不是标准json就当纯文本或行分割
            lines = raw.splitlines()
            segments = []
            chunk = ""
            for line in lines:
                if len(chunk) + len(line) > max_chars:
                    segments.append({"text": chunk})
                    chunk = ""
                chunk += line
            if chunk.strip():
                segments.append({"text": chunk})
            return segments

    if isinstance(content, list):
        # 按元素分割，每个元素为一个块
        out = []
        for item in content:
            s = json.dumps(item, ensure_ascii=False)
            # 若超长还分割
            for i in range(0, len(s), max_chars):
                out.append({"text": s[i:i+max_chars]})
        return out
    elif isinstance(content, dict):
        # 按键值对为基础分块
        segments = []
        for k, v in content.items():
            s = f"{k}: {json.dumps(v, ensure_ascii=False)}"
            for i in range(0, len(s), max_chars):
                segments.append({"text": s[i:i+max_chars]})
        return segments
    else:
        txt = json.dumps(content, ensure_ascii=False)
        return [{"text": txt[i:i+max_chars]} for i in range(0, len(txt), max_chars)]

