# Güvenlik Politikası

## Desteklenen Sürümler

Bu repository, sürekli güncellenen bir öğrenim/portfolyo kaynağıdır ve resmi bir sürümleme (semver) süreci izlemez. Güvenlik açığı bildirimleri her zaman **`main` dalının en güncel hali** için değerlendirilir.

| Dal | Destekleniyor mu? |
|-----|:-:|
| `main` | ✅ |

## Güvenlik Açığı Bildirme

Bu repoda **hassas kullanıcı verisi işlenmez** ve production'da çalışan bir servis barındırılmaz — içerik, öğrenim amaçlı kod örnekleri, notebook'lar ve dokümanlardan oluşur. Bununla birlikte aşağıdaki türde bulgular güvenlik açığı olarak değerlendirilir ve bildirilmesi rica olunur:

- Kod içinde yanlışlıkla bırakılmış bir API anahtarı, token veya kimlik bilgisi
- `requirements*.txt` içindeki bir bağımlılıkta bilinen kritik bir güvenlik açığı (CVE)
- Kod örneklerinde güvensiz bir kullanım deseni gösteren (örn. komut enjeksiyonuna açık) bir örnek

### Nasıl Bildirilir?

**Tercih edilen yol:** GitHub'ın [Private Vulnerability Reporting](https://github.com/AlicanKaya192/Data-Science-RoadMap/security/advisories/new) özelliğini kullanarak bildirin — bu, sorunu herkese açık bir issue açmadan doğrudan repo sahibine iletir.

Alternatif olarak, [LinkedIn](https://www.linkedin.com/in/alican-kaya-881650234/) üzerinden doğrudan mesaj gönderebilirsiniz.

**Lütfen genel/herkese açık bir issue üzerinden güvenlik açığı bildirmeyin** — bu, sorun düzeltilmeden önce kötüye kullanılmasına yol açabilir.

### Ne Bekleyebilirsiniz?

- Bildiriminiz makul bir süre içinde (genellikle birkaç gün içinde) yanıtlanmaya çalışılır.
- Bulgu doğrulanırsa bir düzeltme hazırlanır ve mümkünse bildirende bulunan kişiye atıf yapılır (aksi istenmedikçe).
- Bu bir açık kaynak / bireysel portfolyo projesi olduğu için ödül (bug bounty) programı bulunmamaktadır.

Teşekkürler — sorumlu bildirim (responsible disclosure) sayesinde bu repo daha güvenli hale gelir. 🔒
