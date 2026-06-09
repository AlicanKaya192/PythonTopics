# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════╗
║   04 — Docker Network Yönetimi Demo                      ║
║   Alican Kaya | Data Science RoadMap                    ║
╚══════════════════════════════════════════════════════════╝
"""

import subprocess
import sys


def run(cmd, desc=""):
    if desc:
        print(f"\n🔧 {desc}")
    print(f"$ {cmd}")
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if r.stdout:
        print(r.stdout.strip())
    if r.returncode != 0 and r.stderr:
        print(f"⚠️  {r.stderr.strip()}")
    return r.returncode, r.stdout


def demo_bridge_network():
    """Custom bridge network ve DNS çözümlemesi"""
    print("\n" + "="*60)
    print("🌐 CUSTOM BRIDGE NETWORK — DNS ile Container İletişimi")
    print("="*60)

    NETWORK = "demo_net"
    run(f"docker network create --driver bridge {NETWORK}", "Custom bridge network oluştur")

    run(
        f"docker run -d --name server --network {NETWORK} nginx:alpine",
        "Server container başlat (nginx)"
    )

    run(
        f"docker run --rm --network {NETWORK} alpine "
        "wget -qO- http://server/",
        "Client'tan server'a DNS ile bağlan"
    )

    run("docker rm -f server", "")
    run(f"docker network rm {NETWORK}", "")


def demo_network_isolation():
    """Network izolasyonu"""
    print("\n" + "="*60)
    print("🔒 NETWORK İZOLASYONU")
    print("="*60)

    run("docker network create frontend_net", "Frontend ağı")
    run("docker network create backend_net", "Backend ağı")

    run(
        "docker run -d --name web_server --network frontend_net nginx:alpine",
        "Web: sadece frontend"
    )
    run(
        "docker run -d --name db_server --network backend_net alpine sleep 60",
        "DB: sadece backend"
    )
    run(
        "docker run -d --name api_server --network frontend_net alpine sleep 60",
        "API: frontend'de başlar"
    )
    run(
        "docker network connect backend_net api_server",
        "API'yi backend'e de bağla (köprü görevi)"
    )

    print("\n📊 İzolasyon testi:")
    run(
        "docker exec api_server ping -c 1 web_server 2>&1 || echo BAŞARISIZ",
        "web → api (aynı ağ) ✅"
    )
    run(
        "docker exec web_server ping -c 1 db_server 2>&1 || echo ULAŞILAMADI",
        "web → db (farklı ağ) ❌ izole!"
    )

    run("docker rm -f web_server db_server api_server", "")
    run("docker network rm frontend_net backend_net", "")


def demo_host_network():
    """Host network modu"""
    print("\n" + "="*60)
    print("🖥️  HOST NETWORK — Yüksek Performans Modu")
    print("="*60)

    print("""
    Host network: Container'ın kendi ağ stack'i yok,
    host'un ağını doğrudan kullanır.
    
    Avantaj: Port mapping overhead yok → Yüksek performans
    Dezavantaj: İzolasyon yok, port çakışması riski
    
    $ docker run --network host nginx
    # nginx 80 portunu doğrudan host'ta açar
    
    Linux'ta tam destekli, macOS/Windows'ta sınırlı
    """)


def main():
    print("""
╔══════════════════════════════════════════════════════════╗
║            DOCKER NETWORK YÖNETİMİ — DEMO              ║
╚══════════════════════════════════════════════════════════╝
    """)

    r = subprocess.run("docker info", shell=True, capture_output=True)
    if r.returncode != 0:
        print("❌ Docker çalışmıyor!")
        sys.exit(1)

    menus = {
        "1": ("Custom Bridge Network & DNS", demo_bridge_network),
        "2": ("Network İzolasyonu", demo_network_isolation),
        "3": ("Host Network Açıklaması", demo_host_network),
        "0": ("Hepsini Çalıştır", None),
    }

    print("📋 Demo Menüsü:")
    for k, (n, _) in menus.items():
        print(f"  [{k}] {n}")

    choice = input("\nSeçim: ").strip()
    if choice == "0":
        for k, (n, fn) in menus.items():
            if fn:
                fn()
    elif choice in menus and menus[choice][1]:
        menus[choice][1]()


if __name__ == "__main__":
    main()
