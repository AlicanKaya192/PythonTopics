# =============================================================================
# DİJİTAL MASAÜSTÜ SAATİ PROJESİ
# =============================================================================
# Bu projede Python ile masaüstünde çalışan, canlı güncellenen bir dijital saat
# uygulaması yapıyoruz. Hem saat hem de tarih bilgisini ekranda gösteriyoruz.
# Arayüz (pencere, butonlar, yazılar vs.) oluşturmak için tkinter kütüphanesini,
# anlık saat/tarih bilgisini almak için de time modülünü kullanıyoruz.
# =============================================================================


# =============================================================================
# KÜTÜPHANE AÇIKLAMALARI
# =============================================================================
# tkinter Nedir?
# ---------------
# tkinter, Python'un standart GUI (Graphical User Interface - Grafik Kullanıcı Arayüzü)
# kütüphanesidir. Yani masaüstü uygulamaları yapmamızı sağlar.
# Python ile birlikte gelir, ekstra kurulum gerektirmez (çoğu durumda).
#
# tkinter ile neler yapabiliriz?
#   - Pencereler, butonlar, yazı alanları, menüler oluşturabiliriz
#   - Hesap makinesi, not defteri, saat gibi masaüstü uygulamaları geliştirebiliriz
#   - Formlar, listeler, grafiksel arayüzler tasarlayabiliriz
#
# tkinter'ın temel bileşenleri:
#   Tk()     -> Ana pencereyi oluşturur (her uygulamanın bir ana penceresi olmalı)
#   Label    -> Ekranda yazı/metin göstermek için kullanılır (etiket)
#   Button   -> Tıklanabilir buton oluşturur
#   Entry    -> Kullanıcıdan tek satır metin girişi almak için kullanılır
#   Frame    -> Widgetları gruplamak için bir çerçeve oluşturur
#   Canvas   -> Çizim yapmak, şekiller oluşturmak için kullanılır
#
# Yerleşim yöneticileri (Layout Managers):
#   .pack()  -> Widgetları sırayla (üstten alta veya soldan sağa) yerleştirir
#   .grid()  -> Widgetları satır-sütun (tablo) mantığıyla yerleştirir
#   .place() -> Widgetları piksel piksel koordinatla yerleştirir
#
# Kurulum:
# py -m pip install tk
# (Genellikle Python ile birlikte gelir, ayrıca kurmaya gerek kalmaz)
# =============================================================================


# tkinter kütüphanesinden sadece ihtiyacımız olan sınıfları import ediyoruz.
# Label -> ekranda yazı göstermek için kullanacağız (saat ve tarih metinleri)
# Tk    -> ana pencereyi (uygulamanın kendisini) oluşturmak için kullanacağız
from tkinter import Label, Tk

# time modülü Python'da yerleşik olarak gelir, tarih ve saat işlemleri için kullanılır.
# Biz burada strftime() fonksiyonuyla anlık saati ve tarihi biçimlendirilmiş
# bir metin olarak alacağız. (strftime = "string format time" yani "zamanı metne çevir")
import time


# =============================================================================
# SAAT GÜNCELLEME FONKSİYONU
# =============================================================================
# Bu fonksiyon saati ve tarihi her 200 milisaniyede bir güncelliyor.
# Yani ekrandaki saat sürekli "canlı" kalıyor, donmuyor.
# Bunu bir nevi sonsuz döngü gibi düşünebilirsiniz ama tkinter'a özgü
# .after() metodu sayesinde arayüz donmadan tekrar tekrar çalışıyor.
def digital_clock():

    # time.strftime() fonksiyonu o anki sistem saatini alıp bizim istediğimiz
    # formatta bir metin (string) olarak döndürür.
    # %H -> Saat (24 saat formatında, 00-23 arası, mesela 17)
    # %M -> Dakika (00-59 arası, mesela 31)
    # %S -> Saniye (00-59 arası, mesela 45)
    # Sonuç olarak "17:31:45" gibi bir metin elde ediyoruz.
    time_live = time.strftime("%H:%M:%S")

    # label.config() metodu ile daha önce oluşturduğumuz saat etiketinin
    # text (metin) özelliğini güncelliyoruz.
    # Yani her çağrıldığında ekrandaki saat yazısı yeni değerle değişiyor.
    label.config(text=time_live)

    # Aynı mantıkla tarihi de alıyoruz:
    # %d -> Ayın kaçıncı günü (01-31 arası, mesela 08)
    # %B -> Ayın tam adı (January, February... veya sistemin diline göre Ocak, Şubat...)
    # %Y -> 4 haneli yıl (mesela 2026)
    # Sonuç olarak "08 May 2026" gibi bir metin elde ediyoruz.
    date_info = time.strftime("%d %B %Y")

    # Tarih etiketinin metnini güncelliyoruz, tıpkı saat etiketinde yaptığımız gibi.
    date_label.config(text=date_info)

    # .after() metodu tkinter'ın en güzel özelliklerinden biri.
    # İlk parametre: kaç milisaniye sonra tekrar çalışsın (200ms = 0.2 saniye)
    # İkinci parametre: hangi fonksiyon çağrılsın (kendisi! yani digital_clock)
    # Bu sayede fonksiyon kendini 200ms sonra tekrar çağırıyor (özyinelemeli/recursive).
    # while True döngüsü kullansak arayüz donar, ama .after() ile tkinter
    # arka planda bu işi hallediyor ve pencere açık kalmaya devam ediyor.
    label.after(200, digital_clock)


# =============================================================================
# ANA PENCERE AYARLARI
# =============================================================================

# Tk() sınıfından bir nesne oluşturuyoruz. Bu bizim ana uygulama penceremiz.
# Masaüstünde gördüğümüz pencere işte bu nesne. Her tkinter uygulaması
# mutlaka bir Tk() nesnesiyle başlar, bu uygulamanın kalbidir.
app_window = Tk()

# Pencerenin başlık çubuğundaki yazıyı belirliyoruz.
# Windows'ta sol üstte, pencerenin en tepesinde "Dijital Saat" yazacak.
app_window.title("Dijital Saat")

# Pencerenin boyutunu ayarlıyoruz: 350 piksel genişlik x 350 piksel yükseklik.
# "350x350" bir string olarak verilir, çarpı işareti küçük "x" harfidir.
app_window.geometry("350x300")

# Pencerenin yeniden boyutlandırılabilir olup olmayacağını belirliyoruz.
# İlk parametre: yatay (genişlik) yönde boyutlandırma (1 = evet, 0 = hayır)
# İkinci parametre: dikey (yükseklik) yönde boyutlandırma (1 = evet, 0 = hayır)
# Burada ikisi de 1 olduğu için kullanıcı pencereyi istediği gibi büyütüp küçültebilir.
app_window.resizable(0, 0)

# Pencerenin arka plan rengini siyah yapıyoruz.
# bg = background (arka plan) anlamına gelir.
# Dijital saat konseptine uygun olarak karanlık bir tema tercih ediyoruz.
app_window.configure(bg="black")


# =============================================================================
# GÖRÜNÜM AYARLARI (STİL DEĞİŞKENLERİ)
# =============================================================================
# Aşağıdaki değişkenleri ayrı ayrı tanımlamamızın sebebi kod tekrarını önlemek.
# Hem saat hem tarih etiketi aynı stili kullanacak, bu yüzden bir kere tanımlayıp
# her iki etikette de kullanıyoruz. İleride değiştirmek istersek tek yerden değiştiririz.

# Font (yazı tipi) ayarı bir tuple (demet) olarak verilir:
# 1. eleman: yazı tipi adı ("Boulder")
# 2. eleman: yazı boyutu (36 punto - oldukça büyük, dijital saat için ideal)
# 3. eleman: yazı stili ("bold" = kalın yazı)
text_font = ("Boulder", 36, 'bold')

# Etiketlerin arka plan rengi - siyah (pencere arka planıyla aynı olsun diye)
background = "black"

# Etiketlerin yazı rengi - beyaz (siyah arka plan üzerinde okunabilir olsun diye)
foreground = "White"

# Etiketlerin kenarlık (border) genişliği - 20 piksel
# Bu değer etiketin etrafında ne kadar boşluk bırakılacağını belirler.
border_width = 20


# =============================================================================
# SAAT ETİKETİ (LABEL) OLUŞTURMA
# =============================================================================

# Label() ile bir etiket (yazı alanı) oluşturuyoruz.
# Parametreler:
#   app_window -> bu etiket hangi pencereye ait? Ana penceremize ait.
#   font       -> yazı tipi, boyutu ve stili (yukarıda tanımladığımız tuple)
#   bg         -> arka plan rengi (background = "black")
#   fg         -> yazı rengi (foreground = "White"), fg = foreground demek
#   border     -> kenarlık kalınlığı (20 piksel)
# Bu etiket başlangıçta boş, digital_clock() fonksiyonu çalışınca içi dolacak.
label = Label(app_window, font=text_font, bg=background, fg=foreground, border=border_width)

# .grid() metodu ile etiketi pencere üzerinde konumlandırıyoruz.
# grid sistemi bir tablo gibi çalışır: satır (row) ve sütun (column) belirtiyoruz.
#   row=0      -> ilk satıra yerleştir (0'dan başlar, yani en üst satır)
#   column=1   -> ikinci sütuna yerleştir (0'dan başlar)
#   padx=10    -> yatay yönde (sağ-sol) 10 piksel boşluk bırak
#   pady=10    -> dikey yönde (üst-alt) 10 piksel boşluk bırak
# Padding (padx/pady) etiketin etrafında nefes alacak alan bırakır,
# böylece yazılar pencere kenarlarına yapışmaz.
label.grid(row=0, column=1, padx=10, pady=10)


# =============================================================================
# TARİH ETİKETİ (LABEL) OLUŞTURMA
# =============================================================================

# Saat etiketiyle aynı mantıkta ikinci bir etiket oluşturuyoruz.
# Bu sefer tarih bilgisini gösterecek. Aynı font, renk ve kenarlık ayarlarını kullanıyoruz.
date_label = Label(app_window, font=text_font, bg=background, fg=foreground, border=border_width)

# Tarih etiketini saat etiketinin hemen altına yerleştiriyoruz.
#   row=1    -> ikinci satır (saat row=0'da, tarih row=1'de, yani altında)
#   column=1 -> aynı sütunda (saatle hizalı olsun diye)
# Böylece ekranda üstte saat, altta tarih görünecek.
date_label.grid(row=1, column=1, padx=10, pady=10)


# =============================================================================
# FONKSİYONU İLK KEZ ÇAĞIRIYORUZ
# =============================================================================
# digital_clock() fonksiyonunu burada ilk kez çağırıyoruz.
# Bu çağrı hem saati hem tarihi ekrana yazdıracak, sonra .after() sayesinde
# fonksiyon kendini 200ms sonra tekrar çağıracak ve bu böyle sürekli devam edecek.
# Eğer bu satırı yazmasaydık etiketler boş kalırdı, saat hiç başlamazdı.
digital_clock()


# =============================================================================
# ANA DÖNGÜ (MAINLOOP)
# =============================================================================
# mainloop() tkinter'ın kalbidir. Bu metod pencereyi açık tutar ve kullanıcı
# etkileşimlerini (tıklama, klavye, pencere kapatma vs.) dinler.
# Bu satır olmadan pencere bir anlığına açılıp hemen kapanır.
# mainloop() çalıştığı sürece program yaşar, pencere kapatılınca program biter.
# Dikkat: mainloop() her zaman kodun EN SONUNDA yazılmalıdır, çünkü bu satırdan
# sonra yazılan kodlar pencere kapanana kadar çalışmaz.
app_window.mainloop()