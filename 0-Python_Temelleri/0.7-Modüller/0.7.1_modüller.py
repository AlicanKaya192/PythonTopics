############################
# Modül Kavramı
############################

# Modüller (Modules) Nedir?
# Python'da modüller, belirli bir amaca yönelik olarak yazılmış fonksiyonları, 
# sınıfları ve değişkenleri içeren .py uzantılı dosyalardır.
# Modüller sayesinde kodlarımızı daha düzenli, okunabilir ve tekrar kullanılabilir hale getiririz.
# Kendi yazdığımız kodları başka projelerde kullanabilmek veya Python'un geniş 
# standart kütüphanesinden faydalanmak için "import" anahtar kelimesi ile dahil edilirler.
#
# Örnek Kullanım:
# import math (Matematiksel işlemler için yerleşik bir modül)
# import os   (İşletim sistemi işlemleri için yerleşik bir modül)

# Oluşturduğumuz toplama python dosyasını import ediyoruz.
import toplama

# Toplama modülündeki topla fonksiyonunu çağırıyoruz.
toplama.topla()

# Eğer modül ismi uzunsa veya değiştirmek istersek "as" anahtar kelimesini kullanabiliriz.
# import toplama as tp

# tp.topla()


# Eğer modülün içindeki fonksiyonları tek tek import etmek istersek "from" anahtar kelimesini kullanabiliriz.
from islemler import topla

topla()
# Bu şekilde direk fonksiyon ismini yazarak kullanabiliriz.
# Ancak bu yöntemle fonksiyon ismini değiştiremeyiz.
# Eğer fonksiyon ismini değiştirmek istersek "as" anahtar kelimesini kullanabiliriz.
from islemler import topla as tp

tp.topla()
# Ancak bir önceki durum bundan daha mantıklı.


############################
# Random Modülü
############################

# Random modülü, rastgele sayılar üretmek için kullanılır ve bu modül python'a gömülüdür yani sonradan yüklemeye gerek yoktur.

import random

print(dir(random)) # Random modülünün metodlarını görürüz.

# Modülün metodlarını görmek için dir() fonksiyonu kullanılır.
# Bunu kod tarafında değil terminalde yapmalıyız.
# Terminale dir(random) yazarak modülün metodlarını görebiliriz.

a = random.random() # 0 ile 1 arasında rastgele bir sayı üretir. Burada ki random fonksiyonu parametre almıyor.

print(a*10) # Eğer ondalıklı gelmesini istersek bunu 10 ile çarpabiliriz. 
# Ancak bunu yaptığımızda küsaratları olacak. Bunu engellemek için ise;

print(round(a*10, 2)) # Bu şekilde küsaratları yok ederiz. 
# 2 yerine istediğimiz sayıyı yazarak noktadan sonraki küsarat sayısını belirleyebiliriz.

b = random.uniform(1.5, 2.5) # 1.5 ile 2.5 arasında rastgele bir ondalıklı sayı üretir. 
# random fonksiyonu ile aralarında ki tek fark uniform parametre alıyor. 
print(b)

c = random.randint(1, 10) # 1 ile 10 arasında rastgele bir tam sayı üretir. 10 dahil değildir.
# Burada üretilen sayılar küsüratsızdır ve bu fonksiyon 2 adet parametre almak zorundadır.
print(c)

liste = ["Alican", "Kaya", "Data", "Bilimi", "AI"]

d = random.choice(liste) # Listeden rastgele bir eleman seçer.
print(d)

e = random.choices(liste, k=3) # Listeden rastgele 3 eleman seçer.
print(e)

f = random.sample(liste, 3) # Listeden rastgele 3 eleman seçer. Ancak bu elemanlar tekrar etmez.
print(f)

g = random.shuffle(liste) # Listeyi karıştırır.
print(g)


############################
# DateTime Modülü
############################

# DateTime modülü, tarih ve saat işlemleri için kullanılır ve bu modül python'a gömülüdür yani sonradan yüklemeye gerek yoktur.
# Modülün içindeki metodları görmek için dir() fonksiyonu kullanılır.
# Bunu kod tarafında değil terminalde yapmalıyız.
# Terminale dir(datetime) yazarak modülün metodlarını görebiliriz.
# Ben konunun anlaşılması için kod tarafında yaptım.
import datetime

print(dir(datetime))

# Sadece belirli bir metodu çekmek istersek
from datetime import datetime

# datetime modülünün içindeki datetime metodunu kullanıyoruz.
# datetime metodunun içindeki now metodunu kullanıyoruz.
# Bu metod bize o anki tarih ve saati verir.
h = datetime.now()
print(h)

# Eğer sadece yılı almak istersek
i = datetime.year
print(i)

# Eğer sadece ayı almak istersek
j = datetime.month
print(j)

# Eğer sadece günü almak istersek
k = datetime.day
print(k)

# Eğer sadece saati almak istersek
l = datetime.hour
print(l)

# Eğer sadece dakikayı almak istersek
m = datetime.minute
print(m)

# Eğer sadece saniyeyi almak istersek
n = datetime.second
print(n)

# strftime metodu, tarih ve saat nesnesini belirli bir formatta string'e dönüştürmek için kullanılır.
# %a hafta gününün kısaltılmış adı
# %A hafta gününün tam adı
# %b ayın kısaltılmış adı
# %B ayın tam adı
# %c tam tarih, saat ve zaman bilgisi
# %d sayısal değerli bir karakter dizisi olarak gün
# %j belirli bir tarihin, yılın kaçıncı gününe denk geldiğini gösteren 1-366 arası bir sayı
# %m sayısal değerli bir karakter dizisi olarak ay
# %M sayısal değerli bir karakter dizisi olarak dakika
# %S sayısal değerli bir karakter dizisi olarak saniye
# %y sayısal değerli bir karakter dizisi olarak yılın son iki hanesi
# %Y sayısal değerli bir karakter dizisi olarak yılın tam adı
tam_tarih = datetime.strftime(h, "%c")
print(tam_tarih)

# Gelen tarih bilgileri İngilizce formatında gelecek. Bunu Türkçe'ye çevirmek için ise; 
# locale modülünü kullanmalıyız.
# locale modülü bilgileri sistemden çeker.
# Sistemde Türkçe dil paketi yüklü değilse bu modül çalışmayabilir.
import locale

# Türkçe dil paketini yüklüyoruz.
locale.setlocale(locale.LC_ALL, "Turkish_Turkey.1254")

tam_tarih = datetime.strftime(h, "%c")
print(tam_tarih)


############################
# Alıştırma 1 - Çekiliş Uygulaması
############################

# random modülünü projemize dahil ediyoruz. Rastgele seçimler ve listedeki elemanları karıştırmak için kullanacağız.
import random
import time

# Çekilişe katılacak kullanıcıları tutacağımız boş bir liste oluşturuyoruz.
kullanıcılar = list()

def kullanici_ekle(x):
    # Bu fonksiyon, aldığı 'x' (kullanıcılar listesi) içine yeni bir kullanıcı eklememizi sağlar.
    print("-" * 30)
    print("Kullanıcı Ekleme Ekranına Hoşgeldiniz.")
    # Kullanıcıdan eklenecek kişinin adını girmesini istiyoruz.
    ekle = input("Lütfen Eklenecek Kullancıyı Yazınız : ")
    # append() metodu ile kullanıcının girdiği ismi listenin sonuna ekliyoruz.
    x.append(ekle)
    print("-" * 30)


def kullanıcı_gor(x):
    # Bu fonksiyon, listeye eklenen tüm kullanıcıları sırasıyla ve numaralandırarak ekrana yazdırır.
    say = 1  # Kullanıcıları numaralandırmak için bir sayaç başlatıyoruz.
    print("-" * 30)
    print("Kullanıcı Listesi")
    # 'x' listesi içindeki her bir elemanı (i) tek tek döngüye alıyoruz.
    for i in x:
        # sayacı string'e çevirip yanına kullanıcı adını yazdırıyoruz.
        print(str(say) + " - Kullanıcı Adı : " + i)
        say += 1 # Her yazdırılan kullanıcıdan sonra sayacı 1 arttırıyoruz.
    print("-" * 30)


def sec(x):
    # Bu fonksiyon, listeden kullanıcının belirlediği sayıda rastgele kazananlar seçer.
    say = 1
    print("-" * 30)
    print("Seçim Ekranına Hoşgeldiniz.")
    # Kullanıcıdan kaç kişi seçileceğini girmesini istiyoruz. input string döndürdüğü için int() ile tam sayıya çeviriyoruz.
    kisi_sec = int(input("Lütfen Seçilecek Kişi Sayısını Yazınız : "))
    
    # random.sample() fonksiyonu bir dizi (örneğin liste) içinden rastgele ve TEKRARSIZ olarak belirtilen sayıda eleman seçer.
    # Burada 'x' (kullanıcılar listesi) içinden, 'kisi_sec' değişkenindeki sayı kadar kişi seçer.
    # ÖNEMLİ NOT: random.sample() fonksiyonu her zaman bir LİSTE (list) döndürür.
    # Yani 'sonuc' değişkenine atanan değer bir tuple DEĞİLDİR, yeni bir LİSTEDİR.
    sonuc = random.sample(x, kisi_sec)
    
    # sonuc isimli rastgele seçilenlerden oluşan YENİ listemizi döngüye sokup ekrana yazdırıyoruz.
    for i in sonuc:
        print(str(say) + " - Kullanıcı Adı : " + i)
        say += 1
    print("-" * 30)


def salla(x):
    print("-" * 30)
    # Bu fonksiyon, elimizdeki kullanıcı listesinin var olan sırasını tamamen ve rastgele şekilde değiştirir (karıştırır).
    say = 1
    # random.shuffle() liste elemanlarının yerini kendi içinde karıştırır. Geriye bir şey döndürmez (None döndürür),
    # doğrudan içine parametre olarak verilen 'x' listesini günceller.
    random.shuffle(x)
    
    # Karıştırılmış olan orijinal listeyi tekrar ekrana döngü ile yazdırıyoruz.
    for i in x:
        print(str(say) + " - Kullanıcı Adı : " + i)
        say += 1
    print("-" * 30)


while True:
    print("-" * 30)
    print("Çekiliş Uygulamasına Hoşgeldiniz.")
    print("1 - Kullanıcı Ekle")
    print("2 - Kullanıcıları Gör")
    print("3 - Seçim Yap")
    print("4 - Listeyi Karıştır")
    print("5 - Çıkış")
    print("-" * 30)

    secim = int(input("Lütfen Seçiminizi Yapınız : "))

    if secim == 1:
        kullanici_ekle(kullanıcılar)
    elif secim == 2:
        kullanıcı_gor(kullanıcılar)
    elif secim == 3:
        sec(kullanıcılar)
    elif secim == 4:
        print("Listeyi Karıştırıyoruz...")
        # time modülünün sleep fonksiyonu ile 2 saniye bekliyoruz.
        time.sleep(2)
        salla(kullanıcılar)
    elif secim == 5:
        break
    else:
        print("Hatalı Seçim!")


############################
# Alıştırma 2 - Şifre Korumalı Uygulama Yazma
############################

# subprocess modülü, python'dan başka bir programı çalıştırmak için kullanılır.
# Daha net anlaşılması için sizlere döküman linkini veriyorum.
# https://docs.python.org/3/library/subprocess.html
# subprocess, Python içerisinden işletim sistemi komutlarını çalıştırmak, yeni süreçler (process) başlatmak,
# ve bu süreçlerin girdi/çıktı (I/O) işlemlerini kontrol etmek için kullanılan çok güçlü bir yerleşik modüldür.
# Eskiden kullanılan os.system() gibi fonksiyonların yerini alması için tasarlanmıştır.
# 'as sp' kullanarak modülün adını kod içinde 'sp' olarak kısalttık, böylece sürekli 'subprocess' yazmak zorunda kalmayacağız.
import subprocess as sp

# Sisteme giriş için belirlediğimiz sabit şifre. Bu örnekte basit bir metin ("1234") kullanıyoruz.
psw = "1234"

# Kullanıcıdan şifreyi girmesini istiyoruz. input() fonksiyonu her zaman string (metin) döndürür.
kullanıcı_psw = input("Lütfen Şifrenizi Giriniz : ")

# Kullanıcının girdiği şifre ile bizim belirlediğimiz şifrenin aynı olup olmadığını kontrol ediyoruz.
if psw == kullanıcı_psw:
    # Şifre doğruysa sonsuz bir döngü başlatıyoruz (while True). Böylece kullanıcı çıkış yapmak isteyene kadar program menüde kalacak.
    while True:
        print("-" * 30)
        print("Uygulama Açma Programına Hoşgeldiniz.")
        print("-" * 30)

        # Kullanıcıya bir menü sunuyoruz ve hangi uygulamayı açmak istediğini soruyoruz.
        # \n karakterleri string içerisinde alt satıra geçmek (kodu alt satıra indirmek) için kullanılır.
        secim_yap = input("1-Notepad\n2-Paint\n3-Google\n4-Hesap Makinesi\n5-Çıkış\nLütfen Seçiminizi Yapınız : ")

        # Kullanıcının seçimine göre ilgili işlemleri (işletim sistemi bazında) yapıyoruz.
        if secim_yap == "1":
            # sp.call(): Verdiğimiz argümanı (komutu) işletim sistemine gönderir ve çalışmasını sağlar.
            # ÖNEMLİ: call() fonksiyonu çağrılan uygulama kapatılana kadar ana programın (scriptin) beklemesine neden olur.
            sp.call("notepad.exe")
        elif secim_yap == "2":
            # mspaint.exe komutu Windows'un yerleşik Paint uygulamasını çalıştırır.
            sp.call("mspaint.exe")
        elif secim_yap == "3":
            # chrome.exe komutu Google Chrome tarayıcısını başlatır. 
            # Not: Çalışması için Chrome'un sistem PATH çevre değişkenlerine eklenmiş olması gerekebilir.
            sp.call("chrome.exe")
        elif secim_yap == "4":
            # calc.exe komutu Windows Hesap Makinesini (Calculator) başlatır.
            sp.call("calc.exe")
        elif secim_yap == "5":
            # break komutu içindeki sonsuz döngüyü (while True) kırar ve programın güvenlice sonlanmasını sağlar.
            break
        else:
            # 1 ile 5 arasında olmayan bir tuşlama yapıldığında uyarı veriyoruz.
            print("Hatalı Seçim!")

else:
    # Eğer if psw == kullanıcı_psw bloğuna girmezse (yani şifre yanlışsa) bu kısım çalışır.
    print("Hatalı Şifre!")
    # exit() komutu yerleşik bir Python fonksiyonudur, anında programın çalışmasını durdurup çıkış yapar.
    exit()