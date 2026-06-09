# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════╗
║   01 — Docker Temel Kavramlar & CLI Komutları           ║
║   Alican Kaya | Data Science RoadMap                    ║
╚══════════════════════════════════════════════════════════╝

Bu dosya Docker temel komutlarını subprocess üzerinden
çalıştırarak sonuçları açıklayan interaktif bir rehberdir.
Docker Desktop / Engine kurulu olması gerekir.
"""

import subprocess
import sys
import json


def run_cmd(cmd: str, desc: str = "", check: bool = False) -> tuple[int, str, str]:
    """Docker komutunu çalıştır ve sonucu döndür."""
    print(f"\n{'─'*60}")
    if desc:
        print(f"📌 {desc}")
    print(f"$ {cmd}")
    print("─" * 60)

    result = subprocess.run(
        cmd, shell=True, capture_output=True, text=True
    )
    if result.stdout:
        print(result.stdout.strip())
    if result.stderr and result.returncode != 0:
        print(f"⚠️  STDERR: {result.stderr.strip()}", file=sys.stderr)
    return result.returncode, result.stdout, result.stderr


def check_docker():
    """Docker kurulu ve çalışıyor mu?"""
    print("\n🐳 Docker Kurulum Kontrolü")
    print("=" * 60)

    code, out, _ = run_cmd("docker --version", "Docker sürümü")
    if code != 0:
        print("❌ Docker bulunamadı! Lütfen Docker Desktop kurulumunu yapın.")
        sys.exit(1)

    run_cmd("docker info --format '{{.ServerVersion}}'", "Docker Engine sürümü")
    print("\n✅ Docker hazır!")


def demo_hello_world():
    """İlk container: hello-world"""
    print("\n\n🚀 İlk Container — Hello World")
    print("=" * 60)
    print("""
    docker run hello-world adımları:
    1. Local'de hello-world image var mı? → Yok
    2. Docker Hub'dan çek (pull)
    3. Image'dan container oluştur (create)  
    4. Container'ı başlat (start)
    5. Ekrana yaz, çık (exit 0)
    """)
    run_cmd("docker run --rm hello-world", "Hello World container'ı çalıştır")


def demo_image_management():
    """Image indirme ve listeleme"""
    print("\n\n📦 Image Yönetimi")
    print("=" * 60)

    # Alpine çek (en küçük Linux)
    run_cmd(
        "docker pull alpine:latest",
        "Alpine Linux image'ı çek (küçük boyutlu)"
    )

    # Image listesi
    run_cmd(
        "docker images --format 'table {{.Repository}}\\t{{.Tag}}\\t{{.Size}}\\t{{.CreatedSince}}'",
        "Tüm local image'ları listele"
    )

    # Image detayları
    run_cmd(
        "docker image inspect alpine:latest --format '{{.Os}}/{{.Architecture}} | {{.Size}} bytes'",
        "Alpine image detayları"
    )


def demo_container_lifecycle():
    """Container yaşam döngüsü"""
    print("\n\n🔄 Container Yaşam Döngüsü")
    print("=" * 60)

    CONTAINER = "demo_lifecycle"

    # Oluştur ve başlat
    run_cmd(
        f"docker run -d --name {CONTAINER} alpine sleep 60",
        "Detach modda container başlat (arka planda)"
    )

    # Durum
    run_cmd(
        f"docker inspect {CONTAINER} --format '{{{{.State.Status}}}}'",
        "Container durumu"
    )

    # Container içinde komut çalıştır
    run_cmd(
        f"docker exec {CONTAINER} sh -c 'echo Merhaba && hostname && date'",
        "Container içinde komut çalıştır"
    )

    # Durdur
    run_cmd(f"docker stop {CONTAINER}", "Container'ı durdur (SIGTERM)")

    # Yeniden başlat
    run_cmd(f"docker start {CONTAINER}", "Durdurulmuş container'ı başlat")

    # Log
    run_cmd(
        f"docker logs --tail 5 {CONTAINER}",
        "Son 5 log satırı"
    )

    # Sil
    run_cmd(f"docker rm -f {CONTAINER}", "Container'ı zorla sil")


def demo_interactive_container():
    """İnteraktif container kullanımı"""
    print("\n\n💻 Interaktif Container")
    print("=" * 60)
    print("""
    İnteraktif container (-it flag):
    -i  → stdin açık tut (input alabilsin)
    -t  → pseudo-TTY tahsis et (terminal gibi)
    
    Örnek kullanımlar:
    docker run -it ubuntu bash        # Ubuntu shell
    docker run -it python:3.11 python # Python REPL
    docker run -it alpine sh          # Alpine shell
    
    Mevcut container'a bağlan:
    docker exec -it mycontainer bash
    """)

    # Non-interactive örnek (script içinde çalışabilen)
    run_cmd(
        "docker run --rm alpine sh -c 'echo Alpine sürümü: && cat /etc/alpine-release && uname -a'",
        "Alpine'da sistem bilgisi al"
    )

    run_cmd(
        "docker run --rm python:3.11-slim python -c \"import sys; print(f'Python {sys.version}')\"",
        "Python container'da sürüm kontrolü"
    )


def demo_port_mapping():
    """Port yönlendirme"""
    print("\n\n🔌 Port Mapping")
    print("=" * 60)
    print("""
    Sözdizimi: -p HOST_PORT:CONTAINER_PORT
    
    -p 8080:80      → localhost:8080 → container:80
    -p 127.0.0.1:8080:80  → Sadece localhost
    -p 8080:80/udp  → UDP protokolü
    -P              → Tüm expose portları otomatik map
    """)

    # Nginx başlat
    run_cmd(
        "docker run -d --name demo_nginx -p 8088:80 nginx:alpine",
        "Nginx'i 8088 portunda başlat"
    )

    run_cmd(
        "docker port demo_nginx",
        "Container port mapping'ini görüntüle"
    )

    # HTTP isteği at
    run_cmd(
        "curl -s -o /dev/null -w 'HTTP Status: %{http_code}' http://localhost:8088",
        "Nginx'e HTTP isteği gönder"
    )

    run_cmd("docker rm -f demo_nginx", "Temizle")


def demo_environment_variables():
    """Ortam değişkenleri"""
    print("\n\n🌍 Ortam Değişkenleri")
    print("=" * 60)

    run_cmd(
        "docker run --rm "
        "-e APP_NAME='Docker Demo' "
        "-e APP_VERSION=1.0 "
        "-e DEBUG=true "
        "alpine sh -c 'echo $APP_NAME v$APP_VERSION, Debug=$DEBUG'",
        "Ortam değişkeni ile container çalıştır"
    )


def demo_cleanup():
    """Sistem temizliği"""
    print("\n\n🧹 Sistem Temizliği")
    print("=" * 60)

    run_cmd("docker ps -a", "Tüm container'lar")
    run_cmd("docker images", "Tüm image'lar")
    run_cmd("docker system df", "Docker disk kullanımı")

    print("""
    Temizlik komutları (dikkatli kullan!):
    
    docker container prune      # Durmuş container'lar
    docker image prune          # Dangling image'lar  
    docker image prune -a       # Kullanılmayan hepsi
    docker volume prune         # Kullanılmayan volume'lar
    docker network prune        # Kullanılmayan ağlar
    docker system prune -a      # HER ŞEY (tehlikeli!)
    """)


def main():
    print("""
╔══════════════════════════════════════════════════════════╗
║          DOCKER TEMEL KOMUTLAR — İNTERAKTİF DEMO       ║
╚══════════════════════════════════════════════════════════╝
    """)

    check_docker()

    demos = {
        "1": ("Hello World", demo_hello_world),
        "2": ("Image Yönetimi", demo_image_management),
        "3": ("Container Yaşam Döngüsü", demo_container_lifecycle),
        "4": ("İnteraktif Container", demo_interactive_container),
        "5": ("Port Mapping", demo_port_mapping),
        "6": ("Ortam Değişkenleri", demo_environment_variables),
        "7": ("Sistem Temizliği", demo_cleanup),
        "0": ("Hepsini Çalıştır", None),
    }

    print("\n📋 Demo Menüsü:")
    for key, (name, _) in demos.items():
        print(f"  [{key}] {name}")

    choice = input("\nSeçim yapın (0-7): ").strip()

    if choice == "0":
        for key, (name, fn) in demos.items():
            if fn:
                fn()
    elif choice in demos and demos[choice][1]:
        demos[choice][1]()
    else:
        print("Geçersiz seçim!")


if __name__ == "__main__":
    main()
