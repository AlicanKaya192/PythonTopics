# ==============================================================================
# VidChat: YouTube Video Veri Modeli
# ==============================================================================
# Bu sınıf, bir YouTube videosunun temel bilgilerini tutmak için tasarlanmıştır.
# Basit bir "data class" örneğidir - sadece veri saklar, karmaşık işlem yapmaz.
#
# Neden bir sınıf kullanıyoruz?
# ----------------------------
# Python'da verileri tutmak için dict kullanabiliriz, ancak bir sınıf:
# 1. Kodun okunabilirliğini artırır (video.title vs video["title"])
# 2. IDE'ler autocomplete ve tip kontrolü yapabilir
# 3. Hangi alanların olduğu açıkça bellidir
# 4. Gerekirse metot ekleyebiliriz (örn: formatted_duration())
# 5. Hata yapma olasılığı azalır (yanlış anahtar adı kullanma riski yok)
#
# Alternatif: Python 3.7+ için @dataclass dekoratörü de kullanılabilirdi,
# ama bu haliyle daha açıklayıcı ve anlaşılır.
#
# Kullanım Örneği:
# ----------------
# video = YoutubeVideo(
#     video_id="dQw4w9WgXcQ",
#     video_title="Rick Astley - Never Gonna Give You Up",
#     video_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
#     channel_name="Rick Astley",
#     duration="3 dakika 32 saniye",
#     publish_date="14 yıl önce"
# )
# print(video.video_title)  # "Rick Astley - Never Gonna Give You Up"
# ==============================================================================


class YoutubeVideo:
    """
    YouTube video bilgilerini tutan veri sınıfı.
    
    Bu sınıf, scrapetube'den gelen ham video verisini
    düzenli ve erişilebilir bir formatta saklar.
    
    Özellikler (Attributes):
    ------------------------
    video_id : str
        YouTube'un verdiği benzersiz video kimliği
        Örnek: "dQw4w9WgXcQ"
    
    video_title : str
        Videonun başlığı
        Örnek: "Python Dersleri - Giriş"
    
    video_url : str
        Videonun tam URL'si
        Örnek: "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    channel_name : str
        Videoyu yükleyen kanalın adı
        Örnek: "BTK Akademi"
    
    duration : str
        Videonun süresi (okunabilir format)
        Örnek: "45 dakika 12 saniye"
    
    publish_date : str
        Videonun yüklenme tarihi (görece format)
        Örnek: "2 hafta önce", "1 yıl önce"
    """

    def __init__ (self, video_id, video_title, video_url, channel_name, duration, publish_date):
        """
        YoutubeVideo nesnesini başlatır.
        
        Tüm parametreler zorunludur çünkü bir video hakkında
        bu bilgilerin hepsine ihtiyacımız var. Eksik bilgi olursa
        uygulama düzgün çalışmaz.
        
        Parametreler:
        ------------
        video_id : str - YouTube'un verdiği benzersiz kimlik
        video_title : str - Video başlığı
        video_url : str - Videonun tam URL'si
        channel_name : str - Kanal adı
        duration : str - Video süresi
        publish_date : str - Yüklenme tarihi
        """
        self.video_id = video_id          # Benzersiz kimlik (video linkinde görünen kısım)
        self.video_title = video_title     # Video başlığı (kullanıcıya gösterilir)
        self.video_url = video_url         # Tam URL (video oynatmak için)
        self.channel_name = channel_name   # Kanal adı (içerik üreticisi bilgisi)
        self.duration = duration           # Süre (kullanıcı için önemli bilgi)
        self.publish_date = publish_date   # Yüklenme tarihi (güncellik bilgisi)