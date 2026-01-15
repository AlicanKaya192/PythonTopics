# =============================================================================
# ReLU (RECTIFIED LINEAR UNIT) AKTİVASYON FONKSİYONU GÖRSELLEŞTİRMESİ
# Bu dosya, derin öğrenme ve yapay sinir ağlarında en çok kullanılan
# aktivasyon fonksiyonlarından biri olan ReLU'yu görselleştirir.
# =============================================================================

# -----------------------------------------------------------------------------
# KÜTÜPHANE İMPORTLARI
# -----------------------------------------------------------------------------

# matplotlib.pyplot: Python'da grafik ve görselleştirme oluşturmak için kullanılır.
# pyplot, MATLAB benzeri bir arayüz sunarak grafik çizmeyi kolaylaştırır.
import matplotlib.pyplot as plt

# numpy: Sayısal hesaplamalar ve dizi işlemleri için temel Python kütüphanesi.
# Matematiksel işlemler, dizi manipülasyonu ve sayısal analiz için kullanılır.
import numpy as np

# -----------------------------------------------------------------------------
# ReLU AKTİVASYON FONKSİYONU TANIMI
# -----------------------------------------------------------------------------

def relu(x):
    """
    ReLU (Rectified Linear Unit) aktivasyon fonksiyonu.
    
    ReLU, modern derin öğrenmenin temel taşlarından biridir ve şu formüle sahiptir:
    f(x) = max(0, x)
    
    Davranış:
    - x < 0 için: çıktı = 0 (negatif değerler sıfırlanır)
    - x >= 0 için: çıktı = x (pozitif değerler değişmeden geçer)
    
    ReLU'nun Avantajları:
    1. Hesaplama açısından çok basit ve hızlı
    2. Vanishing gradient (kaybolan gradyan) problemini azaltır
    3. Sparse activation (seyrek aktivasyon) sağlar - bazı nöronlar aktif olmaz
    4. Sigmoid/Tanh'a göre daha hızlı yakınsama (convergence)
    
    ReLU'nun Dezavantajları:
    1. "Dying ReLU" problemi - negatif girişlerde nöron kalıcı olarak ölebilir
    2. Çıktının maksimum değeri sınırsızdır (unbounded)
    3. Sıfır noktasında türev tanımsızdır (pratik uygulamada 0 veya 1 alınır)
    
    Alternatif ReLU Varyantları:
    - Leaky ReLU: f(x) = max(αx, x), α küçük bir pozitif sayı (örn. 0.01)
    - Parametric ReLU (PReLU): α öğrenilebilir parametre
    - ELU (Exponential Linear Unit): Negatif bölgede eksponansiyel
    - GELU (Gaussian Error Linear Unit): Stokastik yaklaşım
    
    Args:
        x (numpy.ndarray veya float): Giriş değer(ler)i
    
    Returns:
        numpy.ndarray veya float: ReLU uygulanmış çıktı değer(ler)i
    
    Matematiksel İfade:
        ReLU(x) = max(0, x) = { 0,  x < 0
                              { x,  x >= 0
    """
    # np.maximum: Element-wise maksimum hesaplar.
    # 0 ile x arasındaki maksimum değeri döndürür.
    # Bu, negatif değerleri 0'a çevirirken pozitif değerleri korur.
    return np.maximum(0, x)

# -----------------------------------------------------------------------------
# VERİ HAZIRLAMA
# -----------------------------------------------------------------------------

# Örnek veri oluştur - X ekseni değerleri.
# np.linspace: Belirtilen aralıkta eşit aralıklı noktalar oluşturur.
# -5'ten 5'e kadar 100 nokta oluşturuyoruz.
# Sample data
x = np.linspace(-5, 5, 100)

# ReLU fonksiyonunu uygula - Y ekseni değerleri.
# x değerlerinin her birine ReLU uygulanır.
# Apply ReLU
y = relu(x)

# -----------------------------------------------------------------------------
# GRAFİK ÇİZİMİ
# -----------------------------------------------------------------------------

# ReLU fonksiyonunun grafiğini çiz.
# plt.plot: Çizgi grafiği oluşturur.
# Plot 
plt.plot(x, y)

# X ekseni etiketi ekle.
plt.xlabel('Input')

# Y ekseni etiketi ekle.
plt.ylabel('Output')

# Grafik başlığı ekle.
plt.title('ReLU Activation Function')

# Grafik arka planına ızgara (grid) ekle.
# Bu, değerlerin okunmasını kolaylaştırır.
plt.grid(True)

# Grafiği ekranda göster.
# Bu satır, matplotlib penceresini açar ve grafiği görüntüler.
plt.show()

# =============================================================================
# ReLU'NUN DERİN ÖĞRENME TARİHÇESİNDEKİ ÖNEMİ:
# =============================================================================
#
# 1. TARİHSEL BAĞLAM:
#    - 2012 AlexNet'in ImageNet yarışmasını kazanmasıyla popülerleşti
#    - Öncesinde Sigmoid ve Tanh gibi fonksiyonlar kullanılıyordu
#    - ReLU, derin ağların eğitimini çok hızlandırdı
#
# 2. VANISHING GRADIENT PROBLEMİ:
#    - Sigmoid/Tanh: Büyük değerlerde gradyan çok küçülür (0'a yaklaşır)
#    - Bu, derin ağlarda ilk katmanların öğrenmesini engeller
#    - ReLU: Pozitif bölgede gradyan her zaman 1'dir
#    - Bu sayede gradyan "kaybolmaz"
#
# 3. HESAPLAMA VERİMLİLİĞİ:
#    - Sigmoid: exp() ve bölme işlemi gerektirir
#    - ReLU: Sadece max(0, x) - çok hızlı
#    - GPU'larda önemli hız artışı sağlar
#
# 4. BİYOLOJİK İLHAM:
#    - Gerçek nöronlar ya aktif ya da pasif
#    - Bu "ya hep ya hiç" davranışı ReLU ile modellenebilir
#    - Sparse coding (seyrek kodlama) konseptine uygundur
#
# =============================================================================
