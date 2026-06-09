# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════╗
║   03 — Volume Yönetimi Demo                              ║
║   Alican Kaya | Data Science RoadMap                    ║
╚══════════════════════════════════════════════════════════╝
"""

import subprocess
import time
import sys
import os


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


def demo_named_volume():
    """Named volume ile kalıcı veri"""
    print("\n" + "="*60)
    print("💾 NAMED VOLUME — Kalıcı PostgreSQL Verisi")
    print("="*60)

    VOLUME = "demo_pgdata"
    CONTAINER = "demo_postgres"

    run(f"docker volume create {VOLUME}", "Named volume oluştur")
    run(f"docker volume inspect {VOLUME}", "Volume detayları")

    run(
        f"docker run -d --name {CONTAINER} "
        f"-v {VOLUME}:/var/lib/postgresql/data "
        "-e POSTGRES_PASSWORD=demo123 "
        "-e POSTGRES_DB=testdb "
        "postgres:15-alpine",
        "PostgreSQL'i named volume ile başlat"
    )

    time.sleep(5)

    run(
        f'docker exec {CONTAINER} psql -U postgres -d testdb '
        '-c "CREATE TABLE users (id SERIAL PRIMARY KEY, name TEXT); '
        "INSERT INTO users (name) VALUES ('Alice'), ('Bob'), ('Charlie');\"",
        "Veritabanında tablo oluştur ve veri ekle"
    )

    run(
        f"docker exec {CONTAINER} psql -U postgres -d testdb "
        "-c 'SELECT * FROM users;'",
        "Veriyi oku"
    )

    run(f"docker rm -f {CONTAINER}", "Container'ı SİL (volume kalacak!)")

    run(
        f"docker run -d --name {CONTAINER}_v2 "
        f"-v {VOLUME}:/var/lib/postgresql/data "
        "-e POSTGRES_PASSWORD=demo123 "
        "postgres:15-alpine",
        "YENİ container — aynı volume"
    )
    time.sleep(5)

    run(
        f"docker exec {CONTAINER}_v2 psql -U postgres -d testdb "
        "-c 'SELECT * FROM users;'",
        "Veriler hâlâ orada!"
    )

    run(f"docker rm -f {CONTAINER}_v2", "")
    run(f"docker volume rm {VOLUME}", "Volume'u sil")


def demo_bind_mount():
    """Bind mount ile canlı kod geliştirme"""
    print("\n" + "="*60)
    print("📁 BIND MOUNT — Canlı Kod Geliştirme")
    print("="*60)

    host_dir = os.path.join(os.getcwd(), "bind_demo")
    os.makedirs(host_dir, exist_ok=True)

    with open(os.path.join(host_dir, "script.py"), "w", encoding="utf-8") as f:
        f.write("print('Versiyon 1 — Host dosyasından!')\n")

    run(
        f"docker run --rm -v {host_dir}:/code python:3.11-slim python /code/script.py",
        "Host dosyasını container içinde çalıştır (v1)"
    )

    with open(os.path.join(host_dir, "script.py"), "w", encoding="utf-8") as f:
        f.write("print('Versiyon 2 — Dosya değişti, build yok!')\n")
        f.write("import sys; print(f'Python: {sys.version}')\n")

    run(
        f"docker run --rm -v {host_dir}:/code python:3.11-slim python /code/script.py",
        "Değişen dosyayı çalıştır (v2) — IMAGE AYNI!"
    )

    print("""
    💡 Bind Mount kullanım şekilleri:
    
    # Geliştirme: Kod değişikliği anında yansır
    docker run -v $(pwd):/app -p 5000:5000 flask_app
    
    # Config dosyası inject etme
    docker run -v $(pwd)/nginx.conf:/etc/nginx/nginx.conf:ro nginx
    
    # :ro = read-only (container yazamaz)
    docker run -v $(pwd)/data:/data:ro myapp
    """)


def demo_volume_backup():
    """Volume backup ve restore"""
    print("\n" + "="*60)
    print("💾 VOLUME BACKUP & RESTORE")
    print("="*60)

    vol = "demo_backup_vol"
    run(f"docker volume create {vol}", "")

    run(
        f"docker run --rm -v {vol}:/data alpine sh -c "
        "'echo \"Önemli veriler!\" > /data/data.txt && ls -la /data'",
        "Volume'a veri yaz"
    )

    backup_dir = os.path.join(os.getcwd(), "backup_demo")
    os.makedirs(backup_dir, exist_ok=True)

    run(
        f"docker run --rm "
        f"-v {vol}:/data "
        f"-v {backup_dir}:/backup "
        f"alpine tar czf /backup/volume_backup.tar.gz -C /data .",
        "Volume'u tar ile yedekle"
    )

    new_vol = "demo_restored_vol"
    run(f"docker volume create {new_vol}", "Yeni volume oluştur")
    run(
        f"docker run --rm "
        f"-v {new_vol}:/data "
        f"-v {backup_dir}:/backup "
        f"alpine tar xzf /backup/volume_backup.tar.gz -C /data",
        "Backup'tan restore et"
    )
    run(
        f"docker run --rm -v {new_vol}:/data alpine cat /data/data.txt",
        "Restore edilen veriyi oku"
    )

    run(f"docker volume rm {vol} {new_vol}", "Temizle")


def main():
    print("""
╔══════════════════════════════════════════════════════════╗
║              VOLUME YÖNETİMİ — DEMO                    ║
╚══════════════════════════════════════════════════════════╝
    """)

    r = subprocess.run("docker info", shell=True, capture_output=True)
    if r.returncode != 0:
        print("❌ Docker çalışmıyor!")
        sys.exit(1)

    menus = {
        "1": ("Named Volume — Kalıcı Veri (PostgreSQL)", demo_named_volume),
        "2": ("Bind Mount — Canlı Kod Geliştirme", demo_bind_mount),
        "3": ("Volume Backup & Restore", demo_volume_backup),
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
