# Machine Learning (Makine Öğrenimi)

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
