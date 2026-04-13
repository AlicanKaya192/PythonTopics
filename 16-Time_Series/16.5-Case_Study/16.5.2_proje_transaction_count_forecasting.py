###############################################################
# İş Problemi (Business Problem)
###############################################################

# Iyzico, internetten alışveriş deneyimini hem alıcılar hem de satıcılar için kolaylaştıran bir finansal teknolojiler şirketidir.
# E-ticaret firmaları, pazaryerleri ve bireysel kullanıcılar için ödeme altyapısı sağlamaktadır.
# Bizden İstenen: 2020 yılının son 3 ayı için "merchant_id" (üye işyeri) ve "gün" bazında TOPLAM İŞLEM HACMİ (Kaç adet satış yapacaklar?) tahmini yapılması beklenmektedir.


###############################################################
# Veri Seti Hikayesi (Dataset Story)
###############################################################
# 7 farklı üye iş yerinin (merchant) 2018’den 2020’e kadar olan günlük finansal verileri yer almaktadır.

# Değişkenler:
# Transaction : İşlem sayısı (Bizim tahmin etmeye çalışacağımız Hedef - Target değişkenimiz)
# MerchantID : Üye iş yerlerinin id'leri (Kategorik ayrım)
# Paid Price : Ödeme miktarı (Bunu tahmin etmeyeceğiz ama featue/özellik olarak belki işimize yarar)

###############################################################
# GÖREVLER (TASKS)
###############################################################

# Görev 1 : Veri Setinin Keşfi (EDA)
            # 1. iyzico_data.csv dosyasını okutunuz. transaction_date değişkeninin tipini date'e çeviriniz.
            # 2. Veri setinin başlangıc ve bitiş tarihleri nedir?
            # 3. Her üye iş yerindeki toplam işlem sayısı kaçtır?
            # 4. Her üye iş yerindeki toplam ödeme miktarı kaçtır?
            # 5. Her üye iş yerinin her bir yıl içerisindeki transaction count grafiklerini gözlemleyiniz.

# Görev 2 : Feature Engineering tekniklerini uygulayınız. Yeni feature'lar türetiniz.
            # - Date Features (Tarihten Yıl, Ay, Hafta, Gün çekme)
            # - Lag/Shifted Features (Geçmiş günler ne alemdeydi?)
            # - Rolling Mean Features (Hareketli ortalama)
            # - Exponentially Weighted Mean Features (Ağırlıklı ortalama)

# Görev 3 : Modellemeye Hazırlık
            # 1. One-hot encoding yapınız. (Kategorikleri ML algoritmalarının anlayacağı formata, yani 0-1 lerden oluşan matrislere çevir)
            # 2. Custom Cost Function'ları tanımlayınız. (Yarışma/Proje bizden SMAPE istiyor)
            # 3. Veri setini train ve validation olarak zaman bazlı ayırınız.

# Görev 4 : LightGBM Modelini oluşturunuz ve SMAPE ile hata değerini gözlemleyiniz.

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import lightgbm as lgb
import warnings

# Çıktıları daha nezi okuyabilmek için temel Pandas ayarları:
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 500)
pd.set_option('display.float_format', lambda x: '%.3f' % x) # Virgülden sonra 3 basamak limitlesin.
warnings.filterwarnings('ignore')



###############################################################
# Görev 1 : Veri Setinin Keşfi (EDA)
###############################################################

# 1. iyzico_data.csv dosyasını okutunuz. transaction_date değişkeninin tipini date'e çeviriniz.
# Dosya yolumuzu klasör yapımıza göre güncelledik (üst klasördeki time_series_datasets içinden)
df = pd.read_csv("../time_series_datasets/iyzico_m/iyzico_data.csv")

# Fazlalıktan gelen, index numaralarını tutan kolonu çöpe atıyoruz.
df.drop("Unnamed: 0", axis=1,inplace=True)

df.head() # Tepeden bak
df.tail() # Alttan bak

df["transaction_date"].dtypes # Tipini kontrol (Object - yani metin döner muhtemelen)

# Tarih yazan metinleri Pandas'ın algılayabileceği zaman objesine dönüştürdük:
df["transaction_date"] = pd.to_datetime(df["transaction_date"]) 


# 2. Veri setinin başlangıc ve bitiş tarihleri nedir?
df["transaction_date"].min() # Timestamp('2018-01-01 00:00:00') (Veri macerası bu tarihte başlamış)
df["transaction_date"].max() # Timestamp('2020-12-31 00:00:00') (Veri kapanış tarihi)

# 3. Her üye iş yerindeki toplam işlem sayısı kaçtır?
df["merchant_id"].unique() # Kimmiş bu mağazalar bi bakalım. (Örn: 53531.0 vs..)

# 4. Her üye iş yerindeki toplam ödeme miktarı kaçtır?
# Mağazalara göre grupla ve Total_Paid kolonunun toplam(sum)'unu al!
df.groupby("merchant_id").agg({"Total_Paid":"sum"})

# 5. üye iş yerlerinin her bir yıl içerisindeki transaction count (İşlem Hacmi) grafiklerini gözlemleyiniz.
for id in df.merchant_id.unique():
    # Şirket her bir mağazanın kendi içindeki döngüsünü merak etmiş.
    plt.figure(figsize=(15, 15))
    
    # 2018-2019 Arası
    plt.subplot(3, 1, 1, title = str(id) + ' 2018-2019 Transaction Count')
    df[(df.merchant_id == id) & ( df.transaction_date >= "2018-01-01" ) & (df.transaction_date < "2019-01-01")]["Total_Transaction"].plot()
    plt.xlabel('')
    
    # 2019-2020 Arası
    plt.subplot(3, 1, 2,title = str(id) + ' 2019-2020 Transaction Count')
    df[(df.merchant_id == id) &( df.transaction_date >= "2019-01-01" )& (df.transaction_date < "2020-01-01")]["Total_Transaction"].plot()
    plt.xlabel('')
    
    plt.show() # Bu çizimlerle satıcıların kampanya günleri, black friday gibi patlama anları net görülebilmektedir.


###############################################################
# Görev 2 : Feature Engineering (Veriden Elmas Çıkarma Sanatı)
###############################################################

########################
# Date Features (Zaman Özelliklerini Parçalama)
########################

def create_date_features(df, date_column):
    # ML algoritması "1 Ocak 2020" stringini zerre anlamaz. Biz ona "Ay 1", "Gün 1", "Haftanın 1.Günü", "Yılın Başı=Evet" gibi matematiksel özellikler fırlatmalıyız.
    df['month'] = df[date_column].dt.month
    df['day_of_month'] = df[date_column].dt.day
    df['day_of_year'] = df[date_column].dt.dayofyear
    df['week_of_year'] = df[date_column].dt.isocalendar().week # weekofyear kullanım dışı olabileceği için isocalendar().week idealdir.
    df['day_of_week'] = df[date_column].dt.dayofweek
    df['year'] = df[date_column].dt.year
    df["is_wknd"] = df[date_column].dt.weekday // 4 # Cuma, Cumartesi, Pazar yakalayıcısı
    df['is_month_start'] =df[date_column].dt.is_month_start.astype(int)
    df['is_month_end'] = df[date_column].dt.is_month_end.astype(int)
    df['quarter'] = df[date_column].dt.quarter # Yılın kaçıncı Çeyreği? (1,2,3,4)
    df['is_quarter_start'] = df[date_column].dt.is_quarter_start.astype(int)
    df['is_quarter_end'] = df[date_column].dt.is_quarter_end.astype(int)
    df['is_year_start'] = df[date_column].dt.is_year_start.astype(int)
    df['is_year_end'] = df[date_column].dt.is_year_end.astype(int)
    return df

df = create_date_features(df, "transaction_date") # Zaman parçalayıcı fonksiyonumuzu dataframe'in üstüne koşturduk.
df.head()

# Üye iş yerlerinin yıl ve ay bazında işlem sayılarının incelenmesi (Analiz: Örneğin kasım aylarında işlem sayıları çok mu yükseliyor?)
df.groupby(["merchant_id","year","month","day_of_month"]).agg({"Total_Transaction": ["sum", "mean", "median"]})

# Üye iş yerlerinin yıl ve ay bazında toplam ödeme miktarlarının incelenmesi
df.groupby(["merchant_id","year","month"]).agg({"Total_Paid": ["sum", "mean", "median"]})


########################
# Lag/Shifted Features (Dünün Sırları)
########################

def random_noise(dataframe):
    # Overfitting önleyici gizli silah: gürültü. İşlem hacmine rastgele "ufak" sapmalar ekler ki model veriyi ezberlemesin, trendi kavramaya çalışsın.
    return np.random.normal(scale=1.6, size=(len(dataframe),))

def lag_features(dataframe, lags):
    # Belirlediğimiz 'lags' paketini dön. Her mağazanın kendi içinde dünkü, 3 gün önceki, 1 yıl önceki satışlarını (işlem hacmini) bugünün sonuna etiketle.
    for lag in lags:
        dataframe['sales_lag_' + str(lag)] = dataframe.groupby(["merchant_id"])['Total_Transaction'].transform(
            lambda x: x.shift(lag)) + random_noise(dataframe)
    return dataframe

# Iyzico verisi için neden bu kadar uçuk rakamlı laglar eklendi (91, 190, 365..)?
# ÇÜNKÜ: Bizden son 3 AYIN (90 günün) tahmini isteniyor! Yarın için bugünün Lagına(lag 1) güvenemeyiz çünkü test verisinde son 3 ay bomboş olacak! Model 90 gün öncesinden başlayarak referans bulmalı. 
df = lag_features(df, [91,92,170,171,172,173,174,175,176,177,178,179,180,181,182,183,184,185,186,187,188,189,190,
                       350,351,352,352,354,355,356,357,358,359,360,361,362,363,364,365,366,367,368,369,370,
                       538,539,540,541,542,
                       718,719,720,721,722])


########################
# Rolling Mean Features (Hareketli Ortalamalar)
########################

def roll_mean_features(dataframe, windows):
    # Seçilen pencere boyutu kadar günün ortalama işlem hacmini yaz!
    for window in windows:
        dataframe['sales_roll_mean_' + str(window)] = dataframe.groupby("merchant_id")['Total_Transaction']. \
                                                          transform(
            lambda x: x.shift(1).rolling(window=window, min_periods=10, win_type="triang").mean()) + random_noise(
            dataframe)
    return dataframe

df = roll_mean_features(df, [91,92,178,179,180,181,182,359,360,361,449,450,451,539,540,541,629,630,631,720])


########################
# Exponentially Weighted Mean Features (Üstel Ağırlıklı Ortalamalar)
########################

def ewm_features(dataframe, alphas, lags):
    # Eski tarihlere ve yeni tarihlere verilen "Alpha" (önem katsayısı) üzerinden ortalama yazar.
    for alpha in alphas:
        for lag in lags:
            dataframe['sales_ewm_alpha_' + str(alpha).replace(".", "") + "_lag_" + str(lag)] = \
                dataframe.groupby("merchant_id")['Total_Transaction'].transform(lambda x: x.shift(lag).ewm(alpha=alpha).mean())
    return dataframe

alphas = [0.95, 0.9, 0.8, 0.7, 0.5]
lags = [91,92,178,179,180,181,182,359,360,361,449,450,451,539,540,541,629,630,631,720]

df = ewm_features(df, alphas, lags)
df.tail()


########################
# Black Friday - Summer Solstice (Özel Gün Mühendisliği)
########################
# Makine Öğrenmesinde bir uzmanın algoritmaya fark atacağı yer Domain (Sektörel) bilgisidir.
# E-ticarette Black Friday kasırga koparır. Modele bu günlerin black friday olduğunu bildirirsek mükemmel öğrenir!

df["is_black_friday"] = 0
# Efsane cumaları 1 ile işaretledik.
df.loc[df["transaction_date"].isin(["2018-11-22","2018-11-23","2019-11-29","2019-11-30"]) ,"is_black_friday"]=1

df["is_summer_solstice"] = 0
# Yaz dönümü/kampanyaları da alışılagelmişin dışında harcama yaptırıyorsa onları da işaretleriz.
df.loc[df["transaction_date"].isin(["2018-06-19","2018-06-20","2018-06-21","2018-06-22",
                                    "2019-06-19","2019-06-20","2019-06-21","2019-06-22",]) ,"is_summer_solstice"]=1




########################
# One-Hot Encoding
########################
df.head()

# merchant_id(Mağaza), day_of_week(haftanın günü), month(ay) kolonlarını ağacın kolları çok daha rahat dallanabilsin diye Kukla (Dummy/OneHot) değişkenlere ayırıyoruz.
df = pd.get_dummies(df, columns=['merchant_id','day_of_week', 'month'])

# Gürültülü hedef değişkeni(Target/İşlem Hacmini) uslu, normal dağılımlı bir gence dönüştürmek için doğasını ufacık büküp Logaritmaya yatırıyoruz. Eğitimi çok kolaylaştıracak.
df['Total_Transaction'] = np.log1p(df["Total_Transaction"].values)


########################
# Custom Cost Function
########################

# MAE: mean absolute error (Hata kaç tane)
# MAPE: mean absolute percentage error (Hata Yüzde kaç)
# SMAPE: Symmetric mean absolute percentage error (Hatanın, hem testin hem gerçek değerlerin üzerinden dengelenmiş hali) Kaggle ve Büyük Şirketlerin favorisi.

def smape(preds, target):
    n = len(preds)
    masked_arr = ~((preds == 0) & (target == 0))
    preds, target = preds[masked_arr], target[masked_arr]
    num = np.abs(preds - target)
    denom = np.abs(preds) + np.abs(target)
    smape_val = (200 * np.sum(num / denom)) / n
    return smape_val

def lgbm_smape(preds, train_data):
    # Modeli ölçmeden önce logaritmanın 'anti-büyü'sü olan expm1 ile eski rakamları buluyoruz. Sonuçları şişirmeden sönük loglarla ölçmek haksız performans gösterir.
    labels = train_data.get_label()
    smape_val = smape(np.expm1(preds), np.expm1(labels))
    return 'SMAPE', smape_val, False

########################
# Time-Based Validation Sets (Eğitim ve Test Kümelerini Ayarlama)
########################

import re # İsimlendirmelerdeki sorun çıkarıbilecek garip Regex uyumsuz karakterleri silip atalım. 
df = df.rename(columns = lambda x:re.sub('[^A-Za-z0-9_]+', '', x))

# BİZDEN İSTENEN NEDİR? 2020 SON 3 AYININ TAHMİNİ.
# O VAKİT:
# 2020'nin 10.ayına kadar olan koskoca her şey bizim TRAIN (EĞİTİM) setimizdir.
train = df.loc[(df["transaction_date"] < "2020-10-01"), :]

# 2020'nin son 3 ayı ise sınavımızı olup Müşteriye "Yaptım abi!" diyeceğimiz Validasyon setimizdir.
val = df.loc[(df["transaction_date"] >= "2020-10-01"), :]

# Kolonların içinden hedefimizi (Transaction), tarih kolonumuzu vs kaldırıp sadece X'lerimizi(Features) bir listeye dolduruyoruz.
cols = [col for col in train.columns if col not in ['transaction_date', 'id', "Total_Transaction","Total_Paid", "year" ]]

Y_train = train['Total_Transaction']
X_train = train[cols]

Y_val = val['Total_Transaction']
X_val = val[cols]

# Kontrol. Veriler sağlıklı parçalanmış mı?
Y_train.shape, X_train.shape, Y_val.shape, X_val.shape

########################
# LightGBM Model (Final Aşama)
########################

# LightGBM parameters (Ağacın genetik yapısını ayarladığımız sözlük)
lgb_params = {'metric': {'mae'}, # Hata ölçütü
              'num_leaves': 10, # Maksimum yaprak
              'learning_rate': 0.02, # Öğrenme adımı (hızı)
              'feature_fraction': 0.8, # Rasgele feature seçme oranı (%80)
              'max_depth': 5, # Ağaç dalı en fazla 5 adım derine gitsin ki aşırı öğrenmesin
              'verbose': 0, # Mesajları kapat.
              'num_boost_round': 1000, # 1000 ağaçlık orman kur.
              'early_stopping_rounds': 200, # 200 ağaç kurdun da hala hatayı 1 dirhem düşüremediysen işlemi durdur.
              'nthread': -1}


lgbtrain = lgb.Dataset(data=X_train, label=Y_train, feature_name=cols)
lgbval = lgb.Dataset(data=X_val, label=Y_val, reference=lgbtrain, feature_name=cols)

# Model Motorunu Ateşle!
model = lgb.train(lgb_params, lgbtrain,
                  valid_sets=[lgbtrain, lgbval],
                  num_boost_round=lgb_params['num_boost_round'],
                  feval=lgbm_smape,
                  # Yukaıdaki early_stopping_rounds ve verbose_eval parametreleri yeni lgbm sürümlerinde callbacks içinde verilir:
                  callbacks=[lgb.early_stopping(stopping_rounds=lgb_params['early_stopping_rounds']), lgb.log_evaluation(100)])

# En parlak bulduğumuz "best_iteration" (En verimli tur) ile test tahmini istiyoruz.
y_pred_val = model.predict(X_val, num_iteration=model.best_iteration)

# Skoru Görelim: Müşteriye sunacağımız başarımız!
smape(np.expm1(y_pred_val), np.expm1(Y_val))

########################
# Değişken Önem Düzeyleri (Feature Importance)
########################
# Müşteriye "Al bu da kodlar kardeşim" deyip geçilmez, onlara İçgörü (Insight) verilmelidir.
# Hangi değişken satışları/işlemleri roket gibi uçurdu? Black Friday cidden etkili olmuş mu? Ekranda göstereceğiz:

def plot_lgb_importances(model, plot=False, num=10):

    # Modelden Gain'leri (kazanç) yani bilgi teorisindeki işe yapıcılık katsayılarını çek
    gain = model.feature_importance('gain')
    feat_imp = pd.DataFrame({'feature': model.feature_name(),
                             'split': model.feature_importance('split'),
                             'gain': 100 * gain / gain.sum()}).sort_values('gain', ascending=False)
    
    # Çizgiyi (Barplot'u) renklendirip ekrana bas.
    if plot:
        plt.figure(figsize=(10, 10))
        sns.set(font_scale=1)
        sns.barplot(x="gain", y="feature", data=feat_imp[0:25])
        plt.title('feature')
        plt.tight_layout()
        plt.show()
    else:
        print(feat_imp.head(num))

# İlk 30 çok kazandıran değişkeni ekrana bas ve Iyzico yetkililerine hava at!
plot_lgb_importances(model, num=30, plot=True)

# Alternatif olarak kütüphanenin kendi özelliği ile de çizilebilir:
lgb.plot_importance(model, max_num_features=20, figsize=(10, 10), importance_type="gain")
plt.show()

# Proje Başarıyla Tamamlanmıştır! Geçmiş olsun.
