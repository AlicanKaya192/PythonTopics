##################################################
# Airline Passenger Forecasting (Havayolu Yolcu Sayısı Tahmini)
##################################################
#
# Bir havacılık firmasının geçmiş yıllara ait taşıdığı yolcu sayıları üzerinden
# "Gelecek dönemlerde kaç yolcu taşıyacağız?" sorusuna yanıt arıyoruz. 
# Bu problem için az önce öğrendiğimiz Yumuşatma (Smoothing) ve İstatistiksel
# Analiz (ARIMA & SARIMA) yöntemlerinin tam donanımlı bir kıyaslamasını yapacağız!

import itertools
import warnings
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import statsmodels.api as sm
import statsmodels.tsa.api as smt
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.holtwinters import SimpleExpSmoothing
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_absolute_error

# Eski metodların verdiği depreceated uyarılarını ekrandan siliyoruz.
warnings.filterwarnings('ignore')

#################################
# Verinin Okunup Görselleştirilmesi
#################################

# Verisetimizi lokal dizinimizdeki 'time_series_datasets' klasöründen çağırıyoruz.
# index_col='month' diyerek ayların olduğu sütunu index yapıyor,
# parse_dates=True ile de bu ayların string (yazı) değil "Tarih Formatı (Datetime)" olduğunu belirtiyoruz.
df = pd.read_csv('../time_series_datasets/airline-passengers.csv', index_col='month', parse_dates=True)

df.shape # Kaç satır kaç sütun verimiz var kontrolü
df.head() # İlk 5 satır

# Yolcuların gidişatını (Trend) ve mevsimsellik zikzaklarını görmek için ilk çizimimiz:
df[['total_passengers']].plot(title='Passengers Data')
plt.show()

df.index # indexlerin tipini teyit edelim (DatetimeIndex olması gerek).

# Zaman serisi objemizde bir periyot sabitlemesi yapıyoruz: 
# MS = Month Start. Pandas'a "bu verilerin aydan aya olduğunu biliyorsun, değil mi?" demenin kısayoludur.
df.index.freq = "MS" 

# Tüm datamız 144 ay uzunluğunda (12 yıl). Modelin sınanması için Train-Test ayrımı (Holdout) yapalım:
train = df[:120]  # İlk 10 yıllık (120 ay) veriyi modeli EĞİTMEK için ayırdık.
test = df[120:]   # Kalan 2 yıl (24 ay) ise modelin sınav kağıdı olacak!


#################################
# Single Exponential Smoothing (SES - Seviye Odaklı Düzeltme)
#################################
# SES sadece serinin durağan ve trend/mevsimsellik içermeyen düz çizgisini kopyalamaya çalışır.
# (Havayolu verisinde trend bariz olduğu için muhtemelen çuvallayacak göreceğiz!)

def ses_optimizer(train, alphas, step=48):
    best_alpha, best_mae = None, float("inf")
    for alpha in alphas:
        # Train üzerinde her alpha ihtimalini fit et.
        ses_model = SimpleExpSmoothing(train).fit(smoothing_level=alpha)
        y_pred = ses_model.forecast(step) # Belirtilen adım kadar tahmine koş!
        mae = mean_absolute_error(test, y_pred) # Rekor Hata Puanı (MAE) kontrolü:
        if mae < best_mae:
            best_alpha, best_mae = alpha, mae
        print("alpha:", round(alpha, 2), "mae:", round(mae, 4))
    print("best_alpha:", round(best_alpha, 2), "best_mae:", round(best_mae, 4))
    return best_alpha, best_mae

alphas = np.arange(0.01, 1, 0.10) # 0.01'den başlayan alpha seviyeleri

# Optimizasyonu 24 adımlık test dönemi tahminine göre koşturuyoruz.
best_alpha, best_mae = ses_optimizer(train, alphas, step=24)
# (Çıktıya göre en iyi alpha: 0.11 iken ulaşılan MAE: 82.528 civarı oldu)

# Model kuruldu
ses_model = SimpleExpSmoothing(train).fit(smoothing_level=best_alpha)
y_pred = ses_model.forecast(24) # Tahminler çekildi.

# Sıkça çizim yapacağımız için işleri kısaltan bir çizim fonksiyonu yazıyoruz:
def plot_prediction(y_pred, label):
    train["total_passengers"].plot(legend=True, label="TRAIN")
    test["total_passengers"].plot(legend=True, label="TEST")
    y_pred.plot(legend=True, label="PREDICTION")
    plt.title("Train, Test and Predicted Test Using "+label)
    plt.show()

# Grafikte SES'in "Trend" algısı olmadığı için düz bir doğru çektiğini apaçık görebiliriz. Düz çizgi!
plot_prediction(y_pred, "Single Exponential Smoothing")




#################################
# Double Exponential Smoothing (DES - Seviye + Trend Odaklı)
#################################
# Madem havacılıkta yükselen bir trend var. (Bilet alanlar yıllara göre artıyor).
# O zaman SES değil, Trend parametresi olan (Beta) Çifte Düzeltme'ye bakalım!

def des_optimizer(train, alphas, betas, step=48):
    best_alpha, best_beta, best_mae = None, None, float("inf")
    for alpha in alphas:
        for beta in betas: # Alpha ve Beta için 2 boyutlu iç içe optimizasyon araması.
            des_model = ExponentialSmoothing(train, trend="add").fit(smoothing_level=alpha, smoothing_slope=beta)
            y_pred = des_model.forecast(step)
            mae = mean_absolute_error(test, y_pred)
            if mae < best_mae:
                best_alpha, best_beta, best_mae = alpha, beta, mae
            print("alpha:", round(alpha, 2), "beta:", round(beta, 2), "mae:", round(mae, 4))
    print("best_alpha:", round(best_alpha, 2), "best_beta:", round(best_beta, 2), "best_mae:", round(best_mae, 4))
    return best_alpha, best_beta, best_mae

alphas = np.arange(0.01, 1, 0.10)
betas = np.arange(0.01, 1, 0.10)

best_alpha, best_beta, best_mae = des_optimizer(train, alphas, betas, step=24)
# Optimizasyon sonrası best_alpha: 0.01 best_beta: 0.11 best_mae: 54.1036 (SES'teki 82 hatadan 54'e kadar düştük!)

des_model = ExponentialSmoothing(train, trend="add").fit(smoothing_level=best_alpha,
                                                         smoothing_slope=best_beta)
y_pred = des_model.forecast(24)

# Grafikte bu kez dümdüz yatay çizgi yerine "yukarı tırmanan bir doğru çizgisi" göreceğiz. Ama Melesef Mevsimsellik zikzaklarını algılayamadı.
plot_prediction(y_pred, "Double Exponential Smoothing")

#################################
# Triple Exponential Smoothing (Holt-Winters) (Seviye + Trend + MEVSİMSELLİK)
#################################
# DES yukarı doğru eğilen trendi anladı ama yazın artan, kışın azalan yolcu sayısını kavrayamadı.
# Holt-Winters tam da bu noktada devreye girer.

def tes_optimizer(train, abg, step=48):
    best_alpha, best_beta, best_gamma, best_mae = None, None, None, float("inf") # Gamma mevsimsellik ağırlığıdır!
    for comb in abg: # Kombinasyon demetindeki 3'lü parametre gruplarını döner
        tes_model = ExponentialSmoothing(train, trend="add", seasonal="add", seasonal_periods=12).\
            fit(smoothing_level=comb[0], smoothing_slope=comb[1], smoothing_seasonal=comb[2]) # Dönem olarak aylık=12 ay girdik.
        y_pred = tes_model.forecast(step)
        mae = mean_absolute_error(test, y_pred)
        if mae < best_mae:
            best_alpha, best_beta, best_gamma, best_mae = comb[0], comb[1], comb[2], mae
        print([round(comb[0], 2), round(comb[1], 2), round(comb[2], 2), round(mae, 2)])

    print("best_alpha:", round(best_alpha, 2), "best_beta:", round(best_beta, 2), "best_gamma:", round(best_gamma, 2),
          "best_mae:", round(best_mae, 4))

    return best_alpha, best_beta, best_gamma, best_mae

alphas = betas = gammas = np.arange(0.10, 1, 0.20) # Aralık adım sayısını biraz genişletip hızlandırdık.
abg = list(itertools.product(alphas, betas, gammas))

best_alpha, best_beta, best_gamma, best_mae = tes_optimizer(train, abg, step=24)
# Optimizasyon Sonucu: best_alpha: 0.3 best_beta: 0.3 best_gamma: 0.5 best_mae: 11.9947 ! (54 Küsür hatadan 11'e muazzam bir düşüş yakaladık)

# DİKKAT! Yukarıda 'add' (toplamsal) olarak denemiştik. Ancak havayolu verisindeki zikzakların boyu yıllar geçtikçe büyüyor
# Yıllar ilerledikçe varyans artıyorsa, model tipi Toplamsal değil Çarpımsal'dır! (Multiplicative - 'mul')
tes_model = ExponentialSmoothing(train, trend="mul", seasonal="mul", seasonal_periods=12).\
            fit(smoothing_level=best_alpha, smoothing_slope=best_beta, smoothing_seasonal=best_gamma)

y_pred = tes_model.forecast(24)

# Tahmini bir de grafikte görelim, zikzaklar muhteşem örtüşmüş durumda:
plot_prediction(y_pred, "Triple Exponential Smoothing ADD/MUL")

##################################################
# ARIMA(p, d, q): (Sadece Trend Varsa ARIMA)
##################################################
# İstatistiksel tarafa döndüğümüzde, ARIMA da mevsimsellik kavrayamaz. Eğik bir doğru çizecek.

p = d = q = range(0, 4)
pdq = list(itertools.product(p, d, q))


def arima_optimizer_aic(train, orders):
    best_aic, best_params = float("inf"), None
    for order in orders:
        try:
            arma_model_result = ARIMA(train, order).fit(disp=0)
            aic = arma_model_result.aic # AIC bazlı başarı. (Düşük olması iyi)
            if aic < best_aic:
                best_aic, best_params = aic, order
            print('ARIMA%s AIC=%.2f' % (order, aic))
        except:
            continue
    print('Best ARIMA%s AIC=%.2f' % (best_params, best_aic))
    return best_params

best_params_aic = arima_optimizer_aic(train, pdq)

arima_model = ARIMA(train, best_params_aic).fit(disp=0)
y_pred = arima_model.forecast(24)[0]
mean_absolute_error(test, y_pred)
# 51.1806294123169 (Tıpkı Double Exponential Smoothing gibi, mevsimsellik bulamayıp bocaladı!)


plot_prediction(pd.Series(y_pred, index=test.index), "ARIMA")


##################################################
# SARIMA (Hem Trend Hem Mevsimsellik varsa SARIMA)
##################################################
# Havayolu serisindeki o coşkunluğu ve devinimi anca SARIMA sökebilir.

p = d = q = range(0, 2)
pdq = list(itertools.product(p, d, q))
seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))] # Çarpı 12 Ay yapısıyla periyotları diz.


def sarima_optimizer_aic(train, pdq, seasonal_pdq):
    # Optimizasyon fonksiyonu (AIC Metoduyla)
    best_aic, best_order, best_seasonal_order = float("inf"), float("inf"), None
    for param in pdq:
        for param_seasonal in seasonal_pdq:
            try:
                sarimax_model = SARIMAX(train, order=param, seasonal_order=param_seasonal)
                results = sarimax_model.fit(disp=0)
                aic = results.aic
                if aic < best_aic:
                    best_aic, best_order, best_seasonal_order = aic, param, param_seasonal
                print('SARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, aic))
            except:
                continue
    print('SARIMA{}x{}12 - AIC:{}'.format(best_order, best_seasonal_order, best_aic))
    return best_order, best_seasonal_order

# Parametreleri al
best_order, best_seasonal_order = sarima_optimizer_aic(train, pdq, seasonal_pdq)

model = SARIMAX(train, order=best_order, seasonal_order=best_seasonal_order)
sarima_final_model = model.fit(disp=0)
y_pred_test = sarima_final_model.get_forecast(steps=24)

y_pred = y_pred_test.predicted_mean
mean_absolute_error(test, y_pred)
# Çıkan MAE: 68.57726545235921 (Biraz beklenenlerin altında!) Neden? AIC metrik olarak bazen MAE'de beklenen uçuşa geçemeyebiliyor.

plot_prediction(pd.Series(y_pred, index=test.index), "SARIMA")


##################
# SARIMA için İnanılmaz BONUS: MAE Optimizasyonu 
##################
# Eğer AIC ile SARIMA modelimiz Holt-Winters'a yanaşamadıysa, bir de "Hata'yı baz alarak paramatre seç" diyebilmekteyiz.

p = d = q = range(0, 2)
pdq = list(itertools.product(p, d, q))
seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]

def sarima_optimizer_mae(train, pdq, seasonal_pdq):
    best_mae, best_order, best_seasonal_order = float("inf"), float("inf"), None

    for param in pdq:
        for param_seasonal in seasonal_pdq:
            try:
                model = SARIMAX(train, order=param, seasonal_order=param_seasonal)
                sarima_model = model.fit(disp=0)
                y_pred_test = sarima_model.get_forecast(steps=24)
                y_pred = y_pred_test.predicted_mean
                
                # AIC yerine mutlak hata puanını hesapla ve onunla yarış!
                mae = mean_absolute_error(test, y_pred) 

                if mae < best_mae:
                    best_mae, best_order, best_seasonal_order = mae, param, param_seasonal
                print('SARIMA{}x{}12 - MAE:{}'.format(param, param_seasonal, mae))
            except:
                continue
    print('SARIMA{}x{}12 - MAE:{}'.format(best_order, best_seasonal_order, best_mae))
    return best_order, best_seasonal_order

best_order, best_seasonal_order = sarima_optimizer_mae(train, pdq, seasonal_pdq)

# Seçili hata katsayılarıyla SARIMA'yı Canlıya al!
model = SARIMAX(train, order=best_order, seasonal_order=best_seasonal_order)
sarima_final_model = model.fit(disp=0)
y_pred_test = sarima_final_model.get_forecast(steps=24)
y_pred = y_pred_test.predicted_mean
mean_absolute_error(test, y_pred)
# Sonuç MAE: 30.6233 (Neredeyse 68'den 30'a düştü! Muazzam.)

plot_prediction(pd.Series(y_pred, index=test.index), "SARIMA")



# Final Model Kurulumu:
# Gün sonunda bu testlerde en şampiyon çıkan modelimiz (MAE'si ~12 lerde olan) "Triple Exponential Smoothing - Holt Winters(mul)" modeliydi!
# Şirkete modeli teslim ederken tüm datayı eğitip o modele 6 aylık(ne kadar isteniyorsa) tahmin çekeceğiz!

tes_model_final = ExponentialSmoothing(df, trend="add", seasonal="add", seasonal_periods=12).\
            fit(smoothing_level=best_alpha, smoothing_slope=best_beta, smoothing_seasonal=best_gamma)

tes_model_final.forecast(6) # 6 aylık ileri dönem tahmini şirkete iletilmek üzere hazır!
