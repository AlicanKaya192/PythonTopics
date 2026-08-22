################################################
# Q-LEARNING İLE FROZENLAKE ORTAMINI ÇÖZMEK
################################################

# İş Problemi: Bir ajanın, buzlu bir gölün üzerinde (4x4'lük ızgara) başlangıç noktasından
# hedefe, buz deliklerine düşmeden ulaşmasını sağlayacak bir strateji (politika) öğrenmesi.
# Bu script, 21.2.1-Q_Learning_Nedir.pdf dosyasında anlatılan Bellman güncelleme kuralının
# uçtan uca, çalışan bir Python uygulamasıdır.

# Gerekli kütüphaneyi kurmak için: pip install gymnasium

import numpy as np
import gymnasium as gym
import matplotlib.pyplot as plt

import warnings
warnings.simplefilter(action="ignore")

##################################################
# 1. Ortamın Kurulumu
##################################################

# is_slippery=True -> buz kaygandır, seçilen eylem %33 ihtimalle yan yönlere kayabilir (stokastik ortam).
# Bu, gerçek dünyadaki belirsizliği simüle eder ve öğrenmeyi zorlaştırır.
env = gym.make("FrozenLake-v1", is_slippery=True)

n_states = env.observation_space.n   # 16 durum (4x4 ızgara)
n_actions = env.action_space.n       # 4 eylem (0: Sol, 1: Aşağı, 2: Sağ, 3: Yukarı)

print(f"Durum sayısı: {n_states}, Eylem sayısı: {n_actions}")

##################################################
# 2. Q-Tablosunun ve Hiperparametrelerin Tanımlanması
##################################################

# Q-tablosu, her (durum, eylem) çifti için öğrenilen "kalite" değerini tutar.
# Başlangıçta ajan hiçbir şey bilmediği için tüm değerler sıfırdır.
q_table = np.zeros((n_states, n_actions))

alpha = 0.1          # Öğrenme oranı (düşük tutulur: kaygan/stokastik ortamda büyük alpha kararsızlığa yol açar)
gamma = 0.99         # İndirim faktörü (ajan ne kadar "sabırlı")
epsilon = 1.0        # Başlangıç keşif oranı (tamamen rastgele başla)
epsilon_min = 0.01
epsilon_decay = 0.9997

n_episodes = 25000
max_steps_per_episode = 100

##################################################
# 3. Eğitim Döngüsü (Q-Learning)
##################################################

rewards_per_episode = []

for episode in range(n_episodes):
    state, _ = env.reset()
    total_reward = 0

    for step in range(max_steps_per_episode):
        # Epsilon-Greedy eylem seçimi: ya keşfet (rastgele) ya da sömür (en iyi bilineni seç).
        if np.random.uniform(0, 1) < epsilon:
            action = env.action_space.sample()
        else:
            action = np.argmax(q_table[state, :])

        next_state, reward, terminated, truncated, _ = env.step(action)
        done = terminated or truncated

        # Bellman güncelleme kuralı (bkz. 21.2.1-Q_Learning_Nedir.pdf, Bölüm 2):
        # Q(s,a) <- Q(s,a) + alpha * [ r + gamma * max_a' Q(s',a') - Q(s,a) ]
        best_next_q = np.max(q_table[next_state, :])
        td_target = reward + gamma * best_next_q
        td_error = td_target - q_table[state, action]
        q_table[state, action] += alpha * td_error

        state = next_state
        total_reward += reward

        if done:
            break

    # Epsilon'u kademeli olarak azalt (epsilon decay) -> ajan zamanla daha çok sömürü yapar.
    epsilon = max(epsilon_min, epsilon * epsilon_decay)
    rewards_per_episode.append(total_reward)

print("Eğitim tamamlandı.")

##################################################
# 4. Öğrenme Performansının Görselleştirilmesi
##################################################

# Ödüller çok gürültülü (0 ya da 1) olduğu için, 100'lük pencerelerin ortalamasını alarak
# başarı oranındaki (hedefe ulaşma yüzdesi) trendi daha net görebiliriz.
window = 100
success_rate = [
    np.mean(rewards_per_episode[max(0, i - window):i + 1])
    for i in range(len(rewards_per_episode))
]

plt.figure(figsize=(10, 5))
plt.plot(success_rate)
plt.title("FrozenLake - Q-Learning Öğrenme Eğrisi (100 Epizotluk Ortalama Başarı Oranı)")
plt.xlabel("Epizot")
plt.ylabel("Başarı Oranı (Hedefe Ulaşma)")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("frozenlake_q_learning_egri.png", dpi=100)
plt.show()
plt.close()

print(f"Son 1000 epizotun ortalama başarı oranı: {np.mean(rewards_per_episode[-1000:]):.2%}")

##################################################
# 5. Öğrenilen Q-Tablosunu İnceleme
##################################################

print("\nÖğrenilen Q-Tablosu (satırlar: durum 0-15, sütunlar: Sol, Aşağı, Sağ, Yukarı):")
print(np.round(q_table, 3))

# Her durum için ajanın öğrendiği en iyi eylemi okunabilir bir haritaya dönüştürelim.
# NOT: Ok karakterleri yerine ASCII sembolleri kullanılıyor; bazı Windows konsollarının
# varsayılan kod sayfası (cp1254 vb.) Unicode ok karakterlerini yazdıramayıp hataya düşebiliyor.
action_symbols = {0: "<", 1: "v", 2: ">", 3: "^"}
learned_policy = np.array([action_symbols[np.argmax(q_table[s, :])] for s in range(n_states)])
print("\nÖğrenilen Politika (4x4 ızgara):")
print(learned_policy.reshape(4, 4))

##################################################
# 6. Öğrenilmiş Politikayla Test Etme
##################################################

# Artık eğitim bitti; epsilon=0 kabul edip (tamamen sömürü) ajanın gerçekten hedefe ulaşıp
# ulaşamadığını birkaç epizotluk bir testle doğrulayalım.
test_episodes = 100
test_successes = 0

for _ in range(test_episodes):
    state, _ = env.reset()
    for _ in range(max_steps_per_episode):
        action = np.argmax(q_table[state, :])
        state, reward, terminated, truncated, _ = env.step(action)
        if terminated or truncated:
            test_successes += reward
            break

print(f"\nTest sonucu ({test_episodes} epizot, tamamen öğrenilen politika ile): "
      f"{test_successes:.0f}/{test_episodes} başarı ({test_successes / test_episodes:.2%})")

env.close()
