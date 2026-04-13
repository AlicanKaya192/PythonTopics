#####################################################
# Demand Forecasting (Makine Öğrenmesi ile Talep Tahmini)
#####################################################
#
# Bu dosyada daha önceki Smoothing ya da ARIMA gibi klasik istatistiksel modeller yerine
# ağaç bazlı güçlü bir Makine Öğrenmesi algoritması olan LightGBM kullanarak Zaman Serisi tahmini yapacağız.
# Makine öğrenmesi algoritmaları zamanı doğal olarak anlamaz! Onlara zamanı öğretebilmek için
# Feature Engineering (Özellik Mühendisliği) ile Gecikme (Lag) ve Hareketli Ortalama (Rolling Mean) gibi 
# değişkenler türeteceğiz.

# Kaggle Yarışması: Store Item Demand Forecasting Challenge
# Amaç: Farklı mağazalarda, çeşitli ürünlerin gelecek satışlarını olabildiğince az hatayla tahmin edebilmek.

import time
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import lightgbm as lgb # Efsanevi LightGBM (Hızlı, güçlü, ağaç tabanlı model algoritması)
import warnings

# Çıktıların terminale/konsola güzel basılması için gereken Pandas ayarları:
pd.set_option('display.max_columns', None) # Tüm sütunları göster
pd.set_option('display.width', 500) # Tek ekranda sığacağı genişlik limiti
warnings.filterwarnings('ignore') # Kırmızı uyarı yazılarını gizle

# Dataframelerdeki bilgileri hızlıca analiz edebilmek için yardımcı bir EDA fonksiyonumuz:
def check_df(dataframe, head=5):
    print("##################### Shape #####################")
    print(dataframe.shape) # Satır ve sütun sayısı
    print("##################### Types #####################")
    print(dataframe.dtypes) # Her bir kolonun veri tipi
    print("##################### Head #####################")
    print(dataframe.head(head)) # Baştan 5 satır
    print("##################### Tail #####################")
    print(dataframe.tail(head)) # Sondan 5 satır
    print("##################### NA #####################")
    print(dataframe.isnull().sum()) # Kolonlardaki eksik (null) veri sayısı
    print("##################### Quantiles #####################")
    print(dataframe.quantile([0, 0.05, 0.50, 0.95, 0.99, 1]).T) # Sayısal verilerin dağılımındaki yüzdelik çeyreklikler (Aykırı değer kontrolü)


########################
# Loading the data (Veriyi Yükleme)
########################

# Train (Eğitim) ve Test verilerimizi yüklüyoruz. 'parse_dates' ile date isimli kolonu direkt Zaman Objesine çevirmesini söylüyoruz ki işimiz kolaylaşsın.
train = pd.read_csv('../time_series_datasets/demand_forecasting/train.csv', parse_dates=['date'])
test = pd.read_csv('../time_series_datasets/demand_forecasting/test.csv', parse_dates=['date'])

# Yarışmalardaki teslim şablonu.
sample_sub = pd.read_csv('../time_series_datasets/demand_forecasting/sample_submission.csv')

# Machine Learning verisinde Feature Engineering yaparken hepimizin kullandığı taktik: 
# Train ve Test'i alt alta birleştir (concat)! Ki aynı lag vs ürettiğimiz yeni kolonlar tüm veride standart bulunsun.
df = pd.concat([train, test], sort=False)


#####################################################
# EDA (Keşifçi Veri Analizi)
#####################################################

# Elimizdeki verinin ilk tarihi ve son tahiri nedir?
df["date"].min(), df["date"].max()

check_df(df) # İlk bakış: sales kolonunda test kısmından ötürü boşluklar var (Biz oralara tahmin üreteceğiz)

df[["store"]].nunique() # Kaç farklı mağaza var? (Veride 10 mağaza varmış)

df[["item"]].nunique() # Kaç farklı ürün var? (50 ürün varmış)

df.groupby(["store"])["item"].nunique() # Hangi mağazada kaç ürün var? (Hepsinde eşit)

df.groupby(["store", "item"]).agg({"sales": ["sum"]}) # Her mağazadaki her ürünün toplam satışları nedir?

# Aynı kırılımda Ortalama, Ortanca (Medyan) ve Standart Sapmasına bakalım:
df.groupby(["store", "item"]).agg({"sales": ["sum", "mean", "median", "std"]})

df.head() # Tabloya bir gözat.


#####################################################
# FEATURE ENGINEERING (Makine Öğrenimi İçin Veriyi Yoğurma)
#####################################################
# Zaman serisini ML algoritmalarına öğretmenin bir numaralı yolu; zaman değişkenini olabildiğince atomlarına ayırmaktır.

def create_date_features(df):
    # 'date' bilgisinden ay,  aydaki günü, yıldaki günü vb... üretiyoruz. Algoritma "aaa bugün ayın sonuymuş o zaman maaş günüdür fazla satar!" öğrenebilsin.
    df['month'] = df.date.dt.month
    df['day_of_month'] = df.date.dt.day
    df['day_of_year'] = df.date.dt.dayofyear
    df['week_of_year'] = df.date.dt.isocalendar().week # Pandas yeni sürümlerinde weekofyear deprecated olduğu için isocalendar kullanılması daha doğrudur.
    df['day_of_week'] = df.date.dt.dayofweek
    df['year'] = df.date.dt.year
    df["is_wknd"] = df.date.dt.weekday // 4 # Haftasonu mu? (Cuma,ctesi,pazar 4 e bölünce 1 çıkar mantığı)
    df['is_month_start'] = df.date.dt.is_month_start.astype(int) # Ayın ilk günü mü? (True/False'u 1/0'a çevir)
    df['is_month_end'] = df.date.dt.is_month_end.astype(int) # Ayın son günü mü?
    return df

df = create_date_features(df)

# Ürettiğimiz aylara göre bir göz atalım: (Örneğin yaz aylarında satışlar patlıyor mu?)
df.groupby(["store", "item", "month"]).agg({"sales": ["sum", "mean", "median", "std"]})


########################
# Random Noise (Rastgele Gürültü Ekleme)
########################

def random_noise(dataframe):
    # Veriye lag vb eklerken Overfitting'i (Modelin veriyi ezberlemesini) engellemek için ufak ufak şaşırtmacalar, noise (gürültü) katmalıyız.
    return np.random.normal(scale=1.6, size=(len(dataframe),))


########################
# Lag/Shifted Features (Gecikmeli Değişkenler - DÜN NE KADAR SATTIM?)
########################
# Bir mağazada yarın ne kadar süt satılacağını bulmanın en büyük ipucu: "Dün ne kadar satıldı? Ondan önceki gün ne satıldı?" sorusudur.

# Önce verimizi mağaza, ürün ve zamana göre kusursuz olarak eskiye-yeniye göre sıralıyoruz ki veriler karışık kaymasın.
df.sort_values(by=['store', 'item', 'date'], axis=0, inplace=True)

# shift(1) demek satış kolonunu zaman ekseninde 1 adım aşağı kaydır demektir.
# Yani dünün satışı artık bugünün yanına "lag1" ismiyle yeni bir özellik olarak geldi!
pd.DataFrame({"sales": df["sales"].values[0:10],
              "lag1": df["sales"].shift(1).values[0:10],
              "lag2": df["sales"].shift(2).values[0:10],
              "lag3": df["sales"].shift(3).values[0:10],
              "lag4": df["sales"].shift(4).values[0:10]})

df.groupby(["store", "item"])['sales'].head()
# Groupby yapmamızın tek sebebi, ürün değiştiğinde shift komutunun gidip alakasız ürünün dünkü satışını şimdiki ürüne aktarmaması içindir! 
df.groupby(["store", "item"])['sales'].transform(lambda x: x.shift(1))

def lag_features(dataframe, lags):
    for lag in lags:
        # Belirtilen adım kadar verileri aşağı kaydırıp yeni kolon açıyoruz. (Eş zamanlı gürültü de ekleyip ezberciliği bozuyoruz)
        dataframe['sales_lag_' + str(lag)] = dataframe.groupby(["store", "item"])['sales'].transform(
            lambda x: x.shift(lag)) + random_noise(dataframe)
    return dataframe

# Satışlarda döngüsellik olur genelde. O yüzden 3 aylık(90. gün civarı), 6 aylık(180) ve Senelik(364) lag (gecikme) periyotlarını koyduk! 
df = lag_features(df, [91, 98, 105, 112, 119, 126, 182, 364, 546, 728])

check_df(df) # lag'lardan dolayı ilk ayların bazılarında (Geçmişi olmadığından) N/A oluştu ama dert değil. Lgbm affeder.

########################
# Rolling Mean Features (Hareketli Ortalama - SON X GÜNÜN ORTALAMASI!)
########################
# Lag sadece dünü veya bir geçmiş günü hatırlamak demektir. Ama "Son 3 gün ortalamam neydi?" sorusu trendi anlamamızı sağlar.

pd.DataFrame({"sales": df["sales"].values[0:10],
              "roll2": df["sales"].rolling(window=2).mean().values[0:10],
              "roll3": df["sales"].rolling(window=3).mean().values[0:10],
              "roll5": df["sales"].rolling(window=5).mean().values[0:10]})

# DİKKAT: Zaman serisinde tahmin yaparken kendiside dahil (bugün) rolling mean ALAMAZSINIZ! Veri sızar. O yüzden önce shift(1) yapıp sonra rolling alıyoruz!
pd.DataFrame({"sales": df["sales"].values[0:10],
              "roll2": df["sales"].shift(1).rolling(window=2).mean().values[0:10],
              "roll3": df["sales"].shift(1).rolling(window=3).mean().values[0:10],
              "roll5": df["sales"].shift(1).rolling(window=5).mean().values[0:10]})


def roll_mean_features(dataframe, windows):
    for window in windows:
        # Pencereler kadar kaydırarak (shift+rolling) geçmiş x günün trend/ortalama ağırlığını çıkarıyoruz. win_type=triang diyerek merkeze daha önem ver de diyebiliriz.
        dataframe['sales_roll_mean_' + str(window)] = dataframe.groupby(["store", "item"])['sales']. \
                                                          transform(
            lambda x: x.shift(1).rolling(window=window, min_periods=10, win_type="triang").mean()) + random_noise(dataframe)
    return dataframe


df = roll_mean_features(df, [365, 546]) # 1 Yıllık ve 1.5 Yıllık kayan ortalama hareketliliklerini çektik.

########################
# Exponentially Weighted Mean Features (Üstel Ağırlıklı Ortalama)
########################
# Rolling Mean eski günlerle yeni günleri adil (veya düz) çarpar. 
# Ama biz biliyoruz ki dünün satışı benim için, 30 gün önceki satıştan DAHA ÖNEMLİDİR. 
# Geçmişe dair yakınlığına göre ağırlık ver!(alfa etkisi)

pd.DataFrame({"sales": df["sales"].values[0:10],
              "roll2": df["sales"].shift(1).rolling(window=2).mean().values[0:10],
              "ewm099": df["sales"].shift(1).ewm(alpha=0.99).mean().values[0:10], # Alpha 0.99 : Yakın tarihe %99, eskiye %1 güven = Nerdeyse Lag!
              "ewm095": df["sales"].shift(1).ewm(alpha=0.95).mean().values[0:10],
              "ewm07": df["sales"].shift(1).ewm(alpha=0.7).mean().values[0:10],
              "ewm02": df["sales"].shift(1).ewm(alpha=0.1).mean().values[0:10]})

def ewm_features(dataframe, alphas, lags):
    for alpha in alphas:
        for lag in lags:
            dataframe['sales_ewm_alpha_' + str(alpha).replace(".", "") + "_lag_" + str(lag)] = \
                dataframe.groupby(["store", "item"])['sales'].transform(lambda x: x.shift(lag).ewm(alpha=alpha).mean())
    return dataframe

alphas = [0.95, 0.9, 0.8, 0.7, 0.5]
lags = [91, 98, 105, 112, 180, 270, 365, 546, 728]

df = ewm_features(df, alphas, lags)
check_df(df)

########################
# One-Hot Encoding (Ağaç Modeline Anlatım)
########################
# Ağaç modelleri gerçi kategorikleri handle etseler bile 'ay:1...' verisini bazen küçük rakam sanabilir, bunlardan dummy (kukla) kolon türetiriz:

df = pd.get_dummies(df, columns=['store', 'item', 'day_of_week', 'month'])

check_df(df)


########################
# Converting sales to log(1+sales) (Satış Verisini Logaritmaya Çevirme)
########################
# Veride bir gün 10 diğer gün 200 satmışsa varyans devasa demektir, model afallar.
# Veriyi sıkıştırıp uslu bir normal dağılıma çekmek için üzerine Logaritma giydiriyoruz.
# 1p demesi: olur da satış 0 sa matematik çökmesin (0=tanımsız) 0'lara 1 ekle logaritmasını öyle al.

df['sales'] = np.log1p(df["sales"].values)

check_df(df)

#####################################################
# Model Kurulumu
#####################################################

########################
# Custom Cost Function (LGBM İçin Özel Hata Fonksiyonu)
########################
# Yarışmanın bizden istediği hata ölçütü SMAPE (Simetrik ortalama mutlak hata yüzdesi)'dir. 
# lgbm standart metrikleri içinde bulunmuyor, bu yüzden kendi ellerimizle kodluyoruz. 

def smape(preds, target):
    n = len(preds)
    masked_arr = ~((preds == 0) & (target == 0))
    preds, target = preds[masked_arr], target[masked_arr]
    num = np.abs(preds - target)
    denom = np.abs(preds) + np.abs(target)
    smape_val = (200 * np.sum(num / denom)) / n
    return smape_val

# LGBM modeli fit olurken logaritma halindeki tahminleri alacak, ondan dolayı içini "expm1" ile ters-logaritma (eski haline getirme) yapıp smape'e yolluyoruz ki gerçek puan görelim.
def lgbm_smape(preds, train_data):
    labels = train_data.get_label()
    smape_val = smape(np.expm1(preds), np.expm1(labels))
    return 'SMAPE', smape_val, False


########################
# Time-Based Validation Sets (Zaman Bazlı Eğit/Test Ayrımı)
########################
# ML'de veriler rastgele ayrılırdı hatırlarsanız (train_test_split). AMA ZAMAN SERİSİNDE GELECEĞİ RASTGELE ALIP GEÇMİŞİ SORAMAZSIN!
# O yüzden kronolojik (zamanı baz alarak) sondan belli bir periyodu doğrulama (validation) yapıp kalanı eğitim veriyoruz.

# 2017'nin başına kadar (2016'nın sonuna kadar) train seti.
train = df.loc[(df["date"] < "2017-01-01"), :]

# 2017'nin ilk 3'ayı validasyon (doğrulama) seti. 
val = df.loc[(df["date"] >= "2017-01-01") & (df["date"] < "2017-04-01"), :]

# İhtiyacımız olmayan; target, kimlik vb şeyleri listemizden çıkartıyoruz:
cols = [col for col in train.columns if col not in ['date', 'id', "sales", "year"]]

Y_train = train['sales'] # Hedef Y (SATIŞLAR)
X_train = train[cols] # Bağımsız Değişken X'ler (Özelliklerimiz)

Y_val = val['sales']
X_val = val[cols]

Y_train.shape, X_train.shape, Y_val.shape, X_val.shape

########################
# LightGBM ile Zaman Serisi Modeli
########################

# LightGBM parameters (Ağacın beyni)
lgb_params = {'num_leaves': 10,  # Tek bir ağaçtaki max yaprak (dal) sayısı. Fazlası overfite götürür.
              'learning_rate': 0.02, # Öğrenmenin adımları, yavaş adımlar şaşmaz!
              'feature_fraction': 0.8, # Her yinelemede (ağaçta) rastgele seçilecek kolonların sadece %80'ini kullanarak ezberi boz.
              'max_depth': 5, # Ağacın derinliği
              'verbose': 0, # Saçma sapan konsol satırlarını kapat
              'num_boost_round': 1000, # N_estimators. 1000 iterasyon
              'early_stopping_rounds': 200, # Model en az 200 adım boyunca hata azaltmamışsa çakılı kalmıştır de ve fit işlemini kes! (Süre tasarrufu)
              'nthread': -1} # Cihazdaki tüm CPU çekirdeklerini aslan gibi kullan.

# LightGBM'in kendi performanslı Matrix formlarına (Dataset) dönüştürüyoruz.
lgbtrain = lgb.Dataset(data=X_train, label=Y_train, feature_name=cols)
lgbval = lgb.Dataset(data=X_val, label=Y_val, reference=lgbtrain, feature_name=cols)

# Tren kalkıyor! Modeli verilerimiz ebesine kavuşana dek eğitiyoruz:
model = lgb.train(lgb_params, lgbtrain,
                  valid_sets=[lgbtrain, lgbval],
                  num_boost_round=lgb_params['num_boost_round'],
                  feval=lgbm_smape, # Özel Hata Fonksiyonumuz
                  # early_stopping_rounds parametresi artık callbacks içine eklenerek kullanılıyor güncel lgbm sürümlerinde! Orijinal kodu bozmamak için devam edelim.
                  callbacks=[lgb.early_stopping(stopping_rounds=lgb_params['early_stopping_rounds']), lgb.log_evaluation(100)])

y_pred_val = model.predict(X_val, num_iteration=model.best_iteration) # Eğitimin en parlak anındaki haliyle tahmin çektik.

smape(np.expm1(y_pred_val), np.expm1(Y_val)) # Ve skoru ölçtük. Yüzde kaçlık sapmamız var diye!


########################
# Feature Importance (Hangi Değişkenler Satışı Belirliyor?)
########################

def plot_lgb_importances(model, plot=False, num=10):
    gain = model.feature_importance('gain') # Modele göre özellikleri ne kadar kazanç getirdi (önem sırası)
    feat_imp = pd.DataFrame({'feature': model.feature_name(),
                             'split': model.feature_importance('split'),
                             'gain': 100 * gain / gain.sum()}).sort_values('gain', ascending=False)
    if plot: # Görsel izni geldiyse Barplot çizer.
        plt.figure(figsize=(10, 10))
        sns.set(font_scale=1)
        sns.barplot(x="gain", y="feature", data=feat_imp[0:25])
        plt.title('feature')
        plt.tight_layout()
        plt.show()
    else:
        print(feat_imp.head(num))
    return feat_imp

plot_lgb_importances(model, num=200) # En iyi 200 lü listeleme
plot_lgb_importances(model, num=30, plot=True) # Top 30 Grafiği. Muhtemelen Lag (Geçmiş günler) kolonları ilk sıraları istila etmiştir :)

# Hiçbir işlevi (Gain = 0) olmayan yani satışlara zerre katkısı olmayan boş beleş kolonları bulup tespit ediyoruz ki ilerde gereksiz yer kaplamasın.
feat_imp = plot_lgb_importances(model, num=200)
importance_zero = feat_imp[feat_imp["gain"] == 0]["feature"].values
imp_feats = [col for col in cols if col not in importance_zero]
len(imp_feats)


########################
# Final Model (Yarışma Teslimatı İçin Tüm Veri İle Eğitim)
########################
# Parametreleri ve işe yarayan değişkenleri bulduk. Artık sadece Train ile değil tüm Train+Validation paketiyle
# nihai bir model kurup yarışmaya gitme vakti!

train = df.loc[~df.sales.isna()] # Satışları eksik olmayan (Kaggle orjinal traini) ayır.
Y_train = train['sales']
X_train = train[cols]

test = df.loc[df.sales.isna()] # Satışları boş NA yollanmış (Kaggle orjinal testi, yani Kaggle'ın "Bunları bana bul kardeş" dediği blok).
X_test = test[cols]

# Sadece Iterasyon sayısına daha önce bulduğumuz ve emin olduğumuz 'best_iteration' u çakıyoruz!
lgb_params = {'num_leaves': 10,
              'learning_rate': 0.02,
              'feature_fraction': 0.8,
              'max_depth': 5,
              'verbose': 0,
              'nthread': -1,
              "num_boost_round": model.best_iteration}

lgbtrain_all = lgb.Dataset(data=X_train, label=Y_train, feature_name=cols) # Bütün kalabalığı formata ver

# FİNAL EĞİTİMİ (Artık early stopping vs yok, sadece elimizdeki en iyi iterasyon değeri kadar ağaç inşa ediyoruz)
final_model = lgb.train(lgb_params, lgbtrain_all, num_boost_round=model.best_iteration)

# Kaggle için nihai tahminleri ateşle...
test_preds = final_model.predict(X_test, num_iteration=model.best_iteration)

########################
# Submission File (Teslim Dosyasını İhracat Etme)
########################

test.head()

submission_df = test.loc[:, ["id", "sales"]] # Boşlukları artık elimizde
submission_df['sales'] = np.expm1(test_preds) # Tabi biz tahminleri Logaritmik yaptık. expm1 diyerek Onları tekrar asıl haline şişirip uyandırıyoruz!

submission_df['id'] = submission_df.id.astype(int)

# Dosyaya kaydet! Geçmiş olsun, bir Makine Öğrenmesi Projesini harika bitirdik.
submission_df.to_csv("submission_demand.csv", index=False)
