# İlk öğreneceğimiz fonksiyonlar open() ve close()
# open() fonksiyonu dosyayı açar.
# open() fonksiyonu iki parametre alır. 
# 1. Dosya adı
# 2. Dosya modu
# Dosya modları:
# 'w' - Yazma modu
# 'r' - Okuma modu
# 'a' - Ekleme modu
# 'x' - Oluşturma modu
# Eğer dosya yoksa 'w' ve 'a' modları dosyayı oluşturur.
# Eğer dosya varsa 'w' modu dosyanın içeriğini siler ve üzerine yazar.
# Eğer dosya varsa 'a' modu dosyanın içeriğini silmez, veriyi dosyanın sonuna ekler.
# 'r' modu dosya yoksa hata verir.
# 'x' modu dosya varsa hata verir.

# Göreceli Yol (Relative Path): Kodu çalıştırdığımız klasöre göre dosya yolu belirtilir.
dosya = open("0-Python_Temelleri/0.9-Dosya_İslemleri/deneme.txt", "w")
# 'w' modu eski dosyanın içeriğini silip üzerine yazar.
dosya.write("Merhaba Dunya\nBu bir deneme dosyasıdır.\nPython dersleri\n")
# close() fonksiyonu dosyayı kapatır, RAM'i boşaltır ve değişiklikleri diske kaydeder.
dosya.close()

dosya = open("0-Python_Temelleri/0.9-Dosya_İslemleri/deneme.txt", "a")
# 'a' modu dosyanın içeriğini silmez, eski verinin sonuna yeni veriyi ekler.
dosya.write("Merhaba Dunya 2")
dosya.close()

dosya = open("0-Python_Temelleri/0.9-Dosya_İslemleri/deneme.txt", "r")
# 'r' modu dosyanın içeriğini okur.
print(dosya.read())
dosya.close()

######################################
# Read metodun da türkçe karakter sorunu
######################################

# 'codecs' (coder-decoder) modülü, Türkçe gibi özel karakterler barındıran metin ,
# dosyalarını hatasız (örneğin utf-8 formatında) okumak/yazmak için kullanılır.
import codecs 

# 'with' bloğu: Dosya işlemleri tamamlandığında 'close()' metodunu yazmamıza gerek kalmadan 
# dosyanın otomatik ve güvenli kapanmasını sağlar. Hata çıksa bile dosyayı kapatır.
# codecs.open() : standart open() fonksiyonuna benzer ama 'encoding' parametresi alarak karakter 
# kodlamasını açıkça belirtebilmemizi sağlar.
# "0-Python_Temelleri/..." : Açılacak dosyanın projedeki göreceli yolu (relative path).
# "r" : 'Read' (Okuma) modu. Dosya sadece içerik okumak için açılır.
# encoding="utf-8" : Dünyada en yaygın kullanılan karakter kodlama standardı. Türkçe (ş, ğ, ı, ö, ç, ü) 
# karakterlerin okunurken bozulmamasını sağlar.
# as dosya : Açtığımız bu belgeyi alt satırlarda kullanabilmek için ona kod içinde 'dosya' ismini veriyoruz (Alias/takma ad).
# with sayesinde dosya otomatik kapanır. dosya.close() yazmamıza gerek kalmaz. 
# Bu sayede dosya bellekte gereksiz yer kaplamaz ve veri kaybı önlenir.
with codecs.open("0-Python_Temelleri/0.9-Dosya_İslemleri/deneme.txt", "r", encoding="utf-8") as dosya:
    # dosya.read() : Açılan metin dosyasının bütün içeriğini tek seferde baştan sona okur ve 
    # bir metin (string) olarak döndürür, print ise bunu ekrana yazdırır.
    print(dosya.read())

# readline() metodu, dosyadan sadece bir satır okur.
# dosya.readline() : Dosyanın imlecini (cursor) bir satır ileri kaydırır ve o satırdaki metni ekrana yazdırır.
# Eğer dosyanın sonuna gelinmişse boş bir değer döndürür.
# Satırları tek tek okumak için kullanılır.
# Satır sonundaki \n karakterini de okur.
# Bunun çalışması için bir değişkene atamamız gerekir.
# İlk koddan sonra readline() metodu tekrardan çalıştırılırsa dosyanın ikinci satırını okur.
a = dosya.readline()
print(a)

# readlines() metodu, dosyadan tüm satırları okur ve bir liste olarak döndürür.
# Satır sonundaki \n karakterini de okur.
b = dosya.readlines()
print(b)

for i in b:
    print(i)

# İstediğimiz satırı çağırabiliriz.
print(b[2])


######################################
# Var Olan Dosyaya Veri Ekleme
######################################

# "a" : 'Append' (Ekleme) Modu.
# Eğer dosya içinde önceden var olan verilerin silinmemesini ve yeni ekleyeceğimiz verilerin
# doğrudan dosyanın en sonuna eklenmesini istiyorsak 'a' modunu tercih ederiz.

# 'with' yapısı, islem bitince veya hata çıkarsa bile 'dosya.close()' gerektirmeden dosyanin guvenli sekilde kapanmasini saglar.
with codecs.open("0-Python_Temelleri/0.9-Dosya_İslemleri/deneme.txt", "a", encoding="utf-8") as dosya:
    
    # write() bir FONKSİYON DEĞİL, bir METODDUR (Nesne üzerinden çağırıldığı için dosya.write metod adını alır).
    # Görevi: İcine verdigimiz parametreyi (string) dosyanin icerisine yazmaktir.
    # 'a' moduyla actigimiz icin dosyanın sonundan eklemeye baslar.
    # \n karakteri bir alt satira gecis yapar.
    dosya.write("\nMerhaba Dunya 3")


######################################
# Var Olan Dosyanın Başına Veri Ekleme
######################################


# "r+" : 'Read and Write' (Okuma ve Yazma) Modu. 
# Dosyanin hem okunmasina hem de uzerinde degisiklik yapilmasina (yazilmasina) olanak tanir.
# Modun calismasi icin dosyanin halihazirda mevcut olmasi gereklidir (yoksa FileNotFoundError verir).
with codecs.open("0-Python_Temelleri/0.9-Dosya_İslemleri/deneme.txt", "r+", encoding="utf-8") as dosya:
    
    # Görevi: Dosyadaki tüm metin verisini baştan sona kadar okur ve string (metin) olarak dondurur.
    # Burada butun icerigi okuyup 'db' isimli degiskene kaydediyoruz.
    # Bu okuma islemi sonucunda dosya imleci (cursor) en sona ulasmis olur.
    db = dosya.read()
    
    # Görevi: Dosya okuma/yazma imlecinin (cursor) nerede duracağını(konumunu) degistirmektir.
    # Parametre olarak byte (bayt) cinsinden bir sayi alir. 
    # Imlecimiz 'read()' kullandigimiz icin dosyanin en sonundaydi. 
    # Eger 0 parametresi verirsek: dosya.seek(0) imleci dosyanın en basına (ilk karaktere, yani 0. endekse(index)) tasir.
    dosya.seek(0)
    
    # Burada, eski dosya iceriginin (db degiskeni) basina "Merhaba Dunya 4\n" stringini ekliyoruz. 
    # Arti isaretiyle metinleri birlestirip 'db' degiskenini bastan asagiya guncelemis oluyoruz.
    db = "Merhaba Dunya 4\n" + db
    
    # Görevi: Verilen icerigi yazmaktir. İmlecimiz 'seek(0)' yuzunden en basta oldugu icin,
    # guncellenmis 'db' verisini dosyanin ilk karakterinden baslayarak tamamen asagi dogru yazar.
    # Böylece metnin basina veriyi eklemis olduk.
    dosya.write(db)


######################################
# Var Olan Dosyanın İçine Veri Ekleme
######################################

# Yine hem okuma hem yazma yapacagimiz icin 'r+' (Read and Write) modunu kullaniyoruz.
with codecs.open("0-Python_Temelleri/0.9-Dosya_İslemleri/deneme.txt", "r+", encoding="utf-8") as dosya:
    
    # readlines() bir METODDUR (dosya objesine aittir).
    # Görevi: Dosyanin icindeki butun satirlari tek tek okuyup, her bir satiri virgüllerle ayrılmış bir liste (List) elemani olarak dondurmektir.
    # Sonuclar sunun gibi bir listeye kaydolur: ['1. satir\n', '2. satir\n', '3. satir\n'] 
    # Bu metod calistiktan sonra dosya imleci en sona gelmis olur.
    db = dosya.readlines()
    
    # insert() bir METODDUR (Python'daki yerleşik 'list' (liste) sinifina aittir, db bir liste oldugu icin db üzerinden cagirilir).
    # Görevi: Listede belli bir endekse (index) yeni bir eleman eklemektir.
    # Parametre olarak (index_numarası, eklenecek_veri) alir.
    # Burada 2. endekse (bilgisayar saymaya 0'dan basladigi icin aslinda 3. siraya denk gelir) "Merhaba Dunya....\n" verisini ekle dedik.
    # Eski 2. endeksteki ve sonrasındaki veriler silinmez, bir alt siraya (3. endekse doğru) kaydirilir.
    db.insert(2, "Merhaba Dunya....\n")
    
    # seek() bir METODDUR.
    # Görevi: Okuma/yazma imlecini dosya icinde konumlandirmaktir.
    # Az once readlines() ile tüm satirlari okuyup imleci dosyanin en sonuna tasimistik.
    # Eger 'db' listesini bu sekilde (imlec en sondayken) dosyaya geri yazsaydik, verileri eskinin altina en sondan eklemis (tekrarlamis) olurduk.
    # Bunu onlemek icin seek(0) diyerek imleci dosyanin en basina aliyoruz ki yeni yazacagimiz icerik var olanlarin uzerine bastan (0. byte'tan baslayarak) yazilsin.
    dosya.seek(0)
    
    # writelines() bir METODDUR (yine dosya objesine aittir).
    # Görevi: Icerisine verilen bir veri dizisini veya listesini (bizim durumumuzda db isimli liste) dosyanin icerisine yazdırmaktır.
    # Döngü (for loop) kullanmadan, icinde degisiklik yapip yepyeni bir satir ekledigimiz o koca listeyi alir, 
    # liste elemanlarini arka arkaya tek seferde metin formatında dosyaya yazar.
    # İmlecimiz dosyanın başında olduğu için (seek(0)) baştan aşağı tüm listeyi eski yazının üzerine ezer ve dosyaya yerleştirir.
    dosya.writelines(db)


######################################
# ALIŞTIRMA
######################################

# codecs modülünü eğer yukarıda import etmediysek diye bağımsız çalışabilmesi adına tekrar kuruyoruz.
import codecs

# 1. Kullanıcıdan oluşturmak istediği dosyanın temel adını alıp ilgili değişkene atıyoruz.
dosya_olustur = input("Lütfen Dosya Adını Giriniz : ")

# 2. Girilen ismin sonuna string birleştirmesi (+) ile ".txt" uzantısını bitişik olarak ekliyoruz.
dosya_new = dosya_olustur + ".txt"

# 3. f-string yöntemi (f"") kullanarak dosya_new ismini metne gömüyor ve dosyaya yazılacak ilk veriyi istiyoruz.
veri_gir = input(f"Lütfen {dosya_new} dosyasına veri ekleyin : ")

# 4. 'with' yapısıyla yeni dosyamızı 'w' (write/yazma) modunda açıyoruz (dosya yoksa sistem sıfırdan yaratacaktır).
with open(dosya_new, "w", encoding="utf-8") as dosya:
    
    # 'w' moduyla yarattığımız bu dosyanın içine az evvel kullanıcıdan aldığımız string veriyi doğrudan yazıyoruz.
    dosya.write(veri_gir)
    
    # İşleme devam etmek isteyip istemediğini soruyor, küçük 'e' harfi girse bile .upper() metodu ile büyük 'E' devşiriyoruz.
    soru_sor = input("Dosya Üzerine Ekleme Yapmak İstiyor Musunuz ? E/H : ").upper()

    # Eğer kullanıcının onayı veya tuşlaması 'E' ise:
    if soru_sor == "E":
        
        # EĞİTİM NOTU: Buradaki 'open(dosya_new, "a")' satırı aslında hiçbir işe yaramaz. Çünkü bu dosya zaten üstteki
        # 'with' bloğu sayesinde 'w' moduyla açık tutuluyor ve buradaki ikinci open metodu hiçbir değişkene atanmamış.
        # Hemen altındaki 'dosya.write()', hala en dıştaki 'w' modlu 'dosya' değişkenine emretmektedir.
        # Kod bu haliyle sorunsuz çalışır (çünkü with bloğu henüz kapanmadı) ancak gerçek bir 'a' modunda ekleme işlemi değildir.
        open(dosya_new, "a")
        
        # Eklemek istediği yeni veriyi alıyoruz ve cümlenin başına '\n' stringi koyarak yazının alt satıra geçmesini emrediyoruz.
        yeni_veri = "\n" + input("Lütfen eklemek istediğiniz veriyi yazınız : ")
        
        # Yeni veriyi de 'w' modunun açık tuttuğu bağlantıyı kullanarak dosyaya gönderiyoruz.
        dosya.write(yeni_veri)
        print("Verileriniz güncellendi.")
        
    # Eğer cevap 'H' ise veya rastgele bir giriş yapıldıysa işlemi sonlandırıyoruz.
    else:
        print("Çıkış Yapıldı")


# 5. Yukarıda 'with' bloğunun tamamen dışına çıktığımız an dosya hafızadan güvenle otomatik close() oldu.
# Yazdıklarımızı kontrol etmek için o aynı dosyayı bu kez de 'info' değişkeni altında 'r' (okuma) modunda tekrar uyandırıyoruz.
info = open(dosya_new, "r", encoding="utf-8")

# 6. Klasördeki dosyanın tüm içeriğini info.read() diyerek devasa bir string parçası olarak okuyup print() ile ekrana yansıtıyoruz.
print(info.read())

# EĞİTİM NOTU BİLGİSİ: Bu son blokta 'with' güvenlik yapısı kullanmadan manuel open() açtığımız için, RAM bellekte yer kaplamaması 
# ve belleğin sızıntı yapmaması adına en sona 'info.close()' yazarak dosyayı el ile kapatmamız en iyi programcı alışkanlıklarındandır.
info.close()