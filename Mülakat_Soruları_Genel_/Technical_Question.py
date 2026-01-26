# =============================================================================
# DATA SCIENCE TEKNİK MÜLAKAT SORULARI VE CEVAPLARI
# =============================================================================

# =============================================================================
# BÖLÜM 1: PYTHON TEMELLERİ
# =============================================================================

# 1 - Python mı, R mı? Hangisini neden kullanıyorsun?
"""
CEVAP:
Ben genellikle Python tercih ediyorum çünkü hem veri analizi hem de yazılım geliştirme 
tarafında çok güçlü. Mesela bir model geliştirdikten sonra bunu production'a almak 
Python ile çok daha kolay. Flask veya FastAPI ile hızlıca API yazabiliyorum.

R'ın istatistik tarafında çok güçlü olduğunu biliyorum, özellikle akademik çalışmalarda 
ve ileri düzey istatistiksel analizlerde R kütüphaneleri daha zengin. Ama Python'un 
ekosistemi çok daha geniş - web scraping, otomasyon, deep learning derken her şeyi 
tek bir dilde yapabiliyorum.

Şirketinizde R kullanılıyorsa benim için sorun değil, R'a da aşinayım. Sonuçta mantık 
aynı, sadece syntax farklı. İkisini birlikte kullanmak da mümkün, mesela reticulate 
paketi ile R içinden Python çağırabiliyoruz.
"""

# 2 - C ve Java varken neden Python?
"""
CEVAP:
Veri bilimi için Python'un tercih edilmesinin birkaç önemli sebebi var. Birincisi, 
Python'un syntax'ı çok temiz ve okunabilir - bu da prototipleme aşamasında çok hızlı 
olmamı sağlıyor. Bir fikri test etmek için saatler harcamak istemiyorum.

İkincisi, NumPy, Pandas, Scikit-learn gibi kütüphaneler zaten C ile yazılmış, yani 
performans konusunda aslında perde arkasında C kullanıyoruz. Python sadece üst 
katmanda bize kolaylık sağlıyor.

Üçüncüsü, veri bilimi topluluğu Python etrafında şekillendi. Yeni bir algoritma 
çıktığında ilk Python implementasyonu geliyor. Stack Overflow'da soru sorduğumda 
cevap bulma şansım çok yüksek.

Tabii ki performans kritik durumlarda veya gömülü sistemlerde C/C++ kullanırım, 
ama veri analizi ve ML için Python ideal.
"""

# 3 - Aşağıdaki fonksiyonun analizi:
def alternating(string):
    new_string = ""
    for string_index in range(len(string)):
        if string_index % 2 == 0:
            new_string += string[string_index].upper()
        else:
            new_string += string[string_index].lower()
    print(new_string)

"""
CEVAP:
Bu fonksiyon bir string alıp karakterleri sırayla büyük-küçük harf yapıyor.

Satır satır açıklarsam:
- new_string = "" : Sonucu biriktireceğimiz boş string oluşturduk
- for string_index in range(len(string)) : String'in uzunluğu kadar döngü kuruyoruz
- if string_index % 2 == 0 : İndeks çift sayıysa (0, 2, 4...) büyük harf yapıyoruz
- else: Tek indekslerde küçük harf yapıyoruz
- print(new_string) : Sonucu yazdırıyoruz

Enumerate ile yazarsak daha Pythonic olur:

def alternating_v2(string):
    new_string = ""
    for index, char in enumerate(string):
        new_string += char.upper() if index % 2 == 0 else char.lower()
    print(new_string)

Enumerate'in avantajı: range(len()) yazmak yerine direkt index ve değeri alıyoruz.
Kod daha okunabilir oluyor ve hata yapma şansımız azalıyor. Ayrıca her seferinde
string[string_index] yazmak yerine direkt char kullanabiliyoruz.
"""

# =============================================================================
# BÖLÜM 2: VERİ YAPILARI
# =============================================================================

# 4 - Liste, Tuple, Set ve Dictionary arasındaki farklar nelerdir?
"""
CEVAP:
Liste: Sıralı, değiştirilebilir ve tekrarlı elemanlara izin verir. Örneğin bir 
alışveriş listesi gibi düşünebilirsiniz - sırası önemli, aynı üründen birden fazla 
olabilir.

Tuple: Listeden tek farkı değiştirilemez olması. Koordinatlar gibi sabit değerler 
için kullanırım. Mesela (x, y) koordinatı bir kere tanımlandıktan sonra değişmemeli.

Set: Sırasız ve sadece benzersiz elemanlar içerir. Bir veri setindeki unique 
değerleri bulmak için çok kullanışlı. Matematikteki küme kavramı gibi.

Dictionary: Key-value çiftleri tutar. Bir kişinin bilgilerini tutmak için ideal - 
{"ad": "Ali", "yaş": 25} gibi. Lookup işlemi O(1) olduğu için çok hızlı.

Gerçek hayat örneği: Bir e-ticaret sitesinde ürün listesi için liste, kategoriler 
için set (tekrar olmasın), ürün detayları için dictionary kullanırım.
"""

# 5 - List Comprehension nedir? Neden kullanırız?
"""
CEVAP:
List comprehension, döngü ve koşulları tek satırda yazarak liste oluşturmamızı 
sağlayan Pythonic bir yapı. Hem daha okunabilir hem de genellikle daha hızlı.

Örnek - klasik yol:
kareler = []
for i in range(10):
    kareler.append(i**2)

List comprehension ile:
kareler = [i**2 for i in range(10)]

Koşullu örnek - sadece çift sayıların kareleri:
cift_kareler = [i**2 for i in range(10) if i % 2 == 0]

Nested örnek - 2D matris oluşturma:
matris = [[j for j in range(3)] for i in range(3)]

Neden kullanırız? Kod daha kısa ve okunabilir oluyor. Ayrıca Python'un iç 
optimizasyonları sayesinde genellikle klasik döngüden %10-20 daha hızlı çalışıyor.
Ama çok karmaşık comprehension'lar okunabilirliği bozar, o zaman normal döngü 
tercih edilmeli.
"""

# 6 - Mutable ve Immutable nedir? Örneklerle açıklar mısınız?
"""
CEVAP:
Mutable objeler oluşturulduktan sonra değiştirilebilir, immutable objeler değiştirilemez.

Mutable: list, dict, set
Immutable: int, float, str, tuple, frozenset

Bu neden önemli? Fonksiyonlara argüman geçerken dikkat etmeliyiz:

def fonk(liste):
    liste.append(4)
    
orijinal = [1, 2, 3]
fonk(orijinal)
print(orijinal)  # [1, 2, 3, 4] - Orijinal liste değişti!

Bu yüzden fonksiyonlarda listeyi değiştirmek istemiyorsak .copy() kullanmalıyız.

String'ler immutable olduğu için her string işleminde yeni bir obje oluşuyor. 
Bu yüzden çok fazla string birleştirme yapacaksak join() kullanmak daha performanslı.
"""

# =============================================================================
# BÖLÜM 3: NUMPY
# =============================================================================

# 7 - NumPy nedir ve neden Python listelerinden daha hızlıdır?
"""
CEVAP:
NumPy, Python'da bilimsel hesaplama için temel kütüphanedir. ndarray adı verilen 
çok boyutlu array yapısı sunar.

Neden hızlı?
1. Homojen veri tipi: Tüm elemanlar aynı tipte, bu yüzden bellek erişimi çok hızlı
2. Vektörizasyon: C seviyesinde optimize edilmiş işlemler, döngü yazmaya gerek yok
3. Bellek düzeni: Veriler bellekte ardışık tutulur (contiguous memory)

Örnek karşılaştırma:
import numpy as np
import time

# Python listesi ile
liste = list(range(1000000))
start = time.time()
sonuc = [x*2 for x in liste]
print(f"Liste: {time.time()-start:.4f} saniye")

# NumPy ile
arr = np.arange(1000000)
start = time.time()
sonuc = arr * 2
print(f"NumPy: {time.time()-start:.4f} saniye")

NumPy genellikle 10-100 kat daha hızlı çıkar. Büyük veri setlerinde bu fark kritik.
"""

# 8 - Broadcasting nedir?
"""
CEVAP:
Broadcasting, farklı boyutlardaki array'lerle işlem yapmamızı sağlayan bir NumPy 
özelliği. Küçük array otomatik olarak büyük array'in boyutuna 'yayılır'.

Örnek:
import numpy as np

a = np.array([[1, 2, 3],
              [4, 5, 6]])  # 2x3 matris

b = np.array([10, 20, 30])  # 1x3 vektör

sonuc = a + b
# [[11, 22, 33],
#  [14, 25, 36]]

Burada b vektörü otomatik olarak her satıra uygulandı. Manuel olarak döngü 
yazmamıza gerek kalmadı.

Kurallar:
1. Boyutlar sağdan sola karşılaştırılır
2. Boyutlar eşit veya biri 1 ise uyumludur
3. Eksik boyutlar 1 olarak kabul edilir

Bu özellik hem kodu kısaltır hem de çok daha hızlı çalışır çünkü C seviyesinde 
optimize edilmiştir.
"""

# 9 - Reshape, flatten ve ravel arasındaki fark nedir?
"""
CEVAP:
Hepsi array'in şeklini değiştirmek için kullanılır ama farklı amaçları var.

Reshape: Array'i istediğimiz boyuta dönüştürür
arr = np.arange(12)
arr.reshape(3, 4)  # 3x4 matris
arr.reshape(-1, 4)  # -1 otomatik hesapla demek

Flatten: Array'i 1D'ye dönüştürür ve HER ZAMAN kopya oluşturur
arr = np.array([[1,2], [3,4]])
flat = arr.flatten()
flat[0] = 99  # orijinal arr değişmez

Ravel: Flatten gibi ama MÜMKÜNSE kopya oluşturmaz (view döner)
arr = np.array([[1,2], [3,4]])
rav = arr.ravel()
rav[0] = 99  # orijinal arr de değişir!

Ne zaman hangisi?
- Orijinalin değişmesini istemiyorsanız: flatten()
- Performans önemliyse ve orijinalin değişmesi sorun değilse: ravel()
- Belirli bir şekle dönüştürmek istiyorsanız: reshape()
"""

# =============================================================================
# BÖLÜM 4: PANDAS
# =============================================================================

# 10 - Series ve DataFrame arasındaki fark nedir?
"""
CEVAP:
Series: Tek boyutlu, indeksli bir veri yapısı. Bir sütun gibi düşünebilirsiniz.
Her elemanın bir indeksi var.

import pandas as pd
s = pd.Series([10, 20, 30], index=['a', 'b', 'c'])
print(s['a'])  # 10

DataFrame: İki boyutlu, tablo şeklinde veri yapısı. Birden fazla Series'in 
birleşimi gibi düşünebilirsiniz.

df = pd.DataFrame({
    'isim': ['Ali', 'Veli'],
    'yas': [25, 30]
})

Aslında DataFrame, aynı indeksi paylaşan Series'lerin bir koleksiyonu. Her sütun 
bir Series. Bu yüzden df['isim'] yazdığımızda bir Series döner.

Gerçek hayatta genellikle DataFrame kullanıyoruz çünkü veriler tablolar halinde 
geliyor. Series daha çok ara işlemler veya tek bir değişken ile çalışırken kullanılır.
"""

# 11 - loc ve iloc arasındaki fark nedir?
"""
CEVAP:
loc: Label-based, yani indeks isimleriyle erişim sağlar
iloc: Integer-based, yani pozisyon numarasıyla erişim sağlar

df = pd.DataFrame({
    'A': [1, 2, 3],
    'B': [4, 5, 6]
}, index=['x', 'y', 'z'])

# loc ile:
df.loc['x', 'A']  # 1 - indeks ismi ve sütun ismi
df.loc['x':'y', 'A']  # x ve y satırları - SON DAHİL

# iloc ile:
df.iloc[0, 0]  # 1 - 0. satır, 0. sütun
df.iloc[0:2, 0]  # 0 ve 1. satırlar - SON HARİÇ

Önemli fark: loc'da slice yaparken son eleman DAHİL, iloc'da HARİÇ.
Bu Python'un genel indexing kuralıyla uyumlu (iloc) ve karışıklığa yol açabilir.

Tavsiyem: İndeks isimleri anlamlıysa loc, pozisyonla çalışıyorsanız iloc kullanın.
"""

# 12 - Groupby nasıl çalışır? Örnek verir misiniz?
"""
CEVAP:
Groupby, SQL'deki GROUP BY gibi veriyi kategorilere ayırıp her kategori için 
işlem yapmamızı sağlar. Split-Apply-Combine mantığıyla çalışır.

df = pd.DataFrame({
    'departman': ['IT', 'HR', 'IT', 'HR', 'IT'],
    'maas': [5000, 4000, 6000, 4500, 5500]
})

# Her departmanın ortalama maaşı
df.groupby('departman')['maas'].mean()
# HR: 4250, IT: 5500

# Birden fazla aggregation
df.groupby('departman')['maas'].agg(['mean', 'min', 'max', 'count'])

# Birden fazla sütunla gruplama
df.groupby(['departman', 'yil'])['maas'].mean()

# Transform - orijinal boyutta sonuç döner
df['dept_ort'] = df.groupby('departman')['maas'].transform('mean')
# Her satıra kendi departmanının ortalaması eklenir

Gerçek hayat örneği: E-ticarette müşteri bazında toplam harcama, ürün kategorisi 
bazında satış adetleri gibi analizler için vazgeçilmez.
"""

# 13 - Merge, join ve concat arasındaki farklar nelerdir?
"""
CEVAP:
Üçü de veri birleştirmek için ama farklı senaryolarda kullanılır.

CONCAT: Satır veya sütun bazında basit birleştirme
df1 = pd.DataFrame({'A': [1, 2]})
df2 = pd.DataFrame({'A': [3, 4]})
pd.concat([df1, df2])  # Alt alta birleşir

MERGE: SQL join gibi, ortak sütuna göre birleştirir
customers = pd.DataFrame({'id': [1, 2], 'name': ['Ali', 'Veli']})
orders = pd.DataFrame({'customer_id': [1, 1, 2], 'amount': [100, 200, 150]})
pd.merge(customers, orders, left_on='id', right_on='customer_id')

# Merge türleri:
# inner: sadece eşleşenler (default)
# left: sol tablo tam, sağdan eşleşenler
# right: sağ tablo tam, soldan eşleşenler  
# outer: her iki tablo da tam

JOIN: Merge ile aynı ama indeks üzerinden çalışır
df1.join(df2)  # İndekslere göre birleşir

Hangisini ne zaman?
- Basit alt alta/yan yana birleştirme: concat
- Ortak sütuna göre: merge  
- İndekse göre: join
"""

# 14 - Apply fonksiyonu ne işe yarar?
"""
CEVAP:
Apply, DataFrame veya Series'e özel fonksiyonlar uygulamak için kullanılır.
Pandas'ın built-in fonksiyonları yetmediğinde devreye girer.

# Series üzerinde apply
df['isim'].apply(lambda x: x.upper())
df['isim'].apply(len)  # her ismin uzunluğu

# DataFrame üzerinde apply
df.apply(lambda x: x.max() - x.min())  # her sütunun range'i

# axis parametresi
df.apply(lambda row: row['fiyat'] * row['adet'], axis=1)  # satır bazında

# Özel fonksiyon ile
def kategorize(yas):
    if yas < 18:
        return 'Çocuk'
    elif yas < 65:
        return 'Yetişkin'
    else:
        return 'Yaşlı'

df['yas_grubu'] = df['yas'].apply(kategorize)

Dikkat: Apply her zaman en hızlı çözüm değil. Mümkünse vektörel işlemler tercih 
edilmeli. Ama karmaşık mantık gerektiğinde apply çok işe yarıyor.
"""

# 15 - Eksik verileri nasıl tespit eder ve doldurursunuz?
"""
CEVAP:
Eksik veri tespiti:
df.isnull().sum()  # her sütundaki eksik sayısı
df.isnull().sum().sum()  # toplam eksik sayısı
df.info()  # non-null count gösterir

Eksik verileri doldurma stratejileri:

1. Silme:
df.dropna()  # eksik olan satırları sil
df.dropna(subset=['onemli_sutun'])  # belirli sütunda eksik olanları sil

2. Sabit değerle doldurma:
df['sutun'].fillna(0)
df['sutun'].fillna('Bilinmiyor')

3. İstatistiksel değerle:
df['sutun'].fillna(df['sutun'].mean())  # ortalama
df['sutun'].fillna(df['sutun'].median())  # medyan - outlier varsa daha iyi
df['sutun'].fillna(df['sutun'].mode()[0])  # mod - kategorik için

4. Forward/Backward fill:
df['sutun'].fillna(method='ffill')  # önceki değerle doldur
df['sutun'].fillna(method='bfill')  # sonraki değerle doldur

5. Grup bazında doldurma:
df['maas'] = df.groupby('departman')['maas'].transform(
    lambda x: x.fillna(x.mean())
)

Hangi yöntemi seçeceğim verinin yapısına ve eksikliğin nedenine bağlı. Random 
eksiklik varsa mean/median, sistematik eksiklik varsa farklı yaklaşımlar gerekir.
"""

# =============================================================================
# BÖLÜM 5: VERİ GÖRSELLEŞTİRME
# =============================================================================

# 16 - Matplotlib ve Seaborn arasındaki fark nedir?
"""
CEVAP:
Matplotlib: Python'un temel görselleştirme kütüphanesi. Çok esnek ama bazen 
fazla kod yazmak gerekiyor. Low-level kontrol istediğimde kullanıyorum.

Seaborn: Matplotlib üzerine kurulu, daha az kodla daha güzel grafikler. 
İstatistiksel görselleştirmeler için özellikle güçlü.

Karşılaştırma örneği - scatter plot:

# Matplotlib
plt.figure(figsize=(10, 6))
plt.scatter(df['x'], df['y'], c=df['kategori'])
plt.xlabel('X değeri')
plt.ylabel('Y değeri')
plt.title('Scatter Plot')
plt.show()

# Seaborn
sns.scatterplot(data=df, x='x', y='y', hue='kategori')
plt.show()

Seaborn'un avantajları:
- Otomatik renk paletleri
- DataFrame ile doğrudan çalışma
- Hue parametresi ile kolay gruplandırma
- Güzel default stiller

Ne zaman hangisi?
- Hızlı EDA ve istatistiksel grafikler: Seaborn
- Özelleştirilmiş, publication-ready grafikler: Matplotlib
- Genellikle ikisini birlikte kullanıyorum
"""

# 17 - Hangi grafik türünü ne zaman kullanırsınız?
"""
CEVAP:
İki sayısal değişken ilişkisi: Scatter plot
sns.scatterplot(x='education', y='income', data=df)

Dağılım görmek: Histogram veya KDE
sns.histplot(df['age'], kde=True)

Kategorik vs sayısal: Box plot veya Violin plot
sns.boxplot(x='department', y='salary', data=df)

Zaman serisi: Line plot
plt.plot(df['date'], df['sales'])

Kategorik oranlar: Pie chart veya bar plot
df['category'].value_counts().plot(kind='bar')

Korelasyon matrisi: Heatmap
sns.heatmap(df.corr(), annot=True, cmap='coolwarm')

Çoklu değişken ilişkileri: Pair plot
sns.pairplot(df, hue='target')

Pratik kural: Verinin tipine ve anlatmak istediğim hikayeye göre seçiyorum.
Her zaman en basit ve anlaşılır grafiği tercih etmeye çalışıyorum.
"""

# =============================================================================
# BÖLÜM 6: MACHINE LEARNING TEMELLERİ
# =============================================================================

# 18 - Supervised ve Unsupervised Learning arasındaki fark nedir?
"""
CEVAP:
Supervised Learning (Denetimli): Etiketli veri ile eğitim yapılır. Model, girdi ve 
çıktı arasındaki ilişkiyi öğrenir. Örn: Spam tespiti, fiyat tahmini.

Unsupervised Learning (Denetimsiz): Etiketsiz veri ile çalışır. Model, verideki 
gizli kalıpları keşfeder. Örn: Müşteri segmentasyonu, anomali tespiti.

Supervised'da "doğru cevap" var, Unsupervised'da yok.
"""

# 19 - Overfitting nedir ve nasıl önlenir?
"""
CEVAP:
Modelin eğitim verisini ezberlediği durum. Training accuracy yüksek, test düşük.

Önleme: Daha fazla veri, Cross-validation, Regularization (L1/L2), Early stopping,
Dropout, Feature selection, Model basitleştirme.
"""

# 20 - Bias-Variance Tradeoff nedir?
"""
CEVAP:
Bias: Modelin basitleştirme hatası (underfitting)
Variance: Modelin veriye aşırı hassasiyeti (overfitting)

İkisi arasında denge gerekli. Karmaşıklık artınca bias düşer variance artar.
"""

# 21 - Cross-validation nedir?
"""
CEVAP:
Veriyi K parçaya bölüp her seferinde farklı parçayı test olarak kullanma. 
Daha güvenilir performans tahmini sağlar. Tek split'e bağımlılık azalır.
"""

# 22 - Linear Regression varsayımları nelerdir?
"""
CEVAP:
1. Doğrusallık - X ve y arasında lineer ilişki
2. Bağımsızlık - Gözlemler bağımsız
3. Homojenlik - Sabit varyans
4. Normallik - Hatalar normal dağılımlı
5. Çoklu doğrusal bağlantı yok - Değişkenler arası düşük korelasyon
"""

# 23 - Decision Tree vs Random Forest farkı nedir?
"""
CEVAP:
Decision Tree tek ağaç, overfitting riski yüksek.
Random Forest birçok ağacın ensemble'ı, daha stabil ve genelleme iyi.

RF bagging kullanır: Bootstrap samples + rastgele feature seçimi.
"""

# 24 - Precision, Recall, F1-Score nedir?
"""
CEVAP:
Precision: Pozitif dediğimizin ne kadarı doğru? TP/(TP+FP)
Recall: Gerçek pozitiflerin ne kadarını yakaladık? TP/(TP+FN)
F1: İkisinin harmonik ortalaması

FP maliyetliyse Precision, FN maliyetliyse Recall önemli.
"""

# 25 - Feature Scaling neden önemli?
"""
CEVAP:
Özellikleri aynı ölçeğe getirir. KNN, SVM, Neural Networks için zorunlu.
StandardScaler: (x-mean)/std, MinMaxScaler: (x-min)/(max-min)
Tree-based modeller için gerekmez.
"""

# 26 - Kategorik değişkenler nasıl encode edilir?
"""
CEVAP:
Label Encoding: Her kategoriye sayı atar (ordinal için)
One-Hot Encoding: Her kategori için ayrı sütun (nominal için)
Target Encoding: Kategorileri hedef ortalamasıyla değiştirir
"""

# =============================================================================
# BÖLÜM 7: SQL
# =============================================================================

# 27 - JOIN türlerini açıklar mısınız?
"""
CEVAP:
INNER JOIN: Sadece eşleşen kayıtlar
LEFT JOIN: Sol tablo tam, sağdan eşleşenler
RIGHT JOIN: Sağ tablo tam, soldan eşleşenler
FULL OUTER JOIN: Her iki tablo da tam
CROSS JOIN: Kartezyen çarpım

SELECT * FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
"""

# 28 - GROUP BY ve HAVING farkı nedir?
"""
CEVAP:
GROUP BY gruplama yapar, HAVING grupları filtreler.
WHERE satır bazında filtre, HAVING grup bazında.

SELECT department, AVG(salary) 
FROM employees 
GROUP BY department 
HAVING AVG(salary) > 5000
"""

# 29 - Window Functions nedir?
"""
CEVAP:
Satırları gruplamadan hesaplama yapar. Her satır korunur.
ROW_NUMBER(), RANK(), DENSE_RANK(), LAG(), LEAD(), SUM() OVER()

SELECT name, salary, 
       RANK() OVER (ORDER BY salary DESC) as rank
FROM employees
"""

# =============================================================================
# BÖLÜM 8: CRM ANALİTİK
# =============================================================================

# 30 - RFM analizi nedir?
"""
CEVAP:
Müşteri segmentasyonu için kullanılan yöntem:
R (Recency): Son alışverişten bu yana geçen süre
F (Frequency): Toplam alışveriş sayısı
M (Monetary): Toplam harcama miktarı

Her metrik için skor verilir (1-5), müşteriler segmentlere ayrılır.
"""

# 31 - Customer Lifetime Value (CLV) nedir?
"""
CEVAP:
Bir müşterinin işletmeye toplam katkısının tahmini değeri.
CLV = Ortalama Sipariş Değeri × Satın Alma Sıklığı × Müşteri Ömrü

Pazarlama bütçesi ve müşteri edinme maliyeti kararlarında kullanılır.
"""

# =============================================================================
# BÖLÜM 9: TAVSİYE SİSTEMLERİ
# =============================================================================

# 32 - Collaborative vs Content-Based Filtering farkı?
"""
CEVAP:
Collaborative Filtering: Benzer kullanıcıların tercihlerine göre öneri.
"Seni beğenenler bunu da beğendi"

Content-Based Filtering: Ürün özelliklerine göre öneri.
"Buna benzer ürünler"

Hybrid: İkisini birleştiren sistemler daha iyi sonuç verir.
"""

# 33 - Cold Start problemi nedir?
"""
CEVAP:
Yeni kullanıcı veya ürün için yeterli veri olmadığında öneri yapamama durumu.

Çözümler: Demografik bilgiler, popüler ürünler, açık tercih sorma.
"""

# =============================================================================
# BÖLÜM 10: NLP
# =============================================================================

# 34 - Tokenization nedir?
"""
CEVAP:
Metni daha küçük birimlere (token) ayırma işlemi.
Kelime tokenization: "Merhaba dünya" → ["Merhaba", "dünya"]
Cümle tokenization: Paragrafi cümlelere ayırır.
"""

# 35 - TF-IDF nedir?
"""
CEVAP:
Term Frequency-Inverse Document Frequency. Bir kelimenin belgedeki önemini ölçer.

TF: Kelimenin belgede geçme sıklığı
IDF: Kelimenin tüm belgelerdeki nadirligi
TF-IDF = TF × IDF

Nadir ama belgede sık geçen kelimeler yüksek skor alır.
"""

# 36 - Word Embedding nedir?
"""
CEVAP:
Kelimeleri sayısal vektörlere dönüştürme. Anlamsal benzerliği yakalar.
Word2Vec, GloVe, FastText popüler yöntemler.

"kral" - "erkek" + "kadın" ≈ "kraliçe" gibi ilişkiler öğrenilir.
"""

# =============================================================================
# BÖLÜM 11: GENERATİF AI
# =============================================================================

# 37 - Prompt Engineering nedir?
"""
CEVAP:
LLM'lerden en iyi sonucu almak için prompt tasarlama sanatı.

Teknikler: Zero-shot, Few-shot, Chain of Thought, Role-playing
İyi prompt: Net, örnekli, bağlamlı, format belirtilmiş.
"""

# 38 - RAG (Retrieval Augmented Generation) nedir?
"""
CEVAP:
LLM'i harici bilgi kaynağıyla zenginleştirme yöntemi.
1. Soru gelir
2. İlgili dokümanlar veritabanından alınır
3. LLM'e bağlam olarak verilir
4. Güncel ve doğru cevap üretilir

Hallucination azaltır, güncel bilgi sağlar.
"""

# 39 - Fine-tuning nedir?
"""
CEVAP:
Önceden eğitilmiş modeli özel veri setiyle yeniden eğitme.
Base modeli alıp domain-specific hale getirme.

Transfer learning'in bir uygulaması. Sıfırdan eğitmekten çok daha hızlı ve ucuz.
"""

# =============================================================================
# BÖLÜM 12: GIT VE SÜRÜM KONTROLÜ
# =============================================================================

# 40 - Git branch stratejileri nelerdir?
"""
CEVAP:
Git Flow: main, develop, feature, release, hotfix dalları
GitHub Flow: Basit, sadece main ve feature dalları
Trunk-Based: Sürekli main'e merge, kısa ömürlü dallar

Proje büyüklüğüne göre seçilir. Küçük takımlar için GitHub Flow yeterli.
"""

# 41 - Merge vs Rebase farkı nedir?
"""
CEVAP:
Merge: İki branch'i birleştirir, merge commit oluşur. Tarihçe korunur.
Rebase: Commit'leri yeni base üzerine taşır. Temiz history.

Public branch'lerde merge, local feature branch'lerde rebase tercih edilir.
"""

# 42 - Git stash nedir ve ne zaman kullanılır?
"""
CEVAP:
Stash, yarım kalmış değişiklikleri geçici olarak saklamamızı sağlar.

git stash        # değişiklikleri sakla
git stash list   # saklananları listele
git stash pop    # geri al ve listeden sil
git stash apply  # geri al ama listede kalsın

Ne zaman kullanırız: Acil bir hotfix gerekti ama feature üzerinde çalışıyorum.
Commit atmak için erken. Stash yapıp branch değiştirip sonra geri dönüyorum.
"""

# 43 - Cherry-pick nedir?
"""
CEVAP:
Belirli bir commit'i başka bir branch'e almak için kullanılır.

git cherry-pick <commit-hash>

Örnek: Feature branch'deki sadece bir bug fix'i main'e almak istiyorum ama
tüm feature'ı değil. O zaman sadece o commit'i cherry-pick yaparım.

Dikkat: Aynı commit iki yerde olur, merge'de conflict çıkabilir.
"""

# 44 - Git reset vs revert farkı nedir?
"""
CEVAP:
Reset: Commit'leri tarihten siler (tehlikeli)
git reset --soft HEAD~1   # commit gider, değişiklikler staged kalır
git reset --hard HEAD~1   # commit ve değişiklikler tamamen silinir

Revert: Tersine commit oluşturur (güvenli)
git revert <commit-hash>  # değişiklikleri geri alan yeni commit

Paylaşılmış branch'lerde revert, local branch'te reset kullanılır.
"""

# 45 - Git conflict nasıl çözülür?
"""
CEVAP:
Conflict, iki kişi aynı satırı değiştirdiğinde oluşur.

1. git status ile conflict olan dosyaları gör
2. Dosyayı aç, <<<<<<< ve >>>>>>> işaretlerini bul
3. Hangi değişikliğin kalacağına karar ver
4. İşaretleri temizle, doğru kodu bırak
5. git add <dosya> ile staged yap
6. git commit ile tamamla

VS Code gibi IDE'ler conflict çözümünü görsel olarak kolaylaştırır.
"""

# 46 - .gitignore ne işe yarar?
"""
CEVAP:
Git'in takip etmemesi gereken dosya ve klasörleri belirtir.

Örnek .gitignore:
*.pyc           # Python bytecode
__pycache__/    # Cache klasörü
.env            # Gizli API keyleri
venv/           # Sanal ortam
*.log           # Log dosyaları
.DS_Store       # Mac sistem dosyası

Önemli: Zaten tracked dosyalar ignore edilmez. Önce git rm --cached gerekir.
"""

# =============================================================================
# EK PYTHON SORULARI
# =============================================================================

# 47 - *args ve **kwargs nedir?
"""
CEVAP:
*args: Fonksiyona istediğin kadar positional argüman geçirmeni sağlar. Tuple olarak alır.
**kwargs: İstediğin kadar keyword argüman geçirmeni sağlar. Dictionary olarak alır.

def ornek(*args, **kwargs):
    print(f"args: {args}")      # (1, 2, 3)
    print(f"kwargs: {kwargs}")  # {'isim': 'Ali', 'yas': 25}

ornek(1, 2, 3, isim='Ali', yas=25)

Wrapper fonksiyonlar ve decoratorlerde çok kullanılır.
"""

# 48 - Decorator nedir?
"""
CEVAP:
Decorator, bir fonksiyonun davranışını değiştirmek için kullanılan fonksiyondur.
@ sembolü ile kullanılır.

def timer(func):
    def wrapper(*args, **kwargs):
        import time
        start = time.time()
        result = func(*args, **kwargs)
        print(f"Süre: {time.time() - start:.2f}s")
        return result
    return wrapper

@timer
def yavaş_fonksiyon():
    import time
    time.sleep(1)

Kullanım alanları: Loglama, yetkilendirme, caching, timing.
"""

# 49 - Lambda fonksiyonu nedir?
"""
CEVAP:
Tek satırlık anonim fonksiyon. Kısa işlemler için kullanılır.

# Normal fonksiyon
def kare(x):
    return x ** 2

# Lambda eşdeğeri
kare = lambda x: x ** 2

# Genellikle map, filter, sorted içinde kullanılır
liste = [1, 2, 3, 4]
kareler = list(map(lambda x: x**2, liste))
ciftler = list(filter(lambda x: x % 2 == 0, liste))
sirali = sorted(liste, key=lambda x: -x)  # Azalan sıra

Dikkat: Karmaşık işlemler için normal fonksiyon daha okunabilir.
"""

# 50 - Generator nedir?
"""
CEVAP:
Lazy evaluation ile değerleri teker teker üreten fonksiyon. yield kullanır.

def sayilar(n):
    for i in range(n):
        yield i * 2

# Tüm değerleri bellekte tutmaz, ihtiyaç oldukça üretir
for sayi in sayilar(1000000):
    print(sayi)
    if sayi > 10:
        break

Avantaj: Büyük veri setleri için bellek tasarrufu sağlar.
List comprehension yerine generator expression: (x**2 for x in range(1000000))
"""

# 51 - Exception handling nasıl yapılır?
"""
CEVAP:
try-except bloğu ile hataları yakalarız.

try:
    sonuc = 10 / 0
except ZeroDivisionError as e:
    print(f"Sıfıra bölme hatası: {e}")
except Exception as e:
    print(f"Beklenmeyen hata: {e}")
else:
    print("Hata olmadı")
finally:
    print("Her durumda çalışır")

Özel exception tanımlama:
class OzelHata(Exception):
    pass

raise OzelHata("Bir şeyler yanlış gitti")
"""

# =============================================================================
# EK PANDAS SORULARI
# =============================================================================

# 52 - Pivot table nedir?
"""
CEVAP:
Veriyi özetlemek için kullanılan güçlü bir araç. Excel pivot table gibi.

df.pivot_table(
    values='satis',          # Özetlenecek değer
    index='kategori',        # Satırlar
    columns='ay',            # Sütunlar
    aggfunc='sum'            # Toplama fonksiyonu
)

Birden fazla aggregation:
df.pivot_table(values='satis', index='kategori', aggfunc=['sum', 'mean', 'count'])
"""

# 53 - Melt fonksiyonu ne yapar?
"""
CEVAP:
Wide format'tan long format'a dönüşüm yapar. Pivot'un tersi.

# Wide format
   isim  mat  fen
0  Ali   90   85
1  Veli  80   95

pd.melt(df, id_vars=['isim'], value_vars=['mat', 'fen'], 
        var_name='ders', value_name='not')

# Long format
   isim  ders  not
0  Ali   mat   90
1  Veli  mat   80
2  Ali   fen   85
3  Veli  fen   95

Görselleştirme ve bazı analizler için long format gerekir.
"""

# 54 - Query metodu nasıl kullanılır?
"""
CEVAP:
SQL benzeri syntax ile filtreleme yapar. Okunabilir ve kısa.

# Klasik yöntem
df[(df['yas'] > 25) & (df['sehir'] == 'İstanbul')]

# Query ile
df.query('yas > 25 and sehir == "İstanbul"')

# Değişken kullanımı
min_yas = 25
df.query('yas > @min_yas')

Uzun koşulları yazmak için çok kullanışlı.
"""

# =============================================================================
# EK MACHINE LEARNING SORULARI
# =============================================================================

# 55 - Regularization (L1 ve L2) nedir?
"""
CEVAP:
Overfitting'i önlemek için loss fonksiyonuna ceza terimi ekleme.

L1 (Lasso): |w| toplamını ekler. Feature selection yapar, bazı katsayıları sıfırlar.
L2 (Ridge): w² toplamını ekler. Katsayıları küçültür ama sıfırlamaz.
ElasticNet: L1 + L2 kombinasyonu.

from sklearn.linear_model import Ridge, Lasso

ridge = Ridge(alpha=1.0)  # alpha = regularization strength
lasso = Lasso(alpha=0.1)

Ne zaman hangisi: Çok feature varsa ve seçim istiyorsan L1, genel shrinkage L2.
"""

# 56 - Ensemble Methods nelerdir?
"""
CEVAP:
Birden fazla modeli birleştirerek daha güçlü tahmin yapma.

Bagging: Bootstrap samples + paralel eğitim + ortalama/oylama
Örnek: Random Forest

Boosting: Sıralı eğitim, her model öncekinin hatasını düzeltir
Örnek: XGBoost, LightGBM, AdaBoost

Stacking: Farklı model türlerini birleştir, meta-model eğit
Örnek: RF + XGB + LogReg → Meta model

Bagging variance'ı azaltır, boosting bias'ı azaltır.
"""

# 57 - Hyperparameter tuning nasıl yapılır?
"""
CEVAP:
Model dışından ayarlanan parametreleri optimize etme.

Grid Search: Tüm kombinasyonları dener, kapsamlı ama yavaş
from sklearn.model_selection import GridSearchCV
grid = GridSearchCV(model, param_grid, cv=5)
grid.fit(X, y)
print(grid.best_params_)

Random Search: Rastgele kombinasyonlar, daha hızlı genelde yeterli
from sklearn.model_selection import RandomizedSearchCV

Bayesian Optimization: Akıllı arama, önceki sonuçlara göre yönlendirir
Optuna, hyperopt kütüphaneleri

Pratik: Önce geniş aralıkta random search, sonra dar aralıkta grid search.
"""

# 58 - Imbalanced data nasıl ele alınır?
"""
CEVAP:
Sınıf dağılımı dengesiz olduğunda (%95 negatif, %5 pozitif gibi).

Resampling:
- Oversampling: Azınlık sınıfını çoğalt (SMOTE)
- Undersampling: Çoğunluk sınıfını azalt

from imblearn.over_sampling import SMOTE
smote = SMOTE()
X_resampled, y_resampled = smote.fit_resample(X, y)

Class Weight:
model = RandomForestClassifier(class_weight='balanced')

Threshold Adjustment:
Olasılık threshold'unu 0.5'ten farklı ayarla

Metrik Seçimi:
Accuracy yerine F1, AUC, Precision-Recall kullan
"""

# 59 - PCA (Principal Component Analysis) nedir?
"""
CEVAP:
Boyut indirgeme tekniği. Yüksek boyutlu veriyi daha az boyuta sıkıştırır.

Nasıl çalışır:
1. Veriyi standartlaştır
2. Kovaryans matrisini hesapla
3. Eigenvector ve eigenvalue bul
4. En büyük eigenvalue'lara sahip bileşenleri seç

from sklearn.decomposition import PCA
pca = PCA(n_components=2)
X_reduced = pca.fit_transform(X)

# Açıklanan varyans oranı
print(pca.explained_variance_ratio_)

Kullanım: Görselleştirme, noise reduction, feature extraction.
"""

# =============================================================================
# EK SQL SORULARI
# =============================================================================

# 60 - Subquery nedir?
"""
CEVAP:
Sorgu içinde sorgu. İç sorgu önce çalışır, sonucu dış sorguda kullanılır.

SELECT * FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees)

Correlated subquery: Her satır için tekrar çalışır
SELECT e1.name, e1.salary
FROM employees e1
WHERE salary > (SELECT AVG(salary) 
                FROM employees e2 
                WHERE e2.department = e1.department)

CTE (Common Table Expression) daha okunabilir alternatif:
WITH avg_salaries AS (
    SELECT department, AVG(salary) as avg_sal
    FROM employees GROUP BY department
)
SELECT * FROM employees e
JOIN avg_salaries a ON e.department = a.department
WHERE e.salary > a.avg_sal
"""

# 61 - Index nedir ve nasıl çalışır?
"""
CEVAP:
Veritabanında arama hızlandıran veri yapısı. Kitabın dizini gibi.

CREATE INDEX idx_name ON employees(name);

Avantaj: SELECT sorgularını hızlandırır
Dezavantaj: INSERT/UPDATE yavaşlar, ekstra disk alanı

Ne zaman kullanılır:
- Sık arama yapılan sütunlar
- WHERE, JOIN, ORDER BY'da kullanılan sütunlar
- Primary key ve foreign key (otomatik)

Ne zaman kullanılmaz:
- Çok sık güncellenen tablolar
- Az kayıt içeren tablolar
- Çok fazla NULL içeren sütunlar
"""

# 62 - CASE WHEN kullanımı?
"""
CEVAP:
SQL'de if-else mantığı sağlar.

SELECT name, salary,
       CASE 
           WHEN salary < 3000 THEN 'Düşük'
           WHEN salary < 7000 THEN 'Orta'
           ELSE 'Yüksek'
       END as salary_kategori
FROM employees

Pivot benzeri kullanım:
SELECT department,
       SUM(CASE WHEN gender = 'M' THEN 1 ELSE 0 END) as erkek,
       SUM(CASE WHEN gender = 'F' THEN 1 ELSE 0 END) as kadin
FROM employees
GROUP BY department
"""

# 63 - UNION vs UNION ALL farkı?
"""
CEVAP:
İki sorgu sonucunu birleştirir.

UNION: Tekrarları kaldırır (DISTINCT)
UNION ALL: Tekrarları korur, daha hızlı

SELECT name FROM employees
UNION
SELECT name FROM contractors

Kurallar:
- Sütun sayısı aynı olmalı
- Veri tipleri uyumlu olmalı
- İlk sorgunun sütun isimleri kullanılır

Performans için mümkünse UNION ALL tercih edilir.
"""

# =============================================================================
# EK CRM VE İŞ ANALİTİĞİ SORULARI
# =============================================================================

# 64 - Cohort analizi nedir?
"""
CEVAP:
Benzer özellikteki grupları zaman içinde karşılaştırma.

Örnek: İlk satın alma ayına göre müşteri grupları oluştur,
her grubun retention'ını aylık takip et.

Cohort matrisi:
          Ay1   Ay2   Ay3
Ocak      100%  60%   40%
Şubat     100%  55%   35%

Kullanım: Ürün güncellemelerinin etkisi, müşteri kalıcılığı,
farklı kampanyaların uzun vadeli etkisi.
"""

# 65 - Churn prediction nedir?
"""
CEVAP:
Müşterilerin hizmeti bırakma olasılığını tahmin etme.

Özellikler:
- Son aktivite tarihi
- Kullanım sıklığı değişimi
- Şikayet sayısı
- Sözleşme tipi

Model: Genellikle binary classification (Logistic Regression, XGBoost)
Metrik: Churn'ün maliyeti yüksek olduğu için Recall önemli

Aksiyon: Yüksek riskli müşterilere özel kampanya, indirim, iletişim.
"""

# 66 - A/B Testing nedir?
"""
CEVAP:
İki versiyonu karşılaştırarak hangisinin daha iyi olduğunu ölçme.

Adımlar:
1. Hipotez kur: "Yeni buton rengi dönüşümü artırır"
2. Kullanıcıları rastgele A ve B'ye ayır
3. Test süresince veri topla
4. İstatistiksel anlamlılık kontrol et

from scipy.stats import ttest_ind
stat, pvalue = ttest_ind(group_a, group_b)
if pvalue < 0.05:
    print("Anlamlı fark var")

Dikkat: Yeterli örneklem, tek değişken, sample ratio mismatch kontrolü.
"""

# =============================================================================
# EK NLP SORULARI
# =============================================================================

# 67 - Stemming ve Lemmatization farkı?
"""
CEVAP:
Kelimeleri kök formuna indirme teknikleri.

Stemming: Kurallara göre sonekleri keser, hızlı ama kaba
koşuyordum → koş
running → run

Lemmatization: Sözlük kullanır, anlamlı kök bulur, daha yavaş ama doğru
better → good (stemming bunu yapamaz)
are → be

from nltk.stem import PorterStemmer, WordNetLemmatizer

stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

Hız önemliyse stemming, doğruluk önemliyse lemmatization.
"""

# 68 - Named Entity Recognition (NER) nedir?
"""
CEVAP:
Metindeki özel varlıkları (isim, yer, tarih, kurum) tanıma.

import spacy
nlp = spacy.load("en_core_web_sm")
doc = nlp("Apple was founded by Steve Jobs in California")

for ent in doc.ents:
    print(ent.text, ent.label_)
# Apple - ORG
# Steve Jobs - PERSON
# California - GPE

Kullanım: Bilgi çıkarma, soru cevaplama, belge sınıflandırma.
"""

# 69 - Sentiment Analysis nasıl yapılır?
"""
CEVAP:
Metindeki duygu durumunu (pozitif/negatif/nötr) belirleme.

Yöntemler:
1. Kural tabanlı: Pozitif/negatif kelime listeleri
2. ML tabanlı: TF-IDF + Classifier
3. Deep Learning: BERT, Transformer modelleri

from transformers import pipeline
classifier = pipeline("sentiment-analysis")
result = classifier("Bu ürün harika!")
# [{'label': 'POSITIVE', 'score': 0.99}]

Kullanım: Müşteri yorumları, sosyal medya analizi, marka takibi.
"""

# 70 - Attention mekanizması nedir?
"""
CEVAP:
Modelin girdiğin farklı bölümlerine farklı önem vermesi.

Transformer mimarisinin temelidir. Self-attention: Her kelime diğer 
kelimelere ne kadar dikkat etmeli hesaplanır.

"The cat sat on the mat because it was tired"
it → cat'e yüksek attention (hangi 'it' olduğunu anlamak için)

Avantaj: Uzun mesafe bağımlılıklarını yakalar, paralel işlenir.
BERT, GPT, T5 gibi modellerin temelidir.
"""

# =============================================================================
# EK GENERATİF AI SORULARI
# =============================================================================

# 71 - LLM Hallucination nedir?
"""
CEVAP:
LLM'lerin gerçek olmayan bilgiyi gerçekmiş gibi üretmesi.

Örnekler:
- Olmayan kitaplara referans verme
- Yanlış tarihler söyleme
- Uydurma istatistikler

Azaltma yöntemleri:
- RAG kullanma (dış kaynak)
- Temperature düşürme
- Fact-checking prompts
- Fine-tuning with grounded data

"Emin değilsen bilmediğini söyle" gibi system prompt'lar yardımcı olur.
"""

# 72 - Vector Database nedir?
"""
CEVAP:
Yüksek boyutlu vektörler (embeddings) için optimize edilmiş veritabanı.

Kullanım: RAG sistemlerinde semantik arama
Örnekler: Pinecone, Weaviate, Milvus, ChromaDB

import chromadb
client = chromadb.Client()
collection = client.create_collection("docs")
collection.add(documents=["..."], ids=["id1"])
results = collection.query(query_texts=["soru"], n_results=5)

Normal DB: Exact match
Vector DB: Similarity search (cosine, euclidean)
"""

# 73 - LangChain nedir?
"""
CEVAP:
LLM uygulamaları geliştirmek için framework.

Bileşenler:
- Chains: İşlem akışları
- Agents: Araç kullanan otonom sistemler
- Memory: Konuşma geçmişi
- Retrievers: RAG için belge alma

from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

llm = ChatOpenAI()
prompt = PromptTemplate(template="Özet: {text}")
chain = LLMChain(llm=llm, prompt=prompt)
result = chain.run(text="uzun metin...")

RAG, chatbot, agent uygulamaları için standart haline geldi.
"""

# 74 - Embedding nedir?
"""
CEVAP:
Metin, görüntü gibi verileri sayısal vektörlere dönüştürme.

Benzer anlamlı şeyler yakın vektörlere sahip olur.

from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
embedding = model.encode("Merhaba dünya")
# 384 boyutlu vektör

Kullanım: Semantik arama, benzerlik hesaplama, clustering, RAG.
Popüler modeller: OpenAI embeddings, sentence-transformers, Cohere.
"""

# 75 - Token limiti ve context window nedir?
"""
CEVAP:
Token: LLM'in işlediği en küçük birim (kelime parçası)
"Merhaba" ≈ 2-3 token

Context Window: Modelin aynı anda işleyebildiği maksimum token
GPT-4: 128K tokens
Claude: 100K tokens

Sınırı aşınca:
- Eski mesajlar unutulur
- Truncation gerekir
- RAG ile sadece relevant parçalar alınır

Tiktoken kütüphanesi ile token sayısı hesaplanabilir.
"""

# =============================================================================
# EK NUMPY SORULARI
# =============================================================================

# 76 - NumPy array ile Python listesi arasında performans farkı nasıl ölçülür?
"""
CEVAP:
import numpy as np
import time

# Python listesi
liste = list(range(1000000))
start = time.time()
sonuc = [x * 2 for x in liste]
print(f"Liste: {time.time() - start:.4f}s")

# NumPy array
arr = np.arange(1000000)
start = time.time()
sonuc = arr * 2
print(f"NumPy: {time.time() - start:.4f}s")

NumPy genellikle 10-100 kat daha hızlı çıkar. Sebebi: vektörizasyon ve C kodu.
"""

# 77 - np.where nasıl kullanılır?
"""
CEVAP:
Koşullu seçim ve değer atama için kullanılır. if-else'in vektörel hali.

arr = np.array([1, 2, 3, 4, 5])

# Koşula göre değer atama
sonuc = np.where(arr > 3, 'büyük', 'küçük')
# ['küçük', 'küçük', 'küçük', 'büyük', 'büyük']

# Koşulu sağlayan indeksleri bulma
indeksler = np.where(arr > 3)
# (array([3, 4]),)

# Birden fazla koşul
sonuc = np.where((arr > 2) & (arr < 5), arr * 2, arr)
"""

# 78 - np.concatenate, np.vstack, np.hstack farkı nedir?
"""
CEVAP:
Hepsi array birleştirme için kullanılır ama farklı eksenler için.

a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])

# concatenate: Belirtilen eksende birleştirir
np.concatenate([a, b], axis=0)  # Alt alta
np.concatenate([a, b], axis=1)  # Yan yana

# vstack: Dikey birleştirme (axis=0)
np.vstack([a, b])
# [[1, 2], [3, 4], [5, 6], [7, 8]]

# hstack: Yatay birleştirme (axis=1)
np.hstack([a, b])
# [[1, 2, 5, 6], [3, 4, 7, 8]]

Pratik: 2D için vstack/hstack daha okunabilir.
"""

# 79 - NumPy'da random sayı üretimi nasıl yapılır?
"""
CEVAP:
import numpy as np

# Tekrarlanabilirlik için seed
np.random.seed(42)

# Uniform dağılım [0, 1)
np.random.rand(3, 3)

# Normal dağılım (mean=0, std=1)
np.random.randn(3, 3)

# Belirli aralıkta integer
np.random.randint(0, 10, size=(3, 3))

# Belirli aralıkta uniform
np.random.uniform(low=0, high=10, size=5)

# Normal dağılım (özel mean ve std)
np.random.normal(loc=50, scale=10, size=100)

# Array'i karıştırma
arr = np.arange(10)
np.random.shuffle(arr)

# Örnekleme
np.random.choice([1, 2, 3, 4, 5], size=3, replace=False)
"""

# 80 - np.apply_along_axis ne işe yarar?
"""
CEVAP:
Bir fonksiyonu array'in belirli ekseni boyunca uygular.

arr = np.array([[1, 2, 3],
                [4, 5, 6],
                [7, 8, 9]])

def my_func(x):
    return x[0] + x[-1]  # ilk ve son elemanı topla

# Sütunlar boyunca (axis=0)
np.apply_along_axis(my_func, 0, arr)
# [8, 10, 12]  (1+7, 2+8, 3+9)

# Satırlar boyunca (axis=1)
np.apply_along_axis(my_func, 1, arr)
# [4, 10, 16]  (1+3, 4+6, 7+9)

Not: Mümkünse vektörel işlemler tercih edilmeli, apply_along_axis yavaş.
"""

# 81 - NumPy'da maskeleme (boolean indexing) nasıl yapılır?
"""
CEVAP:
Boolean array ile filtreleme yapmak.

arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# Maske oluştur
maske = arr > 5
# [False, False, False, False, False, True, True, True, True, True]

# Maskeyi uygula
arr[maske]
# [6, 7, 8, 9, 10]

# Tek satırda
arr[arr > 5]

# Birden fazla koşul
arr[(arr > 3) & (arr < 8)]
# [4, 5, 6, 7]

# Değer değiştirme
arr[arr > 5] = 0
# [1, 2, 3, 4, 5, 0, 0, 0, 0, 0]
"""

# =============================================================================
# EK PANDAS SORULARI
# =============================================================================

# 82 - DataFrame'de memory kullanımını nasıl optimize edersiniz?
"""
CEVAP:
Büyük veri setlerinde bellek kritik.

# Mevcut bellek kullanımı
df.info(memory_usage='deep')
df.memory_usage(deep=True)

# Optimizasyon teknikleri:

# 1. Veri tiplerini küçült
df['col'] = df['col'].astype('int32')  # int64 yerine
df['col'] = df['col'].astype('float32')  # float64 yerine

# 2. Kategorik dönüşüm (tekrarlayan stringler için)
df['kategori'] = df['kategori'].astype('category')

# 3. Sparse array (çok sıfır içeren veriler için)
df['sparse_col'] = pd.arrays.SparseArray(df['col'])

# 4. Chunk'lar halinde okuma
for chunk in pd.read_csv('big_file.csv', chunksize=10000):
    process(chunk)

Kategorik dönüşüm %90'a varan bellek tasarrufu sağlayabilir.
"""

# 83 - Rolling ve Expanding window nedir?
"""
CEVAP:
Hareketli pencere hesaplamaları için kullanılır.

df = pd.DataFrame({'sales': [100, 120, 130, 110, 150, 140]})

# Rolling: Sabit pencere boyutu
df['rolling_mean'] = df['sales'].rolling(window=3).mean()
# NaN, NaN, 116.67, 120, 130, 133.33

# Expanding: Baştan itibaren büyüyen pencere
df['expanding_mean'] = df['sales'].expanding().mean()
# 100, 110, 116.67, 115, 122, 125

# Exponential weighted: Son değerlere daha fazla ağırlık
df['ewm_mean'] = df['sales'].ewm(span=3).mean()

Kullanım: Zaman serisi analizi, trend analizi, hareketli ortalamalar.
"""

# 84 - MultiIndex (hiyerarşik index) nasıl kullanılır?
"""
CEVAP:
Birden fazla seviyeli indeks oluşturma.

# MultiIndex oluşturma
arrays = [['A', 'A', 'B', 'B'], [1, 2, 1, 2]]
index = pd.MultiIndex.from_arrays(arrays, names=['letter', 'number'])
df = pd.DataFrame({'value': [10, 20, 30, 40]}, index=index)

# Erişim
df.loc['A']          # A harfine ait tüm satırlar
df.loc[('A', 1)]     # A harfi ve 1 numarası
df.xs(1, level='number')  # Tüm 1 numaralı satırlar

# Seviye değiştirme
df.swaplevel()
df.reorder_levels(['number', 'letter'])

# Flatten
df.reset_index()

GroupBy sonuçları genellikle MultiIndex döner.
"""

# 85 - Pandas'ta pipe() ne işe yarar?
"""
CEVAP:
Method chaining'i daha okunabilir hale getirir.

# Pipe olmadan
result = fonk3(fonk2(fonk1(df)))

# Pipe ile
result = (df
    .pipe(fonk1)
    .pipe(fonk2)
    .pipe(fonk3)
)

# Parametre ile
def filter_by_col(df, col, value):
    return df[df[col] > value]

result = (df
    .pipe(filter_by_col, 'age', 25)
    .pipe(lambda x: x.dropna())
    .groupby('category')
    .agg('mean')
)

Veri pipeline'ları için çok kullanışlı.
"""

# 86 - cut ve qcut farkı nedir?
"""
CEVAP:
Sürekli değişkenleri kategorilere ayırmak için kullanılır.

df['age'] = [22, 35, 58, 45, 29, 67, 31, 42]

# cut: Eşit aralıklı binler
df['age_group'] = pd.cut(df['age'], bins=3)
# Aralıklar eşit: (21, 37], (37, 52], (52, 67]

# qcut: Eşit frekanslı binler (quantile-based)
df['age_quartile'] = pd.qcut(df['age'], q=4)
# Her grupta eşit sayıda eleman

# Özel etiketler
pd.cut(df['age'], bins=[0, 18, 35, 50, 100], 
       labels=['Genç', 'Yetişkin', 'Orta Yaş', 'Yaşlı'])

cut: Aralıkların eşit olması önemliyse
qcut: Grup boyutlarının eşit olması önemliyse
"""

# 87 - assign() metodu nasıl kullanılır?
"""
CEVAP:
Yeni sütun eklerken method chaining yapmayı sağlar.

# Klasik yöntem
df['yeni_sutun'] = df['a'] + df['b']
df['baska_sutun'] = df['yeni_sutun'] * 2

# assign ile
df = (df
    .assign(yeni_sutun = lambda x: x['a'] + x['b'])
    .assign(baska_sutun = lambda x: x['yeni_sutun'] * 2)
)

# Tek assign'da birden fazla sütun
df = df.assign(
    toplam = df['a'] + df['b'],
    ortalama = (df['a'] + df['b']) / 2,
    is_positive = df['a'] > 0
)

Orijinal DataFrame'i değiştirmez, yeni DataFrame döner.
"""

# =============================================================================
# EK FEATURE ENGINEERING SORULARI
# =============================================================================

# 88 - Outlier (aykırı değer) tespiti nasıl yapılır?
"""
CEVAP:
Birkaç yöntem var:

# 1. IQR yöntemi
Q1 = df['col'].quantile(0.25)
Q3 = df['col'].quantile(0.75)
IQR = Q3 - Q1
lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR
outliers = df[(df['col'] < lower) | (df['col'] > upper)]

# 2. Z-score yöntemi
from scipy import stats
z_scores = np.abs(stats.zscore(df['col']))
outliers = df[z_scores > 3]

# 3. Isolation Forest (ML tabanlı)
from sklearn.ensemble import IsolationForest
iso = IsolationForest(contamination=0.1)
df['outlier'] = iso.fit_predict(df[['col']])

Ne yapılır: Silme, kırpma (clip), dönüştürme, ayrı modelleme.
"""

# 89 - Target Encoding nedir ve nasıl yapılır?
"""
CEVAP:
Kategorik değişkeni hedef değişkenin ortalamasıyla kodlama.

# Manuel yöntem
means = df.groupby('category')['target'].mean()
df['category_encoded'] = df['category'].map(means)

# category_encoders kütüphanesi ile
from category_encoders import TargetEncoder
encoder = TargetEncoder()
df['encoded'] = encoder.fit_transform(df['category'], df['target'])

Avantaj: One-hot'tan daha az boyut
Dezavantajı: Overfitting riski (özellikle küçük kategorilerde)

Çözüm: Cross-validation ile veya smoothing uygula.
"""

# 90 - Feature Selection yöntemleri nelerdir?
"""
CEVAP:
Önemli özellikleri seçip gereksizleri eleyerek model performansını artırma.

# 1. Filter Methods (istatistiksel)
from sklearn.feature_selection import SelectKBest, f_classif
selector = SelectKBest(f_classif, k=10)
X_selected = selector.fit_transform(X, y)

# 2. Wrapper Methods (model tabanlı)
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
rfe = RFE(LogisticRegression(), n_features_to_select=5)
X_selected = rfe.fit_transform(X, y)

# 3. Embedded Methods (model içinde)
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier()
model.fit(X, y)
importances = model.feature_importances_

# Korelasyon bazlı eleme
corr_matrix = df.corr()
# Yüksek korelasyonlu sütunları bul ve birini ele
"""

# 91 - Log ve Box-Cox dönüşümü ne zaman kullanılır?
"""
CEVAP:
Çarpık dağılımları normale yaklaştırmak için.

import numpy as np
from scipy import stats

# Log dönüşümü (sağa çarpık veriler için)
df['log_col'] = np.log1p(df['col'])  # log(1+x) sıfır sorununu çözer

# Square root dönüşümü
df['sqrt_col'] = np.sqrt(df['col'])

# Box-Cox dönüşümü (optimum lambda bulur)
from sklearn.preprocessing import PowerTransformer
pt = PowerTransformer(method='box-cox')  # sadece pozitif değerler
df['boxcox_col'] = pt.fit_transform(df[['col']])

# Yeo-Johnson (negatif değerler için de çalışır)
pt = PowerTransformer(method='yeo-johnson')

Ne zaman: Linear regression varsayımlarını sağlamak, outlier etkisini azaltmak.
"""

# 92 - Interaction features nasıl oluşturulur?
"""
CEVAP:
İki veya daha fazla özelliğin kombinasyonuyla yeni özellik oluşturma.

# Manuel
df['price_per_sqm'] = df['price'] / df['area']
df['age_income'] = df['age'] * df['income']

# Polynomial Features
from sklearn.preprocessing import PolynomialFeatures
poly = PolynomialFeatures(degree=2, interaction_only=True)
X_poly = poly.fit_transform(df[['age', 'income']])
# [1, age, income, age*income] sütunları oluşur

# interaction_only=True: Sadece çarpımlar (age² gibi terimler yok)
# interaction_only=False: Tüm kombinasyonlar

Domain knowledge önemli: Hangi etkileşimlerin anlamlı olduğunu bilmek gerekir.
"""

# 93 - Time-based features nasıl oluşturulur?
"""
CEVAP:
Tarih/saat değişkenlerinden anlamlı özellikler çıkarma.

df['date'] = pd.to_datetime(df['date'])

# Temel parçalar
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day'] = df['date'].dt.day
df['dayofweek'] = df['date'].dt.dayofweek  # 0=Pazartesi
df['hour'] = df['date'].dt.hour
df['quarter'] = df['date'].dt.quarter

# Türetilmiş özellikler
df['is_weekend'] = df['dayofweek'].isin([5, 6]).astype(int)
df['is_month_start'] = df['date'].dt.is_month_start.astype(int)
df['is_month_end'] = df['date'].dt.is_month_end.astype(int)

# Döngüsel encoding (sin/cos) - saat/gün için
df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)

# Lag features (zaman serisi için)
df['sales_lag1'] = df['sales'].shift(1)
df['sales_lag7'] = df['sales'].shift(7)
"""

# 94 - Label Encoding vs Ordinal Encoding farkı nedir?
"""
CEVAP:
Her ikisi de kategorileri sayılara dönüştürür ama farklı amaçlar için.

# Label Encoding: Rastgele sıra
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
df['encoded'] = le.fit_transform(df['color'])
# red=0, blue=1, green=2 (alfabetik sıra)

# Ordinal Encoding: Anlamlı sıra
from sklearn.preprocessing import OrdinalEncoder
oe = OrdinalEncoder(categories=[['low', 'medium', 'high']])
df['encoded'] = oe.fit_transform(df[['priority']])
# low=0, medium=1, high=2 (mantıksal sıra)

Label Encoding: Hedef değişken için veya tree-based modeller
Ordinal Encoding: Doğal sıralaması olan kategoriler (eğitim seviyesi gibi)

Dikkat: Linear modellerde label encoding sıralama anlamı katar, sorun olabilir.
"""

# =============================================================================
# EK MACHINE LEARNING SORULARI
# =============================================================================

# 95 - SVM (Support Vector Machine) nasıl çalışır?
"""
CEVAP:
Sınıfları ayıran en iyi hyperplane'i bulmaya çalışır.

Temel konseptler:
- Hyperplane: Sınıfları ayıran karar sınırı
- Support Vectors: Hyperplane'e en yakın noktalar
- Margin: Hyperplane ile support vector'ler arası mesafe

Amaç: Margin'i maksimize etmek

# Linear SVM
from sklearn.svm import SVC
svm = SVC(kernel='linear')

# Non-linear: Kernel trick
svm_rbf = SVC(kernel='rbf')  # Radial Basis Function
svm_poly = SVC(kernel='poly', degree=3)

Kernel trick: Veriyi yüksek boyuta taşımadan non-linear sınırlar çizer

Avantaj: Yüksek boyutlu veride iyi, outlier'a dayanıklı
Dezavantaj: Büyük veri setlerinde yavaş, parametre hassasiyeti
"""

# 96 - Gradient Descent nasıl çalışır?
"""
CEVAP:
Optimizasyon algoritması. Loss fonksiyonunu minimize etmek için parametreleri günceller.

Mantık:
1. Rastgele parametrelerle başla
2. Loss'un gradyanını (türevini) hesapla
3. Parametreleri gradyanın tersi yönünde güncelle
4. Convergence'a kadar tekrarla

w = w - learning_rate * gradient

Türleri:
- Batch GD: Tüm veriyle güncelleme (yavaş ama stabil)
- Stochastic GD: Tek örnekle güncelleme (hızlı ama gürültülü)
- Mini-batch GD: Küçük gruplarla güncelleme (dengeli)

Learning rate önemi:
- Çok büyük: Diverge eder, optimal'i atlar
- Çok küçük: Çok yavaş converge eder, local minima riski

Adam, RMSprop gibi adaptive yöntemler learning rate'i otomatik ayarlar.
"""

# 97 - Model interpretability (yorumlanabilirlik) nasıl sağlanır?
"""
CEVAP:
Black-box modelleri anlamak için teknikler.

# 1. Feature Importance (tree-based modeller)
model.feature_importances_

# 2. Permutation Importance
from sklearn.inspection import permutation_importance
result = permutation_importance(model, X_test, y_test)

# 3. SHAP (SHapley Additive exPlanations)
import shap
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)
shap.summary_plot(shap_values, X_test)

# 4. LIME (Local Interpretable Model-agnostic Explanations)
from lime import lime_tabular
explainer = lime_tabular.LimeTabularExplainer(X_train)
exp = explainer.explain_instance(X_test[0], model.predict_proba)

# 5. Partial Dependence Plots
from sklearn.inspection import PartialDependenceDisplay
PartialDependenceDisplay.from_estimator(model, X, ['feature1'])

SHAP global ve local, LIME sadece local açıklama verir.
"""

# 98 - Naive Bayes nasıl çalışır?
"""
CEVAP:
Bayes teoremini kullanarak sınıflandırma yapar.

P(y|X) = P(X|y) * P(y) / P(X)

"Naive" çünkü özelliklerin bağımsız olduğunu varsayar.

Türleri:
- GaussianNB: Sürekli veriler için (normal dağılım varsayar)
- MultinomialNB: Sayım verileri için (metin sınıflandırma)
- BernoulliNB: Binary özellikler için

from sklearn.naive_bayes import GaussianNB
model = GaussianNB()
model.fit(X_train, y_train)

Avantajları:
- Çok hızlı eğitim
- Az veriyle bile çalışır
- Metin sınıflandırmada çok iyi

Dezavantajları:
- Bağımsızlık varsayımı gerçekçi değil
- Sürekli verilerde dağılım varsayımı
"""

# 99 - K-Means nasıl çalışır?
"""
CEVAP:
Unsupervised kümeleme algoritması.

Adımlar:
1. K tane rastgele centroid seç
2. Her noktayı en yakın centroid'e ata
3. Centroid'leri cluster ortalamasına taşı
4. Değişim olmayana kadar tekrarla

from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=3, random_state=42)
labels = kmeans.fit_predict(X)

# Optimal K bulma (Elbow method)
inertias = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(X)
    inertias.append(kmeans.inertia_)
plt.plot(range(1, 11), inertias, 'bo-')

Dezavantajlar:
- K'yı önceden bilmek gerek
- Küresel olmayan şekillerde başarısız
- Outlier'a hassas
- Farklı başlangıçlarda farklı sonuç (n_init kullan)
"""

# 100 - Cross-validation stratejileri nelerdir?
"""
CEVAP:
Model değerlendirme için farklı CV stratejileri.

# 1. K-Fold CV
from sklearn.model_selection import KFold
kf = KFold(n_splits=5, shuffle=True, random_state=42)

# 2. Stratified K-Fold (sınıf dengesini korur)
from sklearn.model_selection import StratifiedKFold
skf = StratifiedKFold(n_splits=5)

# 3. Leave-One-Out (çok küçük veri setleri için)
from sklearn.model_selection import LeaveOneOut
loo = LeaveOneOut()

# 4. Time Series Split (zaman serisi için)
from sklearn.model_selection import TimeSeriesSplit
tscv = TimeSeriesSplit(n_splits=5)

# 5. Group K-Fold (aynı grubun train-test'e dağılmaması için)
from sklearn.model_selection import GroupKFold
gkf = GroupKFold(n_splits=5)

# Kullanım
from sklearn.model_selection import cross_val_score
scores = cross_val_score(model, X, y, cv=skf)

Zaman serisi için asla normal K-Fold kullanma - veri sızıntısı olur.
"""

# 101 - Train-Test-Validation split neden önemli?
"""
CEVAP:
Üç ayrı setten her birinin farklı amacı var:

Train (%60-70): Model eğitimi
Validation (%15-20): Hyperparameter tuning, model seçimi
Test (%15-20): Final değerlendirme, tek seferlik kullanım

from sklearn.model_selection import train_test_split

# İlk split: Train + Validation vs Test
X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=0.2)

# İkinci split: Train vs Validation
X_train, X_val, y_train, y_val = train_test_split(X_temp, y_temp, test_size=0.25)

Neden validation: Test seti birden fazla kullanılırsa overfitting olur.
Hyperparameter tuning sırasında validation kullan, test'e asla bakma.

Cross-validation validation set ihtiyacını azaltır ama final test hala gerekli.
"""

# 102 - Data Leakage nedir ve nasıl önlenir?
"""
CEVAP:
Eğitim sırasında modelin test verisinden bilgi sızması.

Yaygın nedenler:
1. Preprocessing'i tüm veriye uygulamak
   Yanlış: scaler.fit_transform(X) sonra split
   Doğru: Split sonra train'de fit, test'te sadece transform

2. Future data kullanmak (zaman serisi)
   Yanlış: Gelecek tarihin ortalamasını feature olarak kullanmak

3. Target'tan türetilmiş feature
   Yanlış: target_mean gibi aggregate feature'lar

Önleme:
# Pipeline kullan
from sklearn.pipeline import Pipeline
pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('model', LogisticRegression())
])
pipe.fit(X_train, y_train)  # scaler sadece train'den öğrenir
pipe.score(X_test, y_test)

# Cross-validation doğru kullan
cross_val_score(pipe, X, y, cv=5)  # her fold'da ayrı fit
"""

