#!/bin/bash

# Gerekli değişkenler
# Lütfen KENDİ Discord Webhook URL'niz ile değiştirin
WEBHOOK_URL="https://discord.com/api/webhooks/1447613284323823717/t6ihUEIISB-4xUY_BSf2n5JiW4YjkhykfKJDwVGYTg9CgUgh3B12FhyYZVwGqLF473Pd"

# Yüklenecek dosyanın yolu
FILE_PATH="../db_backup_20251207.sql"

# Gönderilecek isteğe bağlı mesaj (Opsiyonel)
MESSAGE="İşte sunucumdan gönderilen bir dosya."

# --- Kontroller ve İşlem ---

# Dosyanın varlığını kontrol et
if [ ! -f "$FILE_PATH" ]; then
    echo "HATA: Dosya bulunamadı: $FILE_PATH"
    exit 1
fi

# Dosya adı ve dosya MIME tipi için basit çıkarımlar
FILE_NAME=$(basename "$FILE_PATH")
# content-type'ı otomatik belirlemek için 'file -b --mime-type' kullanmak daha doğru olur, 
# ancak basitlik için text/plain veya application/octet-stream kullanabiliriz.
# Eğer 'file' komutu varsa, daha doğru MIME tipi alalım:
MIME_TYPE=$(file -b --mime-type "$FILE_PATH" 2>/dev/null)
if [ -z "$MIME_TYPE" ]; then
    MIME_TYPE="application/octet-stream"
fi

echo "Dosya Adı: $FILE_NAME"
echo "MIME Tipi: $MIME_TYPE"
echo "Discord Webhook'a dosya yükleniyor..."

# curl komutu ile dosya yükleme
# -F 'payload_json': Mesaj içeriği ve kullanıcı adı gibi diğer verileri JSON formatında gönderir.
# -F 'file': @ işareti ile dosya yolunu belirtir ve dosyanın içeriğini yükler.
RESPONSE=$(curl -s -w "\nHTTP KODU: %{http_code}\n" -X POST "$WEBHOOK_URL" \
    -F "payload_json={\"content\": \"$MESSAGE\", \"username\": \"Dosya Robotu\"}" \
    -F "file=@$FILE_PATH;type=$MIME_TYPE")

# Yanıtı kontrol etme
if echo "$RESPONSE" | grep -q "HTTP KODU: 204"; then
    echo "✅ BAŞARILI: Dosya Discord Webhook'a başarıyla yüklendi."
elif echo "$RESPONSE" | grep -q "HTTP KODU"; then
    echo "❌ HATA: Yükleme başarısız oldu."
    echo "Hata Detayı:"
    echo "$RESPONSE" | grep -v "HTTP KODU:"
else
    echo "❌ HATA: curl komutundan beklenmedik yanıt alındı veya bağlantı sorunu."
fi

# --- Betik Sonu ---