import requests
import os
import mimetypes
import json

# =================================================================
# Gerekli Değişkenler
# =================================================================

# Lütfen KENDİ Discord Webhook URL'niz ile değiştirin
WEBHOOK_URL = "https://discord.com/api/webhooks/1447613284323823717/t6ihUEIISB-4xUY_BSf2n5JiW4YjkhykfKJDwVGYTg9CgUgh3B12FhyYZVwGqLF473Pd"

# Yüklenecek dosyanın yolu (Bash'deki gibi göreceli yol)
FILE_PATH = "sex.sh"

# Gönderilecek isteğe bağlı mesaj (Opsiyonel)
MESSAGE = "İşte sunucumdan gönderilen bir dosya."
USERNAME = "Dosya Robotu"

# =================================================================
# Fonksiyon ve İşlem
# =================================================================

def upload_file_to_discord(webhook_url: str, file_path: str, message: str, username: str):
    """
    Belirtilen dosyayı Discord Webhook'a yükler.
    """
    
    # 1. Dosyanın varlığını kontrol et
    if not os.path.exists(file_path):
        print(f"HATA: Dosya bulunamadı: {file_path}")
        return
    
    # 2. Dosya Adı ve MIME Tipi belirleme
    file_name = os.path.basename(file_path)
    # mimetypes kütüphanesi ile MIME tipi çıkarımı
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type:
        # Çıkarım yapılamazsa varsayılan değer
        mime_type = "application/octet-stream" 
    
    print(f"Dosya Adı: {file_name}")
    print(f"MIME Tipi: {mime_type}")
    print("Discord Webhook'a dosya yükleniyor...")

    try:
        # Dosya yükleme (Multipart/form-data)
        
        # 'payload_json' için JSON verisi
        payload = {
            "content": message,
            "username": username
        }
        
        # 'file' için dosya içeriği
        # requests, dosyayı açmak için bir tuple formatı bekler: (dosya adı, dosya objesi, mime tipi)
        files = {
            "file": (file_name, open(file_path, 'rb'), mime_type)
        }
        
        # 'payload_json' alanını da 'data' yerine 'files' ile göndermek gerekiyor
        # Discord API Multipart formunda tüm alanları form verisi olarak bekler.
        
        response = requests.post(
            webhook_url,
            data={"payload_json": json.dumps(payload)},
            files=files
        )
        
        # Dosya objesini kapat
        files['file'][1].close()

        # 3. Yanıtı kontrol etme
        if response.status_code == 204:
            # 204 No Content, Discord'da başarılı yükleme kodudur
            print("✅ BAŞARILI: Dosya Discord Webhook'a başarıyla yüklendi.")
        else:
            print("❌ HATA: Yükleme başarısız oldu.")
            print(f"HTTP KODU: {response.status_code}")
            try:
                # Discord hata mesajını yazdırma
                print("Hata Detayı:", response.json())
            except requests.exceptions.JSONDecodeError:
                print("Hata Detayı:", response.text)

    except requests.exceptions.RequestException as e:
        print(f"❌ HATA: Bağlantı hatası oluştu: {e}")

# Betiği çalıştırma
if __name__ == "__main__":
    # Kullanmadan önce 'requests' kütüphanesini kurmayı unutmayın: pip install requests

    upload_file_to_discord(WEBHOOK_URL, FILE_PATH, MESSAGE, USERNAME)
