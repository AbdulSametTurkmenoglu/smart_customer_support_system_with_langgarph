import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise EnvironmentError("OPENAI_API_KEY .env dosyasında bulunamadı")

# İleride LangSmith entegrasyonu isterseniz buraya ekleyebilirsiniz:
# os.environ["LANGCHAIN_TRACING_V2"] = "true"
# os.environ["LANGCHAIN_API_KEY"] = "..."
# os.environ["LANGCHAIN_PROJECT"] = "Musteri Destek Sistemi"