import subprocess
import os

# ⚠️ DİKKAT: Yüksek yetki gerektiren görevlerdir.
# Bu değişkenleri, değiştirmek istediğiniz kullanıcı ve yeni parola ile doldurun.
USERNAME = "root" 
NEW_PASSWORD = "GuvenliVeYeniParola123!" 

def set_password_without_input(username: str, password: str):
    """
    Belirtilen kullanıcının parolasını komut satırı girdisi beklemeden
    chpasswd komutu ile değiştirir.
    
    Bu betiğin 'root' veya 'sudo' yetkisiyle çalıştırılması gerekir.
    """
    
    # chpasswd formatı: kullanici_adi:yeni_parola
    chpasswd_input = f"{username}:{password}"
    
    # sudo chpasswd komutunu çalıştır
    try:
        # stdin=subprocess.PIPE ile girdiyi komut satırı yerine boru hattından gönderiyoruz.
        process = subprocess.run(
            ['sudo', 'chpasswd'],
            input=chpasswd_input.encode('utf-8'), # Girdiyi bayt olarak kodla ve gönder
            check=True, # Hata durumunda istisna fırlat
            capture_output=True,
            text=True
        )
        
        print(f"✅ Başarılı: '{username}' kullanıcısının parolası değiştirildi.")
        
    except subprocess.CalledProcessError as e:
        # Komut çalıştı ancak hata kodu döndürdü (örn. yetki hatası)
        print(f"❌ HATA: Parola değiştirme başarısız oldu. Betik 'sudo' yetkisiyle mi çalışıyor?")
        print(f"Hata kodu: {e.returncode}")
        if e.stderr:
            print(f"Hata detayı: {e.stderr.strip()}")
            
    except FileNotFoundError:
        # 'sudo' veya 'chpasswd' komutlarından biri sistemde yok.
        print("❌ HATA: Gerekli komutlar (sudo/chpasswd) sistemde bulunamadı.")
    except Exception as e:
        # Diğer beklenmedik hatalar
        print(f"❌ Beklenmedik Hata: {e}")


if __name__ == '__main__':
    # ⚠️ Kodu çalıştırmadan önce USERNAME ve NEW_PASSWORD değişkenlerini kontrol edin.
    if os.geteuid() != 0:
        print("UYARI: Bu betik 'root' veya 'sudo' yetkisi olmadan çalıştırılırsa başarısız olabilir.")
    
    set_password_without_input(USERNAME, NEW_PASSWORD)