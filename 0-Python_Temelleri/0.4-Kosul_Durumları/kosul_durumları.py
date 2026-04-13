# Python'da koşul durumları, programın belirli koşullara göre farklı davranışlar sergilemesini sağlar.
# Koşul durumları, if, elif ve else anahtar kelimeleri ile oluşturulur.
# if bloğu, koşul doğru ise çalışır.
# elif bloğu, if bloğu yanlış ise çalışır.
# else bloğu, if ve elif blokları yanlış ise çalışır.

####################
# ALIŞTIRMA 1 - Oy Kullanma Yaşı
####################

# Kullanıcıdan yaşını alıp oy kullanıp kullanamayacağını kontrol etme
# input() fonksiyonu ile kullanıcıdan veri alıyoruz.
# int() fonksiyonu ile veriyi tam sayıya çeviriyoruz.
# if else bloğu ile koşul kontrolü yapıyoruz.

yas = int(input("Lütfen yaşınızı giriniz: "))

# Eğer yaş 18'den büyük veya eşitse oy kullanabilir.
if yas >= 18:
    print("Oy kullanabilirsiniz.", yas, "yaşındasınız.")
else:
    print("Oy kullanamazsınız.", yas, "yaşındasınız.")

####################
# ALIŞTIRMA 2 - Not Hesaplama
####################

# Kullanıcıdan notunu alıp harf notunu hesaplama
# input() fonksiyonu ile kullanıcıdan veri alıyoruz.
# int() fonksiyonu ile veriyi tam sayıya çeviriyoruz.
# if elif else bloğu ile koşul kontrolü yapıyoruz.
# elif bloğu, if bloğundan sonra gelir ve koşul kontrolü yapar.
# else bloğu, if ve elif bloklarından sonra gelir ve koşul kontrolü yapar.

note = int(input("Lütfen notunuzu giriniz: "))

# Eğer not 90'dan büyük veya eşitse A harf notunu alır.
if note >= 90:
    print("A")
# Değilse not 80'den büyük veya eşitse B harf notunu alır.
elif note >= 80:
    print("B")
# Değilse not 70'den büyük veya eşitse C harf notunu alır.
elif note >= 70:
    print("C")
# Değilse not 60'dan büyük veya eşitse D harf notunu alır.
elif note >= 60:
    print("D")
# Değilse F harf notunu alır.
else:
    print("F")


####################
# ALIŞTIRMA 3 - Korona Virüs Uygulaması
####################

# Kullanıcıdan ateş durumu, öksürük, baş ağrısı ve gün sayısını alıp korona virüs şüphesi olup olmadığını kontrol etme
# input() fonksiyonu ile kullanıcıdan veri alıyoruz.
# float() fonksiyonu ile veriyi ondalıklı sayıya çeviriyoruz.
# int() fonksiyonu ile veriyi tam sayıya çeviriyoruz.
# if elif else bloğu ile koşul kontrolü yapıyoruz.
# and operatörü, iki koşulun da doğru olmasını sağlar.
# or operatörü, iki koşuldan birinin doğru olmasını sağlar.
# not operatörü, koşulun yanlış olmasını sağlar.

ates_durumu = float(input("Lütfen Ateş Derecenizi Giriniz: "))
oksuruk = input("Öksürük var mı? (E/H): ").lower()
bas_agrisi = input("Baş Ağrısı var mı? (E/H): ").lower()
gun = int(input("Kaç gündür belirtileriniz var?: "))

if ates_durumu >= 39:
    if gun >= 3:
        print("Hastaneye gidin.")
    else:
        print("Dinlenin.")

if (ates_durumu >= 39) and (oksuruk == "e") and (bas_agrisi == "e") and (gun >= 3):
    print("Acil Hastaneye Gidin.")

elif (ates_durumu <= 39) or (oksuruk == "e") or (bas_agrisi == "e") or (gun >= 3):
    print("Durumunuzu takip edin.")

else:
    print("Sağlıklı günler dileriz.")


####################
# WHILE DÖNGÜSÜ
####################

# while döngüsü, belirli bir koşul doğru olduğu sürece çalışır.
# while döngüsü, for döngüsünden farklı olarak, belirli bir sayıya kadar çalışmaz.

# Sonsuza kadar çalışır.
# True her zaman doğru olduğu için döngü sonsuza kadar çalışır.
while True:
    print("Sonsuza kadar çalışır.")

# break anahtar kelimesi, döngüyü sonlandırır.
while True:
    print("Sonsuza kadar çalışır.")
    break

sayi = 1

# 1'den başlayarak 10'a kadar sayar.
while sayi < 10:
    print(sayi)
    sayi += 1


####################
# ALIŞTIRMA
####################

db_ka = "admin"
db_ps = 1234

# Kullanıcıdan kullanıcı adı ve şifre alıp giriş yapma
# input() fonksiyonu ile kullanıcıdan veri alıyoruz.
# int() fonksiyonu ile veriyi tam sayıya çeviriyoruz.
# if elif else bloğu ile koşul kontrolü yapıyoruz.
# and operatörü, iki koşulun da doğru olmasını sağlar.
# or operatörü, iki koşuldan birinin doğru olmasını sağlar.
# not operatörü, koşulun yanlış olmasını sağlar.
# Girilen kullanıcı adı ve şifre doğru ise giriş başarılı olur. Döngüden çıkılır.
# Girilen kullanıcı adı veya şifre yanlış ise giriş başarısız olur. Döngü devam eder.
while True:
    k_adi = input("Kullanıcı Adı: ")
    sifre = input("Şifre: ")
    if k_adi == db_ka and sifre == db_ps:
        print("Giriş başarılı.")
        break
    elif k_adi != db_ka:
        print("Kullanıcı adı yanlış.")
    elif sifre != db_ps:
        print("Şifre yanlış.")
        print("Şifreniz değiştirilsin mi ? (E/H): ")
        cevap = input().lower()
        if cevap == "e":
            yeni_sifre = input("Yeni Şifreniz: ")
            db_ps = yeni_sifre
            print("Şifreniz değiştirildi.")
        else:
            print("Şifreniz değiştirilmedi.")
    else:
        print("Kullanıcı adı veya şifre yanlış.")



####################
# FOR DÖNGÜSÜ
####################

liste = ["Alican", "Kaya", "github", "Data Science", "RoadMap"]

# For döngüsü belirli bir koşul doğru olduğu sürece çalışır.
# For döngüsünde yazdığımız i değişkeni, liste elemanlarını tek tek tutar. Buraya istediğimiz ismi verebiliriz.
# For döngüsü, liste elemanlarını tek tek yazdırır.
for i in liste:
    print(i)

# range() fonksiyonu, belirli bir sayıya kadar sayar.
# range() fonksiyonu, 1'den başlayarak 10'a kadar sayar. İlk girilen değeri dahil eder, son girilen değeri dahil etmez.
for sayılar in range(1, 10):
    print(sayılar)

deneme = "Alican"

# i değişkeni, deneme stringinin elemanlarını tek tek tutar. 
# Deneme stringinin elemanlarını tek tek yazdırır.
# Eğer print içerisine i yerine deneme yazsaydık, deneme stringde bulunan metni alt alta metnin uzunluğu kadar yazdırırdı.
# Eğer i yerine deneme yazsaydık bu senaryoda deneme değişkeninde bulunan Alican metnini alt alta 6 kez yazdırırdı.
for i in deneme:
    print(i)


####################
# FOR ALIŞTIRMA 1 - Giriş Uygulaması
####################

# Kullanıcıya şifre belirlemesi için maksimum 3 deneme hakkı veriyoruz.
# range(3) döngüyü 0, 1 ve 2 değerleri ile toplam 3 kez çalıştırır.
for i in range(3):
    # Kullanıcıdan yeni şifresini girmesini istiyoruz.
    sifre = input("Lütfen Şifre Belirleyiniz : ")
    
    # Eğer kullanıcı giriş yapmadan direkt Enter tuşuna basarsa (boş değer girilirse):
    if not sifre:
        print("Bu alan boş bırakılamaz.")
        
    # len() fonksiyonu ile şifrenin uzunluğunu alıp kontrol ediyoruz.
    # range(3, 8) şifre uzunluğunun 3, 4, 5, 6 veya 7 olmasını sağlar (8 dahil değildir).
    elif len(sifre) in range (3, 8):
        print("Yeni şifreniz", sifre)
        # Geçerli şifre girildiği için break komutu ile döngüden tamamen çıkıyoruz.
        break
        
    # Eğer döngünün son adımında (i == 2, yani 3. denemede) geçerli bir şifre girilmemişse:
    elif i == 2:
        print("Şifre belirleme hakkınız dolmuştur.")
        
    # Şifre boş değilse ancak uzunluğu kurallara uymuyorsa (örneğin 2 veya 9 karakterliyse):
    else:
        print("Şifreniz en az 3 en fazla 8 karakter olmalıdır.")


####################
# ALIŞTIRMA 2 - Kelimelerin İlk Harfini Bulan Algoritma
####################

# Split() fonksiyonu, stringi boşluklardan ayırarak bir liste oluşturur.
# Bu sayede stringin elemanlarına erişebiliriz.

deneme = "Alican Kaya"

# String bir ifadenin 0. indeksine ulaştığımızda metnin ilk harfini (karakterini) alırız. Çıktı: "A"
print(deneme[0])

# split() fonksiyonuna parametre vermezsek metni varsayılan olarak boşluk karakterinden bölüp listeye çevirir.
# deneme değişkeni artık ['Alican', 'Kaya'] isimli bir liste oldu.
deneme = deneme.split()

# deneme artık bir liste olduğu için 0. indeksi çağırdığımızda tablodaki ilk elemanı yani "Alican" kelimesini getirir.
print(deneme[0])

# Virgüllerle ayrılmış verilerden oluşan tek bir metin tanımlıyoruz.
deneme2 = "Alican,Kaya,github,Data Science,RoadMap"

# split(",") metodu sayesinde metni boşluktan değil virgül (,) gördüğü yerlerden ayırıp listeye eleman olarak atıyoruz.
deneme2 = deneme2.split(",")

# Ayrıştırılmış ve listeye dönüştürülmüş veriyi ekrana yazdırıyoruz.
print(deneme2)

# Kullanıcıdan birden fazla kelimeden oluşabilecek bir metin girmesini bekliyoruz.
veri_al = input("Lütfen Veri Giriniz: ")

# Girilen metni split() ile boşluklarından ayırıp (listeye çevirip) for döngüsü ile kelime kelime dolaşıyoruz.
for i in veri_al.split():
    # end=" " parametresi print fonksiyonunun her kelimeden sonra alt satıra geçmesini engeller ve yan yana boşlukla yazdırır.
    print(i, end=" ")

# Yine aynı şekilde girilen metindeki her bir kelimeyi döngüyle alıyoruz.
for i in veri_al.split():
    # Bu kez her bir kelimeyi temsil eden i'nin 0. indeksini yani o kelimenin ilk harfini alıp yan yana yazdırıyoruz.
    # Bu algoritma ile girilen kelimelerin baş harflerini yan yana birleştirmiş oluyoruz.
    print(i[0], end=" ")

