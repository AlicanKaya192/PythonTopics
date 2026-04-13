##################################################
# Smoothing Methods (Holt-Winters) 
# Düzeltme Yöntemleri (Zaman Serilerinde Gürültüyü Azaltma)
##################################################
#
# Bir zaman serisinde (Time Series) trend, mevsimsellik ve kalıntı (gürültü) 
# bileşenlerinin birbirine etkisini yumuşatıp öngörü yeteneğimizi artırmak için 
# Üstel Düzeltme (Exponential Smoothing) gibi yöntemlere başvururuz.
# Bu dosyada üç önemli yöntemi uygulayacağız:
# 1. Single Exponential Smoothing (SES) - Sadece Durağan serilerde yatay (Level) etkiyi yakalar.
# 2. Double Exponential Smoothing (DES) - Yatay etki + Trend (eğim) etkisini yakalar.
# 3. Triple Exponential Smoothing (TES) - Yatay etki + Trend + Mevsimselliği (Seasonality) aynı anda yakalar. Holt-Winters olarak da bilinir.

import itertools  # Hiperparametre kombinasyonlarını oluşturmak için kullanılacak iterasyon modülü.
import warnings   # Konsoldaki uyarıları görmezden gelmek için eklendi.
import matplotlib.pyplot as plt  # Veriyi ve tahminleri grafiğe dökmek (görselleştirme) için kullanılır.
import numpy as np  # Matematiksel ve matris operasyonları için güçlü bir kütüphane.
import pandas as pd # Veri manipülasyonu, tablo (dataframe) işlemleri için Pandas kütüphanesi şart.
import statsmodels.api as sm  # İstatistiksel modellerin bulunduğu gelişmiş kütüphanedir. Veri seti de buradan çekilecek.
from sklearn.metrics import mean_absolute_error  # Modelin hata payını ölçmek için kullanacağımız bir metrik (Ortalama Mutlak Hata).
from statsmodels.tsa.holtwinters import ExponentialSmoothing # Çift (DES) ve Üçlü (TES) üstel düzeltme modelleri için çağrıldı.
from statsmodels.tsa.holtwinters import SimpleExpSmoothing   # Sadece Tek (SES) üstel düzeltme hesaplamaları için çağrıldı.
from statsmodels.tsa.seasonal import seasonal_decompose      # Zaman serisi verisini Trend, Mevsimsellik, Kalıntı şeklinde parçalamak için kullanılır.
import statsmodels.tsa.api as smt # Zaman serisi modülü.

# Kod çıktısındaki gereksiz uyarı mesajlarını (deprecation warning vs.) ekrandan gizler, temiz bir görüntü sağlar.
warnings.filterwarnings('ignore')


############################
# Veri Seti (Dataset)
############################

# Atmospheric CO2 from Continuous Air Samples at Mauna Loa Observatory, Hawaii, U.S.A.
# Period of Record: March 1958 - December 2001 (Kayıtlı olunan süreç referansı)
# Veride Hawaii'de ölçülen atmosferik Karbondioksit (CO2) miktarı aylık döngüyle yer almaktadır.

data = sm.datasets.co2.load_pandas() # Kütüphane içerisinde hazır duran CO2 zaman serisi verisi indirilir.
y = data.data # Data objesinden yalnızca asıl veri kısmını sıyırıp alıyoruz, 'y' isminde muhafaza ediyoruz.

# 'resample' ile veriyi aylık başlangıç noktasına ('MS' -> Month Start) göre gruplayıp ortalamalarını alıyoruz.
# Çünkü orijinal veride günler vs olabilir, analiz boyunca aylık bir periyotla çalışıyoruz.
y = y['co2'].resample('MS').mean()

# Zaman serisi analizinde boş veriler (NaN) analizi patlatır. Kaç tane boş değer var kontrol ediyoruz.
y.isnull().sum()

# Eksik verileri doldurmak için "bfill" (backward fill) yöntemini seçiyoruz. 
# Bu metot şunu der: "Eğer burası boşsa, bir sonraki dolu değeri al ve burayı doldur."
y = y.fillna(y.bfill())

# Her şey hazır, şimdi verimiz nasıl bir yapıya (trend var mı vs.) sahip görmek için çizdiriyoruz.
y.plot(figsize=(15, 6))
plt.show() # Grafiği ekrana bas.


############################
# Holdout (Veriyi Eğitim ve Test Olarak İkiye Ayırma)
############################
# Modelimizin ezberlemeyip gerçekten öğrendiğinden nasıl emin oluruz?
# Tabii ki görmediği veriler sayesinde! Serinin bir parçasını eğitim (train), geri kalanını test için bölelim.

train = y[:'1997-12-01'] # 1998'den önceki tüm eski veriler modeli eğitmek için ayrıldı.
len(train)  # 478 ay eğitim kümemizin uzunluğu.

# 1998'ilk ayından 2001'in sonuna kadar (seri sonu) olan son periyodu da modeli sınamak için Test set olarak aldık.
test = y['1998-01-01':]
len(test)  # 48 ay, tahminde kıyaslayacağımız süremiz.

##################################################
# Zaman Serisi Yapısal Analizi (Structural Analysis)
##################################################

# Durağanlık Testi (Dickey-Fuller Testi)
# Bir serinin durağan olması demek; istatistiksel özellikleri (ortalaması, varyansı vs) zaman içinde değişmiyor anlamına gelir.

def is_stationary(y):

    # "HO: Non-stationary" -> Dickey-Fuller testinin Hipotez 0'ı derki: Seri DURAĞAN DEĞİLDİR.
    # "H1: Stationary" -> Hipotez 1: Hayır, seri DURAĞANDIR.

    # adfuller metodu Dickey-Fuller testini yapar ve sonuçlar listesi döner. Bize [1]. indeksli yerdeki 'p-value' lazımdır.
    p_value = sm.tsa.stattools.adfuller(y)[1] 
    
    # p-value < 0.05 ise H0 hipotezini reddederiz ve "Durağandır" sonucuna ulaşırız. Değilse reddedemeyiz.
    if p_value < 0.05:
        print(F"Result: Stationary (H0: non-stationary, p-value: {round(p_value, 3)})")
    else:
        print(F"Result: Non-Stationary (H0: non-stationary, p-value: {round(p_value, 3)})")

is_stationary(y) # CO2 verimiz muhtemelen durağan değil (yukarı doğru agresif trendi olduğundan) çıkar.

# Zaman Serisi Bileşenleri ve Durağanlık Testi (Decompose işlemi)
# Serimizin iç dünyasına inip 'Trend', 'Mevsimsellik' ve elde kalan 'Artık (Residual)' kısımlarını grafikte bölüyoruz.
def ts_decompose(y, model="additive", stationary=False):
    # 'seasonal_decompose' ile yukarıda saydığım bölümleri ayırıyoruz. (additive = Toplamsal model bazında)
    result = seasonal_decompose(y, model=model)
    fig, axes = plt.subplots(4, 1, sharex=True, sharey=False) # Alt alta 4 adet satırlık görsel paneli açarız.
    fig.set_figheight(10) # Figür yüksekliği vs. boyutları ayarlanır.
    fig.set_figwidth(15)

    # 1. Eksen (Axes 0): Serinin Orjinal Halini Çiz:
    axes[0].set_title("Decomposition for " + model + " model")
    axes[0].plot(y, 'k', label='Original ' + model)
    axes[0].legend(loc='upper left')

    # 2. Eksen (Axes 1): Seriden çıkarılan saf Yöneliş (Trend) Çizilir:
    axes[1].plot(result.trend, label='Trend')
    axes[1].legend(loc='upper left')

    # 3. Eksen (Axes 2): Seride bulunan döngüsel paternler, mevsimsellik izleri çizilir.
    axes[2].plot(result.seasonal, 'g', label='Seasonality & Mean: ' + str(round(result.seasonal.mean(), 4)))
    axes[2].legend(loc='upper left')

    # 4. Eksen (Axes 3): Ne trend ile ne mevsimsellik ile açıklanamayan, seride hata oranını veren Kalan Tortu. (Noise)
    axes[3].plot(result.resid, 'r', label='Residuals & Mean: ' + str(round(result.resid.mean(), 4)))
    axes[3].legend(loc='upper left')
    plt.show(block=True) 

    # Fonksiyon çağrıldığında parametre olarak stationary=True gelmişse durağanlık testi çalışıp çıktı verir.
    if stationary:
        is_stationary(y)

ts_decompose(y, stationary=True) # Analizi gerçekleştirip grafikleri kontrol ediyoruz.


##################################################
# Single Exponential Smoothing (SES - Tekil Üstel Düzeltme)
##################################################

# SES Yalnızca Seviyeyi (Level) algılar. Trend veya mevsimsellik varsa bu model başarısız olur çünkü onları anlayamaz!

ses_model = SimpleExpSmoothing(train).fit(smoothing_level=0.5) # Train verisine SES modelini kuruyoruz. smoothing_level dediğimiz alfa ağırlığıdır. (Yani geçmiş ağırlığa %50 önem ver).

y_pred = ses_model.forecast(48) # Gelecek 48 periyot (yani testimizin uzunluğu kadar ay) için SES'e öngörü yaptırıyoruz.

mean_absolute_error(test, y_pred) # Elde edilen tahminlerle test seti arasındeki hata puanına (MAE) bakıyoruz.

# Çıkanları gözlemlemek için grafiği yazalım:
train.plot(title="Single Exponential Smoothing")
test.plot()
y_pred.plot()
plt.show()

# Grafikteki bozulma 1985'ten dolayıysa sadece 1985'ten sonrasını yakınlaştırmak için bu hücredeki gibi plot edilebiliriz.
train["1985":].plot(title="Single Exponential Smoothing")
test.plot()
y_pred.plot()
plt.show()

# Tahminleri ve Test Verilerini Görselliğe dönüştüren yardımcı kolay bir fonksiyon yazıyoruz. 
# Bu sayede her seferinde uzun uzun 5-6 satır çizim koduna maruz kalmayacağız.
def plot_co2(train, test, y_pred, title):
    mae = mean_absolute_error(test, y_pred)
    train["1985":].plot(legend=True, label="TRAIN", title=f"{title}, MAE: {round(mae,2)}")
    test.plot(legend=True, label="TEST", figsize=(6, 4))
    y_pred.plot(legend=True, label="PREDICTION")
    plt.show()

plot_co2(train, test, y_pred, "Single Exponential Smoothing") # Test edelim, gayet güzel yansıtıyor.

ses_model.params # Model içerisine yerleşen istatistiksel sabitleri/parametre parametre sözlüğünü inceleyebilmek için.

############################
# Hyperparameter Optimization (Hiperparametre Optimizasyonu) 
############################
# Biz elle smoothing_level=0.5 seçmiştik ancak belki en optimum hata payını 0.7 sağlayacak? 
# Bunu anlamak adına modelin bir optimizasyon döngüsünden geçerek farklı olasılıkları test etmesi gerekir.

def ses_optimizer(train, alphas, step=48):
    # Başlangıçta en iyi alfa değerini boş ve hata payını sonsuz (çok büyük ulaşılamaz bir limit) bırakıyoruz.
    best_alpha, best_mae = None, float("inf")

    # Gelebilecek tüm olası alfalar (parametreler) içinde deneme yapacağız.
    for alpha in alphas:
        # Seçilen alfanın seviyesiyle modeli eğit ve tahmin oluştur:
        ses_model = SimpleExpSmoothing(train).fit(smoothing_level=alpha)
        y_pred = ses_model.forecast(step)
        mae = mean_absolute_error(test, y_pred) # MAE (Hatayı) ölç!

        # Eğer bulduğum hata miktarı (mae), bir önceki test ettiğim en iyi hatadan daha küçükse (daha iyiyse), yeni en iyi budur:
        if mae < best_mae:
            best_alpha, best_mae = alpha, mae

        print("alpha:", round(alpha, 2), "mae:", round(mae, 4)) # Test sonuçlarını her alfa için loga bas.
    
    print("best_alpha:", round(best_alpha, 2), "best_mae:", round(best_mae, 4))
    return best_alpha, best_mae # Gün sonunda elimizde en temiz, en düşük hatalı model hiperparametreleri kaldı.

alphas = np.arange(0.8, 1, 0.01) # Optimize edilmesi için modele göndereceğimiz farklı ihtimalli alfalar (0.8'den 1'e kadar 0.01 giden oranlarda)

# yt_sapka = a * yt-1 + (1-a)* (yt_-1)_sapka 
# (Üstel düzeltmenin ana felsefesi: Gelecek = alfa * şu anki değer + (1-alfa) * eski tahminimiz)

ses_optimizer(train, alphas) # Algoritmayı koştur.

best_alpha, best_mae = ses_optimizer(train, alphas) # En iyi çıkanı al.

############################
# Final SES Model (Bulunan En İyi Parametre İle Modeli Kalıcı Olarak Kurma)
############################

# Hata oranı en tatmin edici olan best_alpha değeri gelince, modeli son defa fit ediyoruz.
ses_model = SimpleExpSmoothing(train).fit(smoothing_level=best_alpha)
y_pred = ses_model.forecast(48) # 48 adet ileri tahmin

plot_co2(train, test, y_pred, "Single Exponential Smoothing") # En iyi parametreli görselleştirmemizi sunuyoruz.


##################################################
# Double Exponential Smoothing (DES - Çift Üstel Düzeltme)
##################################################

# DES: Level (SES) + Trend 
# (Artık sadece seviye yetmez, bu model veride "yükseliş" veya "düşüş" trendini de öğrenebilir hale geliyor)

# y(t) = Level + Trend + Seasonality + Noise     (Toplamsal Model (add))
# y(t) = Level * Trend * Seasonality * Noise     (Çarpımsal Model (mul))
# Toplamsal demek bu 4 etkinin birbirine eklenerek seriyi oluşturması. Eğer trend mevsimsellikle çığ gibi katlanarak artıyorsa Çarpımsaldır. (Biz toplamsaldan gidiyoruz)

ts_decompose(y) # Nasıl göründüğüne referans hatırlatması.

# 'ExponentialSmoothing' kullanırken trendin yapısını (additive vs. multiplicative) söylemeliyiz. Trend='add' dedik.
# Alpha (smoothing_level) seviyeyi kontrol ederken, Beta (smoothing_trend) ise Trendin ağırlığını kontrol ediyor!
des_model = ExponentialSmoothing(train, trend="add").fit(smoothing_level=0.5,
                                                         smoothing_trend=0.5)

y_pred = des_model.forecast(48) # Yine 48 aylık ileri tahminimiz.

plot_co2(train, test, y_pred, "Double Exponential Smoothing") # Trendi anladığı için sonuç SES'e göre daha yukarı eğilimli akılcı bir sonuç verecektir!

############################
# Hyperparameter Optimization (Çift Parametre İçin Optimizasyon: Alpha ve Beta)
############################
# Az önceki gibi, 0.5 tahmini girmek yerine makineye tüm kombinasyonları deneteceğiz!

def des_optimizer(train, alphas, betas, step=48):
    best_alpha, best_beta, best_mae = None, None, float("inf") # Bu sefer kaydetmek istediğimiz 3 değişkenimiz var (beta dahil).
    
    for alpha in alphas:    # Dış döngü Alpha ağırlıklarını gezer.
        for beta in betas:  # İç döngü ise Beta ağırlıklarını gezer (Böylece her ikisi için olası tüm ikili eşleşmeler denenmiş olur)
            des_model = ExponentialSmoothing(train, trend="add").fit(smoothing_level=alpha, smoothing_slope=beta) # Modeli eğit! (smoothing_slope veya smoothing_trend)
            y_pred = des_model.forecast(step) # Adım sayısı kadar tahminle
            mae = mean_absolute_error(test, y_pred) # Hatanın mutlak değerini ölç.
            
            if mae < best_mae: # En iyi hatayı geçtiyse, best_ değişkenlerini güncelle...
                best_alpha, best_beta, best_mae = alpha, beta, mae
            print("alpha:", round(alpha, 2), "beta:", round(beta, 2), "mae:", round(mae, 4))
    
    print("best_alpha:", round(best_alpha, 2), "best_beta:", round(best_beta, 2), "best_mae:", round(best_mae, 4))
    return best_alpha, best_beta, best_mae

alphas = np.arange(0.01, 1, 0.10) # 0.01 ile 1 arasındaki 0.1 adımlı Alpha liste aralığı.
betas = np.arange(0.01, 1, 0.10)  # Aynı şekilde Trend kontrolcümüz Beta için olan liste ağırlıkları.

# Fonksiyonla en temiz eşleşme neymiş test edip kaydediyoruz.
best_alpha, best_beta, best_mae = des_optimizer(train, alphas, betas)


############################
# Final DES Model (Sonuç Modeli)
############################

# Ve nihayetinde optimizasyondan kopup gelen mükemmel ikilimizle asıl DES (Çift Düzeltme) metodunu eğiterek kullanıyoruz.
final_des_model = ExponentialSmoothing(train, trend="add").fit(smoothing_level=best_alpha,
                                                               smoothing_slope=best_beta) # Veya smoothing_trend de yazılabilir

y_pred = final_des_model.forecast(48)

plot_co2(train, test, y_pred, "Double Exponential Smoothing")


##################################################
# Triple Exponential Smoothing (TES - Üçlü Üstel Düzeltme / Holt-Winters)
##################################################

# TES = SES (Level) + DES (Trend) + Mevsimsellik (Seasonality)
# Seriyi adeta bütün dinamikleriyle söküp kavrayan Holt-Winters! Eğer Seride yıllara yayılan dalgalanmalar veya aylar bazında şekillenmeler varsa TEK İHTİYACINIZ T.E.S!


tes_model = ExponentialSmoothing(train,
                                 trend="add",     # Trend etkisini toplamsal baz al! 
                                 seasonal="add",  # Mevsimselliği de toplamsal baz al! (İhtiyaca göre 'mul' - multiplicative yapılabilir).
                                 seasonal_periods=12).fit(smoothing_level=0.5,     # Level için ALPHA ağırlığı
                                                          smoothing_slope=0.5,     # Trend için BETA ağırlığı
                                                          smoothing_seasonal=0.5)  # Mevsimsellik için GAMMA ağırlığı!

y_pred = tes_model.forecast(48) # Holt Winters modelimizle 48 periyot tahmini çek!
plot_co2(train, test, y_pred, "Triple Exponential Smoothing") # Baktığınızda grafik artık mevsimsellik zikzaklarını da çizebildiği için çok daha gerçekçi.

############################
# Hyperparameter Optimization (Alfayı, Betayı ve Gammayı Optimize Etme)
############################

alphas = betas = gammas = np.arange(0.20, 1, 0.10) # 3 katsayıyı da aynı potada listelerde barındır.

# itertools.product bu 3 listeyi alıp bütün o kombinasyon kombinasyon olası çarpım ve eşleşmelerin paketini yaratacak.
abg = list(itertools.product(alphas, betas, gammas))


def tes_optimizer(train, abg, step=48):
    # Bu sefer 4 parametre tutuyoruz: Alpha (Seviye), Beta (Trend), Gamma (Mevsimsellik) ve MAE (Bu kurgudaki çıkan hatamız)
    best_alpha, best_beta, best_gamma, best_mae = None, None, None, float("inf")
    
    # Tüm liste ihtimallerini 'comb' değişkeni aracılığıyla tek tek test döngüsüne sokuyoruz.
    for comb in abg: 
        tes_model = ExponentialSmoothing(train, trend="add", seasonal="add", seasonal_periods=12).\
            fit(smoothing_level=comb[0], smoothing_slope=comb[1], smoothing_seasonal=comb[2]) # comb[0] = alpha, comb[1] = beta, comb[2] = gamma
        y_pred = tes_model.forecast(step)
        mae = mean_absolute_error(test, y_pred)
        
        # Eğer yepyeni düşük bir MAE yakaladıysak rekoru güncelle:
        if mae < best_mae:
            best_alpha, best_beta, best_gamma, best_mae = comb[0], comb[1], comb[2], mae
        print([round(comb[0], 2), round(comb[1], 2), round(comb[2], 2), round(mae, 2)])

    print("best_alpha:", round(best_alpha, 2), "best_beta:", round(best_beta, 2), "best_gamma:", round(best_gamma, 2),
          "best_mae:", round(best_mae, 4))

    return best_alpha, best_beta, best_gamma, best_mae

best_alpha, best_beta, best_gamma, best_mae = tes_optimizer(train, abg) # Optimizasyon başlatıldı ve optimum (alfa, beta, gamma) çekildi!


############################
# Final TES Model (Holt-Winters Son Karar)
############################

# Üst düzey makine öğrenmesi algısında optimize ettiğimiz hiperparametrelerimizle modelimizi ebedi ikametgahına alıyoruz:
final_tes_model = ExponentialSmoothing(train, trend="add", seasonal="add", seasonal_periods=12).\
            fit(smoothing_level=best_alpha, smoothing_trend=best_beta, smoothing_seasonal=best_gamma)

# Son bir kez tahminde bulunuyoruz...
y_pred = final_tes_model.forecast(48)

# Tahmini ve test edilecek olan doğruluk oranlarını sunuyoruz! Çok güzel örtüştüğünü göreceksiniz.
plot_co2(train, test, y_pred, "Triple Exponential Smoothing")

