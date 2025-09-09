import os
import tempfile
from typing import List, Any

# NOTE: All heavy/optional imports are lazily imported inside functions to avoid
# runtime crashes when deps/env are not ready. We provide a safe fallback retriever.

class _DummyRetriever:
    def get_relevant_documents(self, _query: str) -> List[Any]:
        return []


def _download_pdfs_from_supabase(tmp_dir: str) -> List[str]:
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_ANON_KEY")
    bucket = os.environ.get("SUPABASE_BUCKET")

    if not url or not key or not bucket:
        return []

    try:
        from supabase import create_client  # lazy import
        client = create_client(url, key)
        files = client.storage.from_(bucket).list()
    except Exception:
        return []

    pdf_paths: List[str] = []
    for f in files:
        name = f.get("name", "")
        if name.lower().endswith(".pdf"):
            try:
                local_path = os.path.join(tmp_dir, name)
                data = client.storage.from_(bucket).download(name)
                with open(local_path, "wb") as fh:
                    fh.write(data)
                pdf_paths.append(local_path)
            except Exception:
                continue

    return pdf_paths


def _load_and_split_pdfs(pdf_paths: List[str]):
    try:
        from langchain_community.document_loaders import PyPDFLoader
        from langchain.text_splitter import RecursiveCharacterTextSplitter
    except Exception:
        return []

    docs: List[Any] = []
    for path in pdf_paths:
        try:
            loader = PyPDFLoader(path)
            docs.extend(loader.load())
        except Exception:
            continue

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
    try:
        return splitter.split_documents(docs)
    except Exception:
        return []


_retriever = None


def get_retriever():
    global _retriever
    if _retriever is not None:
        return _retriever

    tmp_dir = tempfile.mkdtemp()
    pdf_paths = _download_pdfs_from_supabase(tmp_dir)

    # Try to import embedding/vector store lazily. Fallback to dummy on failure.
    try:
        from langchain_community.embeddings import HuggingFaceEmbeddings
        from langchain_community.vectorstores import FAISS
    except Exception:
        _retriever = _DummyRetriever()
        return _retriever

    try:
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    except Exception:
        _retriever = _DummyRetriever()
        return _retriever

    if not pdf_paths:
        try:
            _retriever = FAISS.from_texts([""], embeddings).as_retriever(search_kwargs={"k": 4})
            return _retriever
        except Exception:
            _retriever = _DummyRetriever()
            return _retriever

    chunks = _load_and_split_pdfs(pdf_paths)
    if not chunks:
        _retriever = _DummyRetriever()
        return _retriever

    try:
        vectordb = FAISS.from_documents(chunks, embeddings)
        _retriever = vectordb.as_retriever(search_kwargs={"k": 4})
        return _retriever
    except Exception:
        _retriever = _DummyRetriever()
        return _retriever


