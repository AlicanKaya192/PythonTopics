# Veritabanı işlemleri için gerekli SQLite kütüphanesi projeye dahil ediliyor.
import sqlite3

# veresiye.db adında bir veritabanı dosyasına bağlanılıyor. 
# Eğer dosya yoksa, otomatik olarak bulunduğumuz dizinde yeni bir tane oluşturulur.
db = sqlite3.connect("veresiye.db")

# Veritabanında SQL komutlarını çalıştırmak ve sonuçları almak için imleç (cursor) oluşturuluyor.
yetki = db.cursor()

# CREATE TABLE IF NOT EXISTS: 'kisiler' adında, 'isim' ve 'borc' sütunlarına sahip bir tablo oluşturuluyor.
# Eğer 'kisiler' tablosu zaten varsa, hata vermez ve mevcut tabloyu koruyarak çalışmaya devam eder.
yetki.execute("CREATE TABLE IF NOT EXISTS kisiler(isim, borc)")

# Tablo oluşturma bir değişiklik (veritabanına yapısal bir yazma) işlemi olduğu için commit() ile kaydediliyor.
db.commit()

# Kullanıcıya sürekli bir menü sunmak için sonsuz bir while (While True) döngüsü başlatılıyor.
# Döngü ancak kullanıcı '5'i seçip 'break' komutunu çalıştırdığında sonlanır.
while True:
    print("***VERESİYE DEFTERİNE HOŞGELDİNİZ***")
    # Kullanıcıdan yapmak istediği işlemi seçmesi isteniyor ve girilen değer 'sor' değişkenine atanıyor.
    sor = input("1-BORÇLU EKLEME\n2-BORÇLULARI GÖR\n3-KİŞİYE GÖRE GÖR\n4-Kişi Silme\n5-ÇIKIŞ\nSEÇİMİNİZ : ")

    # 1. Seçenek: Sisteme yeni bir borçlu kaydı ekleme işlemi
    if sor == "1":
        print("*" * 30)
        print("***BORÇLU KİŞİ EKLEME***")

        # Kullanıcıdan eklenecek kişinin ismi ve borç miktarı alınıyor.
        isim_ekle = input("EKLENECEK İSİM : ")
        borc = input("BORÇ MİKTARI : ")

        # INSERT INTO: 'kisiler' tablosuna kullanıcının girdiği isim ve borç değerleri ekleniyor.
        # f-string kullanılarak, kullanıcıdan alınan değişkenler doğrudan SQL sorgusuna yerleştiriliyor.
        yetki.execute(f'INSERT INTO kisiler VALUES ("{isim_ekle}","{borc}")')

        # Veritabanında yeni kayıt (ekleme) işlemi yapıldığı için değişiklikler kalıcı olarak kaydediliyor.
        db.commit()

        # İşlemin başarılı olduğuna dair kullanıcıya bilgi mesajı veriliyor.
        print(f"{isim_ekle} kişisi sisteme eklendi. Borcu : {borc}")
        print("*" * 30)

    # 2. Seçenek: Sistemdeki tüm borçluları listeleme (okuma) işlemi
    elif sor == "2":
        print("*" * 30)
        print("***BORÇLULAR***")

        # SELECT * FROM: 'kisiler' tablosundaki tüm kayıtları herhangi bir şart olmadan getiren sorgu.
        yetki.execute("SELECT * FROM kisiler")
        
        # fetchall() ile tablodaki tüm kayıtlar çekilerek bir liste (içinde tuple'lar barındıran) halinde 'yazdir' değişkenine alınıyor.
        yazdir = yetki.fetchall()

        # Listelenen kayıtlar for döngüsü ile tek tek ele alınarak ekrana formatlı bir şekilde yazdırılıyor.
        # i[0] sütunların ilkine (isim), i[1] ise ikinci sütuna (borç) karşılık gelir.
        for i in yazdir:
            print(f"Kisi : {i[0]} - Borcu : {i[1]}")
        
        print("*" * 30)


    # 3. Seçenek: Belirli bir kişinin borcunu sorgulama (Filtreleme) işlemi
    elif sor == "3":
        print("*" * 30)
        print("***ARADIĞINIZ KİŞİ***")

        # Aranacak kişinin ismi kullanıcıdan isteniyor.
        aranacak_kisi = input("Aramak İstediğiniz Kişi Kim ? : ")

        # WHERE: Sadece 'isim' sütunu kullanıcının girdiği (aranacak_kisi) değere eşit olan kayıtları getirmesi için filtre konuluyor.
        yetki.execute(f"SELECT * FROM kisiler WHERE isim = '{aranacak_kisi}' ")

        # Filtreye uyan tüm kayıtlar çekiliyor.
        yazdir = yetki.fetchall()

        # Çekilen filtrelenmiş veriler ekrana yazdırılıyor. (Eğer o isimde kimse yoksa döngüye girmez, bir şey yazdırmaz).
        for i in yazdir:
            print(f"Aradığınız Kişi : {i[0]} - Borcu : {i[1]}")

        print("*" * 30)

    
    # 4. Seçenek: Sistemden kişi silme işlemi (DELETE kullanımı)
    elif sor == "4":
        print("*" * 30)
        print("***KİŞİ SİLME***")

        # Silinecek kişinin ismi kullanıcıdan alınıyor.
        silinecek_kisi = input("Silmek İstediğiniz Kişinin Adı : ")

        # DELETE FROM: Tablodan veri (satır) silmek için kullanılır. 
        # WHERE şartı eklenerek SADECE ismi kullanıcının girdiği kişiye eşit olan satırın silinmesi sağlanır.
        # DİKKAT: Eğer WHERE kullanılmasaydı tablodaki tüm veriler (herkes) silinirdi!
        yetki.execute(f"DELETE FROM kisiler WHERE isim = '{silinecek_kisi}' ")

        # Silme işlemi veritabanında yapısal bir değişiklik olduğu için commit() ile kaydedilmesi şarttır.
        db.commit()

        # Kullanıcıya silme işleminin gerçekleştiğine dair mesaj veriliyor.
        print(f"{silinecek_kisi} kişisi silindi.")

        print("*" * 30)


    # 5. Seçenek: Uygulamadan güvenli bir şekilde çıkış yapma
    elif sor == "5":
        # Programdan çıkmadan önce veritabanı bağlantısı (database connection) kapatılarak sistem kaynakları serbest bırakılıyor.
        db.close()
        
        # break komutu ile içerisindeki bulunduğumuz sonsuz while döngüsü kırılarak kod akışı sonlandırılıyor.
        break

    # 6. Seçenek (veya Diğer Durumlar): Kullanıcı menüde olmayan (1-5 dışı) bir değer girerse burası çalışır.
    else:
        print("Yanlış Girdi.")