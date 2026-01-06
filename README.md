# Alican Kaya Data-Science-RoadMap

[Portfolio](https://alican-kaya.com/) | [LinkedIn](https://www.linkedin.com/in/alican-kaya-881650234/)

---

![License](https://img.shields.io/badge/license-Custom-blue) ![Version](https://img.shields.io/badge/version-3.14.2-blue) ![Language](https://img.shields.io/badge/language-Python-yellow) ![GitHub](https://img.shields.io/badge/GitHub-AlicanKaya192/PythonTopics.git-black?logo=github)

---

<img src="https://github.com/user-attachments/assets/7c5aefab-2a2d-4d28-afb6-fb2863392e6f" width="640" />

## 📑 İçindekiler
* [📌 Repository Hakkında](#-repository-hakkında)
* [📚 Öğrenim Yol Haritası ve İçerikler](#-öğrenim-yol-haritası-ve-içerikler)
  * [1️⃣ Çalışma Ortamı Ayarları](#1️⃣-çalışma-ortamı-ayarları)
  * [2️⃣ Veri Yapıları](#2️⃣-veri-yapıları)
  * [3️⃣ Fonksiyonlar, Koşullar, Döngüler ve Comprehensions](#3️⃣-fonksiyonlar-koşullar-döngüler-ve-comprehensions)
  * [4️⃣ Egzersizler (Python ve List Comprehensions)](#4️⃣-egzersizler-python-ve-list-comprehensions)
  * [5️⃣ Numpy](#5️⃣-numpy)
  * [6️⃣ Pandas](#6️⃣-pandas)
  * [7️⃣ Veri Görselleştirme (Matplotlib & Seaborn)](#7️⃣-veri-görselleştirme-matplotlib--seaborn)
  * [8️⃣ Gelişmiş Fonksiyonel Keşifçi Veri Analizi (EDA)](#8️⃣-gelişmiş-fonksiyonel-keşifçi-veri-analizi-eda)
  * [9️⃣ CRM Analitik](#9️⃣-crm-analitik)
  * [1️⃣0️⃣ Ölçümleme Problemleri](#1️⃣0️⃣-ölçümleme-problemleri)
  * [1️⃣1️⃣ Tavsiye Sistemleri (Recommendation Systems)](#1️⃣1️⃣-tavsiye-sistemleri-recommendation-systems)
  * [1️⃣2️⃣ Feature Engineering (Özellik Mühendisliği)](#1️⃣2️⃣-feature-engineering-özellik-mühendisliği)
  * [1️⃣3️⃣ Machine Learning (Makine Öğrenimi)](#1️⃣3️⃣-machine-learning-makine-öğrenimi)
  * [1️⃣4️⃣ GIT](#1️⃣4️⃣-git)
  * [1️⃣9️⃣ Generative AI & Prompt Engineering](#1️⃣9️⃣-generative-ai--prompt-engineering)
* [📂 Ekstra Projeler ve Kaynaklar](#-ekstra-projeler-ve-kaynaklar)
* [📖 Proje Durumu ve İlerleme](#-proje-durumu-ve-ilerleme)
* [💡 Önerilen Çalışma Yöntemleri](#-önerilen-çalışma-yöntemleri)
* [🤝 Katkıda Bulunma](#-katkıda-bulunma)

---

## 📌 Repository Hakkında

Bu repository, Python programlama dili öğrenim sürecimde oluşturduğum notları, örnek kodları ve projeleri içeren kapsamlı bir kaynaktır. **Veri Bilimi ve Makine Öğrenimi** yol haritasını takip ederek; temel Python konularından başlayıp, ileri seviye veri analizi, özellik mühendisliği ve makine öğrenimi modellerine kadar uzanan bir yapı sunmaktadır.

Amacım, bu süreçte öğrendiklerimi organize bir şekilde belgelemek ve benzer yoldan geçenler için faydalı bir rehber oluşturmaktır.

---

> [!CAUTION]
> ## ⚠️ Kritik: Gerekli Bağımlılıkların Kurulumu
> 
> Bu repository'deki kodları çalıştırabilmek için **`requirements.txt`** dosyasındaki tüm kütüphanelerin yüklenmesi gerekmektedir.
> 
> ### `requirements.txt` Nedir?
> Bu dosya, projenin ihtiyaç duyduğu Python kütüphanelerinin listesini içerir. İçeriğinde; **pandas**, **numpy**, **scikit-learn**, **matplotlib**, **seaborn**, **xgboost**, **lightgbm**, **catboost**, **streamlit**, **openai**, **google.generativeai** ve daha birçok veri bilimi, makine öğrenimi ve üretken AI kütüphanesi bulunmaktadır.
> 
> ### Kurulum Adımları:
> ```bash
> # 1. Repository'yi klonlayın
> git clone https://github.com/AlicanKaya192/Data-Science-RoadMap.git
> 
> # 2. Proje dizinine gidin
> cd Data-Science-RoadMap
> 
> # 3. (Önerilen) Sanal ortam oluşturun ve aktif edin
> python -m venv venv
> # Windows:
> venv\Scripts\activate
> # macOS/Linux:
> source venv/bin/activate
> 
> # 4. Tüm bağımlılıkları yükleyin
> pip install -r requirements.txt
> ```
> 
> **Not:** Bazı kütüphaneler (örn: `google.generativeai`, `openai`) API anahtarı gerektirebilir. İlgili modüllerin dokümantasyonlarını inceleyiniz.

---

## 📚 Öğrenim Yol Haritası ve İçerikler

Repository içerisindeki klasörler, öğrenim sırasına göre numaralandırılmıştır. Aşağıdaki adımları takiperek sistematik bir şekilde ilerleyebilirsiniz.

### 1️⃣ Çalışma Ortamı Ayarları
Python geliştirme ortamının kurulması ve yönetilmesi ile ilgili temel adımlar.
- **1.1 - setting_up_working_environment.py:** Çalışma ortamı kurulumu ve temel ayarlar.
- **1.2 - What is a virtual environment ( Sanal Ortam Nedir ? ):** Sanal ortamların (Virtual Environment) tanımı, neden gerekli olduğu ve izole çalışma ortamlarının önemi.
- **1.3 - Package Management ( Paket Yönetimi ):** Python paket yönetimi kavramı, `pip`, `pipenv` ve `conda` araçlarının kullanımı ve farkları.

### 2️⃣ Veri Yapıları
Python'un temel yapı taşları olan veri tiplerinin detaylı incelenmesi.
- **data_structures.py:** String, List, Dictionary, Tuple ve Set veri yapıları, metodları ve kullanım alanları.

### 3️⃣ Fonksiyonlar, Koşullar, Döngüler ve Comprehensions
Programlama mantığının temelleri ve fonksiyonel programlama araçları.
- **functions_conditions_loops_comprehensions.py:** Fonksiyon tanımlama, `if-else` yapıları, döngüler, `zip`, `lambda`, `map`, `filter`, `reduce` ve Comprehension yapıları.

### 4️⃣ Egzersizler (Python ve List Comprehensions)
Öğrenilen temel konuların pekiştirilmesi için pratik çalışmalar.
- **4.1_Python_Exercises.py:** Veri yapıları, string manipülasyonları ve temel Python fonksiyonları üzerine alıştırmalar.
- **4.2_List_Comprehension_Exercises.py:** `Car_crashes` veri seti üzerinde List Comprehension yapısı ile değişken isimlendirme ve filtreleme pratikleri.

### 5️⃣ Numpy
Bilimsel hesaplamalar ve çok boyutlu dizi işlemleri.
- **data_analysis_numpy.py:** Array yapısı, boyutlandırma, indeksleme, fancy index ve matematiksel işlemler.

### 6️⃣ Pandas
Veri analizi ve manipülasyonu için en temel kütüphane.
- **1 - data_analysis_pandas.py:**
    - **Pandas Series:** Seri oluşturma ve özelliklerini inceleme.
    - **Veri Okuma:** Farklı kaynaklardan veri yükleme.
    - **Veri Manipülasyonu:** Seçim, filtreleme, toplulaştırma (Aggregation), gruplama (Grouping) ve birleştirme (Join) işlemleri.
- **2 - Pandas_exercise.py:** Titanic veri seti üzerinde veri analizi, tip dönüşümleri ve `apply`, `lambda` fonksiyonlarının kullanımıyla ilgili kapsamlı alıştırmalar.

> **🔗 Ek Kaynaklar ve Dokümantasyon:**
>
> *   **Veri Filtreleme ve Sorgulama:**
>     *   [`str.contains`](https://pandas.pydata.org/docs/reference/api/pandas.Series.str.contains.html): String içeren verileri filtreleme.
>     *   [`isin`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.isin.html): Liste içindeki değerlere göre filtreleme.
> *   **Veri Özetleme ve Gruplama:**
>     *   [`groupby`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html): Veriyi gruplara ayırarak işlem yapma.
>     *   [`pivot_table`](https://pandas.pydata.org/docs/reference/api/pandas.pivot_table.html): Veriyi özet tablo haline getirme.
> *   **Veri Tipleri (Object vs Category):**
>     *   [When to use Category rather than Object?](https://www.includehelp.com/python/when-to-use-category-rather-than-object.aspx)
>     *   [Pandas Categorical Data Types](https://pbpython.com/pandas_dtypes_cat.html)
>     *   [`CategoricalDtype` Dokümantasyonu](https://pandas.pydata.org/docs/reference/api/pandas.CategoricalDtype.html)

### 7️⃣ Veri Görselleştirme (Matplotlib & Seaborn)
Veriyi anlamlandırmak ve sunmak için görselleştirme teknikleri.
- **Veri_Görselleştirme_Matplotlib&Seaborn.py:** Çizgi, sütun, histogram, scatter plot grafikleri ve özelleştirme teknikleri.

### 8️⃣ Gelişmiş Fonksiyonel Keşifçi Veri Analizi (EDA)
Veri setini sistematik olarak analiz etme metodolojisi.
- **gelişmiş_fonksiyonel_keşifçi_veri_analizi.py:** Genel resim, kategorik/sayısal değişken analizi, hedef değişken analizi ve korelasyon analizi.

### 9️⃣ CRM Analitik
Müşteri İlişkileri Yönetimi ve veri odaklı pazarlama stratejileri.
- **9.1 CRM Giriş:**
    - **9.1.1 - CRM NEDİR ?:** CRM kavramı, Müşteri Yaşam Döngüsü (Customer Lifecycle) ve KPI'ların önemi.
    - **9.1.2 - CRM.pdf:** CRM kavramları ve stratejileri üzerine detaylı sunum dosyası.
    - **9.1.3 - KPIs_NEDİR:** Temel Performans Göstergeleri (KPI) detayları, Müşteri Kazanma Oranı (Customer Acquisition Rate) ve Müşteri Elde Tutma Oranı (Customer Retention Rate).
    - **9.1.4 - Cohort_Analizi:** Cohort analizi tanımı, ortak özelliklere sahip grupların zaman içindeki davranışlarının incelenmesi.
- **9.2 RFM Analizi:**
    - **9.2.1 - RFM NEDİR ?:** RFM analizi tanımı, metrikleri (Recency, Frequency, Monetary) ve müşteri segmentasyonundaki rolü.
    - **9.2.2_rfm_analizi.py:** Python ile RFM analizi ve müşteri segmentasyonu uygulaması.
- **9.3 Müşteri Yaşam Boyu Değeri (CLTV) ve Tahmini:**
    - **9.3.1 - Yaşam Boyu Değeri:**
        - **9.3.1.1 - What is customer lifetime value ?:** CLTV kavramı, hesaplama mantığı ve işletmeler için önemi.
        - **9.3.1.2_cltv.py:** CLTV hesaplama uygulaması.
    - **9.3.2 - Yaşam Boyu Tahmini:**
        - **9.3.2.1 - Customer Lifetime Value Prediction:** Geleceğe yönelik CLTV tahmini ve stratejik önemi.
        - **9.3.2.2 - Expected Number of Transaction with BG and NBD:** BG-NBD modeli ile müşterilerin gelecekteki işlem sayılarının tahmini.
        - **9.3.2.3 - Gamma Gamma Sub Model:** Gamma-Gamma modeli ile müşterilerin ortalama işlem değerlerinin tahmini.
        - **9.3.2.4_BG-NBD_ve_GammaGamma_ile_CLTV_tahmini.py:** BG-NBD ve Gamma-Gamma modelleri ile CLTV tahmini uygulaması.
- **9.4 Projeler:**
    - **9.4.1 - FLO_RFM_Analizi.pdf:** FLO RFM analizi projesi için detaylı açıklamalar ve görevler.
    - **9.4.2_FLO_CLTV_Prediction.py:** FLO verisi ile BG-NBD ve Gamma-Gamma modelleri kullanılarak CLTV tahmini projesi.
    - **9.4.3_FLO_RFM.py:** FLO verisi ile uçtan uca RFM analizi ve segmentasyon projesi.

### 1️⃣0️⃣ Ölçümleme Problemleri
Ürünlerin ve kullanıcı geri bildirimlerinin doğru bir şekilde değerlendirilmesi ve sıralanması için kullanılan istatistiksel yöntemler.
- **10.1 - Ölçüm Problemleri:** Ölçümleme problemlerine giriş, sosyal ispat (Social Proof) kavramı ve sıralama mantığı.
- **10.2 - Ürünleri Puanlama (Rating Products):**
    - **10.2.1_rating_products.py:** Ortalama puan, zamana dayalı ağırlıklı ortalama (Time-Based Weighted Average) ve kullanıcı temelli ağırlıklı ortalama (User-Based Weighted Average) hesaplamaları.
- **10.3 - Ürünleri Sıralama (Sorting Products):**
    - **10.3.1_sorting_products.py:** Derecelendirme, yorum ve satın alma sayılarına göre sıralama, Bayesian Average Rating (BAR) Score ve Hibrit Sıralama yöntemleri. IMDB film veri seti üzerinde uygulama.
- **10.4 - Değerlendirmeleri Sıralama (Sorting Reviews):**
    - **10.4.1_sorting_reviews.py:** Kullanıcı yorumlarını sıralama yöntemleri. Up-Down Diff Score, Average Rating Score ve Wilson Lower Bound Score ile güven aralığına dayalı sıralama.
- **10.5 - AB Testing:**
    > **Not:** Bu bölümdeki teorik konuları (.txt dosyaları), `10.5.8_ab_testing.py` uygulama dosyasındaki ilgili kod bloklarına geldiğinizde okumanız, konuları daha iyi pekiştirmenizi sağlayacaktır.

    - **10.5.1 - AB Testing Nedir ?:** AB Testinin tanımı, kullanım amaçları ve temel prensipleri.
    - **10.5.2 - Güven Aralığı:** İstatistiksel güven aralığı kavramı ve hesaplanması.
    - **10.5.3 - Korelasyon:** Değişkenler arasındaki ilişkinin yönü ve şiddeti.
    - **10.5.4 - Hipotez Testleri:** Hipotez kurma, H0 ve H1 hipotezleri, p-value ve istatistiksel anlamlılık.
    - **10.5.5 - İki Grup Ortalamasını Karşılaştırma:** Bağımsız iki örneklem T-Testi ve varsayımları.
    - **10.5.6 - İki Grup Oran Karşılaştırma:** İki farklı grubun oranlarının karşılaştırılması.
    - **10.5.7 - ikiden Fazla Grup Ortalaması Karşılaştırma:** ANOVA (Varyans Analizi) testi.
    - **10.5.8_ab_testing.py:** AB Testi uygulamaları, parametrik ve non-parametrik testler, hipotez testleri ve sonuçların yorumlanması.

### 1️⃣1️⃣ Tavsiye Sistemleri (Recommendation Systems)
Kullanıcılara ilgi duyabilecekleri ürün veya içerikleri önermek için kullanılan algoritmalar.
- **11.1 - Birliktelik Kuralı (Association Rule Learning):**
    - **11.1.1 - Tavsiye Sistemleri:** Tavsiye sistemlerine genel bakış ve türleri.
    - **11.1.2 - Birliktelik Kuralı:** Birliktelik kuralı analizi nedir? (Support, Confidence, Lift).
    - **11.1.3 - Apriori Algoritması Nasıl Çalışır ?:** Apriori algoritmasının çalışma mantığı.
    - **11.1.4_birliktelik_kuralı.py:** Online Retail II veri seti üzerinde birliktelik kuralı analizi uygulaması.
- **11.2 - İçerik Bazlı Öneri (Content Based Recommendation):**
    - **11.2.1 - İçerik Temelli Filtreleme:** İçerik temelli filtreleme nedir?
    - **11.2.2 - Sayım Vektörü:** Metinlerin sayım vektörlerine dönüştürülmesi.
    - **11.2.3 - Metin Vektörleştirme:** TF-IDF yöntemi ile metin vektörleştirme.
    - **11.2.4_içerik_bazlı_öneri.py:** Film açıklamaları (overview) üzerinden içerik bazlı film öneri sistemi.
- **11.3 - Öğe Tabanlı İşbirlikçi Filtreleme (Item-Based Collaborative Filtering):**
    - **11.3.1 - İş Birlikçi Filtreleme:** İşbirlikçi filtreleme yöntemlerine giriş.
    - **11.3.2_öğe_tabanlı_işbirlikçi_filtreleme.py:** MovieLens veri seti üzerinde öğe tabanlı işbirlikçi filtreleme uygulaması.
- **11.4 - Kullanıcı Tabanlı İşbirlikçi Filtreleme (User-Based Collaborative Filtering):**
    - **11.4.1 - Kullanıcı Tabanlı İşbirlikçi Filtreleme:** Kullanıcı tabanlı filtreleme mantığı.
    - **11.4.2_kullanıcı_tabanlı_işbirlikçi_filtreleme.py:** Benzer kullanıcıların beğenilerine göre film önerisi yapma uygulaması.
- **11.5 - Model Tabanlı Matris Faktörleştirme (Model-Based Matrix Factorization):**
    - **11.5.1 - Model Tabanlı Matris Faktörleştirme:** Matris faktörleştirme ve SVD yöntemi.
    - **11.5.2_matris_faktörleştirme.py:** SVD algoritması ile boşluk doldurma ve tahminleme uygulaması.

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

### 1️⃣2️⃣ Feature Engineering (Özellik Mühendisliği)
Ham veriden makine öğrenimi modelleri için anlamlı özellikler türetme sanatı.
- **12.1 Aykırı Değerler (Outliers):**
    - **12.1.1 - Feature Engineering & Data Pre-Processing:** Veri ön işlemenin önemi, "Garbage In, Garbage Out" prensibi.
    - **12.1.2 - Outliers (Aykırı Değerler):** Aykırı değerlerin tanımı, neden olduğu problemler ve tespit yöntemleri.
    - **12.1.3 - Uygulama:** Python ile aykırı değerleri yakalama ve analiz etme.
- **12.2 Eksik Değerler (Missing Values):**
    - **12.2.1 - Eksik Değerler:** Eksik veri türleri ve çözüm stratejileri (Silme, Değer Atama, Tahmine Dayalı Yöntemler).
    - **12.2.2 - Uygulama:** Eksik değerlerin tespiti ve görselleştirilmesi.
- **12.3 Encoding & Scaling:**
    - **12.3.1 - Encoding:** Label Encoding mantığı, değişken dönüşümleri ve uygulama alanları.
    - **12.3.2_Label Encoding Uygulama.py:** Label Encoding ve Binary Encoding uygulamaları.
    - **12.3.3 - One Hot Encoding:** Nominal değişkenler için dönüşüm yöntemi ve sıralama hatasından kaçınma.
    - **12.3.4_One Hot Encoding Uygulama.py:** One Hot Encoding uygulaması ve dummy değişken tuzağı.
    - **12.3.5 - Rare Encoding:** Nadir sınıfların analizi ve birleştirilmesi (Rare Encoding).
    - **12.3.6_Rare Encoding Uygulama.py:** Nadir sınıfların tespiti ve Rare Encoding işlemi.
    - **12.3.7 - Feature Scalling Nedir:** Özellik ölçeklendirme (Feature Scaling) kavramı, neden gerekli olduğu ve mesafe tabanlı algoritmalara etkisi.
    - **12.3.8_Feature Scalling uygulama.py:** StandardScaler, RobustScaler, MinMaxScaler gibi ölçeklendirme yöntemlerinin uygulaması.
- **12.4 Feature Extraction:**
    - **12.4.1 - Feature Extraction:** Özellik çıkarımı nedir? Yapısal ve yapısal olmayan verilerden değişken türetme mantığı.
    - **12.4.2 - Uygulama:** Binary özellikler, metin/tarih analizi ve özellik etkileşimleri (Feature Interactions) ile değişken türetme uygulaması.
- **12.5 Uygulama:** Titanic ve Application Train veri setleri üzerinde özellik mühendisliği tekniklerinin bütünleşik uygulaması.
- **12.6 Extra:** `Diabete_Feature_Engineering.py` ile diyabet veri seti üzerinde uçtan uca özellik mühendisliği uygulaması.

### 1️⃣3️⃣ Machine Learning (Makine Öğrenimi)
Veriden öğrenen modellerin kurulması ve değerlendirilmesi.
- **13.1 - Temel Kavramlar:**
    - **13.1.1 - Makine Öğrenmesine Giriş:** Makine öğrenmesi tanımı, geleneksel programlama ile farkları.
    - **13.1.2 - Değişken Türleri:** Bağımlı/Bağımsız değişkenler ve veri tipleri.
    - **13.1.3 - Öğrenme Türleri:** Gözetimli, Gözetimsiz ve Pekiştirmeli öğrenme.
    - **13.1.4 - Problem Türleri:** Regresyon ve Sınıflandırma problemleri.
    - **13.1.5 - Model Başarı Değerlendirme Yöntemleri:** Confusion Matrix, Accuracy, Precision, Recall, F1-Score, ROC-AUC.
    - **13.1.6 - Model Doğrulama Yöntemleri:** Hold-out, K-Fold Cross Validation.
    - **13.1.7 - Yanlılık - Varyans Değiş Tokuş:** Bias-Variance Tradeoff, Overfitting ve Underfitting.
    - **13.1.8 - Tekrar İçin Sorular:** Konu tekrarı için test soruları.
- **13.2 - Doğrusal Regresyon (Linear Regression):**
    - **13.2.1 - Doğrusal Regresyon:** Basit ve Çoklu Doğrusal Regresyon mantığı.
    - **13.2.2 - Ağırlıkların Bulunması:** Parametre tahmini yöntemleri.
    - **13.2.3 - Regresyon Modellerinde Başarı Değerlendirme:** MSE, RMSE, MAE, R-Squared.
    - **13.2.4 - Parametrelerin Tahmin Edilmesi:** Parametre vs Hiperparametre.
    - **13.2.5 - Doğrusal Regresyon için Gradient Descent:** Gradyan İniş algoritmasının çalışma mantığı.
    - **13.2.6_linear_regression.py:** Python ile Sales Prediction uygulaması (Sklearn & Gradient Descent).
    - **13.2.7 - Tekrar İçin Sorular:** Doğrusal regresyon konu tekrarı soruları.
- **13.3 - Lojistik Regresyon (Logistic Regression):**
    - **13.3.1 - Lojistik Regresyon:** Sınıflandırma algoritması olarak Lojistik Regresyon ve Sigmoid fonksiyonu.
    - **13.3.2 - Lojistik Regresyon için Gradient Descent:** Log Loss fonksiyonu ve optimizasyon süreci.
    - **13.3.3 - Sınıflandırma Problemlerinde Başarı Değerlendirme:** Accuracy, Precision, Recall, F1-Score metrikleri.
    - **13.3.4 - Karmaşıklık Matrisi (Confusion Matrix):** TP, TN, FP, FN kavramları ve hata analizi.
    - **13.3.5 - Classification Threshold:** Sınıflandırma eşik değerinin (Threshold) önemi ve etkisi.
    - **13.3.6 - ROC Eğrisi (ROC Curve):** ROC eğrisi ve AUC (Area Under Curve) ile model performansı ölçümü.
    - **13.3.7 - LOG Loss:** Logaritmik Kayıp (Binary Cross Entropy) fonksiyonunun detayları.
    - **13.3.8_logistic_regression.py:** Python ile Diyabet Tahmini (Diabetes Prediction) uygulaması.
    - **13.3.9 - Tekrar İçin Sorular:** Lojistik regresyon ve sınıflandırma metrikleri üzerine kapsamlı test soruları.
- **13.4 - KNN (K-Nearest Neighbors):**
    - **13.4.1 - K-En Yakın Komşu:** KNN algoritmasının çalışma mantığı, mesafe ölçümleri ve "Lazy Learner" kavramı.
    - **13.4.2_knn.py:** Python ile Diyabet Tahmini (Diabetes Prediction) üzerinde KNN uygulaması ve model tuning.
    - **13.4.3 - Tekrar İçin Sorular:** KNN algoritması üzerine pekiştirme soruları.
- **13.5 - Case Studies (Uygulamalı Çalışmalar):**
    - **13.5.1 - Case Study 1.pdf:** Maaş tahmini projesi için görev tanımları ve açıklamalar.
    - **13.5.2_case_study_1_uygulama.py:** Doğrusal Regresyon ile deneyim yılına göre maaş tahmini uygulaması.
    - **15.5.3 - Case study 2.pdf:** Churn ve Fraud tespiti üzerine vaka analizi dokümanı.
    - **15.5.4_case_study_2_uygulama.py:** Müşteri terk ve dolandırıcılık tespiti üzerine sınıflandırma metrikleri analizi.
    - **15.5.6 - Case Study 3.pdf:** Telco Churn Prediction projesi için detaylı proje dokümanı.
    - **15.5.7_case_study_3_uygulama.py:** Uçtan uca makine öğrenmesi projesi (EDA, Preprocessing, Modelleme).
- **13.6 - CART (Classification & Regression Tree):**
    - **13.6.1 - CART:** Karar ağaçları teorisi, Gini safsızlığı ve entropi kavramları.
    - **13.6.2_cart.py:** Python ile Karar Ağacı Sınıflandırma uygulaması, model tuning ve görselleştirme.
    - **13.6.3 - Tekrar İçin Sorular:** CART algoritması ve karar ağaçları üzerine test soruları.
- **13.7 - Gelişmiş Ağaç Yöntemleri (Advanced Tree Methods):**
    - **13.7.1 - Rastgele Ormanlar:** Rastgele Ormanlar algoritmasının çalışma mantığı, Bagging yöntemi ve teorik temelleri.
    - **13.7.2 - Gradient Boosting Machines:** GBM algoritmasının çalışma prensibi, Boosting yöntemi ve hata düzeltme yaklaşımı.
    - **13.7.3 - XGBoost ( eXtreme Gradient Boosting ):** XGBoost algoritmasının özellikleri, ölçeklenebilirliği ve optimizasyon teknikleri.
    - **13.7.4 - LightGBM:** LightGBM algoritmasının yaprak odaklı büyüme stratejisi ve hız avantajları.
    - **13.7.5 - CatBoost:** CatBoost algoritmasının kategorik değişkenlerle çalışma yeteneği ve simetrik ağaç yapısı.
    - **13.7.6_advanced_trees.py:** Random Forests, GBM, XGBoost, LightGBM ve CatBoost algoritmalarının karşılaştırmalı uygulaması. Hiperparametre optimizasyonu (GridSearchCV, RandomizedSearchCV), değişken önem düzeyleri (Feature Importance) ve doğrulama eğrileri (Validation Curves) analizi.
    - **13.7.7 - Tekrar İçin Sorular:** Gelişmiş ağaç yöntemleri (Random Forest, GBM, XGBoost, LightGBM, CatBoost) üzerine kapsamlı test soruları.
- **13.8 - Dengesiz Veri Seti Nedir? Nasıl Başa Çıkılır? (Imbalanced Datasets):**
    - **13.8.1_Dengesiz_Veri_Seti_Birebir.ipynb:** Dengesiz veri setleri ile başa çıkma yöntemleri. Random Oversampling, Random Undersampling ve SMOTE tekniklerinin uygulanması ve Lojistik Regresyon modeli üzerindeki etkilerinin karşılaştırılması.
        > **🔗 Referanslar:**
        > * [Random Oversampling and Undersampling](https://machinelearningmastery.com/random-oversampling-and-undersampling-for-imbalanced-classification/)
        > * [SMOTE for Imbalanced Classification](https://machinelearningmastery.com/smote-oversampling-for-imbalanced-classification/)
        > * [Understanding Confusion Matrix](https://towardsdatascience.com/understanding-confusion-matrix-a9ad42dcfd62)
        > * [Understanding AUC - ROC Curve](https://towardsdatascience.com/understanding-auc-roc-curve-68b2303cc9c5)
        > * [Tactics to Combat Imbalanced Classes](https://machinelearningmastery.com/tactics-to-combat-imbalanced-classes-in-your-machine-learning-dataset/)
- **13.9 - Case Study (House Price Prediction):**
    - **13.9.1 - House_Price-221119-122427.pdf:** Proje ile ilgili detaylı açıklamaları ve görevleri içeren PDF dosyası.
    - **13.9.2_HOUSE_PRICE_PREDICTON_SOLUTION.py:** Ev fiyat tahminleme projesi. Veri analizi (EDA), özellik mühendisliği (Feature Engineering), encoding, modelleme (Linear, Ridge, Lasso, ElasticNet, KNN, CART, RF, SVR, GBM, XGBoost, LightGBM, CatBoost), hiperparametre optimizasyonu ve özellik önem düzeyi analizi içeren kapsamlı çözüm.
    - **13.9.2_HOUSE_PRICE_PREDICTON_SOLUTION.ipynb:** Projenin Kaggle uyumlu, İngilizce açıklamalı Jupyter Notebook versiyonu.
- **13.10 - Denetimsiz Öğrenme (Unsupervised Learning):**
    - **13.10.1 - Denetimsiz Öğrenme ( Unsupervised Learning ):** Denetimsiz öğrenme kavramı ve kullanım alanları.
    - **13.10.2 - K-Ortalamalar ( K-Means ):** K-Means kümeleme algoritması ve çalışma mantığı.
    - **13.10.3 - Temel Bileşen Analizi ( Principal Component Analysis ):** PCA ile boyut indirgeme ve varyans analizi.
    - **13.10.4_unsupervised_learning.py:** K-Means, Hiyerarşik Kümeleme ve PCA yöntemlerinin Python ile uygulaması. (USArrests, Hitters, Breast Cancer, Iris, Diabetes veri setleri).
    - **13.10.5 - Tekrar İçin Sorular:** Denetimsiz öğrenme konuları üzerine test soruları.
- **13.11 - Makine Öğrenmesi Pipeline (Machine Learning Pipeline):**
    - **13.11.1_diabetes_pipeline.py:** Uçtan uca makine öğrenmesi pipeline'ı. Veri ön işleme, özellik mühendisliği, model eğitimi ve değerlendirme adımlarının otomatikleştirilmesi.
    - **13.11.1_diabetes_prediction.py:** Eğitilen modelin tahminleme için kullanılması.
    - **13.11.1_diabetes_research.py:** Model geliştirme ve araştırma süreci.
- **13.12 - Case Study 2 (Scoutium Yetenek Avcılığı):**
    - **13.12.1 - Scoutium_Yetenek_Avcılığı_Sınıflandırma.pdf:** Proje ile ilgili detaylı açıklamaları ve görevleri içeren PDF dosyası.
    - **13.12.2_scoutium_prediction.py:** Scoutium veri seti üzerinde makine öğrenmesi ile yetenek avcılığı sınıflandırma projesi. Random Forest, GBM, XGBoost ve LightGBM modellerinin kullanımı.
- **13.13 - Case Study 3 (FLO Müşteri Segmentasyonu):**
    - **13.13.1 - FLO_Unsupervised_Learning_Musteri_Segmantasyonu-220805-080321.pdf:** Proje ile ilgili detaylı açıklamaları ve görevleri içeren PDF dosyası.
    - **13.13.2_flo_unsupervised_learning.py:** FLO veri seti üzerinde K-Means ve Hiyerarşik Kümeleme yöntemleri ile gözetimsiz öğrenme tabanlı müşteri segmentasyonu projesi.
- **13.14 - Genel Tekrar Soruları:**
    - **13.14.1 - Genel Tekrar İçin Sorular:** Makine öğrenimi konularını kapsayan 70 soruluk kapsamlı test ve cevap anahtarı.
- **13.15 - Machine Learning Extra:**
    - `13.15.1_Telco_Churn.py`: Sınıflandırma modelleri ile müşteri terk analizi.
    - **Değerlendirme Tabloları:** Regresyon ve Sınıflandırma modelleri için hata değerlendirme Excel dosyaları.

> **🔗 Ek Kaynaklar (Boosting Modelleri ve Değerlendirme):**
>
> *   **Model Değerlendirme:** [GridSearchCV Scoring Parametreleri](https://scikit-learn.org/stable/modules/model_evaluation.html#scoring-parameter)
> *   **CatBoost:**
>     *   [Kategorik Değişken İşleme](https://catboost.ai/en/docs/concepts/algorithm-main-stages_cat-to-numberic#algorithm-main-stages_cat-to-numberic)
>     *   [Parametre Tuning ve One-Hot Encoding](https://catboost.ai/en/docs/concepts/parameter-tuning)
> *   **Karşılaştırmalar (XGBoost vs LightGBM vs CatBoost):**
>     *   [Medium - Pratik Karşılaştırma](https://medium.com/@rajkiranrao205/xgboost-vs-lightgbm-vs-catboost-a-practical-comparison-with-coffee-cats-code-5fab396ed39d)
>     *   [APXML - Karşılaştırma](https://apxml.com/posts/xgboost-vs-lightgbm-vs-catboost)
>     *   [Neptune.ai - Hangisini Seçmeli?](https://neptune.ai/blog/when-to-choose-catboost-over-xgboost-or-lightgbm)

### 1️⃣4️⃣ GIT
Versiyon kontrol sistemi Git'in temelleri, ileri seviye kullanımı ve kurumsal en iyi uygulamalar.
- **14.1 - GIT Kullanımı:** Git kullanımına dair temel bilgiler ve cheat sheet'ler.
    - **14.1.1 - git-cheat-sheet-education.pdf:** Eğitim amaçlı Git kopya kağıdı.
    - **14.1.2 - git-cheat-sheet.pdf:** Genel Git komutları kopya kağıdı.
    - **14.1.3 - git-cheat-sheet-gitlab.pdf:** GitLab özelinde Git komutları.
- **14.2 - Gerçek GIT Kriz Senaryoları:** Karşılaşılabilecek kriz durumları ve çözüm yolları.
- **14.3 - Kurumsal GIT Kullanımı:** Kurumsal projelerde Git kullanımı ve stratejileri.
- **14.4 - Gerçek Ekip GIT Kuralları Checklist:** Ekip çalışması için Git kuralları kontrol listesi.
- **14.5 - GIT Termonolji Netliği:** Git terimlerinin açıklamaları ve netleştirilmesi.
- **14.6 - Merge vs Rebase Karşılaştırması:** Merge ve Rebase işlemleri arasındaki farklar ve kullanım senaryoları.
- **14.7 - Reset Türleri – Soft - Mixed - Hard:** Git reset türleri ve etkileri.
- **14.8 - Reflog Kullanım Senaryosu:** Reflog ile geçmişe dönük işlemler ve kurtarma senaryoları.
- **14.9 - Production Güvenliği İçin Git Kuralları:** Canlı ortam güvenliği için Git kuralları.
- **14.10 - Branch İsimlendirme & Commit Mesaj Standartları:** Düzenli bir geçmiş için isimlendirme ve mesaj standartları.
- **14.11 - CI CD – Git İlişkisi:** Sürekli Entegrasyon ve Dağıtım süreçlerinde Git'in rolü.
- **14.12 - Rol Bazlı Git Sorumlulukları:** Ekip içindeki rollere göre Git sorumlulukları.
- **14.13 - Interview için Git soruları & güçlü cevaplar:** Git mülakat soruları ve cevapları.

### 1️⃣9️⃣ Generative AI & Prompt Engineering
Üretken yapay zeka modelleri, dil modelleri mimarileri ve prompt mühendisliği teknikleri.
- **19.1 - Teorik Alt Yapı ve Modeller:**
    - **19.1.1-Üretken_Yapay_Zeka_vs_Klasik_Yapay_Zeka.pdf:** Üretken AI ve geleneksel AI arasındaki temel farklar, kullanım alanları ve avantajları.
    - **19.1.2-Çekişmeli_Üretici_Ağlar_(GANS).pdf:** GAN mimarisi, Generator ve Discriminator yapıları, eğitim süreci ve görsel üretim uygulamaları.
    - **19.1.3-Transformer_Mimarisi_1.pdf:** Transformer mimarisine giriş, Attention mekanizması ve Self-Attention kavramları.
    - **19.1.4-Transformer_Mimarisi_2.pdf:** Encoder-Decoder yapıları, Multi-Head Attention ve Positional Encoding detayları.
    - **19.1.5-Büyük_Dil_Modelleri_(LLMs).pdf:** GPT, BERT, LLaMA gibi büyük dil modellerinin yapısı, eğitimi ve kullanım senaryoları.
    - **19.1.6-Büyük_Dil_Modelleri_Sözlüğü.pdf:** LLM dünyasında sıkça kullanılan terimler ve tanımları.
    - **19.1.7-Token_ve_Tokenization.pdf:** Tokenization nedir? Subword tokenization yöntemleri (BPE, WordPiece, SentencePiece) ve önemi.
    - **19.1.8-Bağlam_Penceresi.pdf:** Context Window kavramı, token limitleri ve uzun metin işleme stratejileri.
    - **19.1.9-Parametreler.pdf:** Model parametreleri, ağırlıklar ve parametre sayısının model kapasitesine etkisi.
    - **19.1.10-Modellerin_Karşılaştırılması.pdf:** Farklı LLM'lerin performans, hız ve maliyet açısından karşılaştırılması.
    - **19.1.11-Ölçekleme_İlkeleri.pdf:** Scaling Laws, model boyutu, veri miktarı ve hesaplama gücü ilişkisi.
    - **19.1.12-Dil_Modelleri_Genel_Değerlendirme.pdf:** LLM'lerin güçlü yönleri, sınırlamaları ve gelecek perspektifi.
    - **19.1.13-Difüzyon_Modelleri.pdf:** Diffusion Models çalışma prensibi, gürültü ekleme/çıkarma süreci ve görsel üretim yetenekleri.
    - **19.1.14-Difüzyon_Modelleri_Genel_Değerlendirme.pdf:** DALL-E, Stable Diffusion, Midjourney gibi modellerin değerlendirilmesi.
- **19.2 - Temel Operasyonlar:**
    - **19.2.1 - Temel Giriş:** Üretken AI uygulamaları geliştirmek için gerekli temel araçlara giriş.
        - **19.2.1.1-Temel_Operasyonlar_Giriş.pdf:** Geliştirme ortamı ve araçlara genel bakış.
        - **19.2.1.2-Python_Kurulum.pdf:** Python kurulumu ve yapılandırması ile ilgili adımlar.
        - **19.2.1.3-Visual_Studio_Code_Kurulum.pdf:** VS Code kurulumu ve uzantıları ile geliştirme ortamının hazırlanması.
        - **19.2.1.4-GIT.pdf:** Versiyon kontrol sistemi Git'in kurulumu ve temel kullanımı.
        - **19.2.1.5-Sanal_Ortam.pdf:** Python sanal ortamlarının oluşturulması ve yönetimi.
        - **19.2.1.6-Streamlit_Giriş.pdf:** Streamlit framework'üne giriş ve temel kavramlar.
    - **19.2.2 - Streamlit 101:** Streamlit ile web uygulaması geliştirme.
        - **19.2.2.1_app.py:** Streamlit ile hızlı prototipleme uygulaması. Sayfa yapılandırma, metin gösterme, multimedya (resim, video, ses), kullanıcı etkileşim bileşenleri (button, radio, checkbox, slider, text_input, file_uploader), arayüz yerleşimi (sidebar, tabs) ve program akışı ile bileşen entegrasyonu.
        - **19.2.2.2_session.py:** Streamlit Session State mekanizmasının pratik kullanımı. Oturum boyunca değişken saklama, callback fonksiyonları ve dinamik veri görüntüleme.
    - **19.2.3 - Metin Üretme Konu:** Metin üretimi için teorik alt yapı.
        - **19.2.3.1-Metin_Üretme_1.pdf:** API kullanımı, prompt yapısı ve temel kavramlar.
        - **19.2.3.2-Metin_Üretme_2.pdf:** İleri seviye metin üretme teknikleri.
    - **19.2.4 - Metin Üretme Uygulama 101:** Farklı LLM API'leri ile metin üretme uygulamaları.
        - **19.2.4.1_app.py:** OpenAI GPT API temel kullanımı. Chat Completions API, parametreler (temperature, max_tokens) ve yanıt yapısı.
        - **19.2.4.2_chat.py:** OpenAI GPT ile sohbet botu (Chatbot). Session State ile çok turlu konuşma, mesaj geçmişi yönetimi ve Streamlit Chat UI bileşenleri.
        - **19.2.4.3_claude.py:** Anthropic Claude API kullanımı. Claude modelleri, API farkları ve Streamlit entegrasyonu.
        - **19.2.4.4_command.py:** Cohere Command API kullanımı. Chat history yapısı ve Cohere'e özgü parametreler.
        - **19.2.4.5_gemini.py:** Google Gemini API kullanımı. GenerativeModel, sohbet oturumu ve generation_config ayarları.
        - **19.2.4.6_open_source.py:** Açık kaynak modeller ile metin üretimi (Replicate). Llama 2, Mixtral modelleri ve streaming yanıt işleme.
    - **19.2.5 - Görsel Üretme Konu:** Görsel üretimi için teorik alt yapı.
        - **19.2.5.1-Görsel_Üretme.pdf:** DALL-E, Stable Diffusion ve görsel üretim API'leri.
        - **19.2.5.2-Görsel_Üretme-Parametre_ve_Modeller.pdf:** Görsel üretim parametreleri (size, quality, steps) ve model karşılaştırması.
    - **19.2.6 - Görsel Üretme Uygulama 101:** AI ile görsel üretme ve anlama uygulamaları.
        - **19.2.6.1_image_ops.py:** DALL-E 3 ile görsel oluşturma, görsel varyasyonu ve Stable Diffusion XL entegrasyonu. Diffusion modelleri, negative prompt ve API parametreleri.
        - **19.2.6.2_multi_modality.py:** Çoklu modalite (Multimodality) - Görsel anlama uygulaması. GPT-4 Vision ve Gemini Pro Vision ile görsel analiz, Base64 encoding, URL ve yerel dosya işleme.
    - **19.2.7 - Ses Üretme Konu:** Ses üretimi ve işleme için teorik alt yapı.
        - **19.2.7.1-Ses_Üretme.pdf:** TTS (Text-to-Speech), STT (Speech-to-Text) teknolojileri ve API'leri.
    - **19.2.8 - Ses Üretme Uygulama 101:** AI ile ses işleme uygulamaları.
        - **19.2.8.1_audio_ops.py:** OpenAI TTS-1 ile metin okuma (6 farklı ses karakteri), Whisper ile transkripsiyon ve çeviri, AssemblyAI Conformer ile transkripsiyon. Streamlit ile etkileşimli arayüz.
    - **19.2.9 - Kod Üretme Konu:** AI ile kod üretimi için teorik alt yapı.
        - **19.2.9.1-Kod_Üretme.pdf:** LLM'ler ile kod üretimi, code completion ve programlama asistanları.
    - **19.2.10 - Kod Üretme Uygulama 101:** AI ile kod üretme uygulamaları.
        - **code_generation.py:** AI destekli kod üretme uygulaması.
        - **helper.py:** Kod üretme yardımcı fonksiyonları.
        - **test.py / test.html:** Üretilen kodların test edilmesi için örnek dosyalar.
    - **19.2.11 - Çoklu-Form Konu:** Çoklu form (multimodal) uygulamalar için teorik alt yapı.
        - **19.2.11.1-Çoklu-Form.pdf:** Metin, görsel ve ses kombinasyonu ile çoklu modalite uygulamaları.
- **19.3 - VoiceDraw: Sesli Çizim Uygulama Projesi:** Kullanıcının sesli komutlarıyla AI destekli görsel üretebilmesini sağlayan uçtan uca Streamlit web uygulaması.
    - **19.3.1-Proje_Giriş.pdf:** VoiceDraw proje tanıtımı, uygulama akışı ve mimari yapı.
    - **19.3.2_app.py:** Ana uygulama modülü. Streamlit web arayüzü, session state yönetimi, threading ile eşzamanlı ses kaydı, sohbet geçmişi (chat history) ve AI görsel üretim akışı entegrasyonu.
    - **19.3.3_painter.py:** Görsel üretim modülü. DALL-E 3 API ile metin-görsel üretimi (text-to-image), Gemini Vision API ile çoklu-modal görsel analizi ve iteratif görsel düzenleme (mevcut görsel üzerinde değişiklik yapma) yetenekleri.
    - **19.3.4_recorder.py:** Ses kayıt modülü. PyAudio ile mikrofon erişimi, gerçek zamanlı ses kaydı, 16-bit PCM formatında WAV dosyası oluşturma ve threading ile non-blocking kayıt akışı.
    - **19.3.5_transcriptor.py:** Ses-metin dönüşüm modülü. OpenAI Whisper API ile ses dosyalarını metne dönüştürme (speech-to-text, STT), Türkçe dil desteği ve otomatik noktalama işaretleri.
    > **🔗 Kullanılan Teknolojiler:**
    > * **Streamlit:** Hızlı prototipleme için Python web framework'ü
    > * **OpenAI Whisper:** Ses tanıma (Speech-to-Text)
    > * **OpenAI DALL-E 3:** Metin-görsel üretimi (Text-to-Image)
    > * **Google Gemini Vision:** Çoklu-modal görsel anlama
    > * **PyAudio:** Düşük seviyeli ses giriş/çıkış işlemleri
- **19.4 - LangChain Çerçevesi:** LangChain kütüphanesi ile gelişmiş LLM uygulamaları geliştirme. Döküman yükleme, metin bölme, vektör veritabanları ve RAG (Retrieval-Augmented Generation) sistemleri.
    - **19.4.1-LangChain_Çerçevesi_Giriş.pdf:** LangChain framework'üne giriş, temel kavramlar ve mimari yapı.
    - **19.4.2_loaders.py:** LangChain Döküman Yükleyiciler (Document Loaders). WebBaseLoader ile URL'den içerik çekme, PyPDFLoader ile PDF okuma ve OCR desteği, UnstructuredExcelLoader ile Excel dosyalarını işleme ve HTML formatında tablo çıkarma.
    - **19.4.3_splitter_comparison.py:** Metin Bölme Stratejileri Karşılaştırması. CharacterTextSplitter (karakter bazlı), RecursiveCharacterTextSplitter (akıllı paragraf/cümle bazlı) ve SemanticChunker (anlam bazlı) yöntemlerinin Streamlit arayüzünde yan yana karşılaştırılması.
    - **19.4.4_chain.py:** LangChain Zincir Yapıları. Stuff Documents Chain ile döküman birleştirme, OpenAI Function Runnable ile yapılandırılmış veri çıktısı (Structured Output), Pydantic modelleri ile veri şemaları.
    - **19.4.5_model.py:** LLM Model Karşılaştırma Uygulaması. OpenAI GPT-4, Google Gemini, Anthropic Claude ve Cohere Command modellerinin aynı soruda yan yana karşılaştırılması, temperature ve max_tokens ayarları, yanıt süresi ölçümü.
    - **19.4.6_modelhelper.py:** Model Yardımcı Modülü. Farklı LLM sağlayıcıları için API wrapper fonksiyonları, modüler mimari ve API anahtar yönetimi.
    - **19.4.7_rag.py:** RAG (Retrieval-Augmented Generation) Uygulaması. URL ve PDF tabanlı bellek genişletme, RAG aktif/deaktif karşılaştırması, Streamlit web arayüzü.
    - **19.4.8_raghelper.py:** RAG Yardımcı Modülü. FAISS vektör veritabanı entegrasyonu, RecursiveCharacterTextSplitter ile metin bölme, HuggingFace/OpenAI/Cohere embedding modelleri, context-aware prompt oluşturma.
    > **🔗 Kullanılan Teknolojiler:**
    > * **LangChain:** LLM uygulama geliştirme framework'ü
    > * **FAISS:** Facebook AI vektör benzerlik arama kütüphanesi
    > * **OpenAI Embeddings:** Metin vektörleştirme modeli
    > * **HuggingFace Inference API:** Açık kaynak embedding modelleri
    > * **Streamlit:** İnteraktif web arayüzü
- **19.5 - VidChat: YouTube Video ile Sohbet Projesi:** YouTube videolarının içeriğiyle sohbet etmenizi sağlayan RAG (Retrieval-Augmented Generation) tabanlı uçtan uca Streamlit web uygulaması. Video transkripti üzerinde semantik arama yaparak sorulara yanıt verir.
    - **19.5.1-VidChat_Giriş.pdf:** VidChat proje tanıtımı, uygulama akışı ve mimari yapı.
    - **19.5.2_app.py:** Ana uygulama modülü. Streamlit web arayüzü, Session State ile önbellekleme, iki farklı video seçim yöntemi (URL girişi ve YouTube araması), RAG tabanlı soru-cevap ve referans gösterimi.
    - **19.5.3_raghelper.py:** RAG Yardımcı Modülü. Video transkripti üzerinde RAG uygulaması, RecursiveCharacterTextSplitter ile metin bölme, FAISS vektör veritabanı, OpenAI Embeddings ile semantik arama, Google Gemini ile yanıt üretimi.
    - **19.5.4_videohelper.py:** Video İşlemleri Modülü. YoutubeAudioLoader ile video ses indirme, OpenAI Whisper ile ses-metin dönüşümü (transkripsiyon), scrapetube ile YouTube araması ve video metadata çıkarımı.
    - **19.5.5_youtubevideo.py:** YouTube Video Veri Modeli. Video bilgilerini (ID, başlık, URL, kanal, süre, tarih) tutan data class yapısı.
    > **🔗 Kullanılan Teknolojiler:**
    > * **OpenAI Whisper:** Ses-metin dönüşümü (Speech-to-Text)
    > * **Google Gemini:** Soru-cevap için dil modeli
    > * **LangChain:** RAG pipeline ve döküman işleme
    > * **FAISS:** Vektör benzerlik arama
    > * **scrapetube:** YouTube video arama (API gerektirmez)
    > * **Streamlit:** İnteraktif web arayüzü
- **19.6 - Bellek Genişletme RAG (Retrieval-Augmented Generation):** Gelişmiş RAG teknikleri ve vektör veritabanları ile bellek genişletme uygulamaları. Hibrit arama, HyDE, Multi-Query ve Reranking gibi ileri seviye retrieval stratejileri.
    - **19.6 - Teorik Alt Yapı (PDF Dokümanları):**
        - **19.6.1-Bellek_Genişletme_RAG_Giriş.pdf:** RAG kavramına giriş, semantik arama ve vektör veritabanları temelleri.
        - **19.6.2-İsimlendirme.pdf:** RAG terminolojisi ve temel kavramların isimlendirmesi.
        - **19.6.3-Genel_Mimari.pdf:** RAG sistemlerinin genel mimarisi ve bileşenleri.
        - **19.6.4-Embedding_ve_Vektör_İşlemleri.pdf:** Embedding kavramı ve vektör işlemlerinin temelleri.
        - **19.6.5-Word_Embeddings.pdf:** Kelime gömmeleri (Word2Vec, GloVe) ve semantik temsil.
        - **19.6.6-Embedding_Modelleri.pdf:** Farklı embedding modelleri ve karşılaştırmaları.
        - **19.6.7-Vektör_Veri_Tabanları.pdf:** Vektör veritabanları (ChromaDB, FAISS, Pinecone) ve kullanım alanları.
        - **19.6.8-Semantik_Arama.pdf:** Semantik arama teknikleri ve benzerlik metrikleri.
        - **19.6.9-İleri_Düzey_RAG.pdf:** İleri düzey RAG teknikleri (HyDE, Multi-Query, Reranking, Hibrit Arama).
    - **19.6 - Uygulama Dosyaları:**
        - **basic_rag_with_llama-index_local_storage.py:** LlamaIndex ile Temel RAG Uygulaması. Yerel dosya depolama, vektör indeksi oluşturma ve kalıcı depolama (persistence). `gelecek.pdf` dosyası ile çalışır.
        - **basic_rag_with_langchain.py:** LangChain ile Web Tabanlı RAG. WebBaseLoader ile URL'den içerik çekme, FAISS vektör deposu, Cohere Embeddings ve Google Gemini ile yanıt üretimi.
        - **MMR_search_with_chroma.py:** Maximum Marginal Relevance (MMR) Arama. ChromaDB vektör veritabanı, hem alakalı hem de çeşitli sonuçlar getiren MMR algoritması.
        - **hybrid_search.py:** Hibrit Arama Streamlit Uygulaması. BM25 (anahtar kelime bazlı) ve semantik aramanın birleşimi, ağırlık ayarlama slider'ı ile interaktif karşılaştırma.
        - **hybridhelper.py:** Hibrit Arama Yardımcı Modülü. BM25Retriever, FAISS ve EnsembleRetriever entegrasyonu, doküman yükleme ve parçalama fonksiyonları.
        - **hyde.py:** HyDE (Hypothetical Document Embeddings) Streamlit Uygulaması. Kurgusal yanıt üretimi ile arama kalitesini artırma, HyDE vs Standart RAG karşılaştırması.
        - **hydehelper.py:** HyDE Yardımcı Modülü. Kurgusal doküman oluşturma, ChromaDB ile MMR araması ve Gemini ile RAG yanıt üretimi.
        - **multiquery_rag.py:** Multi-Query RAG Streamlit Uygulaması. Tek sorudan birden fazla arama sorgusu üretme, de-duplikasyon ve reranking ile kapsamlı sonuçlar.
        - **multiqueryhelper.py:** Multi-Query RAG Yardımcı Modülü. GPT-4 ile sorgu çeşitlendirme, Cohere Rerank ile yeniden sıralama, FAISS araması ve benzersiz doküman filtreleme.
        - **relu.py:** ReLU Aktivasyon Fonksiyonu Görselleştirmesi. Matplotlib ile ReLU grafiği, derin öğrenme aktivasyon fonksiyonları açıklaması.
        - **reranking_with_cohere.py:** Cohere Reranking Streamlit Uygulaması. Cross-encoder modeli ile doküman yeniden sıralama, relevance_score gösterimi ve orijinal/sıralı sonuç karşılaştırması.
        - **show_and_compare_embeddings.py:** Embedding Modelleri Karşılaştırma Uygulaması. OpenAI, Cohere ve Hugging Face embedding modellerinin yan yana karşılaştırılması, vektör boyutları ve maliyet analizi.
        - **show_similarity_scores_with_chromadb_example.py:** ChromaDB Benzerlik Skorları Örneği. Vektör veritabanı kurulumu, koleksiyon yönetimi, sorgu ve distance (mesafe) skorları gösterimi.
    - **datasets_19/19.6-Datasets/gelecek.pdf:** RAG uygulamalarında kullanılan örnek PDF dokümanı.
    > **🔗 Kullanılan Teknolojiler:**
    > * **LlamaIndex:** LLM tabanlı veri arama ve indeksleme framework'ü
    > * **LangChain:** RAG pipeline ve doküman işleme
    > * **ChromaDB:** Açık kaynak vektör veritabanı
    > * **FAISS:** Facebook AI vektör benzerlik arama
    > * **Cohere Rerank:** Cross-encoder tabanlı yeniden sıralama modeli
    > * **OpenAI Embeddings:** Metin vektörleştirme
    > * **HuggingFace Inference API:** Açık kaynak embedding modelleri
    > * **Streamlit:** İnteraktif web arayüzü
- **19.7 - Otonom Ajanlar (Autonomous Agents):** Yapay zeka ajanları, ReAct (Reasoning and Acting) yaklaşımı ve çoklu ajan sistemleri. LangChain agent'ları, CrewAI ve AutoGen framework'leri ile otonom sistemler geliştirme.
    - **19.7 - Teorik Alt Yapı (PDF Dokümanları):**
        - **19.7.1-Otonom_Ajanlar_Giriş.pdf:** Otonom ajanlara giriş, ajan kavramı ve yapay zeka ajanlarının temel özellikleri.
        - **19.7.2-React_Yaklaşımı.pdf:** ReAct (Reasoning and Acting) framework'ü, Thought-Action-Observation döngüsü ve tool kullanımı.
        - **19.7.3-Çoklu-Ajan_Yaklaşımı.pdf:** Multi-Agent Systems, ajan işbirliği, delegasyon ve çoklu ajan orkestrasyon stratejileri.
    - **19.7 - Uygulama Dosyaları:**
        - **react.py:** LangChain ReAct Ajan Örneği. Tavily arama aracı ile web araması yapabilen otonom ajan, Thought/Action/Observation döngüsü ve GPT-4/Gemini model desteği.
        - **react_chat.py:** Streamlit ReAct Sohbet Uygulaması. Multi-LLM seçimi (GPT-4, Gemini Pro, Claude 2.1), çoklu araç entegrasyonu (arama, görsel üretim, web scraping), StreamlitCallbackHandler ile gerçek zamanlı düşünce zinciri görüntüleme.
        - **customtools.py:** LangChain Özel Araçlar Modülü. DALL-E 3 ve Stable Diffusion XL ile görsel üretim araçları, BeautifulSoup ile web scraping aracı, Tool description ve func yapısı.
        - **crewai.py:** CrewAI Çoklu Ajan Sistemi. Kişilik testi geliştirme senaryosu, üç farklı uzman ajan (Test Uzmanı, Yazılım Mühendisi, Danışman), sequential process ve Crew orkestrasyon.
        - **crewhelper.py:** CrewAI Ajan ve Görev Tanımları. Agent role/goal/backstory yapısı, Task description formatı, prompt mühendisliği teknikleri.
        - **autogen.py:** Microsoft AutoGen Framework. AutoGen Studio web arayüzü kullanımı, çoklu ajan konuşmaları ve kod çalıştırma yetenekleri.
        - **app_assistant.py:** OpenAI Assistants API Streamlit Uygulaması. Python Kodlama Asistanı, Thread/Run/Message yapısı, Session State ile sohbet geçmişi yönetimi.
        - **assistant_helper.py:** OpenAI Assistants API Yardımcı Modülü. Thread oluşturma, mesaj ekleme, Run döngüsü (polling) ve yanıt alma fonksiyonları.
        - **test.py:** CrewAI Çıktı Örneği - Kişilik Testi Uygulaması. CrewAI ajanları tarafından üretilmiş basit Streamlit kişilik testi, Likert ölçeği ve puanlama algoritması.
    > **🔗 Kullanılan Teknolojiler:**
    > * **LangChain Agents:** Tool-using ajan oluşturma framework'ü
    > * **CrewAI:** Çoklu ajan orkestrasyon platformu
    > * **Microsoft AutoGen:** Çoklu ajan konuşma sistemi
    > * **OpenAI Assistants API:** Kalıcı thread'li asistan yapısı
    > * **Tavily Search:** LLM-optimize arama API'si
    > * **DALL-E 3 & Stable Diffusion XL:** Görsel üretim modelleri
    > * **Streamlit:** İnteraktif web arayüzü

---

## 📂 Ekstra Projeler ve Kaynaklar

- **Armut ARL Projesi:** Birliktelik Kuralı Öğrenimi (Association Rule Learning) üzerine gerçek hayat senaryosu.
- **CheatSheets:** Python, Pandas, Numpy, Matplotlib, Seaborn, SQL, Docker, Machine Learning ve AI Agents için hızlı başvuru kağıtları.
- **Datasets:** Çalışmalarda kullanılan veri setleri arşivi.
- **Mülakat Soruları:** Teknik mülakatlara hazırlık için soru ve çözümler.
- **Mentor Çözümleri:** Örnek problemlerin alternatif ve profesyonel çözümleri.
- **Kahoot! Soruları:** Öğrenilen bilgileri test etmek için eğlenceli quizler.
- **[Global CO₂ Analysis & Future Projections](https://github.com/Miuul-Project/Global-CO--Analysis---Future-Projections):** Küresel CO₂ emisyon analizi ve gelecek projeksiyonları projesi. Zaman serisi analizi, veri görselleştirme ve tahminleme modelleri içerir.
    > **Not:** Bu proje, **Machine Learning (13)** ve **Time Series (16)** konularından sonra incelenmelidir.

---

## 📖 Proje Durumu ve İlerleme

| Bölüm / Konu | Durum |
|--------------|-------|
| 1 - Çalışma Ortamı | ✅ Tamamlandı |
| 2 - Veri Yapıları | ✅ Tamamlandı |
| 3 - Fonksiyonlar & Döngüler | ✅ Tamamlandı |
| 4 - Egzersizler | ✅ Tamamlandı |
| 5 - Numpy | ✅ Tamamlandı |
| 6 - Pandas | ✅ Tamamlandı |
| 7 - Veri Görselleştirme | ✅ Tamamlandı |
| 8 - Keşifçi Veri Analizi (EDA) | ✅ Tamamlandı |
| 9 - CRM Analitik | ✅ Tamamlandı |
| 10 - Ölçümleme Problemleri | ✅ Tamamlandı |
| 11 - Tavsiye Sistemleri | ✅ Tamamlandı |
| 12 - Feature Engineering | ✅ Tamamlandı |
| 13 - Machine Learning | ✅ Tamamlandı |
| 14 - GIT | ✅ Tamamlandı |
| 15 - SQL | 🚧 Devam Ediyor |
| 16 - Time Series | 🚧 Devam Ediyor |
| 17 - Docker | ❌ Planlanıyor |
| 18 - Deep Learning Path | ❌ Planlanıyor | 
| 19 - Generative AI & Prompt Engineer | 🚧 Devam Ediyor |
| 20 - Microsoft Azure Cloud For Data Science | ❌ Planlanıyor |

**Not:** 18, 19 ve 20. maddelerin sıralaması ihtiyaca göre değiştirilebilir. Gerekli görülen ek başlıklar ilave edilecektir. Ayrıca, bilinmesi gereken matematiksel konular da kapsama dahil edilecektir.

---

## 💡 Önerilen Çalışma Yöntemleri

1. **Sırayı Takip Edin:** Konular birbirinin üzerine inşa edildiği için klasör numaralarına göre ilerlemeniz tavsiye edilir.
2. **Uygulama Yapın:** Sadece kodları okumak yerine, `Datasets` klasöründeki verileri kullanarak kendi analizlerinizi yapın.
3. **Projeleri İnceleyin:** Özellikle `CRM` ve `Machine Learning` klasörlerindeki uçtan uca projeleri (pipeline) anlamaya çalışın.

### Algoritma ve Kod Pratiği Siteleri
* **Hackerrank:** Başlangıç ve orta seviye sorular için.
* **Codewars:** Küçük, pratik odaklı görevler.
* **Leetcode:** Orta ve ileri seviye kullanıcılar için (önce Hackerrank/Codewars yapılmalı).
* **Spoj:** Sadece sorular içerir, kod editörü yok. Diğer sitelerden sonra kullanılabilir.

> **Not:** Bu sitelere istediğiniz zaman girip ufak pratikler yapabilirsiniz. Veri seti pratiğine daha fazla vakit ayırmanız önerilir.

---

## 🤝 Katkıda Bulunma

Python öğrenimi sürecinde bu kaynakların geliştirilmesine katkıda bulunmak isteyenler için PR (Pull Request) ve issue'lar açmak tamamen açıktır.
