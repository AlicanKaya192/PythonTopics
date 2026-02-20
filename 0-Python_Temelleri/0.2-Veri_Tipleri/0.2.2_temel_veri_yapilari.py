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
# Eğer int değişkeni string ifade ile birlikte kulanmak istiyorsak , karakteri kullanmalısınız. + sembolü kullanmalısınız. 
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

#############################################
# List (Liste)
#############################################

# Python programlama dilinde en yaygın kullanılan veri yapılarından birisidir. 
# Değiştirilebilir, sıralı ve kapsayıcı bir veri yapısıdır.

# - Değiştirelebilir.
# - Sıralıdır. Index işlemleri yapılabilir.
# - Kapsayıcıdır.

notes = [1, 2, 3, 4]
type(notes)

names = ["a", "b", "c", "d"]

not_nam = [1, 2, 3, "a", "b", True, [1,2, 3]] 
# Listeler kapsayıcı olduğu için içinde birden fazla veri yapısı tutabilir.

not_nam[0] # Değişken içerisinde ki ilk elemana erişmiş oluruz.
not_nam[5]
not_nam[6] # Liste içerisinde ki listeye erişir ama hepsini döner

not_nam[6][1] # Liste içerisinde ki listenin istediğimiz elemanına erişmek için kullanılan yöntem.

type(not_nam[6])
type(not_nam[6][1])

notes[0] = 99 # Listeler değiştirilebilir olduğundan index e denk gelen değiştirilebilir.

notes[0:4] # 0'dan 4 e kadar gider ancak 4.index de bulunan değeri dönmez.

list = ["Alican", 2, "Kaya", 4, 5]

list[:2] = ["BJK", "FB"]
# Listeler değiştirilebilir olduğundan index e denk gelen değiştirilebilir.
# : işareti index e kadar olan elemanları siler.
# Çalışma mantığı: 0. ve 1. index de bulunan elemanlar yerine "BJK" ve "FB" elemanlarını ekler.
# : sonrasına yazılan index e kadar olan elemanları kapsar.
# list[0:2] ile list[:2] aynı anlama gelir. Çünkü 0. index den başlar.
print(list)

#############################################
# List Methods (Liste Metotları)
#############################################

dir(notes)
# dir() fonksiyonu ile değişkenin metodlarını görebiliriz.

# En yaygın kullanılan metot append metodudur. Diğerleri daha az kullanılır.

len(notes)
len(not_nam) # Liste içerisinde ki listeyi 1 eleman olarak alır.

#############################################
# append: Listelere eleman ekler.
#############################################

notes.append(100) # 100 değerini listeye ekler.


#############################################
# pop: indexe göre eleman siler.
#############################################

notes.pop(0) # 0.index e denk gelen değeri listeden siler.


#############################################
# insert: indexe ekler.
#############################################

notes.insert(1, 100) # Önce değer eklenmesini istediğimiz index girilir daha sonra girmek istediğimiz değer girilir.


#############################################
# Dictionary (Sözlük)
#############################################

# Değiştirilebilir.
# Sırasız. (3.7 versiyonundan sonra sıralı oldu.)
# Kapsayıcı

# key-value

dictionary = {"REG": "Regression",
              "Log": "Logistic Regression",
              "CART": "Classification and Reg"}

# Alt alta aralarına virgül koyarak key-value şeklinde girebiliriz.
# Okunabilirlik açısından virgülden sonra alta geçilmesi önerilir.

dictionary["REG"] # Burada REG i çağırdığımızda values u gelir.

dictionary = {"REG": ["RMSE", 10],
              "Log": ["MSE", 20],
              "CART": ["SSE", 30]}

# Value tarafına liste de girilebilir. Buraya daha uzun bir liste de girebiliriz, daha farklı veri yapıları da girebiliriz.
# Dolayısıyla key ilk değişken oluşturmada gördüğü görev gibi sözlük içerisinde de önemli bir görev görür.

dictionary["CART"] # Value de ki tüm listeyi döner.

dictionary["CART"][1] # Bu şekilde value tarafında döndüğü listeden istediğimiz elemana ulaşabiliriz.

dictionary = {"REG": 10,
              "Log": 20,
              "CART": 30} # Value tarafımız int değerlerden de oluşabilir.

dictionary["REG"]


#####################
# Key Sorgulama
#####################

"REG" in dictionary # TRUE DÖNER.
"VAR" in dictionary # FALSE DÖNER.


#####################
# Key'e Göre Value'ya Erişmek
#####################

dictionary["REG"]
dictionary.get("REG") # Bu şekilde de girilen parametrenin elemanlarına erişebiliriz.


#####################
# Value Değiştirmek
#####################

dictionary["REG"] = ["YSA", 10] # REG key'in value değerini değiştirdik.


#########################
# Tüm Key'lere Erişmek
#########################

dictionary.keys() # Bütün keylere erişebiliriz.
dictionary.values() # Bütün value lara erişebiliriz.


#############################################
# Tüm Çiftleri Tuple Halinde Listeye Çevirme
#############################################

dictionary.items() # Her anahtar-değer çiftini (key, value) tuple olarak içeren bir dict_items görünümü döndürür


###################################
# Key-Value Değerini Güncellemek
###################################

dictionary.update({"REG": 11}) # Key ve yeni değerini girerek güncelleyebiliriz.


############################
# Yeni Key-Value Eklemek
############################

dictionary.update({"RF": 10}) # Bunu kullandığımızda sözlük yeni key değerinin olmadığını gördüğünde onu oluşturur.


############################
# Tuple (Demet)
############################

# Tuple lar listelerin değişime kapalı halidir.

# - Değiştirilemez.
# - Sıralıdır.
# - Kapsayıcıdır.

t = ("john", "mark", 1, 2)
type(t)

t[0]
t[0:3] # İlgili index e göre bir Slice işlemi yapacak.

# t[0] = 99 / Eleman değiştirme işlemi Tuple'da yapılamayacağı için hata verir.

t = list(t)
t[0] = 99
t = tuple(t) # Önce list'e dönüştürüp istediğimiz elemanı değiştirip daha sonra tuple yaparak değişiklik yapabiliriz.

# Tuple, listelere benzer ama daha güvenli bir şekilde çalışma imkanı sağlar. Dolayısıyla üzerinde çalıştığımız
# bazı senaryolarda belirli bir çıktının tuple formatında olmasını ve değiştirilemiyor olmasını gözlemlemek istiyebiliriz.
# Tuple'ların kullanım sıklığı çok çok azdır.


############################
# Set
############################

# - Değiştirilebilir.
# - Sırasız + Eşsizdir.
# - Kapsayıcıdır.

############################
# difference(): İki kümenin farkı
############################

set1 = set([1, 3, 5]) # Liste üzerinden set oluşuyor. Önce girilene göre döner.
set2 = set([1, 2, 3])

# type() gereksiz kod alanı kaplamaması için python console tarafında da kullanılabilir.

# set1'de olup set2'de olmayanlar
set1.difference(set2) # 5 dönecek.
set1 - set2 # Buradaki kesişimi ifade etmenin bir diğer yolu matematiksel operatördür. - işareti ile set1'de olup set2'de olmayan gelir.

# set2'de olup set1'de olmayanlar
set2.difference(set1) # 2 dönecek.
set2 - set1 # Buradaki kesişimi ifade etmenin bir diğer yolu matematiksel öperatördür. - işareti ile set2'de olup set1'de olmayan gelir.

############################
# symmetric_difference(): İki kümede de birbirlerine göre olmayanlar
############################

set1.symmetric_difference(set2) # 2 ile 5 döner.


############################
# intersection(): İki kümenin kesişimi
############################

set1 = set([1, 3, 5])
set2 = set([1, 2, 3])

set1.intersection(set2)

set1 & set2 # Buradaki kesişimi ifade etmenin bir diğer yolu matematiksel operatördür. Ve işareti ile 2 kümenin kesişimi gelir.


############################
# union(): İki kümenin birleşimi
############################

set1.union(set2) # 2 kümenin birleşimi gerçekleşir.
set2.union(set1) # Bir önceki ile aynı işlevi görür.


############################
# isdisjoint(): İki kümenin kesişimi boş mu?
############################

# Kullanılan ifadenin başında is var ise bu genelde true veya false şeklinde dönüş yapar.

set1 = set([7, 8, 9])
set2 = set([5, 6, 7, 8, 9, 10])


############################
# issubset(): Alt küme olup olmadığını sorgular
############################

set1.issubset(set2) # True döner.
set2.issubset(set1) # False döner.


############################
# issuperset(): 1 küme diğer kümeyi kapsıyor mu
############################

set2.issuperset(set1) # True döner
set1.issuperset(set2) # False döner.
