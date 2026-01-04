# ==============================================================================
# VidChat: Video Yardımcı Modülü
# ==============================================================================
# Bu modül, YouTube videolarıyla ilgili tüm işlemleri yönetir:
# 1. Video transkripti alma (ses -> metin dönüşümü)
# 2. YouTube'da video arama
#
# Kullanılan Teknolojiler:
# ------------------------
# - scrapetube: YouTube API'si olmadan video arama yapan kütüphane (web scraping)
# - LangChain YoutubeAudioLoader: YouTube'dan ses indiren loader
# - OpenAI Whisper: Dünyanın en güçlü ses-metin dönüşüm modeli
#
# Neden YouTube Data API kullanmıyoruz?
# -------------------------------------
# YouTube Data API'si kota sınırlamaları ve karmaşık kurulum gerektirir.
# scrapetube ise basit aramalar için yeterli, kurulumu kolay ve ücretsiz.
# Dezavantajı: YouTube arayüzü değişirse bozulabilir.
# ==============================================================================

import scrapetube  # YouTube'da video arama için (resmi API gerektirmez, web scraping kullanır)
from langchain_community.document_loaders.generic import GenericLoader  # LangChain'in esnek yükleyici yapısı
from langchain_community.document_loaders import YoutubeAudioLoader  # YouTube'dan ses indiren loader
from langchain_community.document_loaders.parsers import OpenAIWhisperParser  # Ses-metin dönüştürücü
import os
from dotenv import load_dotenv
from youtubevideo import YoutubeVideo  # Video bilgilerini tutacak veri sınıfı

# .env dosyasından API anahtarını al
load_dotenv()

my_key_openai = os.getenv("openai_apikey")


# ==============================================================================
# Fonksiyon 1: Video Transkripti Alma
# ==============================================================================
# Bu fonksiyon VidChat'in en kritik parçasıdır. Şu adımları uygular:
# 1. YouTube'dan video sesini indir (MP3 formatında)
# 2. Ses dosyasını OpenAI Whisper API'sine gönder
# 3. Whisper, sesi metne dönüştürür (Speech-to-Text)
# 4. Metin, LangChain Document formatında döner
#
# OpenAI Whisper Hakkında:
# ------------------------
# Whisper, OpenAI'ın geliştirdiği çok güçlü bir ses tanıma modelidir.
# - 680.000 saat çok dilli veri ile eğitilmiş
# - 99 dili destekler (Türkçe dahil ve oldukça başarılı!)
# - Aksanlara ve arka plan gürültüsüne karşı dayanıklı
# - Otomatik dil algılama yapabilir
#
# Dikkat: Uzun videolar için bu işlem birkaç dakika sürebilir!
# ==============================================================================
def get_video_transcript(url):
    """
    YouTube videosunun ses içeriğini metne dönüştürür (transkripsiyon).
    
    Bu fonksiyon, verilen YouTube URL'sindeki videoyu indirir,
    sesini çıkarır ve OpenAI Whisper ile metne dönüştürür.
    
    Parametreler:
    ------------
    url : str
        YouTube video URL'si (örn: "https://www.youtube.com/watch?v=xyz")
    
    Döndürür:
    --------
    list : LangChain Document listesi
        Her Document, transkript metnini (page_content) ve 
        metadata'yı (kaynak bilgisi) içerir
    """
    
    # Ses dosyalarının kaydedileceği klasör
    # Bu dosyalar geçici tutulur, işlem bittikten sonra silinebilir
    target_dir = "./audios/"

    # Klasör yoksa oluştur - ilk çalıştırmada gerekli
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    # GenericLoader: LangChain'in esnek yükleyici yapısı
    # İki bileşen alır ve bunları zincirleme çalıştırır:
    # 1. YoutubeAudioLoader: YouTube'dan ses dosyasını indirir
    # 2. OpenAIWhisperParser: İndirilen sesi Whisper ile metne çevirir
    loader = GenericLoader(
        YoutubeAudioLoader(urls=[url], save_dir=target_dir),  # Sesi indir
        OpenAIWhisperParser(api_key=my_key_openai)  # Metne dönüştür
    )

    # Yükleme işlemini başlat
    # Bu tek satır hem indirme hem de transkripsiyon yapar
    # Uzun videolarda bu adım biraz zaman alabilir
    video_transcript_docs = loader.load()

    return video_transcript_docs


# ==============================================================================
# Fonksiyon 2: YouTube Video Araması
# ==============================================================================
# Bu fonksiyon, scrapetube kütüphanesini kullanarak YouTube'da arama yapar.
# Resmi YouTube Data API'sine ihtiyaç duymaz - web scraping yöntemi kullanır.
#
# scrapetube Avantajları:
# -----------------------
# - API anahtarı veya OAuth gerektirmez
# - Kota sınırlaması yok (YouTube API'de günlük limit var)
# - Kurulumu ve kullanımı çok basit
#
# scrapetube Dezavantajları:
# -------------------------
# - YouTube web arayüzü değişirse kütüphane bozulabilir
# - Resmi API kadar güvenilir ve stabil değil
# - Bazı detaylı bilgilere (istatistikler vb.) erişemeyebilir
# ==============================================================================
def get_videos_for_search_term(search_term, video_count=1, sorting_criteria="relevance"):
    """
    YouTube'da arama yaparak video listesi döndürür.
    
    Parametreler:
    ------------
    search_term : str
        Aranacak sözcükler (örn: "Python dersleri", "machine learning tutorial")
    
    video_count : int
        Kaç video getirileceği (varsayılan: 1, maksimum: 5)
    
    sorting_criteria : str
        Sıralama ölçütü. Seçenekler:
        - "En İlgili": Alakaya göre sırala (YouTube'un varsayılanı)
        - "Tarihe Göre": En yeniden eskiye
        - "İzlenme Sayısı": En çok izlenenden aza
        - "Beğeni Sayısı": En çok beğenilenden aza
    
    Döndürür:
    --------
    list : YoutubeVideo objelerinin listesi
        Her obje video bilgilerini içerir (başlık, kanal, süre vb.)
    """
    
    # Türkçe sıralama seçeneklerini scrapetube'un beklediği parametrelere dönüştür
    # Bu mapping sayesinde kullanıcı Türkçe seçim yapabilir
    convert_sorting_option = {
                                "En İlgili": "relevance",
                                "Tarihe Göre": "upload_date",
                                "İzlenme Sayısı":"view_count", 
                                "Beğeni Sayısı":"rating"
                            }

    # scrapetube ile YouTube araması yap
    # get_search: Arama sonuçlarını generator olarak döner (bellek dostu)
    # limit: Kaç video getirileceği
    # sort_by: Sıralama kriteri
    videos = scrapetube.get_search(query=search_term, limit=video_count, sort_by=convert_sorting_option[sorting_criteria])
    
    # Generator'ı listeye çevir - tüm sonuçları bellekte tut
    videolist = list(videos)
    
    # YoutubeVideo objelerini oluştur
    # scrapetube ham veri döner, biz bunu düzenli bir formata dönüştürüyoruz
    youtube_videos = []

    for video in videolist:
        # Her video için gerekli bilgileri çıkar
        # scrapetube'ün döndürdüğü yapı biraz karmaşık (iç içe sözlükler),
        # bu yüzden her bilgiyi doğru yerden almamız gerekiyor
        new_video = YoutubeVideo(
            video_id = video["videoId"],  # YouTube'un verdiği benzersiz ID
            video_title=video["title"]["runs"][0]["text"],  # Video başlığı
            video_url = "https://www.youtube.com/watch?v=" + video["videoId"],  # Tam URL
            channel_name= video["longBylineText"]["runs"][0]["text"],  # Kanal adı
            duration= video["lengthText"]["accessibility"]["accessibilityData"]["label"],  # Süre (okunabilir format)
            publish_date = video["publishedTimeText"]["simpleText"]  # Yüklenme tarihi (örn: "2 hafta önce")
        )

        youtube_videos.append(new_video)

    return youtube_videos


