# ==============================================================================
# LangChain Zincir (Chain) Yapıları ve Fonksiyon Çağırma Örneği
# ==============================================================================
# Bu dosya, LangChain'in güçlü zincir (chain) mekanizmalarını gösteriyor.
# 
# Zincir nedir ve neden önemli?
# -----------------------------
# LangChain'de "chain" (zincir), birden fazla işlemi sıralı olarak birbirine
# bağlamamızı sağlayan bir yapıdır. Düşünün ki bir fabrika bandı gibi:
# Veri girer -> İşlem 1 -> İşlem 2 -> ... -> Sonuç çıkar
#
# Bu dosyada iki önemli zincir türünü inceliyoruz:
# 1. Stuff Documents Chain: Dökümanları alıp LLM'e toplu olarak sunan basit zincir
# 2. OpenAI Function Runnable: LLM'in yapılandırılmış veri döndürmesini sağlayan zincir
# ==============================================================================


# ==============================================================================
# BÖLÜM 1: Create Stuff Documents Chain
# ==============================================================================
# "Stuff" stratejisi, tüm dökümanları alıp tek bir prompt'a "dolduran" (stuffing)
# en basit yaklaşımdır. Döküman sayısı az ve toplam boyut context window'a
# sığdığında mükemmel çalışır.
#
# Peki neden "stuff"? Çünkü tüm içeriği olduğu gibi LLM'e "tıkıyoruz".
# Alternatifleri: Map-Reduce (büyük dökümanlar için), Refine (kademeli iyileştirme)
# ==============================================================================

from langchain_openai import ChatOpenAI
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain

import os
from dotenv import load_dotenv

# .env dosyasından API anahtarlarını yükle
# Güvenlik kuralı: API anahtarları ASLA kodun içinde yazılmaz!
load_dotenv()

my_key_openai = os.getenv("openai_apikey")

# GPT-4 Turbo modelini başlat
# gpt-4-0125-preview: 2024 Ocak versiyonu, gelişmiş mantık yürütme yetenekleri
llm = ChatOpenAI(model="gpt-4-0125-preview", api_key=my_key_openai)

# Prompt template oluştur
# {context} placeholder'ı daha sonra dökümanlarla doldurulacak
# Sistem mesajı olarak tanımladık - model bunu bir talimat olarak algılayacak
prompt = ChatPromptTemplate.from_messages(
    [("system", "Burada ismi geçen kişilerin en sevdiği rengi tek tek yaz:\n\n{context}")]
)


# Örnek dökümanlar oluştur
# Document objesi, LangChain'in standart döküman formatıdır
# Her döküman page_content (içerik) ve metadata (üst veri) içerir
# Bu örnekte basit metin dökümanları kullanıyoruz
docs = [
    Document(page_content="Gamze kırmızıyı sever ama sarıyı sevmez"),
    Document(page_content="Murat yeşili sever ama maviyi sevdiği kadar değil"),
    Document(page_content="Burak'a sorsan favori rengim yok der ama belli ki turuncu rengi seviyor")
]


# Stuff Documents zincirini oluştur
# Bu zincir, verilen dökümanları prompt'taki {context} yerine yerleştirir
# ve LLM'e gönderir. Çok basit ama etkili bir yaklaşım!
chain_1 = create_stuff_documents_chain(llm, prompt)

# Zinciri çalıştır ve sonucu yazdır
# invoke() metodu zinciri tetikler, context olarak dökümanları geçiyoruz
print(chain_1.invoke({"context": docs}))



# ==============================================================================
# BÖLÜM 2: Create OpenAI Function Runnable Chain
# ==============================================================================
# Bu bölüm, LLM'lerin en güçlü özelliklerinden birini gösteriyor:
# Yapılandırılmış veri çıktısı (Structured Output)
#
# Normal bir LLM sadece metin döndürür. Ama ya biz belirli bir formatta
# veri istiyorsak? Örneğin bir kişinin bilgilerini JSON olarak almak?
# İşte burada Function Calling devreye giriyor.
#
# Pydantic modelleri kullanarak beklenen veri yapısını tanımlıyoruz.
# LLM, verilen metinden bu yapıya uygun veriyi çıkarıp döndürüyor.
# Bu, veri çıkarma (NER), form doldurma gibi görevler için harika!
# ==============================================================================

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Optional
from langchain.chains.openai_functions import create_openai_fn_runnable

import os
from dotenv import load_dotenv

load_dotenv()

my_key_openai = os.getenv("openai_apikey")


# Pydantic model: İnsan varlığını tanımlayan şema
# Bu şema, LLM'e "bir insanı tanımlamak için bu bilgiler gerekli" der
# Field() ile her alanın ne anlama geldiğini açıklıyoruz
class Insan(BaseModel):
    """Bir insan hakkında tanımlayıcı bilgiler"""
    
    # isim alanı: Zorunlu (... ile belirtilmiş), string tipinde
    isim: str = Field(..., description="Kişinin ismi")
    # yas alanı: Zorunlu, integer tipinde
    yas: int = Field(..., description="Kişinin yaşı")
    # meslek alanı: Opsiyonel (None varsayılan), string tipinde
    meslek: Optional[str] = Field(None, description="Kişinin mesleği")


# Pydantic model: Şehir varlığını tanımlayan şema
# İkinci bir varlık türü - LLM metinden hangisini çıkaracağına kendisi karar verecek
class Sehir(BaseModel):
    """Bir şehir hakında tanımlayıcı bilgiler"""
    
    isim: str = Field(..., description="Şehrin ismi")
    plaka_no: str = Field(..., description="Şehrin plaka numarası")
    iklim: Optional[str] = Field(None, description="Şehrin iklimi")


# GPT-4 Turbo modelini tekrar başlat
llm = ChatOpenAI(model="gpt-4-0125-preview", api_key=my_key_openai)

# Çok adımlı prompt template
# Sistem, insan (human) ve tekrar insan mesajlarından oluşuyor
# Bu yapı, role-playing benzeri bir senaryo kuruyor
prompt = ChatPromptTemplate.from_messages(
    [
        # Sistem mesajı: Modelin karakterini ve görevini tanımla
        ("system", "Sen varlıkları kaydetmek konusunda dünyanın en başarılı algoritmasısın"),
        # İnsan mesajı: Asıl girdiyi ve talimatı ver
        ("human", "Şu verdiğim girdideki varlıkları kaydetmek için gerekli fonksiyonlara çağrı yap: {input}"),
        # İpucu mesajı: Cevap kalitesini artırmak için ek yönlendirme
        ("human", "İpucu: Doğru formatta yanıtladığından emin ol")
    ]
)

# OpenAI Function Runnable zincirini oluştur
# [Insan, Sehir]: Bu iki Pydantic modelden birini döndürmesi gerektiğini söylüyoruz
# LLM, girdiden hangi varlığın çıkarılacağını kendisi anlayacak
chain_2 = create_openai_fn_runnable([Insan, Sehir], llm, prompt)

# İlk test: Bir kişi hakkında bilgi içeren cümle
# Beklenti: Insan objesi dönsün (isim: Aydın, yas: 34, meslek: bilgisayar mühendisi)
print(chain_2.invoke({"input": "Aydın 34 yaşında, başarılı bir bilgisayar mühendisiydi"}))

# İkinci test: Bir şehir hakkında bilgi içeren cümle
# Dikkat: "Aydın" burada hem kişi adı hem şehir adı olabilir!
# LLM bağlamdan (plaka, iklim) bunun şehir olduğunu anlayacak
# Beklenti: Sehir objesi dönsün (isim: Aydın, plaka_no: 09, iklim: sıcak)
print(chain_2.invoke({"input": "Aydın'da hava her zaman sıcaktır ve bu yüzden 09 plakalı araçlarda klima hep çalışır"}))
