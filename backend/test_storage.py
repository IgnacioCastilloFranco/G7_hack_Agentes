import os
from dotenv import load_dotenv
from supabase import create_client

# Cargar variables del .env
load_dotenv()

# Leer variables
url = os.getenv("PUBLIC_SUPABASE_URL")
key = os.getenv("SUPABASE_ANON_KEY")
bucket_name = os.getenv("SUPABASE_BUCKET")

# Imprimir variables para depuración
print("PUBLIC_SUPABASE_URL:", url)
print("SUPABASE_ANON_KEY:", key[:10] + "..." if key else None)
print("SUPABASE_BUCKET:", bucket_name)

# Comprobar que no estén vacías
if not url or not key or not bucket_name:
    raise ValueError("⚠️ Alguna variable del .env no se ha cargado correctamente")

# Crear cliente de Supabase
supabase = create_client(url, key)

# Listar archivos en el bucket
res = supabase.storage.from_(bucket_name).list()
if res.data is not None:
    print("✅ Archivos encontrados en el bucket:")
    for f in res.data:
        file_path = f['name']
        file_url = supabase.storage.from_(bucket_name).get_public_url(file_path)
        print(f"- {file_path} -> {file_url['publicURL']}")
else:
    print("❌ Error accediendo al bucket:", res.error)
