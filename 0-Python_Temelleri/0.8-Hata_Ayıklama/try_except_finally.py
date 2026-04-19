############################
# Try ve Except Kavramları
############################

# Try ve Except Kavramları
# Try ve Except, Python'da hata yönetimi için kullanılan yapılardır.
# Try bloğu, hata oluşabilecek kodları içerir.
# Except bloğu, try bloğunda hata oluştuğunda çalışacak kodları içerir.
# Bu yapılar sayesinde programımızda hata oluştuğunda programın durmasını engelleriz.
# Örnek; Kullanıcıdan sayı alırken kullanıcı harf girerse program hata verir. Bunu engellemek için try ve except kullanırız.

# Try içerisine hata oluşabilecek kodları yazarız.
# Except içerisine hata oluştuğunda çalışacak kodları yazarız.

try:
    sayi = int(input("Bir sayı giriniz: "))
except ValueError:
    print("Hatalı giriş! Lütfen bir sayı giriniz.")


# Varsayalım kişi 2 yi 0 a bölmek istesin. Bu durumda program hata verir. Bunu engellemek için try ve except kullanırız.
# ZeroDivisionError hatasını engellemek için except bloğuna ZeroDivisionError yazmalıyız. Bu hata 0 ile bölme hatasıdır.
# ValueError hatasını engellemek için except bloğuna ValueError yazmalıyız. Bu hata sayı yerine harf girme hatasıdır.

try:
    sayi1 = int(input("Bir sayı giriniz: "))
    sayi2 = int(input("Bir sayı giriniz: "))
    print(sayi1 / sayi2)
except ValueError:
    print("Hatalı giriş! Lütfen bir sayı giriniz.")
except ZeroDivisionError:
    print("Sıfıra bölünme hatası!")


# Except hata ismini belirtmezsek tüm hataları yakalar.
try:
    sayi1 = int(input("Bir sayı giriniz: "))
    sayi2 = int(input("Bir sayı giriniz: "))
    print(sayi1 / sayi2)
except:
    print("Bir hata oluştu!")


# Except hata ismini belirtirsek sadece o hatayı yakalar. Bu durumda programın diğer hataları yakalamasını engelleriz. 
# Ayrıca tek bir except bloğu ile birden fazla hatayı yakalayabiliriz.
try:
    sayi1 = int(input("Bir sayı giriniz: "))
    sayi2 = int(input("Bir sayı giriniz: "))
    print(sayi1 / sayi2)
except (ValueError, ZeroDivisionError):
    print("Hatalı giriş!")


# Try bloğunda hata oluşmazsa else bloğu çalışır.
try:
    sayi1 = int(input("Bir sayı giriniz: "))
    sayi2 = int(input("Bir sayı giriniz: "))
    print(sayi1 / sayi2)
except (ValueError, ZeroDivisionError):
    print("Hatalı giriş!")
else:
    print("İşlem başarılı!")


# Finally bloğu, try bloğunda hata oluşsa da oluşmasa da çalışır.
try:
    sayi1 = int(input("Bir sayı giriniz: "))
    sayi2 = int(input("Bir sayı giriniz: "))
    print(sayi1 / sayi2)
except (ValueError, ZeroDivisionError):
    print("Hatalı giriş!")
finally:
    print("İşlem tamamlandı!")


# Try bloğunda hata oluşursa except bloğu çalışır. 
# Try bloğunda hata oluşmazsa else bloğu çalışır.
# Finally bloğu, try bloğunda hata oluşsa da oluşmasa da çalışır.