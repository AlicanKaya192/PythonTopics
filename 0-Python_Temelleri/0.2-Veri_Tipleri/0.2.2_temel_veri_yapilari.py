# Değer atamak istediğimiz zaman = sembolünü kullanırız. 
# String ifadeleri tırnak içine alırız. Tırnaklar " " veya ' ' olabilir.
# print() fonksiyonu ile değişkenleri ekrana yazdırırız.

# 1. Yöntem
isim = "Alican"

print(isim)

# 2. Yöntem
isim = 'Alican'

print(isim)

# Sık yapılan hata

# HATALI KULLANIM ORNEGI: Tek tirnak ile Alicanin arabasi yazildiginda SyntaxError alinir.
# Burada hata alıyoruz çünkü Python 'Alican' kelimesini string olarak algılıyor ancak 'ın' kelimesini string olarak algılamıyor. 
# Çünkü 'ın' kelimesi tırnak içinde değil.

# Çözüm

hata = 'Alican\'ın arabası'
# Burada ters slash kullanarak 'ın' kelimesini string olarak algılatıyoruz. Bu pythonda "kaçış karakteri" olarak bilinir.

takım = "Beşiktaş JK"
takım2 = "Fenerbahçe SK"

print(takım + takım2)
# String ifadeleri birleştirmek için + sembolünü kullanırız. Birleştirmek istediğimiz değişkenklerin 2'side veya fazlası string olmalıdır.
# Aksi takdirde hata alırız. Aralarına boşluk koymak istersek + sembolü ve çift tırnak içinde boşluk kullanırız.

print(takım * 2)
# String ifadeleri çarpmak için * sembolünü kullanırız. Çarpma işlemi string ifadenin kendisini tekrar eder.
# 2 farklı string ifadeyi * ile çarpamayız. Hata alırız.

print(type(takım))
# type() fonksiyonu ile değişkenin veri tipini öğreniriz.

isim = "Alican"
d_yili = 2001
yil = 2026

print(isim,"'ın","doğum yılı",d_yili)
# Bu şekilde string ve int ifadeleri birleştirebiliriz. Burada , karakteri değişkenleri yan yana yazar.
# Aralarına boşluk koymak istersek + sembolü ve çift tırnak içinde boşluk kullanırız.
# Yukarıda + sembolü ile string ifadeleri birleştirdik. Burada , karakteri ile string ve int ifadeleri birleştirdik.
# Eğer int değişkeni string ifade ile birlikte kulanmak istiyorsak , karakteri kullanmalısınız. + sembolü kullanmamalısınız. 
# Eğer + kullanmak istiyorsak str() fonksiyonunu kullanmalısınız.

print(str(d_yili) + " " + isim)
# Burada str() fonksiyonu ile int değişkeni string ifadeye çevirdik. Böylece + sembolü ile string ifadeleri birleştirebiliriz.

yaş = "25"
print(int(yaş))
# Burada int() fonksiyonu ile string değişkeni int ifadeye çevirdik. Böylece int() fonksiyonu ile string ifadeyi int ifadeye çevirebiliriz.

###############################################
# Karakter Dizileri, Print() Fonksiyonu, Fonksiyonu Formatlama ve F Mantığı
###############################################

büyükharfler = "NE MUTLU TÜRK'ÜM DİYENE".lower()
print(büyükharfler)
# lower() fonksiyonu ile string ifadeyi küçük harfe çeviririz.

küçükharfler = "ne mutlu türk'üm diyene".upper()
print(küçükharfler)
# upper() fonksiyonu ile string ifadeyi büyük harfe çeviririz.

sadece_bas_harfi_büyük = "ne mutlu türk'üm diyene".capitalize()
print(sadece_bas_harfi_büyük)
# capitalize() fonksiyonu ile string ifadenin sadece baş harfini büyük harfe çeviririz.

her_kelimenin_bas_harfi_büyük = "ne mutlu türk'üm diyene".title()
print(her_kelimenin_bas_harfi_büyük)
# title() fonksiyonu ile string ifadenin her kelimenin baş harfini büyük harfe çeviririz.

tam_tersi = "BeŞıKtaŞ".swapcase()
print(tam_tersi)
# swapcase() fonksiyonu ile string ifadenin tam tersini alırız. Yani büyük harfleri küçük harfe, küçük harfleri büyük harfe çeviririz.

# Bu fonksiyonların bir farklı kullanım şekli ise;
tam_tersi = "BeŞıKtaŞ"
print(tam_tersi.swapcase())
# Bu şekilde print içerisinde de kullanabiliriz. veya;

tam_tersi = "BeŞıKtaŞ"
tam_tersi = tam_tersi.swapcase()
print(tam_tersi)
# Bu şekilde tekrardan atama yapabiliriz.

sil = "+++Alican+++".strip("+")
print(sil)
# strip() fonksiyonu ile string ifadenin başındaki ve sonundaki karakterleri sileriz. 
# Fonksiyonun içine hangi karakteri silmek istiyorsak onu yazarız.

# strip() fonksiyonu ile string ifadenin sadece başındaki karakterleri silmek istersek lstrip() fonksiyonunu kullanırız.

sil = "+++Alican+++".lstrip("+")
print(sil)

# strip() fonksiyonu ile string ifadenin sadece sonundaki karakterleri silmek istersek rstrip() fonksiyonunu kullanırız.

sil = "+++Alican+++".rstrip("+")
print(sil)

sil = " Alican".strip()
print(sil)
# strip() fonksiyonuna argüman vermezsek boşlukları siler.

# replace() fonksiyonu ile string ifadenin içindeki karakterleri değiştirebiliriz.

replace = "Alican".replace("A", "B")
print(replace)
# replace() fonksiyonu ile string ifadenin içindeki karakterleri değiştirebiliriz.

# split() fonksiyonu ile string ifadeyi bölebiliriz.

split = "AlicanKaya".split("a")
print(split)
# split() fonksiyonu ile string ifadeyi bölebiliriz.
# Fonksiyonun içine hangi karakteri bölmek istiyorsak onu yazarız.
# Burada "a" karakterini böldük. 
# Her "a" karakterini gördüğünde sistem "a" karakterini siler ve "a" karakterini bölür.

print("Alican", "Kaya", sep=":")
# sep() fonksiyonu ile string ifadelerin arasına istediğimiz karakteri koyabiliriz. Default olarak boşluk koyar.

print("Alican", "Kaya", end=":")
# end() fonksiyonu ile string ifadelerin sonuna istediğimiz karakteri koyabiliriz. Default olarak alt satıra geçer.

adi = "Alican"
soyadi = "Kaya"
yas = 25

print(adi, soyadi, yas)
# Normalde böyle yapıyorduk şimdi ise format fonksiyonunu kullanacağız.

print("Benim adım {}\nsoyadım {}\nyaşım {}".format(adi, soyadi, yas))
# format() fonksiyonu ile string ifadeleri birleştirebiliriz. f-string ile de birleştirebiliriz. 
# format() fonksiyonu içerisinde ki sıraya göre {} içerisine değerleri yazar. 
# \n karakteri alt satıra geçer.

print(f"Benim adım {adi}, soyadım {soyadi} ve yaşım {yas}")
# f-string ile string ifadeleri birleştirebiliriz. f-string ile string ifadeleri birleştirmek daha kolaydır.

print(f"Benim adım {adi.upper()}, soyadım {soyadi.upper()} ve yaşım {yas}")

###############################################
# Input Fonksiyonu
###############################################

# input() fonksiyonu ile kullanıcıdan veri alabiliriz.

kullanici_adi = input("Kullanıcı adınızı giriniz: ")
print("Kullanıcı adınız: ", kullanici_adi)

# Kullanıcıdan veri alarak yaş hesaplama

d_yili = input("Doğum yılınızı giriniz: ")
yil = 2026

yas = yil - int(d_yili)
print("Yaşınız: ", yas)

# Doğum yılı int olarak alabiliriz

d_yili = int(input("Doğum yılınızı giriniz: "))
yil = 2026

yas = yil - d_yili
print("Yaşınız: ", yas)

###############################################
# Alıştırma - Ortalama Hesaplama
###############################################

vize_puani = int(input("Vize puanınızı giriniz: "))
final_puani = int(input("Final puanınızı giriniz: "))

ortalama = (vize_puani * 0.4) + (final_puani * 0.6)
print("*"*30)
print(f"Vize puanınız: {vize_puani}, Final puanınız: {final_puani}, Ortalamanız: {ortalama:.2f}")
print("*"*30)
# :.2f ifadesi ondalıklı sayıyı virgülden sonra 2 basamak yazdırır.