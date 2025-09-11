import os
import tempfile
from typing import List, Any
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv(".env")

# NOTE: All heavy/optional imports are lazily imported inside functions to avoid
# runtime crashes when deps/env are not ready. We provide a safe fallback retriever.

class _DummyRetriever:
    def get_relevant_documents(self, _query: str) -> List[Any]:
        return []

def _download_pdfs_from_supabase(tmp_dir: str) -> List[str]:
    url = os.environ.get("SUPABASE_URL", os.environ.get("PUBLIC_SUPABASE_URL"))
    key = os.environ.get("SUPABASE_ANON_KEY")
    bucket = os.environ.get("SUPABASE_BUCKET")

    print("SUPABASE_URL:", url)
    print("SUPABASE_ANON_KEY:", key[:10] + "..." if key else None)
    print("SUPABASE_BUCKET:", bucket)

    if not url or not key or not bucket:
        print("⚠️ Alguna variable del .env no se ha cargado correctamente")
        return []

    try:
        from supabase import create_client  
        client = create_client(url, key)
        files = client.storage.from_(bucket).list()
        print("RAW LIST:", files)  
    except Exception as e:
        print("❌ Error conectando a Supabase Storage:", e)
        return []

    if not files:
        print("⚠️ No se encontraron archivos en el bucket.")
        return []

    pdf_paths: List[str] = []
    for f in files:
        name = f.get("name", "")
        if name.lower().endswith(".pdf"):
            try:
                local_path = os.path.join(tmp_dir, name.replace("/", "_"))
                print(f"Descargando {name} -> {local_path}")
                data = client.storage.from_(bucket).download(name)
                with open(local_path, "wb") as fh:
                    fh.write(data)
                pdf_paths.append(local_path)
            except Exception as e:
                print(f"⚠️ Error descargando {name}: {e}")
                continue

    print(f"✅ PDFs descargados: {pdf_paths}")
    return pdf_paths

def _load_and_split_pdfs(pdf_paths: List[str]):
    try:
        from langchain_community.document_loaders import PyPDFLoader
        from langchain.text_splitter import RecursiveCharacterTextSplitter
    except Exception as e:
        print("⚠️ Error cargando LangChain:", e)
        return []

    docs: List[Any] = []
    for path in pdf_paths:
        try:
            loader = PyPDFLoader(path)
            loaded_docs = loader.load()
            print(f"PDF cargado: {path} -> {len(loaded_docs)} páginas")
            docs.extend(loaded_docs)
        except Exception as e:
            print(f"⚠️ Error cargando PDF {path}: {e}")
            continue

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
    try:
        chunks = splitter.split_documents(docs)
        print(f"✅ Chunks generados: {len(chunks)}")
        return chunks
    except Exception as e:
        print("⚠️ Error generando chunks:", e)
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
        from langchain_huggingface import HuggingFaceEmbeddings
        from langchain_community.vectorstores import FAISS
    except Exception as e:
        print("⚠️ Error importando embeddings/vectorstore:", e)
        _retriever = _DummyRetriever()
        return _retriever

    try:
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    except Exception as e:
        print("⚠️ Error creando embeddings:", e)
        _retriever = _DummyRetriever()
        return _retriever

    if not pdf_paths:
        try:
            _retriever = FAISS.from_texts([""], embeddings).as_retriever(search_kwargs={"k": 4})
            return _retriever
        except Exception as e:
            print("⚠️ Error creando retriever desde texto vacío:", e)
            _retriever = _DummyRetriever()
            return _retriever

    chunks = _load_and_split_pdfs(pdf_paths)
    if not chunks:
        print("[knowledge] No chunks produced from PDFs; using DummyRetriever")
        _retriever = _DummyRetriever()
        return _retriever

    try:
        vectordb = FAISS.from_documents(chunks, embeddings)
        _retriever = vectordb.as_retriever(search_kwargs={"k": 4})
        return _retriever
    except Exception as e:
        print("⚠️ Error creando vectordb/retriever:", e)
        _retriever = _DummyRetriever()
        return _retriever

# -------------------------------------------
# Bloque de prueba
# -------------------------------------------
if __name__ == "__main__":
    print("✅ Probando knowledge.py...")

    retriever = get_retriever()

    query = "test query"
    docs = retriever.get_relevant_documents(query)

    if not docs:
        print("⚠️ No se encontraron documentos relevantes (puede ser DummyRetriever).")
    else:
        print(f"Se encontraron {len(docs)} documentos relevantes:")
        for i, doc in enumerate(docs, 1):
            print(f"--- Documento {i} ---")
            print(doc.page_content[:500])