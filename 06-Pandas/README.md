# Pandas

Veri analizi ve manipülasyonu için en temel kütüphane.
- **1 - data_analysis_pandas.py:**
    - **Pandas Series:** Seri oluşturma ve özelliklerini inceleme.
    - **Veri Okuma:** Farklı kaynaklardan veri yükleme.
    - **Veri Manipülasyonu:** Seçim, filtreleme, toplulaştırma (Aggregation), gruplama (Grouping) ve birleştirme (Join) işlemleri.
    - 📓 [`1-data_analysis_pandas.ipynb`](./1-data_analysis_pandas.ipynb): Aynı içerik, çalıştırılmış çıktılarıyla birlikte Jupyter Notebook formatında.
- **2 - Pandas_exercise.py:** Titanic veri seti üzerinde veri analizi, tip dönüşümleri ve `apply`, `lambda` fonksiyonlarının kullanımıyla ilgili kapsamlı alıştırmalar.
  - 📓 [`2-Pandas_exercise.ipynb`](./2-Pandas_exercise.ipynb): Aynı içerik, çalıştırılmış çıktılarıyla birlikte Jupyter Notebook formatında.

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
