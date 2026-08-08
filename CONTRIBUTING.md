# Katkıda Bulunma Rehberi

Bu repository'nin gelişimine katkıda bulunmak isteyenler için PR (Pull Request) ve issue'lar tamamen açıktır. Öncelikle [Davranış Kuralları](./CODE_OF_CONDUCT.md)'nı okumanızı rica ederiz.

## 📑 İçindekiler
- [Nasıl Katkıda Bulunabilirim?](#nasıl-katkıda-bulunabilirim)
- [Hata Bildirme (Bug Report)](#hata-bildirme-bug-report)
- [Yeni Özellik Önerisi](#yeni-özellik-önerisi)
- [Pull Request Süreci](#pull-request-süreci)
- [Kod ve İçerik Standartları](#kod-ve-i̇çerik-standartları)
- [Testleri Çalıştırma](#testleri-çalıştırma)

## Nasıl Katkıda Bulunabilirim?

- **Hata düzeltmeleri:** Kırık bir dosya yolu, çalışmayan bir kod bloğu, yazım hatası bulduysanız bir issue açın ya da doğrudan PR gönderin.
- **Yeni içerik:** Yeni bir modül, örnek uygulama, notebook ya da veri seti eklemek istiyorsanız önce bir issue ile fikrinizi paylaşmanız önerilir.
- **Çeviri:** Repo şu an Türkçe, İngilizce ([README.en.md](./README.en.md)) ve İspanyolca ([README.es-ES.md](./README.es-ES.md)) sürümlerine sahiptir. Başka bir dile çeviri eklemek isterseniz [`README.en.md`](./README.en.md)'yi referans alarak yeni bir `README.<dil-kodu>.md` dosyası oluşturabilirsiniz. Yeni bir görsel (banner) gerekiyorsa `.github/assets/roadmap-banner.svg` yapısını referans alın.
- **Dokümantasyon:** README'lerdeki veya modül `README.md`'lerindeki açıklamaları iyileştirmek her zaman değerlidir.

## Hata Bildirme (Bug Report)

[Yeni bir issue](https://github.com/AlicanKaya192/Data-Science-RoadMap/issues/new/choose) açarken "Bug Report" şablonunu kullanın. Şunları eklemeye çalışın:
- Hangi dosya/modülde sorun var
- Sorunu yeniden oluşturma adımları
- Beklenen ve gerçekleşen davranış
- Python/işletim sistemi sürümünüz

## Yeni Özellik Önerisi

[Yeni bir issue](https://github.com/AlicanKaya192/Data-Science-RoadMap/issues/new/choose) açarken "Feature Request" şablonunu kullanın ve önerinizin hangi modülle (0-20) ilişkili olduğunu belirtin.

## Pull Request Süreci

```bash
# 1. Repository'yi fork edin (GitHub üzerinden)

# 2. Fork'unuzu klonlayın
git clone https://github.com/KULLANICI_ADINIZ/Data-Science-RoadMap.git

# 3. Yeni bir branch oluşturun
git checkout -b feature/yeni-ozellik

# 4. Değişikliklerinizi yapın ve commit edin
git add .
git commit -m "feat: Yeni özellik açıklaması"

# 5. Branch'inizi push edin
git push origin feature/yeni-ozellik

# 6. GitHub üzerinden Pull Request açın
```

PR açarken lütfen [Pull Request şablonundaki](./.github/PULL_REQUEST_TEMPLATE.md) kontrol listesini doldurun.

## Kod ve İçerik Standartları

- Commit mesajlarında açıklayıcı ifadeler kullanın (örn. `fix:`, `feat:`, `docs:` önekleri tercih edilir).
- Yeni eklenen dosyalar için ilgili modülün `README.md`'sini ve gerekirse ana `README.md`'deki modül tablosunu güncelleyin.
- Kod dosyalarına yeterli Türkçe (ya da eklediğiniz dile uygun) açıklayıcı yorum ekleyin.
- Mümkünse mevcut klasör yapısına ve isimlendirme kurallarına uygun şekilde düzenleyin.
- Veri seti eklerken [`Datasets_Genel_/README.md`](./Datasets_Genel_/README.md)'ye kaynak/lisans notu eklemeyi unutmayın.
- GenAI modülüne (20) dokunuyorsanız API anahtarlarını **asla** commit etmeyin — [`.env.example`](./20-Generative_AI_and_Prompt_Engineer/.env.example) dosyasını referans alın.

## Testleri Çalıştırma

PR açmadan önce testlerin geçtiğinden emin olun:

```bash
pip install -r requirements.txt pytest flake8
pytest tests/ -v
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
```

Her PR, [GitHub Actions](./.github/workflows/python-app.yml) üzerinden otomatik olarak lint + test edilir. Güvenlik açığı bildirmek isterseniz lütfen [SECURITY.md](./SECURITY.md)'ye bakın.
