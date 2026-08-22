# Reinforcement Learning (Pekiştirmeli Öğrenme)

Bir ajanın, bir ortam içinde deneme-yanılma yoluyla, aldığı ödülleri uzun vadede maksimize edecek şekilde
davranmayı öğrendiği makine öğrenmesi paradigması.
- **21.1 - Temel Kavramlar:**
    - **21.1.1 - Pekiştirmeli Öğrenmeye Giriş.pdf:** Ajan, Ortam, Durum, Eylem, Ödül ve Politika kavramları; Markov Karar Süreçleri (MDP); Keşif vs. Sömürü (Exploration vs. Exploitation) ikilemi ve ε-greedy strateji.
    - **21.1.2 - Tekrar_İçin_Sorular.pdf:** 21.1 konusuna özel 12 soruluk çoktan seçmeli test ve cevap anahtarı.
- **21.2 - Q-Learning:**
    - **21.2.1 - Q_Learning_Nedir.pdf:** Q-değeri kavramı, Bellman denklemi ve güncelleme kuralı, FrozenLake ortamı üzerinden uygulama, hiperparametreler ve tablo tabanlı yöntemlerin sınırları.
    - **21.2.2_q_learning_frozenlake.py / .ipynb:** Gymnasium'un FrozenLake-v1 ortamında sıfırdan Q-Learning uygulaması. Eğitim eğrisi görselleştirmesi, öğrenilen Q-tablosu ve politika, öğrenilen politikanın test edilmesi.
    - **21.2.3 - Tekrar_İçin_Sorular.pdf:** 21.2 konusuna özel 12 soruluk çoktan seçmeli test ve cevap anahtarı.
- **21.3 - Policy Gradient ve Deep RL:**
    - **21.3.1 - Policy_Gradient_ve_DQN.pdf:** Politika tabanlı yöntemlere neden ihtiyaç duyulduğu, REINFORCE algoritması (log-türev hilesi ve gradyan formülü), Derin Q-Ağı (DQN) kavramsal çerçevesi (deneyim tekrarı, hedef ağ), CartPole örneği.
    - **21.3.2_dqn_cartpole.py / .ipynb:** Gymnasium'un CartPole-v1 ortamında, tamamen NumPy ile sıfırdan yazılmış bir REINFORCE (politika gradyanı) uygulaması. Softmax politika ağı, indirgenmiş getiri hesaplama, eğitim eğrisi ve öğrenilmiş politikanın test edilmesi.
    - **21.3.3 - Tekrar_İçin_Sorular.pdf:** 21.3 konusuna özel 12 soruluk çoktan seçmeli test ve cevap anahtarı.
- **21.4 - Genel Tekrar Soruları:**
    - **21.4.1 - Genel_Tekrar_İçin_Sorular.pdf:** Modülün tamamını (21.1 - 21.3) kapsayan 20 soruluk çoktan seçmeli test ve cevap anahtarı.

> **🔗 Ek Kaynaklar:**
>
> *   [Gymnasium Dokümantasyonu](https://gymnasium.farama.org/) — Bu modülde kullanılan FrozenLake-v1 ve CartPole-v1 ortamlarının resmi dokümantasyonu.
> *   [Sutton & Barto - Reinforcement Learning: An Introduction](http://incompleteideas.net/book/the-book-2nd.html) — Alanın temel referans kitabı (ücretsiz PDF).
> *   [Human-level control through deep reinforcement learning (DQN, Nature 2015)](https://www.nature.com/articles/nature14236) — DQN'i tanıtan orijinal DeepMind makalesi.
