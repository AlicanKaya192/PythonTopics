######################################
# BÖLÜM 1: BAĞLANTI AÇMA, DATABASE (VERİTABANI) KURMA, TABLO OLUŞTURMA, TABLOYA VERİ EKLEME
# NOT: Bu dosyadaki her bölümü ayrı ayrı çalıştırmanız önerilir. Aksi takdirde 
# aynı işlemleri (kullanıcıdan veri alma, tablo oluşturma) art arda yaparak karmaşaya yol açabilir.
######################################

# SQLite veritabanı ile çalışabilmek için gerekli olan yerleşik (built-in) kütüphaneyi içe aktarıyoruz.
import sqlite3

# sqlite3.connect() metodu: Belirtilen isimde (kitaplar.db) bir veritabanı dosyasına bağlanmayı sağlar.
# Eğer bu isimde bir dosya yoksa, bulunduğumuz dizinde (veya belirtilen dizinde) yeni bir tane oluşturur.
# Bu bağlantıyı 'db' isimli bir değişkende tutuyoruz.
db = sqlite3.connect("kitaplar.db")

# db.cursor() metodu: Veritabanı üzerinde SQL komutlarını çalıştırabilmek ve sonuçları alabilmek için 
# bir imleç (cursor) nesnesi oluşturur. Veritabanı ile aramızdaki iletişim köprüsüdür.
yetki = db.cursor()

# Kullanıcıdan eklenecek kitabın detaylarını konsol üzerinden girmesini istiyoruz.
kitap_adi = input("Kitap adı giriniz : ")
sayfasayisi = input("Sayfasayısı giriniz : ")
kitapyil = input("Kitap yılını giriniz : ")

# cursor.execute() metodu: İçerisine yazılan SQL (Structured Query Language) komutunu çalıştırır.
# CREATE TABLE IF NOT EXISTS: 'Alican' adında bir tablo oluşturur. 'IF NOT EXISTS' ifadesi çok önemlidir,
# tablonun zaten var olup olmadığını kontrol eder. Eğer tablo varsa hata vermez, yoksa yeni oluşturur.
# Parantez içindekiler (isim, sayfasayısı, kitapyılı) oluşturulacak tablonun kolon (sütun) adlarıdır.
yetki.execute("create table if not exists Alican (isim,sayfasayısı,kitapyılı)")

# INSERT INTO tablo_adi VALUES: Tabloya yeni bir veri (satır) eklemek için kullanılır.
# f-string (f'...') kullanarak, kullanıcıdan aldığımız değişkenleri doğrudan SQL sorgusunun içine yerleştiriyoruz.
# DİKKAT: Gerçek uygulamalarda bu şekilde string formatlama SQL Injection saldırılarına açık olabilir. 
# Güvenlik için parametrik sorgular kullanılması (örn: execute("... VALUES (?,?,?)", (kitap, sayfa, yil))) daha doğrudur.
yetki.execute(f'INSERT INTO Alican VALUES ("{kitap_adi}","{sayfasayisi}","{kitapyil}")')

# connection.commit() metodu: Veritabanında yapılan değişiklikleri (ekleme, silme, güncelleme gibi) 
# kalıcı olarak kaydetmek için kullanılır. Sadece okuma (SELECT) yaparken gerekli değildir.
# Eğer commit() demezsek, program kapandığında eklediğimiz veriler veritabanına işlenmez ve silinir.
# commit() metodunu sadece INSERT, UPDATE VE DELETE işlemlerini yaptıkdan sonra kullanınız. Select yaparken gerekmez.
db.commit()

# Kullanıcıya işlemin başarılı olduğuna dair bir geri bildirim mesajı yazdırıyoruz.
print(f"Kitap Eklendi : {kitap_adi}")

# connection.close() metodu: Veritabanı bağlantısını sonlandırır.
# Açık bırakılan bağlantılar arka planda bellek tüketimine ve veritabanı kilitlenmelerine yol açabileceğinden 
# veritabanıyla olan işimiz bittiğinde her zaman kapatılmalıdır.
db.close()


######################################
# BÖLÜM 2: TABLODAN VERİ ÇEKME (TÜM VERİLERİ OKUMA)
######################################

# (Modül zaten yukarıda eklendiği için normalde tekrar eklemeye gerek yoktur ancak mantıksal olarak 
# ayrı bir script gibi düşünülerek bırakılmış olabilir)
import sqlite3

# Yeniden 'kitaplar.db' veritabanına bağlanıyoruz.
db = sqlite3.connect("kitaplar.db")

# SQL sorgularını çalıştırabilmek için cursor (imleç) oluşturuyoruz.
yetki = db.cursor()

# (UYARI: yetki = db.cursor() satırı orijinal kodda iki kere yazılmış, bu fazlalıktır ancak orijinal yapıyı bozmamak için bırakıyoruz)
yetki = db.cursor()

# Yeniden kullanıcıdan veri girişi alıyoruz.
kitap_adi = input("Kitap adı giriniz : ")
sayfasayisi = input("Sayfasayısı giriniz : ")
kitapyil = input("Kitap yılını giriniz : ")

# Tablo yoksa oluşturuyoruz.
yetki.execute("create table if not exists Alican (isim,sayfasayısı,kitapyılı)")

# Aldığımız yeni verileri tabloya ekliyoruz.
yetki.execute(f'INSERT INTO Alican VALUES ("{kitap_adi}","{sayfasayisi}","{kitapyil}")')

# SELECT * FROM tablo_adi: Tablodaki tüm sütunları (*) ve satırları getirmesini sağlayan SQL sorgusudur.
# Sorguyu veritabanına iletiyoruz ancak henüz dönen sonuçları Python tarafında bir değişkene kaydetmedik.
yetki.execute("SELECT * FROM Alican")

# cursor.fetchall() metodu: execute() ile çalıştırılan SELECT sorgusunun sonucunda dönen 
# TÜM kayıtları/satırları alır ve bir Python listesi olarak döndürür. Listenin her bir elemanı bir satırı (tuple) temsil eder.
# Dönen bu listeyi 'yazdir' isimli değişkene atıyoruz.
yazdir = yetki.fetchall()

# Dönen sonuç listesi üzerinde bir 'for' döngüsü oluşturarak her bir satırı (i değişkeni) tek tek ele alıyoruz.
# i değişkeni ('Kitap', '100', '2023') şeklinde bir tuple(demet) olduğu için indeks kullanarak (i[0], i[1]) ilgili sütun değerlerine ulaşıyoruz.
for i in yazdir:
    print(f"Kitap Adı : {i[0]}\nKitap SayfaSayısı : {i[1]}\nKitap Yılı : {i[2]}")

# (NOT: Burada tabloya veri EKLENDİĞİ için commit() işlemi yapıyoruz. Eğer hiçbir ekleme/güncelleme yapmayıp, 
# sadece SELECT ile veri okusaydık commit() işlemine gerek olmazdı.)
db.commit()

# İşlem bitince veritabanı bağlantısını güvenli bir şekilde kapatıyoruz.
db.close()


######################################
# BÖLÜM 3: TÜM TABLOYU DEĞİL İSTEDİĞİMİZ MİKTARDA ÇEKME (fetchmany KULLANIMI)
######################################

import sqlite3

# Veritabanına bağlantı oluşturma işlemi tekrarlanıyor.
db = sqlite3.connect("kitaplar.db")

# İmleç (cursor) oluşturuluyor.
yetki = db.cursor()

# Kullanıcıdan kayıt için veri alınıyor.
kitap_adi = input("Kitap adı giriniz : ")
sayfasayisi = input("Sayfasayısı giriniz : ")
kitapyil = input("Kitap yılını giriniz : ")

# Tablo oluşturuluyor.
yetki.execute("create table if not exists Alican (isim,sayfasayısı,kitapyılı)")

# Yeni veri kaydediliyor.
yetki.execute(f'INSERT INTO Alican VALUES ("{kitap_adi}","{sayfasayisi}","{kitapyil}")')

# Tüm kayıtları getirmek için SELECT sorgusu çalıştırılıyor.
yetki.execute("SELECT * FROM Alican")

# cursor.fetchmany(n) metodu: Çalıştırılan SELECT sorgusunun sonucunda dönen tablodan 
# sadece parantez içinde belirtilen miktar (n) kadar satırı çeker.
# Burada '2' yazıldığı için tablodan sadece ilk 2 satır çekilip liste olarak döndürülecektir.
# Çok büyük veri tabanlarında (örneğin 1 milyon satır) tüm veriyi çekmek için fetchall() kullanmak 
# bilgisayarın RAM'ini (belleğini) doldurup programı çökertebilir.
# Bu gibi senaryolarda verileri parça parça çekmek, sayfalamak ve yönetmek için fetchmany() kullanılması çok önemlidir.
yazdir = yetki.fetchmany(2)

print("\n--- İlk 2 Kayıt (fetchmany) ---")
# Çekilen ilk 2 satır üzerinde döngü oluşturulup, bu sefer satırlar özel bir string formata dönüştürülmeden,
# doğrudan veritabanından geldikleri gibi tuple (demet) halinde ekrana yazdırılıyor.
for i in yazdir:
    print(i)

# fetchall() KULLANIMININ DEVAMI VE İMLEÇ (CURSOR) MANTIĞI:
# fetchmany(2) ile ilk 2 kaydı çektiğimizde imleç (cursor) artık 3. satıra geçmiş ve orada bekliyor olur.
# Eğer bu noktada fetchall() metodunu çağırırsak, verileri BAŞTAN ALMAZ.
# Sadece imlecin kaldığı yerden (3. satırdan) itibaren Geriye Kalan Tüm Verileri çeker.
kalan_veriler = yetki.fetchall()

print("\n--- Geriye Kalan Kayıtlar (fetchall) ---")
for i in kalan_veriler:
    print(i)

# Ekleme yapıldığı için veritabanı değişiklikleri kaydediliyor.
db.commit()

# İşlem bitiminde veritabanı bağlantısı sonlandırılıyor.
db.close()


######################################
# BÖLÜM 4: TABLODAN ÖZEL NİTELİK İLE VERİ ÇEKME (WHERE KULLANIMI)
######################################

# Veritabanı işlemleri için sqlite3 modülü dahil ediliyor.
import sqlite3

# Veritabanına bağlantı sağlanıyor.
db = sqlite3.connect("kitaplar.db")

# Veritabanında işlem yapabilmek için imleç (cursor) oluşturuluyor.
yetki = db.cursor()

# Kullanıcıdan yeni kitap bilgileri alınıyor.
kitap_adi = input("Kitap adı giriniz : ")
sayfasayisi = input("Sayfasayısı giriniz : ")
kitapyil = input("Kitap yılını giriniz : ")

# Tablo oluşturuluyor. Eğer zaten varsa hata vermeyip es geçiyor.
yetki.execute("create table if not exists Alican (isim,sayfasayısı,kitapyılı)")

# Yeni veri, formatlı string (f-string) kullanılarak tabloya ekleniyor.
yetki.execute(f'INSERT INTO Alican VALUES ("{kitap_adi}","{sayfasayisi}","{kitapyil}")')

# WHERE KULLANIMI: Tablodaki verileri belirli bir şarta (koşula) göre filtrelemek için kullanılır.
# Bu sorguda "Alican tablosundaki tüm sütunları (*) getir, AMA SADECE 'kitapyılı' sütunu '1996' olanları getir" diyoruz.
yetki.execute("SELECT * FROM Alican WHERE kitapyılı = '1996' ")

# cursor.fetchall() metodu: Yukarıdaki WHERE şartını sağlayan (örneğin yılı 1996 olan) 
# BÜTÜN kayıtları bir Python listesi (list) olarak çeker ve 'yazdir' değişkenine atar.
yazdir = yetki.fetchall()

# Çekilen filtrelenmiş verileri ekrana yazdırmak için bir for döngüsü oluşturuyoruz.
for i in yazdir:
    print(f"1996 Yılında Çıkan Kitap - Adı: {i[0]}, Sayfa: {i[1]}, Yıl: {i[2]}")

# Ekleme işlemi (INSERT) yaptığımız için değişiklikleri veritabanına kaydediyoruz.
db.commit()

# İşlem bitiminde veritabanı bağlantısı güvenli bir şekilde sonlandırılıyor.
db.close()
