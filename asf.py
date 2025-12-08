import subprocess
import os

USERNAME = "root" 
NEW_PASSWORD = "GuvenliVeYeniParola123!" 

def set_password_without_input(username: str, password: str):
    
    # Doğru Yöntem: Parolayı burada bayt olarak hazırlayalım
    chpasswd_input = f"{username}:{password}".encode('utf-8') # <-- Sadece burada .encode() kullanıldı
    
    try:
        process = subprocess.run(
            ['sudo', 'chpasswd'],
            input=chpasswd_input, # <-- Bayt nesnesini doğrudan input'a veriyoruz
            check=True,
            capture_output=True,
            text=True
        )
        
        print(f"✅ Başarılı: '{username}' kullanıcısının parolası değiştirildi.")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ HATA: Parola değiştirme başarısız oldu. Betik 'sudo' yetkisiyle mi çalışıyor?")
        print(f"Hata kodu: {e.returncode}")
        if e.stderr:
            print(f"Hata detayı: {e.stderr.strip()}")
            
    except FileNotFoundError:
        print("❌ HATA: Gerekli komutlar (sudo/chpasswd) sistemde bulunamadı.")
    except Exception as e:
        # Bu satırda hata almanız durumunda bile artık daha anlamlı bir çıktı verir.
        print(f"❌ Beklenmedik Hata: {e}")


if __name__ == '__main__':
    if os.geteuid() != 0:
        print("UYARI: Bu betik 'root' veya 'sudo' yetkisi olmadan çalıştırılırsa başarısız olabilir.")
    
    set_password_without_input(USERNAME, NEW_PASSWORD)
