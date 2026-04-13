####################
# FONKSİYONLAR
####################

# Fonksiyonlar nedir ?
# Fonksiyonlar, belirli bir görevi yerine getiren kod bloklarıdır.

# Örnek Fonksiyon

# Normalde toplama işlemi yaptırmak istediğimiz de 

a = 5
b = 5

toplama = a + b
print(toplama)

# Fakat sonradan bir toplama işlemi daha yapmak istersek eğer yine aynı şekilde kodları yazmamız gerekecek.
# Bu durumun önüne geçmek için fonksiyonları kullanırız çünkü tekrar kod yazmaktan kurtuluruz. 
# Ayrıca fonksiyonlar kodların daha düzenli ve okunabilir olmasını sağlar.

# Fonksiyon Tanımlama
# Fonksiyon tanımlamak için def anahtar kelimesi kullanılır.
# Fonksiyon parantez içinde parametre alır.
# Parametreler opsiyoneldir. Yani fonksiyon parametresiz de tanımlanabilir. Parametre isimleri isteğe bağlıdır.
# Fonksiyon parantezden sonra iki nokta üst üste konulur.
# Fonksiyon bloğu girintili yazılır.
# return anahtar kelimesi fonksiyonun değerini döndürür. return yazılmazsa fonksiyon None döndürür.

def topla(a, b):
    return a + b

# Fonksiyon Çağırma
# Fonksiyon çağırmak için fonksiyon adı ve parantez kullanılır.
# Fonksiyon parantez içinde parametreler verilir.

print(topla(1, 2))

# Parametresiz Fonksiyon Tanımlama

def topla2():
    a = int(input("Lütfen ilk sayıyı giriniz: "))
    b = int(input("Lütfen ikinci sayıyı giriniz: "))

    toplam = a + b
    print(toplam)

# Parametresiz Fonksiyon Çağırma

# Fonksiyonu çağırmak için fonksiyon adının yanına parantez ekleriz.
# Fonksiyon çalıştığında parantez içindeki kodlar çalışır.
topla2()

####################
# ALIŞTIRMA 1 - Bilgi Alma Fonksiyonu
####################

ad = input("Lütfen adınızı giriniz: ")
soyad = input("Lütfen soyadınızı giriniz: ")
yas = input("Lütfen yaşınız giriniz: ")
meslek = input("Lütfen meslek giriniz: ")

print(f"Adiniz :{ad}\nSoyadiniz :{soyad}\nYasiniz :{yas}\nMeslek :{meslek}")

# Normalde bu şekilde yapıyoruz.
# Ama fonksiyon kullanarak daha düzenli bir şekilde yapabiliriz.

def bilgi(ad, soyad, yas, meslek):
    print(f"Adiniz :{ad}\nSoyadiniz :{soyad}\nYasiniz :{yas}\nMeslek :{meslek}")
    print("*" * 25)

bilgi(ad, soyad, yas, meslek)

####################
# ALIŞTIRMA 2 - Günlük Su Tüketimi
####################

# Kişinin kilosu ve cinsiyetine göre günlük içmesi gereken su miktarını hesaplayan fonksiyon
def su_hesapla(kilo):
    # Erkekler için kiloyu 0.04 ile çarparak su ihtiyacını hesaplar
    e_hesapla = kilo * 0.04
    # Kadınlar için kiloyu 0.03 ile çarparak su ihtiyacını hesaplar
    k_hesapla = kilo * 0.03
    
    # Kullanıcıdan cinsiyet bilgisini alır ve girdiği harfi büyük harfe dönüştürür (E veya K)
    cinsiyet = input("Lütfen Cinsiyetinizi giriniz (K/E) : ").upper()

    # Eğer kullanıcı erkek (E) ise e_hesapla değişkenindeki sonucu ekrana yazdırır
    if cinsiyet == "E":
        print(f"Günlük su tüketiminiz: {e_hesapla} litre")
    # Eğer kullanıcı kadın (K) ise k_hesapla değişkenindeki sonucu ekrana yazdırır
    elif cinsiyet == "K":
        print(f"Günlük su tüketiminiz: {k_hesapla} litre")
    # E veya K dışında hatalı bir değer girilirse kullanıcıya uyarı verir
    else:
        print("Hatalı giriş yaptınız.")

# Kullanıcıdan kilosunu tam sayı (integer) olarak alır
kilo_al = int(input("Lütfen kilonuzu giriniz: "))
# Alınan kilo bilgisini fonksiyona göndererek su_hesapla işlevini başlatır
su_hesapla(kilo_al)


####################
# RETURN
####################

# Return nedir ?
# Return, fonksiyonun değerini döndürmek için kullanılır.
# Return yazılmazsa fonksiyon None döndürür.

def topla(a, b):
    toplam = a + b
    return toplam

# Burda toplam değişkeni sadece fonksiyon içinde geçerlidir.
# Fonksiyon dışında toplam değişkenine erişemeyiz.
# Bu fonksiyonda return etmesi için toplam değişkenine ihtiyaç yoktur. return a + b de yazabilirdik.

print(topla(1, 2))


####################
# Varsayılan Değerler
####################

def kullanıcı(isim, soyisim, departman):

    print(f"Adiniz :{isim}\nSoyadiniz :{soyad}\nDepartman :{departman}")

kullanıcı("Alican", "Kaya", "AI-Data")

# Eğer kullanıcı fonksiyonuna departman bilgisi girilmezse veya diğer parametreler girilmezse 
# missing required positional argument hatası alırız.
# Bu hatayı önlemek için varsayılan değerler kullanırız.

def kullanıcı2(isim, soyisim, departman="IT"):

    print(f"Adiniz :{isim}\nSoyadiniz :{soyad}\nDepartman :{departman}")

kullanıcı2("Alican", "Kaya")

# Bu şekilde departman bilgisi girilmezse varsayılan değer olarak "IT" atanır.

# Fonksiyon parametrelerine varsayılan değer atamak için parametre isminin yanına eşittir (=) işareti konularak değer atanır.
# Varsayılan değer atanan parametreler fonksiyon çağrılırken opsiyoneldir.
# Bütün değişkenlere varsayılan değer ataması yapabiliriz.


####################
# Global Ve Yerel Değişkenler
####################

# Global Değişkenler
# Global değişkenler, fonksiyonların dışında tanımlanan değişkenlerdir.
# Global değişkenler, fonksiyonların içinde ve dışında kullanılabilir.

# Örnek Global Değişken
x = 10

# Fonksiyon içinde x değişkenini kullanıyoruz. Global değişken olduğu için fonksiyon içinde de kullanabiliriz.
def fonksiyon():
    print(x)

fonksiyon()
print(x)

# Yerel Değişkenler
# Yerel değişkenler, fonksiyonların içinde tanımlanan değişkenlerdir.
# Yerel değişkenler, sadece fonksiyonların içinde kullanılabilir.

# Örnek Yerel Değişken
def fonksiyon():
    # Fonksiyon içinde tanımlanan x değişkeni yerel değişkendir.
    # Fonksiyon dışında x değişkenine erişemeyiz.
    x = 10
    print(x)

fonksiyon()
print(x)

# Global değişkeni fonksiyon içinde değiştirmek istersek eğer global anahtar kelimesini kullanırız.

# Örnek Değişken
x = 10

def fonksiyon():
    # Global değişkeni fonksiyon içinde değiştirmek istersek eğer global anahtar kelimesini kullanırız.
    # Global anahtar kelimesi kullanılır ise her yerde ki x değişkeni değişir.
    # Eğer global anahtar kelimesi kullanılmazsa fonksiyon içinde yeni bir yerel değişken oluşturulur.
    # Bu yerel değişken sadece fonksiyon içinde geçerlidir.
    global x
    x = 20
    print(x)

fonksiyon()
print(x)
