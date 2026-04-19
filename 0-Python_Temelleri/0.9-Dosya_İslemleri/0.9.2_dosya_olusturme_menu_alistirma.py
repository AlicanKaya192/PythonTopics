# Dosya kontrolü ve silme gibi işletim sistemi düzeyindeki işlemleri yapabilmek için 'os' modülünü içe aktarıyoruz.
import os

# Türkçe karakterleri (ş, ğ, ç, ö, vb.) hatasız okuyup yazmak için 'codecs' modülünü içe aktarıyoruz.
import codecs

# -------------------------------------------------------------------------
# FONKSİYON TANIMLAMALARI (Hata Ayıklama - Try / Except / Finally)
# Programın beklenmedik durumlarda hata verip çökmesini önlemek(Crash) ve kullanıcıya
# neyin yanlış gittiğini bildirmek için işlemleri 'try-except' blokları içine aldık.
# -------------------------------------------------------------------------

def dosya_olustur():
    dosya_adi = input("Oluşturulacak dosyanın adını giriniz (örnek: veri.txt): ")
    
    # try bloğu: Hata çıkarabilecek olan, denemek istediğimiz kodları yazdığımız güvenli kafestir.
    try:
        # ÖNEMLİ: 'w' (write) modu eğer dosya varsa içindekileri sorgusuz sualsiz siler. 
        # Var olan dosyanın yanlışlıkla ezip yok edilmesini önlemek adına 'x' (Exclusive Creation) modu kullanıyoruz.
        # 'x' modu: Dosyayı sıfırdan oluşturur, ancak DOSYA ZATEN VARSA içine girmeden 'FileExistsError' hatası fırlatır!
        with codecs.open(dosya_adi, "x", encoding="utf-8") as dosya:
            pass
        print(f"BAŞARILI: '{dosya_adi}' başarıyla oluşturuldu.\n")
        
    # except FileExistsError: Eğer 'try' içinde FileExistsError hatası fırlarsa, programın çökmesini engeller ve bu bloğa atlar.
    except FileExistsError:
        print(f"HATA: '{dosya_adi}' adında bir dosya zaten bilgisayarda var! İçindeki verilerin kaybolmaması için işlem iptal edildi.\n")
        
    # except Exception: Belirli olmayan, kalan her türlü genel şemsiye hata türü içindir (sistematik bir kriz vs).
    except Exception as e:
        print(f"BEKLENMEYEN BİR HATA OLUŞTU: {e}\n")
        
    # finally: Hata çıksa da çıkmasa da (işlem başarılı olsun ya da olmasın) en sonda MUTAHLAKA çalışacak olan temizlik/kapanış tetiğidir.
    finally:
        print("-> (Sistem Mesajı): Dosya oluşturma prosedürü sona erdi.\n")


def metin_ekle():
    dosya_adi = input("Üzerine metin eklenecek dosyanın adını giriniz: ")
    metin = input("Dosyaya eklenecek metni giriniz: ")
    
    try:
        # Eğer kullanıcının yanlış isim yazarak sisteme hayali (olmayan) bir dosyaya ekleme yapmasını önlemek istersek:
        # 'os.path.exists()' fonksiyonu ile dosyanın klasörde olup olmadığını sorgularız.
        if not os.path.exists(dosya_adi):
            # Dosya yoksa 'raise' anahtar kelimesiyle KENDİMİZ MANUELA OLARAK bir FileNotFoundError (Dosya Bulunamadı Hatası) fırlatıyoruz!
            raise FileNotFoundError
            
        # Eğer hata fırlatılmadıysa kod normal şekilde aşağıdan çalışmaya devam eder.
        # 'a' (append/ekleme) modu eski içeriğe zarar vermeden yeni veriyi sona ekler.
        with codecs.open(dosya_adi, "a", encoding="utf-8") as dosya:
            dosya.write("\n" + metin)
        print("BAŞARILI: Metin dosyaya güvenle eklendi.\n")
        
    except FileNotFoundError:
        print(f"HATA: Üzerine ekleme yapmak istediğiniz '{dosya_adi}' adında bir dosya yok! Önce dosyayı oluşturunuz.\n")
    except Exception as e:
        print(f"BEKLENMEYEN BİR HATA OLUŞTU: {e}\n")
    finally:
        print("-> (Sistem Mesajı): Metin ekleme bölümü kapatılıyor.\n")


def metin_sil():
    dosya_adi = input("İçinden metin silinecek dosyanın adını giriniz: ")
    
    try:
        # Eğer silinmek istenen kelime için açılacak olan dosya hiç yoksa 'r' (read) modu doğal olarak 'FileNotFoundError' fırlatır.
        with codecs.open(dosya_adi, "r", encoding="utf-8") as dosya:
            db = dosya.read()
            
        silinecek_metin = input("Dosyadan silmek istediğiniz metni veya kelimeyi tam olarak yazınız: ")
        
        # Kelimenin varolup olmamasını test edip 'if/else' ile mantıksal bir ayıklama (Logical Debugging) yapıyoruz.
        if silinecek_metin not in db:
            print(f"UYARI: Silmek istediğiniz '{silinecek_metin}' kelimesi zaten bu dosyanın içinde hiç geçmiyor. Dosyaya dokunulmadı.\n")
        else:
            # Metni bul ve yerine boşluk/hiçlik ("") atayarak cümlenin o kısmını yok et.
            guncel_db = db.replace(silinecek_metin, "")
            
            # Değiştirilmiş yepyeni veriyi eski dosyanın üzerine sıfırdan ('w' ile yaz).
            with codecs.open(dosya_adi, "w", encoding="utf-8") as dosya:
                dosya.write(guncel_db)
            print(f"BAŞARILI: '{silinecek_metin}' yapısı tüm dosyadan başarıyla temizlendi.\n")
            
    except FileNotFoundError:
        print(f"HATA: Silme işlemi yapmak için aranan '{dosya_adi}' adındaki belge sistem klasöründe bulunamadı!\n")
    except PermissionError:
        print(f"HATA: '{dosya_adi}' dosyasına erişim veya değiştirme izniniz yok (Sistem yönetici kısıtlaması olabilir).\n")
    except Exception as e:
         print(f"BİLİNMEYEN HATA: {e}\n")
    finally:
         print("-> (Sistem Mesajı): Metin silme/replace işlemi sonlandırıldı.\n")


def dosya_sil():
    dosya_adi = input("Tamamen silinecek (diske veda edecek) dosyanın adını giriniz: ")
    
    try:
        # os.remove() komutu eğer sileceği hedefi bulamazsa anında hata (FileNotFoundError) verir. 
        # Biz de bunu except ile yumuşatıyoruz.
        os.remove(dosya_adi)
        print(f"BAŞARILI: '{dosya_adi}' isimli dosya bilgisayardan kalıcı olarak çöpe atıldı.\n")
        
    except FileNotFoundError:
        print(f"HATA: Zaten '{dosya_adi}' adında bir dosya ortada yok. Belki de daha önceden ebediyete uğurlandı veya adı yanlış yazıldı!\n")
    # Dosya arkada çalışıyorken veya iznimiz yokken silersek oluşan PermissionError hatası kontrolü
    except PermissionError:
        print(f"HATA: '{dosya_adi}' şu anda arkada başka bir program (vs code vs) tarafından kullanılıyor veya silmeye yetkiniz yok!\n")
    except Exception as e:
        print(f"BEKLENMEYEN HATA DETAYI: {e}\n")
    finally:
        print("-> (Sistem Mesajı): Dosya silme operasyon fonksiyonundan çıkıldı.\n")


# -------------------------------------------------------------------------
# ANA PROGRAM BAŞLANGICI VE MENÜ (Try / Except İlaveli)
# -------------------------------------------------------------------------

while True:
    print("--- DOSYA İŞLEMLERİ MENÜSÜ ---")
    print("1. Dosya Oluşturma")
    print("2. Dosyaya Metin Ekleme")
    print("3. Metin Silme")
    print("4. Dosya Silme")
    print("5. Çıkış")
    
    # Tüm input(veri girişi) durumları da çökme potansiyeli taşıdığı için (Klavye interruptları vs.)
    # ana döngümüzün kalbini de try içine hapsediyoruz.
    try:
        secim = input("Lütfen yapmak istediğiniz işlemi seçiniz (1/2/3/4/5): ")
        
        if secim == '1':
            dosya_olustur()
        elif secim == '2':
            metin_ekle()
        elif secim == '3':
            metin_sil()
        elif secim == '4':
            dosya_sil()
        elif secim == '5':
            print("Sistemden güvenle çıkış yapılıyor... Hoşça kalın.")
            break 
        else:
            print("HATA! Geçersiz sistem girdisi. Lütfen sadece menüdeki tuşlamalardan (1-5) birini yapın.\n")
            
    # KeyboardInterrupt: Kullanıcı terminalde işlemler bitmeden programa 'CTRL+C' çekerek zorla durdurup sonlandırmak istediğinde
    # o çirkin kırmızı hata kodlarını görmesini engelleriz.
    except KeyboardInterrupt:
        print("\n\nSistem terminali üzerinden CTRL+C komutu gönderilerek zorla durduruldu. Acil Çıkış yapılıyor...\n")
        break
    except Exception as e:
        print(f"Ana Menü Beklenmeyen Sistem Hatası: {e}\n")
