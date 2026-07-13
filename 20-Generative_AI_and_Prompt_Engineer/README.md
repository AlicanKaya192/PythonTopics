# Generative AI & Prompt Engineer

Üretken yapay zeka modelleri, dil modelleri mimarileri ve prompt mühendisliği teknikleri.

> **🔑 API Anahtarları:** Bu klasördeki scriptleri çalıştırmak için OpenAI, Anthropic, Google Gemini, Cohere gibi servislere ait API anahtarları gerekir. [`.env.example`](./.env.example) dosyasını `.env` olarak kopyalayıp kendi anahtarlarınızla doldurun. `.env` dosyası `.gitignore` ile korunmaktadır, asla commit etmeyin.
- **20.1 - Teorik Alt Yapı ve Modeller:**
    - **20.1.1-Üretken_Yapay_Zeka_vs_Klasik_Yapay_Zeka.pdf:** Üretken AI ve geleneksel AI arasındaki temel farklar, kullanım alanları ve avantajları.
    - **20.1.2-Çekişmeli_Üretici_Ağlar_(GANS).pdf:** GAN mimarisi, Generator ve Discriminator yapıları, eğitim süreci ve görsel üretim uygulamaları.
    - **20.1.3-Transformer_Mimarisi_1.pdf:** Transformer mimarisine giriş, Attention mekanizması ve Self-Attention kavramları.
    - **20.1.4-Transformer_Mimarisi_2.pdf:** Encoder-Decoder yapıları, Multi-Head Attention ve Positional Encoding detayları.
    - **20.1.5-Büyük_Dil_Modelleri_(LLMs).pdf:** GPT, BERT, LLaMA gibi büyük dil modellerinin yapısı, eğitimi ve kullanım senaryoları.
    - **20.1.6-Büyük_Dil_Modelleri_Sözlüğü.pdf:** LLM dünyasında sıkça kullanılan terimler ve tanımları.
    - **20.1.7-Token_ve_Tokenization.pdf:** Tokenization nedir? Subword tokenization yöntemleri (BPE, WordPiece, SentencePiece) ve önemi.
    - **20.1.8-Bağlam_Penceresi.pdf:** Context Window kavramı, token limitleri ve uzun metin işleme stratejileri.
    - **20.1.9-Parametreler.pdf:** Model parametreleri, ağırlıklar ve parametre sayısının model kapasitesine etkisi.
    - **20.1.10-Modellerin_Karşılaştırılması.pdf:** Farklı LLM'lerin performans, hız ve maliyet açısından karşılaştırılması.
    - **20.1.11-Ölçekleme_İlkeleri.pdf:** Scaling Laws, model boyutu, veri miktarı ve hesaplama gücü ilişkisi.
    - **20.1.12-Dil_Modelleri_Genel_Değerlendirme.pdf:** LLM'lerin güçlü yönleri, sınırlamaları ve gelecek perspektifi.
    - **20.1.13-Difüzyon_Modelleri.pdf:** Diffusion Models çalışma prensibi, gürültü ekleme/çıkarma süreci ve görsel üretim yetenekleri.
    - **20.1.14-Difüzyon_Modelleri_Genel_Değerlendirme.pdf:** DALL-E, Stable Diffusion, Midjourney gibi modellerin değerlendirilmesi.
- **20.2 - Temel Operasyonlar:**
    - **20.2.1 - Temel Giriş:** Üretken AI uygulamaları geliştirmek için gerekli temel araçlara giriş.
    - **20.2.2 - Streamlit 101:** Streamlit ile web uygulaması geliştirme.
    - **20.2.3 - Metin Üretme Konu:** Metin üretimi için teorik alt yapı.
    - **20.2.4 - Metin Üretme Uygulama 101:** Farklı LLM API'leri ile metin üretme uygulamaları.
    - **20.2.5 - Görsel Üretme Konu:** Görsel üretimi için teorik alt yapı.
    - **20.2.6 - Görsel Üretme Uygulama 101:** AI ile görsel üretme ve anlama uygulamaları.
    - **20.2.7 - Ses Üretme Konu:** Ses üretimi ve işleme için teorik alt yapı.
    - **20.2.8 - Ses Üretme Uygulama 101:** AI ile ses işleme uygulamaları.
    - **20.2.9 - Kod Üretme Konu:** AI ile kod üretimi için teorik alt yapı.
    - **20.2.10 - Kod Üretme Uygulama 101:** AI ile kod üretme uygulamaları.
    - **20.2.11 - Çoklu-Form Konu:** Çoklu form (multimodal) uygulamalar için teorik alt yapı.
- **20.3 - VoiceDraw:** Sesli Çizim Uygulama Projesi
- **20.4 - LangChain Çerçevesi:** LangChain kütüphanesi ile gelişmiş LLM uygulamaları geliştirme.
- **20.5 - VidChat:** YouTube Video ile Sohbet Projesi
- **20.6 - Bellek Genişletme RAG (Retrieval-Augmented Generation)**
- **20.7 - Otonom Ajanlar (Autonomous Agents)**
- **20.8 - İnce Ayar (Fine-Tuning)**
- **20.9 - Data Explorer:** Doğal Dilde Veri Keşfi Projesi
- **20.10 - Yerelde Çalışma (Local LLM)**
- **20.11 - Güvenli ve Sorumlu Yapay Zeka Uygulamaları**
