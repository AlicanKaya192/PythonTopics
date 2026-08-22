# Tavsiye Sistemleri (Recommendation Systems)

Kullanıcılara ilgi duyabilecekleri ürün veya içerikleri önermek için kullanılan algoritmalar.
- **11.1 - Birliktelik Kuralı (Association Rule Learning):**
    - **11.1.1 - Tavsiye Sistemleri:** Tavsiye sistemlerine genel bakış ve türleri.
    - **11.1.2 - Birliktelik Kuralı:** Birliktelik kuralı analizi nedir? (Support, Confidence, Lift).
    - **11.1.3 - Apriori Algoritması Nasıl Çalışır ?:** Apriori algoritmasının çalışma mantığı.
    - **11.1.4_birliktelik_kuralı.py:** Online Retail II veri seti üzerinde birliktelik kuralı analizi uygulaması.
    - **11.1.5 - Tekrar_İçin_Sorular.pdf:** 11.1 konusuna özel tekrar soruları ve cevap anahtarı.
- **11.2 - İçerik Bazlı Öneri (Content Based Recommendation):**
    - **11.2.1 - İçerik Temelli Filtreleme:** İçerik temelli filtreleme nedir?
    - **11.2.2 - Sayım Vektörü:** Metinlerin sayım vektörlerine dönüştürülmesi.
    - **11.2.3 - Metin Vektörleştirme:** TF-IDF yöntemi ile metin vektörleştirme.
    - **11.2.4_içerik_bazlı_öneri.py:** Film açıklamaları (overview) üzerinden içerik bazlı film öneri sistemi.
    - **11.2.5 - Tekrar_İçin_Sorular.pdf:** 11.2 konusuna özel tekrar soruları ve cevap anahtarı.
- **11.3 - Öğe Tabanlı İşbirlikçi Filtreleme (Item-Based Collaborative Filtering):**
    - **11.3.1 - İş Birlikçi Filtreleme:** İşbirlikçi filtreleme yöntemlerine giriş.
    - **11.3.2_öğe_tabanlı_işbirlikçi_filtreleme.py:** MovieLens veri seti üzerinde öğe tabanlı işbirlikçi filtreleme uygulaması.
    - **11.3.3 - Tekrar_İçin_Sorular.pdf:** 11.3 konusuna özel tekrar soruları ve cevap anahtarı.
- **11.4 - Kullanıcı Tabanlı İşbirlikçi Filtreleme (User-Based Collaborative Filtering):**
    - **11.4.1 - Kullanıcı Tabanlı İşbirlikçi Filtreleme:** Kullanıcı tabanlı filtreleme mantığı.
    - **11.4.2_kullanıcı_tabanlı_işbirlikçi_filtreleme.py:** Benzer kullanıcıların beğenilerine göre film önerisi yapma uygulaması.
    - **11.4.3 - Tekrar_İçin_Sorular.pdf:** 11.4 konusuna özel tekrar soruları ve cevap anahtarı.
- **11.5 - Model Tabanlı Matris Faktörleştirme (Model-Based Matrix Factorization):**
    - **11.5.1 - Model Tabanlı Matris Faktörleştirme:** Matris faktörleştirme ve SVD yöntemi.
    - **11.5.2_matris_faktörleştirme.py:** SVD algoritması ile boşluk doldurma ve tahminleme uygulaması.
    - **11.5.3 - Tekrar_İçin_Sorular.pdf:** 11.5 konusuna özel tekrar soruları ve cevap anahtarı.
- **11.6 - Genel Tekrar Soruları:**
    - **11.6.1 - Genel_Tekrar_İçin_Sorular.pdf:** Modülün tamamını (11.1 - 11.5) kapsayan çoktan seçmeli test ve cevap anahtarı.

> **🔗 Ek Kaynaklar ve İleri Okumalar:**
>
> *   **Sentence Transformers:** Metin tabanlı içerik önerilerinde kullanılan embedding modelleri.
>     *   [Model Linki](https://huggingface.co/sentence-transformers/paraphrase-MiniLM-L6-v2)
>     *   [Dökümantasyon](https://huggingface.co/sentence-transformers)
> *   **Implicit ALS:** Özellikle büyük veri setlerinde ve implicit feedback (tıklama, izleme vb.) verilerinde kullanılan kütüphane.
>     *   [GitHub Repo](https://github.com/benfred/implicit)
>     *   [Kaggle H&M Çözümü](https://www.kaggle.com/code/julian3833/h-m-implicit-als-model-0-014)
> *   **Vektör Veritabanları ve Arama (FAISS):** Büyük ölçekli vektör benzerlik aramaları için Facebook AI Research tarafından geliştirilen kütüphane.
>     *   [Medium Yazısı](https://medium.com/@mrcoffeeai/faiss-vector-database-be3a9725172f)
>     *   [GitHub Repo](https://github.com/facebookresearch/faiss)
>     *   [Dökümantasyon](https://faiss.ai/index.html)
