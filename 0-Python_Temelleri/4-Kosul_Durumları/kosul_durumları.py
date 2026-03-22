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