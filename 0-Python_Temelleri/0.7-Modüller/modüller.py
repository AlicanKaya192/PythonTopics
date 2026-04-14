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