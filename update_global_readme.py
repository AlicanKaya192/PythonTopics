import os

lines = []
with open('README.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip = False
for line in lines:
    if line.strip() == "<details>":
        if "138" not in globals():
            skip = True
    
    if line.strip() == "[⬆️ Başa Dön](#-i̇çindekiler)":
        if skip:
            skip = False
            
            # Insert the new content
            new_lines.append("Her modülün detaylı içeriği kendi klasöründeki `README.md` dosyasında yer almaktadır. Lütfen aşağıdaki bağlantılara tıklayarak ilgili modüle gidiniz.\n\n")
            new_lines.append("* [0️⃣ Python Temelleri](./0-Python_Temelleri/README.md)\n")
            new_lines.append("* [1️⃣ Çalışma Ortamı Ayarları](./01-Çalışma_Ortamı_Ayarları/README.md)\n")
            new_lines.append("* [2️⃣ Veri Yapıları](./02-Veri_Yapıları/README.md)\n")
            new_lines.append("* [3️⃣ Fonksiyonlar, Koşullar, Döngüler ve Comprehensions](./03-Fonksiyonlar,_Koşullar,_Döngüler_anlamalar/README.md)\n")
            new_lines.append("* [4️⃣ Egzersizler (Python ve List Comprehensions)](./04-Egzersizler_Python_ve_List_Comprehensions_/README.md)\n")
            new_lines.append("* [5️⃣ Numpy](./05-Numpy/README.md)\n")
            new_lines.append("* [6️⃣ Pandas](./06-Pandas/README.md)\n")
            new_lines.append("* [7️⃣ Veri Görselleştirme (Matplotlib & Seaborn)](./07-Veri_Görselleştirme_Matplotlib_&_Seaborn/README.md)\n")
            new_lines.append("* [8️⃣ Gelişmiş Fonksiyonel Keşifçi Veri Analizi (EDA)](./08-Gelişmiş_Fonksiyonel_Keşifçi_Veri_Analizi/README.md)\n")
            new_lines.append("* [9️⃣ CRM Analitik](./09-CRM_Analitik/README.md)\n")
            new_lines.append("* [1️⃣0️⃣ Ölçümleme Problemleri](./10-Ölçümleme_Problemleri/README.md)\n")
            new_lines.append("* [1️⃣1️⃣ Tavsiye Sistemleri (Recommendation Systems)](./11-Tavsiye_Sistemleri/README.md)\n")
            new_lines.append("* [1️⃣2️⃣ Feature Engineering (Özellik Mühendisliği)](./12-Feature_Engineering_Özellik_Mühendisliği_/README.md)\n")
            new_lines.append("* [1️⃣3️⃣ Machine Learning (Makine Öğrenimi)](./13-Machine_Learning_Makine_Öğrenimi_/README.md)\n")
            new_lines.append("* [1️⃣4️⃣ GIT](./14-GIT/README.md)\n")
            new_lines.append("* [1️⃣5️⃣ SQL](./15-SQL/README.md)\n")
            new_lines.append("* [1️⃣6️⃣ Time Series](./16-Time_Series/README.md)\n")
            new_lines.append("* [1️⃣7️⃣ Docker](./17-Docker/README.md)\n")
            new_lines.append("* [1️⃣9️⃣ Natural Language Processing (NLP)](./19-Natural_Language_Processing_(NLP)/README.md)\n")
            new_lines.append("* [2️⃣0️⃣ Generative AI & Prompt Engineer](./20-Generative_AI_and_Prompt_Engineer/README.md)\n\n")

    if not skip:
        new_lines.append(line)

with open('README.md', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Global README updated successfully!")
