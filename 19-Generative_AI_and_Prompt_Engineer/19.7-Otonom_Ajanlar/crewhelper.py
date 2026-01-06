# =======================================================================================
# DOSYA: crewhelper.py
# AÇIKLAMA: CrewAI çerçevesi için ajan ve görev tanımlarını içeren yardımcı modül.
#
# KONU: OTONOM AJANLAR - Çoklu Ajan Yaklaşımı (Multi-Agent Approach)
# 
# Bu modül, kişilik testi geliştirme projesi için kullanılacak ajanları ve
# görevleri tanımlar. CrewAI çerçevesiyle entegre çalışır.
#
# CREWAI AJAN MİMARİSİ
# ====================
# CrewAI'de her ajan belirli özelliklere sahiptir:
#
# 1. ROLE (Rol):
#    - Ajanın mesleği veya uzmanlık alanı
#    - Örnek: "Yazılım Mühendisi", "Veri Analisti"
#
# 2. GOAL (Hedef):
#    - Ajanın birincil amacı
#    - Ne başarmak istediğini tanımlar
#
# 3. BACKSTORY (Arka Hikaye):
#    - Ajanın karakteri ve deneyimi
#    - Davranış ve karar verme sürecini etkiler
#    - LLM'e bağlam sağlar
#
# 4. LLM (Dil Modeli):
#    - Ajanın kullandığı yapay zeka modeli
#    - GPT-4, Gemini Pro vb. olabilir
#
# 5. ALLOW_DELEGATION:
#    - True: Ajan görevleri başka ajanlara delege edebilir
#    - False: Ajan sadece kendi görevini yapar
#
# CREWAI GÖREV (TASK) MİMARİSİ
# ============================
# Her görev şunları içerir:
#
# 1. DESCRIPTION (Açıklama):
#    - Görevin detaylı tanımı
#    - Beklentiler ve kriterler
#
# 2. AGENT (Ajan):
#    - Görevi yürütecek ajan
#
# 3. EXPECTED_OUTPUT (Beklenen Çıktı):
#    - Görevin sonucu olarak ne bekleniyor
#    - Opsiyonel ama önerilir
#
# PROMPT MÜHENDİSLİĞİ İPUÇLARI
# =============================
# Bu dosyada görülen prompt teknikleri:
#
# 1. ROL ATAMA: "Sen bir kişilik testleri uzmanısın"
# 2. BAĞLAM SAĞLAMA: Detaylı backstory ile deneyim tanımlama
# 3. ADIM ADIM TALİMATLAR: Ne yapılacağını sırayla açıklama
# 4. KISITLAMALAR: "Birkaç örnek verip... gibi yaklaşımlar sergileme"
# 5. KALİTE KRİTERLERİ: "Tüm içeriği verdiğinden emin ol"
# =======================================================================================

from crewai import Agent, Task  # CrewAI'nin temel sınıfları

# =======================================================================================
# AJAN TANIMLARI
# =======================================================================================
# Her ajan fonksiyonu, belirli bir rol için yapılandırılmış bir Agent nesnesi döndürür.
# Ajanlar, crewai.py dosyasında oluşturulup Crew'e eklenir.
# =======================================================================================


def test_expert(llm):
    """
    Kişilik Testleri Uzmanı ajanı oluşturur.
    
    Bu ajan, kişilik testleri konusunda derin bilgiye sahip bir uzmanı temsil eder.
    Görevleri:
    - Kişilik tiplerini tanımlamak
    - Test sorularını hazırlamak
    - Değerlendirme kriterlerini belirlemek
    - Sonuç metinlerini yazmak
    
    Parametreler:
    -------------
    llm: CrewAI'nin kullanacağı dil modeli (ChatOpenAI veya ChatGoogleGenerativeAI)
    
    Returns:
        Agent: Yapılandırılmış CrewAI Agent nesnesi
    """
    return Agent(
        # ROLE: Ajanın profesyonel kimliği
        # LLM bu role uygun davranışlar sergiler
        role='Kişilik Testleri Uzmanı',
        
        # GOAL: Ajanın birincil hedefi
        # Tüm kararlar bu hedefe ulaşmak için verilir
        goal='Bireylerin kişilik özelliklerini belirlemekte kullanılan kişilik testleri geliştirmek.',
        
        # BACKSTORY: Ajanın karakterini tanımlayan detaylı arka plan hikayesi
        # Bu prompt, LLM'e nasıl davranması gerektiğini öğretir
        backstory=f"""
                    Sen bir kişilik testleri uzmanısın. Kişilik ve karakter özelliklerini belirlemekte kullanılan psikometrik testler hakkında oldukça kapsamlı bilgi sahibisin.
                    Kişilik testleri oluşturmak için gerekli tüm bileşenleri hazırlayabiliyorsun.
                    Bu bileşenler şöyle: 
                    kişilik tipleri ve tanımları, 
                    kişilik tipleri için temel karaktör özellikleri ve tanımları,
                    kişilik tipleri ve karakter özelliklerini belirlemek üzere kullanılacak sorular,
                    sorulara verilen yanıtlara göre kişilik tipi ve bu kişilik tipinin temel özelliklerini hesaplama yarayan formül veya algoritma,
                    kişilik testi sonunda her bir kişilik tipi içiğn özet metinleri.
                    Tüm bu bileşenleri sırasıyla ve birbirleriyle uyumlu olacak şekilde hazırlıyorsun.
                    Bu bileşenleri hazırlarken halihazırda kullanılmakta olan Big Five, 4 Renk Kişilik Testi, 16 Personalities testi gibi bilindik örnekleri dikkate alıyorsun.
                    Senden bir kişilik testi hazırlaman istendiğinde bu bileşenleri oluşturmak için ihtiyaç duyduğun bilgiler verilmiş mi diye bakıyorsun.
                    Eğer daha fazla bilgi ya da detay gerekirse, bunları talep ediyorsun.
                    Eğer daha fazla bilgi ya da detay verilirse bunlara göre bileşenleri hazırlıyorsun.
                    Ama eğer daha fazla bilgi ya da detay verilmezse, eldeki talimatlara uygun biçimde bileşenleri hazırlamaya başlıyorsun.
                    Senden bir kişilik testi istendiğinde bütün bileşenlerinin içeriğini tam ve eksiksiz olarak veriyorsun.
                    Birkaç örnek verip gerisini siz de böyle yapabilirsiniz gibi yaklaşımlar sergileme.
                    Tüm içeriği verdiğinden emin ol.
        """,
        # ALLOW_DELEGATION: False = Bu ajan görev delege edemez
        # Her ajan kendi işini yapar, başkasına devretmez
        allow_delegation=False,
        
        # LLM: Kullanılacak dil modeli (GPT-4, Gemini Pro vb.)
        llm=llm,
        
        # VERBOSE: True ise detaylı log çıktısı verir
        # Debugging ve ajanın düşünce sürecini görmek için kullanışlı
        verbose=True
    )


def software_engineer(llm):
    """
    Yazılım Mühendisi ajanı oluşturur.
    
    Bu ajan, deneyimli bir Python geliştiricisini temsil eder.
    Özellikle Streamlit uygulamaları geliştirmede uzmanlaşmıştır.
    
    Görevleri:
    - Proje isterlerini analiz etmek
    - Python Streamlit kodu yazmak
    - Tek dosyada çalışan uygulamalar üretmek
    
    Parametreler:
    -------------
    llm: CrewAI'nin kullanacağı dil modeli
    
    Returns:
        Agent: Yapılandırılmış yazılım mühendisi ajanı
    """
    return Agent(
        role='Yazılım Mühendisi',
        
        goal='Verilen isterlere uygun biçimde Python yazılımları için geliştirme yapmak ve gerekli kodları yazmak',
        
        # BACKSTORY: Yazılım geliştirme sürecini tanımlar
        # Önemli kısıtlamalar:
        # 1. Tek .py dosyası üretmeli (harici dosya çağırmamalı)
        # 2. Tüm kodu vermeli (eksik bırakmamalı)
        # 3. Her bileşen için uygun Streamlit widget'ı kullanmalı
        backstory=f"""
                    Sen deneyimli bir yazılım mühendisisin. Sana verilen proje isterlerine uygun olarak gerekli yazılımın tasarımının nasıl olması gerektiğine karar veriyor
                    ve gerekli Python Streamlit kodlarını yazıyorsun. Yazılım geliştirmeye başlamadan önce daha fazla bilgiye veya açıklamaya ihtiyacın varsa, bunları talep et.
                    Eğer daha fazla bilgi ve açıklama verilirse yazılımı geliştirirken bunlara göre hareket et.
                    Ama eğer daha fazla bilgi ya da açıklama verilmezse, başlangıçtaki proje isterlerine göre yazılımını geliştir.
                    Geliştirme işlemini tamamladığında daima tüm kodları ver.
                    Yazdığın kod dışardan herhangi bir başka dosya çağırmamalı. Her şey tek bir .py dosyası içinde gerçekleşmeli.
                    Kişilik testi için oluşturulan her bir bileşeni Streamlit'te doğru bir widget ile dahil etmelisin.
                    Kodların bir kısmını yazıp şu kısmı da siz yazın ya da benim yazdığım gibi siz de geriye kalanları tamamlayın gibi bir yanıt verme.
                    Her zaman tam ve bitmiş kodu ver.
        """,
        allow_delegation=False,
        llm=llm,
        verbose=True
    )


def test_consultant(llm):
    """
    Kişilik Testleri Danışmanı ajanı oluşturur.
    
    Bu ajan, hazırlanan testleri inceleyen bir kalite kontrol uzmanıdır.
    Görevleri:
    - Testleri hatalara karşı incelemek
    - İyileştirme önerileri sunmak
    - Profesyonel standartlara uyumu kontrol etmek
    
    Parametreler:
    -------------
    llm: CrewAI'nin kullanacağı dil modeli
    
    Returns:
        Agent: Yapılandırılmış danışman ajanı
    """
    return Agent(
        role='Kişilik Testleri Danışmanı',
        
        goal='Hazırlanan kişilik testlerini incelemek ve daha iyi hale getirmek üzere öneriler vermek',
        
        # BACKSTORY: İnceleme kriterlerini tanımlar
        # 1. Hata tespiti ve düzeltme önerileri
        # 2. İyileştirme önerileri
        # 3. Profesyonel testlerle uyum kontrolü
        # 4. Proje isterlerine uyum kontrolü
        backstory=f"""
                    Sen deneyimli bir danışmansın ve kişilik testleri konusunda kapsamlı bilgiye sahipsin.
                    Hazırlanan kişilik testlerini incele.
                    Eğer hatalar varsa bunları söyle ve nasıl düzeltilebileceklerini belirt.
                    Eğer iyileştirilecek yönler varsa bunları söyle ve nasıl yapılabileceğini belirt.
                    İncelemelerini yaparken ve geri bildirimlerini verirken başlangıçta sunulan proje isterlerine uyumlu olma durumunu dikkate al.
                    İncelemelerini yaparken ve geri bildirimlerini verirken ayrıca oluşan kişilik testi içeriğinin yaygın uygulamalar ve 
                    Big Five, 4 Renk Kişilik Testi, 16 Personalities testi gibi profesyonel testlerle çelişen yönler içermemesine dikkat et.
                    Verdiğin öneriler doğrudan aksiyona yönelik olsun. Problemin ne olduğunu ve ne yapılması gerektiğini söyle. Uzun açıklamalar yapma.
                    Eğer hazırlanan kişilikt testi yeterli durumdaysa düzeltme ya da öneri verme. Kullanıma hazır olduğunu söyle.
        """,
        allow_delegation=False,
        llm = llm,
        verbose=True
    )


# =======================================================================================
# GÖREV (TASK) TANIMLARI
# =======================================================================================
# Her görev fonksiyonu, belirli bir iş için yapılandırılmış bir Task nesnesi döndürür.
# Görevler, Crew'e eklenerek sıralı veya paralel şekilde yürütülür.
#
# Task Parametreleri:
# - description: Görevin detaylı açıklaması (LLM bunu okur)
# - agent: Görevi yürütecek ajan
# - expected_output: Beklenen çıktı formatı (opsiyonel)
# =======================================================================================


def create_test_task(instructions, agent):
    """
    Kişilik testi geliştirme görevi oluşturur.
    
    Bu görev, test uzmanı ajanına atanır ve kişilik testinin
    tüm bileşenlerini hazırlamasını ister.
    
    Parametreler:
    -------------
    instructions (str): Proje isterleri ve talimatlar
    agent (Agent): Görevi yürütecek ajan (test_expert)
    
    Returns:
        Task: Yapılandırılmış CrewAI Task nesnesi
    """
    return Task(description=f"""
        Bir kişilik testi geliştirilmesi projesinde görev alıyorsun. Proje isterleri aşağıda yer alıyor.
            
        Proje İsterleri: 
        ------------
        {instructions}

        ------------
        Burada belirtilen isterlere uygun olarak bir kişilik testi hazırla.
        Bunun için gerekli tüm bileşenleri oluştur.

        Verdiğin nihai yanıt tüm bileşenleri içermeli ve tüm bileşenler eksiksiz yazılmış olmalı.
        """,
        agent=agent)  # Bu görev test uzmanı ajanına atanır


def create_review_task(instructions, agent):
    """
    Test inceleme görevi oluşturur.
    
    Bu görev, danışman ajanına atanır ve daha önce hazırlanan
    kişilik testini inceleyip geri bildirim vermesini ister.
    
    Parametreler:
    -------------
    instructions (str): Proje isterleri (uyum kontrolü için)
    agent (Agent): Görevi yürütecek ajan (test_consultant)
    
    Returns:
        Task: Yapılandırılmış inceleme görevi
    """
    return Task(description=f"""
        Bir kişilik testi geliştirilmesi projesinde görev alıyorsun. Proje isterleri aşağıda yer alıyor.
            
        Proje İsterleri: 
        ------------
        {instructions}

        ------------
        Burada belirtilen isterlere uygun olarak, hazırlanmış olan kişilik testini incele.
        Bu kişilik testinde hata varsa belirt ve nasıl düzeltilebileceğini söyle.
        Bu kişilik testini daha iyi hale getirmek için önerilerin varsa belirt.
        Eğer kişilik testinin içeriği yeterli ise kullanıma hazır olduğunu söyle.

        Verdiğin nihai yanıt öneriler ve düzeltmelerini ya da her şey yolunda ise kişilik testinin kullanıma hazır olduğunu belirten tarzda olmalı.
        """,
        agent=agent)  # Bu görev danışman ajanına atanır


def create_code_task(instructions, agent):
    """
    Python Streamlit kodu yazma görevi oluşturur.
    
    Bu görev, yazılım mühendisi ajanına atanır ve hazırlanan
    kişilik testini çalışan bir Streamlit uygulamasına dönüştürmesini ister.
    
    Parametreler:
    -------------
    instructions (str): Proje isterleri
    agent (Agent): Görevi yürütecek ajan (software_engineer)
    
    Returns:
        Task: Yapılandırılmış kod yazma görevi
    
    Not:
    ----
    Bu görevin çıktısı, doğrudan çalıştırılabilir Python kodu olmalıdır.
    Crew'in final çıktısı genellikle bu görevin sonucu olur.
    """
    return Task(description=f"""
        Bir kişilik testi geliştirilmesi projesinde görev alıyorsun. Proje isterleri aşağıda yer alıyor.
            
        Proje İsterleri: 
        ------------
        {instructions}

        ------------
        Burada belirtilen isterlere uygun olarak, hazırlanmış olan kişilik testini kullanıcılara sunmak için gerekli Python Streamlit kodunu yaz.
        Kodu doğru ve hatasız yazdığından emin ol.

        Verdiğin nihai yanıt tamamlanmış Python kodu olmalı. Kodu eksiksik olarak verdiğinden emin ol.
        """,
        agent=agent)  # Bu görev yazılım mühendisi ajanına atanır
