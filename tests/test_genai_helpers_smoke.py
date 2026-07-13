"""
Smoke testleri: 20-Generative_AI_and_Prompt_Engineer altındaki yardımcı
(helper) modüllerin en azından import edilebildiğini doğrular.

Bu modüllerin çoğu OpenAI/Anthropic/Cohere/HuggingFace gibi servisler için
istemci nesneleri oluşturur. CI ortamında bu servislere ait API anahtarları
(secrets) bulunmadığından, kimlik doğrulama/bağlantı kaynaklı hatalar
BEKLENEN bir durumdur ve testi başarısız kılmaz (skip edilir).

Yalnızca gerçek kod hataları (eksik/yanlış import, sözdizimi hatası, yanlış
kullanılan bir fonksiyon/argüman vb.) testi düşürür.
"""
import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
GENAI_ROOT = REPO_ROOT / "20-Generative_AI_and_Prompt_Engineer"

# GenAI modülü içindeki tüm "*helper*.py" dosyaları (repo kök dizinine göre).
HELPER_MODULES = [
    "20.10-Yerelde_Çalışma/localhelper.py",
    "20.2-Temel_Operasyonlar/20.2.10-Kod_Üretme_Uygulama_101/helper.py",
    "20.4-LangChain_Çerçevesi/modelhelper.py",
    "20.4-LangChain_Çerçevesi/raghelper.py",
    "20.5-Uygulama_Projesi_VidChat/raghelper.py",
    "20.5-Uygulama_Projesi_VidChat/videohelper.py",
    "20.6-Bellek_Genişletme_RAG/hybridhelper.py",
    "20.6-Bellek_Genişletme_RAG/hydehelper.py",
    "20.6-Bellek_Genişletme_RAG/multiqueryhelper.py",
    "20.7-Otonom_Ajanlar/assistant_helper.py",
    "20.7-Otonom_Ajanlar/crewhelper.py",
    "20.9-Uygulama_Projesi_(Data_Explorer)/datahelper.py",
]

# API anahtarı/ağ bağlantısı olmadığında oluşması beklenen hatalara ait
# ipuçları. Bu kelimelerden biri hata mesajında geçiyorsa, hatayı "kod
# hatası" değil "secrets eksik" olarak kabul edip testi skip ediyoruz.
EXPECTED_RUNTIME_ERROR_HINTS = (
    "api_key",
    "apikey",
    "api key",
    "authentic",
    "unauthorized",
    "credential",
    "token",
    "permission",
    "connection",
    "network",
    "environment variable",
)


@pytest.mark.parametrize("relpath", HELPER_MODULES)
def test_helper_module_is_importable(relpath):
    module_path = GENAI_ROOT / relpath
    assert module_path.exists(), f"Beklenen dosya bulunamadı: {module_path}"

    module_name = f"smoke_test_{module_path.stem}_{abs(hash(relpath))}"
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module

    try:
        spec.loader.exec_module(module)
    except (ImportError, ModuleNotFoundError, SyntaxError) as exc:
        pytest.fail(f"{relpath} import edilemedi (bağımlılık/sözdizimi hatası): {exc!r}")
    except Exception as exc:  # noqa: BLE001 - kasıtlı geniş yakalama, aşağıda ayrıştırılıyor
        message = str(exc).lower()
        if any(hint in message for hint in EXPECTED_RUNTIME_ERROR_HINTS):
            pytest.skip(f"{relpath}: CI'da API anahtarı olmadığı için beklenen hata: {exc!r}")
        raise
    finally:
        sys.modules.pop(module_name, None)
