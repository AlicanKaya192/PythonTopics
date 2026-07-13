# 📂 Datasets — Kaynak ve Lisans Notu

> [!IMPORTANT]
> Bu repository'nin kök dizinindeki **MIT License**, yalnızca bu repo'da yazılmış olan **kod** için geçerlidir. Bu klasördeki veri setlerinin çoğu **üçüncü taraf kaynaklardan** (Kaggle, UCI Machine Learning Repository, GroupLens/MovieLens, TMDB, ISLR vb.) alınmıştır ve kendi lisans/atıf/kullanım şartlarına tabidir. Bu veri setlerini **ticari bir üründe, yeniden dağıtımda veya başka bir yayında** kullanmadan önce lütfen orijinal kaynağın güncel lisans koşullarını kontrol edin.

Aşağıdaki tablo, dosya adlarından ve içeriklerinden yola çıkarak yapılmış **iyi niyetli bir eşleştirmedir** (best-effort). Kesin lisans metni için her zaman orijinal kaynağa bakınız.

| Dosya | Muhtemel Kaynak | Not |
|---|---|---|
| `titanic.csv` | Kaggle — Titanic: Machine Learning from Disaster | Klasik eğitim veri seti |
| `application_train.csv`, `test.csv`, `sample_submission.csv` | Kaggle — Home Credit Default Risk yarışması | Yarışma kuralları/lisansına tabi |
| `breast-cancer.csv`, `breast_cancer.csv` | UCI ML Repository — Breast Cancer Wisconsin (Diagnostic) | Akademik/eğitim amaçlı serbest kullanım, atıf önerilir |
| `diabetes.csv` | UCI ML Repository / Kaggle — Pima Indians Diabetes Dataset | Atıf önerilir |
| `hitters.csv` | ISLR (An Introduction to Statistical Learning) — Hitters veri seti | Kitap materyali kapsamında |
| `USArrests.csv` | R `datasets` paketi (temel R dağıtımı) | Genel kullanım |
| `credits.csv`, `keywords.csv`, `movies_metadata.csv`, `links.csv`, `links_small.csv` | Kaggle — "The Movies Dataset" (TMDB verisi türetilmiştir) | TMDB kullanım şartlarına tabi |
| `genome_scores.csv`, `genome_tags.csv`, `tag.csv`, `rating.csv`, `ratings.csv`, `ratings_small.csv`, `movie.csv`, `link.csv` | GroupLens Research — MovieLens Dataset | MovieLens kullanım şartları (araştırma/eğitim amaçlı, atıf gerektirir) geçerlidir — bkz. [grouplens.org/datasets/movielens](https://grouplens.org/datasets/movielens/) |
| `Telco-Customer-Churn.csv` | IBM örnek veri seti / Kaggle üzerinden yaygın dağıtım | Eğitim amaçlı |
| `flo_data_20k.csv`, `scoutium_attributes.csv`, `scoutium_potential_labels.csv`, `product_sorting.csv`, `course_reviews.csv`, `churn.csv`, `amazon_reviews.csv`, `advertising.csv`, `imdb_ratings.csv` | Eğitim/bootcamp kapsamında sağlanan örnek/vaka çalışması (case study) veri setleri | Şirket/ürün adları örnek/anonimleştirilmiş olabilir; ticari kullanım öncesi orijinal eğitim kaynağıyla teyit edilmelidir |
| `train.csv` | Bağlama göre değişir (genellikle bir Kaggle yarışmasına ait) | İlgili modülün notlarına bakınız |

## Genel Öneriler

- **Akademik/kişisel öğrenim** amaçlı kullanım için bu veri setleri genellikle sorunsuzdur.
- **Ticari kullanım veya yeniden dağıtım** planlıyorsanız, yukarıdaki kaynaklardan (özellikle MovieLens ve TMDB tabanlı "The Movies Dataset") güncel lisans metnini mutlaka okuyun.
- Bir veri setinin kaynağından eminseniz ve tabloda eksik/yanlışsa, lütfen bir PR ile düzeltin.
