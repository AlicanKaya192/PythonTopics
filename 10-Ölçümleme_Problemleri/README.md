# Ölçümleme Problemleri

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
