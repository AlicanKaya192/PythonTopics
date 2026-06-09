# Time Series

Zaman serisi verilerinin analizi, istatistiksel ve makine öğrenmesi algoritmaları ile gelecek tahmini (forecasting) yapma teknikleri.
- **16.1 - Zaman Serisine Giriş:**
    - **16.1.1-Time_Series_Forecasting.pdf:** Zaman serisi tahmini nedir ve nerelerde kullanılır.
    - **16.1.2-Zaman_Serisine_Giriş_ve_Temel_Kavramlar.pdf:** Temel kavramlar ve zaman serisinin yapısı.
    - **16.1.3-Durağanlık_(Stationary).pdf:** Durağanlık kavramı ve önemi.
    - **16.1.4-Trend.pdf:** Zaman ekseninde trend yapısı.
    - **16.1.5-Mevsimsellik_(Seasonality).pdf:** Belirli periyotlarda tekrarlayan zikzak/dalgalanma analizi (Mevsimsellik).
    - **16.1.6-Döngü_(Cycle).pdf:** Mevsimsellikten farklı olan devirsel dalgalanmalar (Döngüsellik).
    - **16.1.7-Zaman_Serisi_Modellerinin_Doğasını_Anlamak.pdf:** Modellerin matematiksel davranışı.
    - **16.1.8-Hareketli_Ortalama_(Moving_Average).pdf:** Basit hareketli ortalama teknikleri.
    - **16.1.9-Ağırlıklı_Ortalama_(Weighted_Average).pdf:** Eski verilere ve yeni verilere verilen ağırlıkların belirlenmesi.
- **16.2 - Smoothing (Yumuşatma) Yöntemleri:**
    - **16.2.1-Smoothing_Yöntemleri.pdf:** Düzeltme tekniklerine giriş.
    - **16.2.2-SES_(Single-Exponential-Smoothing ).pdf:** Durağan seriler için seviye odaklı düzeltme (SES).
    - **16.2.3-DES_(Double-Exponential-Smoothing).pdf:** Trend barındıran seriler için seviye + eğim düzeltme (DES).
    - **16.2.4-Triple_Exponential_Smoothing_a.k.a._Holt-Winters.pdf:** Trend ve Mevsimsellik barındıran seriler için Çifte/Üçlü düzeltme.
    - **16.2.5_smoothing_methods.py:** SES, DES, TES (Holt-Winters) algoritmalarının Python ile kodlanması ve optimizasyonu.
- **16.3 - İstatistiksel Metodlar:**
    - **16.3.1-Statistical_Methods.pdf:** İstatistiksel modellemeye giriş.
    - **16.3.2-ARIMA_(p-d-q).pdf:** Trend içeren seriler için ARIMA model yapısı.
    - **16.3.3-SARIMA_(p-d-q)_(P-D-Q)_m.pdf:** Trend ve Mevsimsellik içeren seriler için SARIMA model yapısı.
    - **16.3.4_statistical_methods.py:** ARIMA ve SARIMA modelleri için AIC parametre optimizasyonu uygulaması.
    - **16.3.5_airline_passengers.py:** Havayolu verisi ile SES, DES, Holt-Winters, ARIMA ve SARIMA uygulamalarının karşılaştırılması.
- **16.4 - Makine Öğrenmesi ile Zaman Serisi:**
    - **demand_forecasting.py:** LightGBM algoritması ile ağaç bazlı makine öğrenmesi yöntemlerinin zaman serisinde kullanımı. Lag (gecikme), Rolling Mean, EWM özellikleri (Feature Engineering) ile veri matrisinin eğitilmesi.
- **16.5 - Case Study (Uygulamalı Proje):**
    - **16.5.1-Iyzico_İşlem_Hacmi_Tahmini.pdf:** Proje görev yönergeleri, e-ticaret üye iş yerlerinin hacim tahminlemesi.
    - **16.5.2_proje_transaction_count_forecasting.py:** İyzico e-ticaret verisiyle makine öğrenmesi kullanarak tahminleme yapılması projesi. Black Friday gibi özel gün feature mühendisliği teknikleri.
