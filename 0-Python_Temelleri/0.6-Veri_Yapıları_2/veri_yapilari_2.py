####################
# Veri Yapıları 2
####################

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

# Kullanıcıdan bir key alıp sözlükte olup olmadığını kontrol etmek istiyoruz.
bul = input("Eklemek istediğiniz key'i giriniz: ")

# get() metodu ile key sorgulaması yapıyoruz. Eğer key sözlükte yoksa "Key bulunamadı" yazdırır.
# Hem get() hem de in() metodu ile key sorgulaması yapabiliriz.
# Bu şekilde if else e gerek kalmadan key sorgulaması yapabiliriz.
print(dictionary.get(bul, "Key bulunamadı"))


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
# DICTIONARY ALIŞTIRMA - 1
############################

süper_lig = {"Galatasaray": "63 Puan", "Fenerbahçe": "61 Puan", "Beşiktaş": "62 Puan"}

# Key'i olmayan bir elemanı eklemek için setdefault kullanıyoruz.
# Eğer key sözlükte yoksa ekler. Eğer key sözlükte varsa ekleme yapmaz.
süper_lig.setdefault("Trabzonspor", "59 Puan") # Trabzonspor key'i sözlükte yoksa ekler.
süper_lig.setdefault("Aydınspor", "50 Puan") # Aydınspor key'i sözlükte yoksa ekler.

# setdefault() metodu yeni değerleri kalıcı olarak eklemez.
# Python programını kapatıp tekrar çalıştırırsan, hafızadaki (RAM) veriler kaybolur. 
# Yani kod tekrar çalıştırıldığında süper_lig baştan oluşturulur ve "Aydınspor" yoksa eklenir, yoksa eklenmez.
# Bu sadece o anki çalışma süresi için geçerlidir.

# Özetle: setdefault() sadece program çalışırken kalıcıdır, 
# kodu kapatıp tekrar çalıştırırsan veri kaybolur. Kalıcı yapmak için dosya veya veri tabanı kullanmalısın.

# append() ve setdefault() farkı:

# append() -> sadece LIST (liste) için kullanılır
# Listeye eleman ekler ve her zaman listenin SONUNA ekleme yapar
# Aynı eleman varsa bile tekrar ekler (kontrol etmez)

# Örnek:
# takimlar = ["Fenerbahçe", "Galatasaray"]
# takimlar.append("Aydınspor")
# Sonuç: ["Fenerbahçe", "Galatasaray", "Aydınspor"]


# setdefault() -> sadece DICT (sözlük) için kullanılır
# Belirtilen key (anahtar) YOKSA ekler
# Eğer key zaten varsa, mevcut değeri DEĞİŞTİRMEZ

# Örnek:
# süper_lig = {"Fenerbahçe": "60 Puan"}
# süper_lig.setdefault("Aydınspor", "50 Puan")   # ekler
# süper_lig.setdefault("Fenerbahçe", "70 Puan")  # değiştirmez

# Sonuç: {'Fenerbahçe': '60 Puan', 'Aydınspor': '50 Puan'}


# Özet:
# append() -> listeye HER ZAMAN ekler
# setdefault() -> sözlükte SADECE YOKSA ekler

# süper_lig.setdefault("Galatasaray", "64 Puan") # Galatasaray key'i sözlükte olduğu için ekleme yapmaz.

# süper_lig listesini gösterir.
print(süper_lig)

# Kullanıcıdan key ve value alıp sözlüğe ekler.
takım_ekle = input("Eklemek istediğiniz takımı giriniz: ")
puan_ekle = input("Eklemek istediğiniz puanı giriniz: ")

# setdefault ile ekleme yapıyoruz.
süper_lig.setdefault(takım_ekle, puan_ekle)

# süper_lig listesini gösterir.
print(süper_lig)

# for döngüsü ile key ve value değerlerini yazdırıyoruz.
# items() metodu ile key ve value değerlerini tuple olarak alıyoruz.
for isim,deger in süper_lig.items():
    print(isim, deger)

süper_lig = {"Galatasaray": "63 Puan", "Fenerbahçe": "61 Puan", "Beşiktaş": "62 Puan"}  # Başlangıçta 3 takım var

while True:  # Bu döngü sürekli çalışır, yani program kapanana kadar devam eder
    takım_ekle = input("Eklemek istediğiniz takımı giriniz: ")
    puan_ekle = input("Eklemek istediğiniz puanı giriniz: ")
    
    # setdefault() burada önemli:
    # Eğer girilen takım DAHA ÖNCE EKLENMEMİŞSE → sözlüğe YENİ olarak eklenir
    # Eğer takım zaten varsa → ESKİ DEĞERİ KORUR, yani üzerine yazmaz
    
    süper_lig.setdefault(takım_ekle, puan_ekle)

    # "İlk eklenen neden silinmiyor?" sorusunun cevabı:
    # Çünkü biz her seferinde yeni bir sözlük oluşturmuyoruz.
    # Aynı 'süper_lig' sözlüğü üzerinde işlem yapıyoruz.
    # Yani her ekleme, önceki verilerin ÜZERİNE EKLENİYOR (birikerek gidiyor).
    # Python sözlükleri RAM'de tutulur ve biz değiştirdikçe güncellenir, sıfırlanmaz.

    # Ayrıca burada silme işlemi yapan hiçbir kod yok (pop, del vs.)
    # Bu yüzden eski veriler olduğu gibi kalır.

    for isim, deger in süper_lig.items():  # Sözlükteki tüm elemanları gezer
        print(isim, deger)

    seçim = input("Çıkmak istiyor musunuz? (e/h): ").lower()
    if seçim == "e":
        print("Programdan çıkılıyor...")
        break
    else:
        pass

    print("------------------")  # Her turu ayırmak için


############################
# DICTIONARY ALIŞTIRMA 2 - Telefon Uygulaması
############################

# Normalde sözlükler {} ile tanımlanır. dict() ile de tanımlanabilir.
# Boş bir telefon rehberi sözlüğü oluşturuyoruz.
tel_rehberi = dict()

# Telefon defterine yeni kişi ekleyen fonksiyon
def tel_no_ekle(x):
    print("***NUMARA EKLEME EKRANINA HOŞGELDİNİZ***")
    # Kullanıcıdan isim ve numara bilgilerini alıyoruz.
    numara_isim_al = input("Lütfen Kayıt Edilecek Kişinin Adını Yazınız :")
    numara_no_al = input("Lütfen Kayıt Edilecek Kişinin Numarasını Yazınız :")

    # setdefault() metodu ile sözlüğe isim ve numarayı ekliyoruz. 
    # Not: Burada global olan tel_rehberi kullanılmış, parametre olan x.setdefault(...) da kullanılabilirdi.
    x = tel_rehberi.setdefault(numara_isim_al, numara_no_al)
    
    # Eklenen kişiyi kullanıcıya bildiriyoruz.
    print(f"{numara_isim_al} kişisinin numarası {numara_no_al} olarak eklendi.")


# Fonksiyonu çağırarak rehbere eleman ekletiyoruz.
tel_no_ekle(tel_rehberi)

# Telefon rehberindeki tüm kayıtları ekranda listeleyen fonksiyon
def tel_rehber_goster(x):
    print("***TELEFON REHBERİ***")

    kisi_sayisi = len(x)
    print(f"Toplam {kisi_sayisi} kişi kayıtlıdır.")

    # x parametresi olarak gelen sözlükteki (key, value) çiftlerini dönüyoruz.
    for isim, numara in x.items():
        print(f"Kişi: {isim}, Numara: {numara}")


# Telefon rehberinden kişi silen fonksiyon
def tel_rehber_sil(x):
    print("***TELEFON REHBERİ SİLME EKRANINA HOŞGELDİNİZ***")
    # Silinecek kişinin ismini (key) kullanıcıdan alıyoruz.
    numara_isim_al = input("Lütfen Silmek İstediğiniz Kişinin Adını Yazınız :")
    
    # pop() metodu ile sözlükten belirlediğimiz key'i bularak siliyoruz ve silinen değeri x'e atıyoruz.
    x = tel_rehberi.pop(numara_isim_al)
    
    # Kişinin başarıyla silindiğini ekrana yazdırıyoruz.
    print(f"{numara_isim_al} kişisinin numarası silindi.")

# Sonsuz bir döngü başlatarak kullanıcı çıkış yapana kadar menünün ekranda kalmasını sağlıyoruz.
while True:
    print("***TELEFON REHBERİ***")
    # Kullanıcıya menü seçeneklerini sunuyoruz ve bir seçim yapmasını istiyoruz.
    seçim = input("1-Ekle\n2-Sil\n3-Göster\n4-Çıkış\nSeçiminizi yapınız: ")

    # Kullanıcının seçimine göre ilgili fonksiyonları çağırıyoruz.
    if seçim == "1":
        # 1 seçilirse ekleme fonksiyonu çalışır.
        tel_no_ekle(tel_rehberi)
    elif seçim == "2":
        # 2 seçilirse silme fonksiyonu çalışır.
        tel_rehber_sil(tel_rehberi)
    elif seçim == "3":
        # 3 seçilirse rehberi gösterme fonksiyonu çalışır.
        tel_rehber_goster(tel_rehberi)
    elif seçim == "4":
        # 4 seçilirse döngü kırılarak (break) programdan çıkış yapılır.
        break
    else:
        # Geçersiz bir tuşlama yapıldığında kullanıcıyı uyarıyoruz.
        print("Geçersiz seçim. Lütfen tekrar deneyiniz.")


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