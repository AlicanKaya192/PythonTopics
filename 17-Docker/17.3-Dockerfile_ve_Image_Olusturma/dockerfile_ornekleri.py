# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════╗
║   02 — Dockerfile Yazma & Image Build Etme             ║
║   Alican Kaya | Data Science RoadMap                    ║
╚══════════════════════════════════════════════════════════╝

Bu modül farklı senaryolar için Dockerfile örnekleri üretir,
build eder ve karşılaştırır. Docker kurulu olması gerekir.
"""

import os
import subprocess
import time
import sys
from pathlib import Path

BUILD_DIR = Path("./docker_build_demo")


def run(cmd: str, desc: str = "") -> tuple[int, str]:
    if desc:
        print(f"\n🔧 {desc}")
    print(f"$ {cmd}")
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if r.stdout:
        print(r.stdout.strip())
    if r.returncode != 0 and r.stderr:
        print(f"⚠️  {r.stderr.strip()}")
    return r.returncode, r.stdout


def write_file(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  📄 Oluşturuldu: {path}")


# ──────────────────────────────────────────────
# SENARYO 1: Basit Python Script
# ──────────────────────────────────────────────
def scenario_01_simple_python():
    """En basit Python Dockerfile"""
    print("\n" + "="*60)
    print("📦 SENARYO 1: Basit Python Script")
    print("="*60)

    d = BUILD_DIR / "s1_simple"

    write_file(d / "app.py", '''\
#!/usr/bin/env python3
"""Basit Merhaba Dünya uygulaması."""
import platform
import os

print("=" * 40)
print("🐳 Docker Container İçinden Merhaba!")
print(f"Python: {platform.python_version()}")
print(f"OS: {platform.system()} {platform.release()}")
print(f"Hostname: {os.environ.get('HOSTNAME', 'unknown')}")
print(f"Mesaj: {os.environ.get('MESAJ', 'Varsayılan mesaj')}")
print("=" * 40)
''')

    write_file(d / "Dockerfile", '''\
# Base image: Official Python slim
FROM python:3.11-slim

# Metadata
LABEL maintainer="Alican Kaya" version="1.0" description="Basit Python Demo"

# Çalışma dizini
WORKDIR /app

# Uygulama kodunu kopyala
COPY app.py .

# Ortam değişkeni (varsayılan)
ENV MESAJ="Docker ile çalışıyorum!"

# Container başlayınca çalış
CMD ["python", "app.py"]
''')

    run(f"docker build -t demo_simple:1.0 {d}", "Image'ı build et")
    run("docker images demo_simple", "Image boyutunu kontrol et")
    run(
        'docker run --rm -e MESAJ="Merhaba Dünya!" demo_simple:1.0',
        "Container'ı çalıştır"
    )


# ──────────────────────────────────────────────
# SENARYO 2: Flask API
# ──────────────────────────────────────────────
def scenario_02_flask_api():
    """Flask REST API Dockerfile"""
    print("\n" + "="*60)
    print("📦 SENARYO 2: Flask REST API")
    print("="*60)

    d = BUILD_DIR / "s2_flask"

    write_file(d / "requirements.txt", "flask==3.0.0\ngunicorn==21.2.0")

    write_file(d / "app.py", '''\
from flask import Flask, jsonify
import os, platform

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({
        "mesaj": "Flask API çalışıyor!",
        "python": platform.python_version(),
        "ortam": os.environ.get("FLASK_ENV", "production")
    })

@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
''')

    write_file(d / "Dockerfile", '''\
FROM python:3.11-slim

# Güvenlik: root olmayan kullanıcı
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Önce bağımlılıkları kopyala (cache optimizasyonu)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Sonra kodu kopyala
COPY --chown=appuser:appuser app.py .

ENV FLASK_ENV=production

EXPOSE 5000

# Non-root user'a geç
USER appuser

HEALTHCHECK --interval=30s --timeout=5s \\
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')"

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
''')

    write_file(d / ".dockerignore", "__pycache__/\n*.pyc\n.env\nvenv/\n.git/")

    run(f"docker build -t demo_flask:1.0 {d}", "Flask image'ını build et")
    run("docker run -d --name flask_demo -p 5001:5000 demo_flask:1.0", "Başlat")
    time.sleep(2)
    run("curl -s http://localhost:5001/ | python3 -m json.tool", "API'ye istek gönder")
    run("curl -s http://localhost:5001/health", "Health check")
    run("docker rm -f flask_demo", "Temizle")


# ──────────────────────────────────────────────
# SENARYO 3: Multi-stage Build
# ──────────────────────────────────────────────
def scenario_03_multistage():
    """Multi-stage build ile boyut optimizasyonu"""
    print("\n" + "="*60)
    print("📦 SENARYO 3: Multi-stage Build — Boyut Optimizasyonu")
    print("="*60)

    d = BUILD_DIR / "s3_multistage"

    write_file(d / "requirements.txt",
               "numpy==1.26.4\npandas==2.1.4\nscikit-learn==1.4.0")

    write_file(d / "app.py", '''\
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

# Basit ML demo
X = np.array([[1], [2], [3], [4], [5]])
y = np.array([2, 4, 5, 4, 5])
model = LinearRegression().fit(X, y)
pred = model.predict([[6]])
print(f"Linear Regression tahmini (x=6): {pred[0]:.2f}")
print(f"numpy: {np.__version__}, pandas: {pd.__version__}")
''')

    # Normal Dockerfile
    write_file(d / "Dockerfile.normal", '''\
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
CMD ["python", "app.py"]
''')

    # Multi-stage Dockerfile
    write_file(d / "Dockerfile.optimized", '''\
# Stage 1: Build — ağır araçlar burada
FROM python:3.11-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Production — sadece runtime
FROM python:3.11-slim AS production
WORKDIR /app
# Sadece kurulmuş paketleri al
COPY --from=builder /install /usr/local
COPY app.py .
CMD ["python", "app.py"]
''')

    print("\n🏗️  Normal Dockerfile build ediliyor...")
    run(f"docker build -f {d}/Dockerfile.normal -t demo_normal:1.0 {d}",
        "Normal build")

    print("\n🏗️  Multi-stage Dockerfile build ediliyor...")
    run(f"docker build -f {d}/Dockerfile.optimized -t demo_optimized:1.0 {d}",
        "Optimized build")

    run(
        "docker images --format 'table {{.Repository}}\\t{{.Tag}}\\t{{.Size}}' | grep demo",
        "Boyut karşılaştırması"
    )

    run("docker run --rm demo_optimized:1.0", "Optimized container çalıştır")


# ──────────────────────────────────────────────
# SENARYO 4: Cache Analizi
# ──────────────────────────────────────────────
def scenario_04_cache_demo():
    """Build cache nasıl çalışır?"""
    print("\n" + "="*60)
    print("📦 SENARYO 4: Layer Cache Analizi")
    print("="*60)

    d = BUILD_DIR / "s4_cache"

    write_file(d / "requirements.txt", "requests==2.31.0")
    write_file(d / "app.py", "print('v1.0 — ilk build')")
    write_file(d / "Dockerfile", '''\
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
CMD ["python", "app.py"]
''')

    print("\n⏱️  1. Build (soğuk start — cache yok):")
    t0 = time.time()
    run(f"docker build -t demo_cache:1.0 {d}", "İlk build")
    t1 = time.time()
    print(f"⏱️  Süre: {t1-t0:.1f}s")

    # Sadece app.py değiştir
    (d / "app.py").write_text("print('v2.0 — sadece kod değişti')", encoding="utf-8")

    print("\n⏱️  2. Build (sadece app.py değişti — pip cache'lendi):")
    t0 = time.time()
    run(f"docker build -t demo_cache:2.0 {d}", "İkinci build (cache'li)")
    t1 = time.time()
    print(f"⏱️  Süre: {t1-t0:.1f}s  ← pip install CACHE'DEN geldi!")

    run("docker run --rm demo_cache:2.0", "Yeni versiyonu çalıştır")


# ──────────────────────────────────────────────
# SENARYO 5: Data Science Container
# ──────────────────────────────────────────────
def scenario_05_datascience():
    """Data Science Jupyter Notebook container'ı"""
    print("\n" + "="*60)
    print("📦 SENARYO 5: Data Science Container")
    print("="*60)

    d = BUILD_DIR / "s5_datascience"

    write_file(d / "requirements.txt",
               "jupyter==1.0.0\npandas==2.1.4\nmatplotlib==3.8.2\nseaborn==0.13.2\nnumpy==1.26.4")

    write_file(d / "Dockerfile", '''\
FROM python:3.11-slim

# Sistem bağımlılıkları
RUN apt-get update && apt-get install -y --no-install-recommends \\
    gcc g++ \\
    && rm -rf /var/lib/apt/lists/*

# Non-root kullanıcı
RUN useradd -m -u 1000 datascientist
WORKDIR /home/datascientist/work

# Bağımlılıklar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

USER datascientist
EXPOSE 8888

CMD ["jupyter", "notebook", "--no-browser", "--ip=0.0.0.0", "--port=8888"]
''')

    print("""
    📓 Data Science Container Kullanımı:
    
    docker build -t ds-notebook:latest .
    
    docker run -d \\
      --name ds_lab \\
      -p 8888:8888 \\
      -v $(pwd)/notebooks:/home/datascientist/work \\
      ds-notebook:latest
    
    Tarayıcıda: http://localhost:8888
    """)


def main():
    print("""
╔══════════════════════════════════════════════════════════╗
║         DOCKERFILE & IMAGE YÖNETİMİ — DEMO             ║
╚══════════════════════════════════════════════════════════╝
    """)

    r = subprocess.run("docker info", shell=True, capture_output=True)
    if r.returncode != 0:
        print("❌ Docker çalışmıyor!")
        sys.exit(1)

    scenarios = {
        "1": ("Basit Python Script", scenario_01_simple_python),
        "2": ("Flask REST API", scenario_02_flask_api),
        "3": ("Multi-stage Build", scenario_03_multistage),
        "4": ("Cache Analizi", scenario_04_cache_demo),
        "5": ("Data Science Container", scenario_05_datascience),
        "0": ("Hepsini Çalıştır", None),
    }

    print("📋 Senaryo Menüsü:")
    for k, (n, _) in scenarios.items():
        print(f"  [{k}] {n}")

    choice = input("\nSeçim: ").strip()

    if choice == "0":
        for k, (n, fn) in scenarios.items():
            if fn:
                fn()
    elif choice in scenarios and scenarios[choice][1]:
        scenarios[choice][1]()

    # Temizlik
    print("\n\n🧹 Demo image'larını temizle?")
    if input("(e/h): ").lower() == "e":
        for img in ["demo_simple", "demo_flask", "demo_normal", "demo_optimized", "demo_cache"]:
            run(f"docker rmi -f {img}:1.0 {img}:2.0 2>/dev/null", "")


if __name__ == "__main__":
    main()
