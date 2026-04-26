######################################
# BÖLÜM 1: OOP NEDİR?
######################################

# OOP (Nesne Tabanlı Programlama),
# programı sınıflar ve nesneler üzerinden modelleme yaklaşımıdır.

# Amaç:
# Gerçek dünyadaki varlıkları (araba, insan, banka hesabı vb.)
# yazılım içinde mantıksal nesneler olarak temsil edebilmek.

# -------------------------------------------------

# Sınıf (Class) Nedir?
# Bir nesnenin fabrikası veya şablonudur.
# İçerisinde:
# - Nitelikler (özellikler / değişkenler - örn: arabanın rengi)
# - Metotlar (fonksiyonlar / davranışlar - örn: arabanın çalışması)
# bulunur.

# -------------------------------------------------

# Nesne (Object) Nedir?
# Sınıf adlı şablondan üretilen somut, elle tutulur örnektir.
# Her nesne kendi verisini, kendi özelliklerini bağımsız olarak taşır.

# -------------------------------------------------

# Nitelik (Attribute) Nedir?
# Sınıfın veya nesnenin sahip olduğu verilerdir (isim, yaş, renk vb.).

# -------------------------------------------------

# Metot (Method) Nedir?
# Nesnenin yetenekleri veya yapabildiği eylemlerdir (koşma, hesaplama vb.).


######################################
# BÖLÜM 2: SINIFLAR VE NESNELER
######################################

# Araba modelini temsil eden basit bir 'Galeri' sınıfı oluşturuyoruz.
class Galeri:

    """
    Bu sınıf bir araba modelini temsil eder. (Docstring)
    """

    # CLASS ATTRIBUTE (Sınıf Özelliği)
    # Bu sınıftan üretilen tüm nesneler için ortak olan, standart özellikler.
    arac_ismi = "Ferrari"
    km_degeri = 9500
    renk = "Kırmızı"

    # Sınıfın sahip olduğu bir yetenek (metot). Sınıf içindeki metotlar her zaman (self) parametresini alır.
    def araba_ozellikleri(self):
        # self = bu metodu çağıran anlık nesneyi temsil eder.
        # Nesnenin kendi değişkenlerine erişmek için başına 'self.' koyarız.
        print(f"Aracın Adı: {self.arac_ismi}")
        print(f"Aracın Km Değeri: {self.km_degeri}")
        print(f"Aracın Rengi: {self.renk}")


# NESNE OLUŞTURMA AŞAMASI
# 'Galeri' şablonunu (sınıfını) kullanarak 'alican_otomotiv' adında somut bir nesne (örnek) oluşturuyoruz.
alican_otomotiv = Galeri()
# Oluşturduğumuz bu nesnenin 'araba_ozellikleri' isimli metodunu çalıştırıp bilgileri ekrana bastırıyoruz.
alican_otomotiv.araba_ozellikleri()


######################################
# BÖLÜM 3: SELF NEDİR?
######################################

# self:
# Sınıf içinde tanımlanan bir metot çalıştığında, o metodu çağıran ve üzerinde işlem yapılan NESNEYİ temsil eder.

# Ne işe yarar?
# - Nesnenin sadece kendine ait olan (başka nesneleri etkilemeyen) verilere erişmesini sağlar.
# - Nesnenin içine yeni veri atamaya yarar.

# Örnek Kullanım:

class Test:

    # Her sınıf metodu ilk parametre olarak 'self' almak zorundadır.
    def yaz(self):
        print("Bu bir test")


# Test sınıfından t1 nesnesini oluşturduk.
t1 = Test()
# t1 üzerinden yaz metodunu çağırdık.
t1.yaz()

# Arka planda Python'un gördüğü kod tam olarak şudur:
# Test.yaz(t1) 
# Yani yaz() fonksiyonunun içindeki 'self' değişkeninin yerine 't1' nesnesi geçmiştir.

# -------------------------------------

# EĞER SELF OLMAZSA NE OLUR?

class HataOrnegi:

    # Burada self parametresi yazılmamış. Bu ölümcül bir hatadır.
    def yaz():
        print("Hatalı kullanım")

# t = HataOrnegi() 
# t.yaz() → Bu kodu çalıştırdığımızda HATA alırız! 
# Çünkü Python otomatik olarak 't' nesnesini parametre olarak yollamaya çalışır ama yaz() fonksiyonu hiç parametre beklemiyordur.


######################################
# BÖLÜM 4: __INIT__ METODU
######################################

# __init__ (Kısaca Initialization - Başlatma):
# Sınıftan bir nesne yaratıldığı (örneğin araba = Galeri2() denildiği) anda otomatik olarak ilk çalışan özel metottur (Yapıcı Metot).
# Ne işe yarar?
# - Nesne doğduğu anda ona başlangıç değerlerini atamak.
# - Her oluşturulan nesnenin özelliklerinin birbirinden farklı (özel) olmasını sağlamak.

class Galeri2:

    # Nesne üretilirken dışarıdan arac_ismi, km_degeri ve renk adında üç bilgi (parametre) istiyoruz.
    def __init__(self, arac_ismi, km_degeri, renk):
        # self = o an üretilmekte olan yepyeni nesne
        
        # INSTANCE ATTRIBUTE (Her nesneye özel özellikler)
        # Dışarıdan gelen 'arac_ismi'ni, nesnenin kendi kalıcı hafızasına (self.arac_ismi) kaydediyoruz.
        self.arac_ismi = arac_ismi
        self.km_degeri = km_degeri
        self.renk = renk

    # Nesnenin kaydedilmiş bilgilerini ekrana basan standart metot.
    def araba_ozellikleri(self):
        print(f"Aracın Adı: {self.arac_ismi}")
        print(f"Aracın Km Değeri: {self.km_degeri}")
        print(f"Aracın Rengi: {self.renk}")


# Yeni nesneleri oluştururken parantez içinde doğrudan onlara ait olan özel bilgileri veriyoruz.
araba1 = Galeri2("BMW", 12000, "Siyah") # araba1 nesnesi yaratıldı, init metodu BMW, 12000, Siyah ile çalıştı.
araba2 = Galeri2("Audi", 8000, "Beyaz") # araba2 nesnesi yaratıldı, init metodu Audi, 8000, Beyaz ile çalıştı.

# Her nesne kendi bilgilerini sakladığı için farklı çıktılar verir.
araba1.araba_ozellikleri()
araba2.araba_ozellikleri()


######################################
# ÖZET
######################################

# class  → Genel şablon, fabrika.
# object → Fabrikadan çıkan somut ürün (nesne).
# attribute → Ürünün özellikleri (rengi, boyu).
# method → Ürünün yapabildiği hareketler veya davranışlar.
# self → O an işlem gören ürünün (nesnenin) ta kendisi.
# __init__ → Ürün fabrikadan çıktığı anda üzerinde yapılan ilk ayarlar (başlangıç metodu).


######################################
# ALIŞTIRMA
######################################

# okul adında bir şablon (sınıf) yaratıyoruz.
class okul: 

    # Nesne oluşturulduğunda ilk çalışacak olan yapıcı metot (constructor).
    def __init__(self, sube, ogretmen, bolum, mevcut):
        # Dışarıdan gelen değerleri nesnenin özelliklerine (self yardımıyla) atıyoruz.
        self.sube = sube
        self.ogretmen = ogretmen
        self.bolum = bolum
        self.mevcut = mevcut

    # Sınıfın genel bilgilerini derli toplu şekilde ekrana yazdırmak için kullandığımız metot.
    def bilgilerini_goster(self):
        print("-" * 45) # Ekrana 45 karakterlik kısa bir çizgi çekerek biçimlendirme yapıyoruz.
        print("Sınıf Bilgileri")
        # .format() yapısını kullanarak string içindeki {} parantezlere sırasıyla değişkenleri yerleştiriyoruz.
        print("Şube : {}\nÖğretmen : {}\n Bölüm : {}\nSınıf Mevcudu : {}".format(self.sube, self.ogretmen, self.bolum, self.mevcut))
        print("-" * 45)

    # Öğretmenin ismini ekrana yazdırmak için basit bir metot.
    def ogretmen_adi(self):
        # f-string yapısı (formatlamanın yeni ve kolay yolu) kullanılarak yazdırıyoruz.
        print(f"Öğretmen Adı : {self.ogretmen}")

    # Okulun mevcut bölümünü (branşını) güncellememizi (değiştirmemizi) sağlayan metot.
    def branch_degistir(self):
        # Kullanıcıdan klavye yoluyla yeni branşı girmesini istiyoruz.
        yeni_branch = input("Lütfen Yeni Branşınızı Yazınız : ")
        # Değiştirmeden önce eski branşı ekrana basarak kullanıcıyı bilgilendiriyoruz.
        print("***Eski Branş***", self.bolum)
        # Nesnenin eski bölüm özelliğinin (self.bolum) üzerine, klavyeden gelen yeni değeri (yeni_branch) yazıyoruz.
        self.bolum = yeni_branch
        print("-" * 45)
        print("Sınıf Bilgileri")
        # Branş güncellendikten sonra sınıf bilgilerini son haliyle tekrar yazdırıyoruz.
        print("Şube : {}\nÖğretmen : {}\n Bölüm : {}\nSınıf Mevcudu : {}".format(self.sube, self.ogretmen, self.bolum, self.mevcut))
        print("-" * 45)


# while True kullanarak sonsuz bir döngü başlatıyoruz. Kullanıcı işlem bitti diyene kadar döngü sürecek.
while True:

    # Kullanıcıdan 'okul' nesnesi oluşturmak için gereken verileri tek tek sorup alıyoruz.
    sinif_adi = input("Lütfen Şube Numarası Giriniz : ")
    ogretmen_bilgisi = input("Lütfen İsminizi Giriniz : ")
    bolum_al = input("Lütfen Branşınızı Giriniz : ")
    mevcut = input("Sınıf Mevcudunuzu Giriniz : ")
    
    # Kullanıcıdan "Sınıf Oluşturunuz" adında bir metin alınıyor ve 'sinif_olustur' değişkenine atılıyor.
    sinif_olustur = input("Sınıf Oluşturunuz : ")

    # ANCAK; hemen bu satırda yukarıda alınan metin SİLİNİYOR. 
    # Onun yerine 'okul' sınıfından üretilen gerçek bir nesne (obje) yaratılıp 'sinif_olustur' değişkeninin içine yerleştiriliyor.
    sinif_olustur = okul(sinif_adi, ogretmen_bilgisi, bolum_al, mevcut)

    print("---Hoşgeldiniz---")
    # Kullanıcının branş değiştirmek isteyip istemediğini soruyoruz.
    secim = input("Branş değiştirmek için Lütfen 1 tuşuna basınız : ")

    # Eğer kullanıcı 1 tuşuna bastıysa:
    if secim == "1":
        # Yukarıda yarattığımız 'sinif_olustur' nesnesinin 'branch_degistir' yeteneğini (metodunu) tetikliyoruz.
        sinif_olustur.branch_degistir()
    # Eğer 1 dışında bir şeye bastıysa:
    else:
        print("İşlem bitti...")
        # break komutu ile döngüyü tamamen durdurup programı sonlandırıyoruz.
        break


######################################
# BÖLÜM 5: KALITIM (MİRAS / INHERITANCE) ve OVERRIDING (EZME)
######################################

# Kalıtım (Inheritance) Nedir ? 
# Yeni yaratılan bir sınıfın (çocuğun), halihazırda var olan başka bir sınıfın (ebeveynin) tüm özelliklerini ve metotlarını bedavaya almasıdır (miras).
# Bunu yapmak için yeni sınıf adının yanına parantez açıp kime mirasçı olacağını yazarız.

# Örnek Mantık:
# class Hayvanlar:           --> Ebeveyn
# class Kopek(Hayvanlar):    --> Çocuk (Hayvanların özelliklerini otomatik alır)


# OVERRIDING (EZME) Nedir?
# Miras aldığınız ebeveyn sınıfta olan bir yeteneğin (metodun) sizin için yeterli olmadığı veya farklı olması gerektiği durumlarda,
# aynı isimde bir metodu çocuk sınıfta tekrar yazarak ebeveyndeki eski metodu geçersiz kılma (ezme) işlemidir.


######################################
# ALIŞTIRMA (KALITIM - INHERITANCE)
######################################

# 'müdür' adında bir sınıf yaratıyoruz ve '(okul)' yazarak yukarıdaki okul sınıfının çocuğu olmasını sağlıyoruz.
class müdür(okul):
    # pass kelimesi, bu sınıfın içine şimdilik ekstra hiçbir yeni kod yazmayacağımızı, olduğu gibi kalacağını belirtir.
    pass 

# Müdür sınıfından bir nesne ('yönetici') yaratıyoruz.
# Müdür sınıfının kendi içinde __init__ metodu (yapıcısı) olmamasına rağmen bu işlem HATA VERMEZ.
# Çünkü ebeveyni olan 'okul' sınıfının 4 parametre isteyen __init__ metodunu miras alarak kullanır.
yönetici = müdür("11", "Alican", "IT", "17")

# Yine müdür sınıfının içinde böyle bir metot olmamasına rağmen, ebeveynden (okul) miras kaldığı için başarılı şekilde çalışır.
yönetici.bilgilerini_goster()

# --------------------------------------------------------------------------------------
# OVERRIDING (EZME) VE YENİ NİTELİK EKLEME
# --------------------------------------------------------------------------------------

# Diyelim ki 'müdür' sınıfını daha yetenekli yapmak ve ebeveynde olmayan 'kidem' adında yepyeni bir özellik eklemek istedik.
class müdür(okul):
    print("YÖNETİCİ PANELİ")

    # Kendi __init__ metodumuzu yazdığımız an, okul sınıfının (ebeveynin) __init__ metodu tamamen geçersiz olur (EZİLİR/OVERRIDE).
    def __init__(self, sube, ogretmen, bolum, mevcut, kidem):
        # Aşağıdaki 4 satırı yazmak büyük bir kod tekrarıdır (ameleliktir) çünkü bunlar ebeveynde zaten atanıyordu.
        # Bu durumu BÖLÜM 11'de super() fonksiyonu ile çözeceğiz.
        self.sube = sube
        self.ogretmen = ogretmen
        self.bolum = bolum
        self.mevcut = mevcut
        
        # Bu ise tamamen müdür sınıfına ait yepyeni özelliktir.
        self.kidem = kidem
    
    # Ebeveynde (okul) olmayan, tamamen 'müdür' nesnelerine has yeni bir yetenek (metot) kazandırıyoruz.
    def mudur_ozel_metot(self):
        print("Müdür özel metodu çalıştı.")

    # Ebeveynde zaten 'bilgilerini_goster' adında bir metot vardı.
    # Biz burada AYNI İSİMLE metot yazdığımız için ebeveyndeki versiyonu EZMİŞ (Override) olduk.
    # Artık bir müdür nesnesine bu komutu verdiğimizde aşağıdaki kodlar çalışacak.
    def bilgilerini_goster(self):
        print("-" * 45) 
        print("Sınıf Bilgileri (Ezilmiş Müdür Versiyonu)")
        # Sadece printin formatını değiştirdik.
        print("Şube : {}\nÖğretmen : {}\n Bölüm : {}\nSınıf Mevcudu : {}".format(self.sube, self.ogretmen, self.bolum, self.mevcut))
        print("-" * 45)

    # Bu da tamamen yeni, kıdem bilgisini de içeren farklı bir bilgi gösterme metodu.
    def mudur_bilgileri(self):
        print("-" * 45) 
        print("Müdür Bilgileri")
        print("Şube : {}\nÖğretmen : {}\n Bölüm : {}\nSınıf Mevcudu : {}\nKıdem : {}".format(self.sube, self.ogretmen, self.bolum, self.mevcut, self.kidem))
        print("-" * 45)


# 'müdür' sınıfının yeni eziçi __init__ metodu artık 5 tane parametre istiyor.
yönetici2 = müdür("11", "Alican", "IT", "17", "Müdür Baş Yard.")

# Ezilmiş olan metot çalışır.
yönetici2.bilgilerini_goster()
# Sadece müdüre has metot çalışır.
yönetici2.mudur_bilgileri()

# --------------------------------------------------------------------------------------
# SUPER() FONKSİYONU İLE EBEVEYN METOTLARINA ERİŞİM
# --------------------------------------------------------------------------------------

# Bu sefer müdür sınıfını da ebeveyn kabul eden yepyeni bir 'müdür2' sınıfı oluşturuyoruz.
class müdür2(müdür):
    print("YÖNETİCİ PANELİ 2")

    # Yine kendi __init__ metodumuzu yazdık (ebeveyni ezdik).
    def __init__(self, sube, ogretmen, bolum, mevcut, kidem):
        
        # super() fonksiyonu, ebeveyn (miras aldığımız) sınıfı temsil eder. 
        # Burada ebeveynin (müdür sınıfının) __init__ metodunu çağırıp gerekli argümanları ona yolluyoruz.
        # Böylece "self.sube = sube" atamalarını uzun uzun tekrar yazmaktan (kod hamallığından) kurtulmuş oluyoruz.
        super().__init__(sube, ogretmen, bolum, mevcut, kidem)
    
    # Yeni sınıfa ait yeni ve özel bir metot daha.
    def müdür_özel_metot_2(self):
        print("Müdür 2 özel metodu çalıştı.")


######################################
# BÖLÜM 6: ENCAPSULATION (KAPSÜLLEME)
######################################

# Encapsulation (Kapsülleme):
# Sınıfın sahip olduğu verileri (değişkenleri) dış dünyadan izole edip korumaya almaktır.
# Amacı, verilerin dışarıdan "doğrudan" ve "kontrolsüz" bir şekilde değiştirilmesini engellemektir.

class Ogrenci:

    # Sınıfın yapıcı metodu
    def __init__(self, isim, notu):
        self.isim = isim # İsim değişkeni korumalı değil (herkes görebilir ve silebilir).
        
        # '_' (tek alt çizgi) işareti ile başlayan özelliklere Yarı Gizli (Protected) denir.
        # Bu, diğer yazılımcılara "Buna sınıf dışından müdahale etme!" uyarısı verir. Güvenlik sağlar.
        # (Eğer '__not' çift alt çizgi yapsaydık tamamen gizli olur ve dışarıdan erişilemezdi).
        self._not = notu   

    # GETTER (Okuma) Mantığı: Öğrencinin gizli olan notunu sadece okumamızı ve görmemizi sağlayan araç.
    def not_goster(self):
        print(f"{self.isim} adlı öğrencinin notu: {self._not}")

    # SETTER (Değiştirme) Mantığı: Öğrencinin notunu sadece bu metot kurallarına uyarak değiştirmemizi sağlayan araç.
    # Dışarıdan biri "ogr1._not = 1000" yapmak yerine mecburen bu metodu kullanmalıdır.
    def not_arttir(self, miktar):
        self._not += miktar
        print("Not artırıldı.")

    # Not azaltma işlemini güvenli yoldan yapmak için oluşturulan metot.
    def not_azalt(self, miktar):
        self._not -= miktar
        print("Not azaltıldı.")


# 'Ogrenci' sınıfından bir nesne üretiliyor.
ogr1 = Ogrenci("Alican", 70)

# Değişkenleri elle kurcalamak yerine, tamamen metotlar (güvenli aracılar) üzerinden sistemi yönetiyoruz.
ogr1.not_goster()
ogr1.not_arttir(10)
ogr1.not_goster()
ogr1.not_azalt(5)
ogr1.not_goster()


######################################
# BÖLÜM 7: ABSTRACTION (SOYUTLAMA)
######################################

# Abstraction (Soyutlama):
# Karmaşık işlemlerin, fonksiyonların veya arka plan sistemlerinin kullanıcıdan gizlenip
# kullanıcıya sadece anlayabileceği basit komutları (metotları) sunmaktır.
# (Televizyon kumandası gibi; düğmeye basarsınız, arka taraftaki elektronik paneli bilmeniz gerekmez).

class Bilgisayar:

    # Kullanıcı "Aç" der, ama içeride işlemcinin ısınması, RAM'in voltaj alması gibi detayları bilmez.
    def ac(self):
        print("Bilgisayar açıldı.")

    def kapat(self):
        print("Bilgisayar kapatıldı.")

    def program_calistir(self):
        print("Program çalıştırılıyor...")


# Bilgisayarımız hazır (Nesne üretildi).
pc = Bilgisayar()

# Kullanıcı detaylara boğulmadan sadece istediği basit komutları çalıştırır. (İşte buna soyutlama denir).
pc.ac()
pc.program_calistir()
pc.kapat()


######################################
# BÖLÜM 8: CLASS vs INSTANCE ATTRIBUTE
######################################

class Telefon:

    # CLASS ATTRIBUTE (Sınıf Özelliği)
    # Metotların dışında, direkt sınıfın içinde tanımlanır. 
    # Bu özellik sınıftan doğacak olan BÜTÜN nesneler için ortak bir kalıptır, paylaşımlıdır.
    marka = "Samsung"  

    # INSTANCE ATTRIBUTE (Örnek/Nesne Özelliği)
    # self kelimesi ile, yapıcı metot içinde atanır.
    # Her nesnenin kendine has, başkasını ilgilendirmeyen özel değişkenidir.
    def __init__(self, model):
        self.model = model  


# İki farklı telefon nesnesi (t1 ve t2) yaratıyoruz.
t1 = Telefon("S23")
t2 = Telefon("S22")

# Sınıf özelliği (marka = Samsung) t1 ve t2 için ortaktır, ikisinde de vardır.
# Biz sadece t1 nesnesine özel bir müdahale yapıp markasını elma yapıyoruz. 
t1.marka = "Apple"

# Bu değişiklik sadece t1'i bağlar, ortak şablondan çıkmış t2 etkilenmez.
print("t1 marka:", t1.marka) # Apple olarak yazdırır
print("t2 marka:", t2.marka) # Şablonun orijinali olan Samsung yazdırır


######################################
# BÖLÜM 9: COMPOSITION (BİLEŞİM)
######################################

# Composition (Bileşim):
# Bütün bir yapıyı oluştururken, diğer sınıfları birbirine mirasçı (baba-oğul) yapmak yerine, 
# bir ana sınıfın içinde diğer sınıfların nesnelerini barındırmaktır. "Sahip Olma (Has-A)" ilişkisidir.
# Örneğin; Araba motorun mirasçısı değildir, "Arabanın motoru vardır."

class Islemci:
    # İşlemcinin kendine ait bir çalış metodu.
    def calis(self):
        print("İşlemci çalışıyor.")


class Ram:
    # RAM'in kendine ait bir yükle metodu.
    def yukle(self):
        print("RAM yükleniyor.")


# Ana sınıfımız olan Bilgisayar
class Bilgisayar:

    # Bilgisayarın kendisi üretildiği an (__init__ çalıştığında)...
    def __init__(self):
        # Arka planda anında bir İşlemci ve bir Ram nesnesi de üretilir 
        # ve Bilgisayarın parçaları olarak 'self.islemci' ve 'self.ram' değişkenlerine takılır.
        self.islemci = Islemci()
        self.ram = Ram()

    # Bilgisayarın ana çalıştırma komutu
    def calistir(self):
        # İçine entegre ettiğimiz diğer sınıf nesnelerinin (islemcinin ve ramın) kendi metotlarını çağırabiliyoruz.
        self.islemci.calis()
        self.ram.yukle()
        print("Bilgisayar çalıştı.")


# Gördüğünüz gibi sadece bilgisayarı yarattık ama arkada işlemci ve ram da bilgisayara monte edildi.
pc = Bilgisayar()
# Bilgisayarı çalıştırdığımızda bileşenler de uyum içinde çalışıyor.
pc.calistir()


######################################
# BÖLÜM 10: MAGIC METHODS (__str__)
######################################

# Magic (Sihirli / Dunder) Methods: 
# Başında ve sonunda iki tane alt çizgi (__) olan metotlardır.
# Bu metotlar kod akışı sırasında özel durumlarda OTOMATİK olarak çalışırlar (biz manuel çağırmasak bile).

class Film:

    # Nesne üretildiği an otomatik tetiklenen yapıcı sihirli metot.
    def __init__(self, isim, yonetmen):
        self.isim = isim
        self.yonetmen = yonetmen

    # __str__ metodu: 
    # Bir nesneyi print(nesne) diyerek doğrudan ekrana bastırmak istediğimizde otomatik tetiklenir.
    # Normalde nesneyi yazdırınca "0x00A1F..." gibi çirkin bir ram adresi çıkar. 
    # Bu metot sayesinde nesnenin ekranda nasıl bir metin formatında görüneceğini belirliyoruz.
    def __str__(self):
        return f"Film: {self.isim} | Yönetmen: {self.yonetmen}"


# Film nesnesi üretiliyor.
f1 = Film("Inception", "Christopher Nolan")

# Doğrudan nesnenin kendisini yazdırıyoruz. Arka planda hemen f1.__str__() metodu tetikleniyor.
print(f1)  


######################################
# BÖLÜM 11: SUPER() KULLANIMI
######################################

# super() : Ebeveyn (miras alınan ana sınıf) demektir. 
# Çocuğun ebeveynine ait yetenekleri (metotları) kolayca çağırması için kullanılan köprüdür.

class Calisan:

    # Ebeveyn sınıfın özellikleri atadığı yapıcı metot
    def __init__(self, isim, maas):
        self.isim = isim
        self.maas = maas


# Yonetici sınıfı, Calisan sınıfından miras alıyor. (Yonetici -> Çocuk, Calisan -> Ebeveyn)
class Yonetici(Calisan):

    # Yonetici sınıfının __init__ metodu (Ebeveyni ezdik).
    def __init__(self, isim, maas, departman):
        # Ancak ebeveyni ezerken, 'isim' ve 'maas' verilerini bir daha amele gibi "self.isim = isim" diye yazmak istemiyoruz.
        # Bu işlemi yapmak için super() ile ebeveyne sesleniyor ve "Al isim ve maaşı, atamalarını sen yap!" diyoruz.
        super().__init__(isim, maas)
        
        # Ebeveynde bulunmayan yepyeni bir özellik olan departmanı ise çocuğa özel kendimiz atıyoruz.
        self.departman = departman


# Yönetici nesnesini yaratırken 3 bilgiyi paslıyoruz.
y1 = Yonetici("Alican", 20000, "IT")

# Ekrana yazdırdığımızda super() fonksiyonu sayesinde ebeveynin yaptığı isim ve maaş atamalarının tıkır tıkır çalıştığını görüyoruz.
print("İsim:", y1.isim)
print("Maaş:", y1.maas)
print("Departman:", y1.departman)