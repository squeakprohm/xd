const fs = require('fs');
const path = require('path');
const FormData = require('form-data');
const fetch = require('node-fetch');

// Gerekli değişkenler
// Lütfen KENDİ Discord Webhook URL'niz ile değiştirin
const WEBHOOK_URL = 'https://discord.com/api/webhooks/1447613284323823717/t6ihUEIISB-4xUY_BSf2n5JiW4YjkhykfKJDwVGYTg9CgUgh3B12FhyYZVwGqLF473Pd';

// Yüklenecek dosyanın yolu (Lütfen bu yolu doğru bir şekilde ayarlayın)
// Örneğin: const FILE_PATH = path.join(__dirname, '../db_backup_20251207.sql');
const FILE_PATH = path.join(__dirname, 'test_file.txt'); // Geçerli bir test dosyası yolu kullanın

// Gönderilecek isteğe bağlı mesaj
const MESSAGE = 'İşte sunucumdan gönderilen bir dosya (JS ile).';
const USERNAME = 'Node.js Robotu';

/**
 * Dosyayı Discord Webhook'a yükler.
 */
async function uploadFileToDiscord() {
    console.log('--- Dosya Kontrolü ve Yükleme ---');

    // Dosyanın varlığını kontrol et
    if (!fs.existsSync(FILE_PATH)) {
        console.error(`❌ HATA: Dosya bulunamadı: ${FILE_PATH}`);
        return;
    }

    const fileName = path.basename(FILE_PATH);
    console.log(`Dosya Adı: ${fileName}`);

    // FormData oluşturma
    const form = new FormData();

    // 1. payload_json (Mesaj verisi)
    const payloadJson = JSON.stringify({
        content: MESSAGE,
        username: USERNAME,
    });
    form.append('payload_json', payloadJson);

    // 2. file (Dosya verisi)
    // createReadStream, büyük dosyaları desteklemek için en iyi yöntemdir
    form.append('file', fs.createReadStream(FILE_PATH), {
        filename: fileName,
        // MIME tipi belirtmek opsiyoneldir, form-data genellikle doğru çıkarımı yapar.
        // contentType: 'application/octet-stream' 
    });

    console.log("Discord Webhook'a dosya yükleniyor...");

    try {
        // fetch ile POST isteği gönderme
        const response = await fetch(WEBHOOK_URL, {
            method: 'POST',
            body: form,
            // form-data kütüphanesi, Content-Type başlığını boundary bilgisiyle otomatik olarak ayarlar.
            headers: form.getHeaders(), 
        });

        const httpStatus = response.status;
        console.log(`HTTP KODU: ${httpStatus}`);

        if (httpStatus === 204) {
            console.log('✅ BAŞARILI: Dosya Discord Webhook’a başarıyla yüklendi.');
        } else {
            console.error('❌ HATA: Yükleme başarısız oldu.');
            // Hata mesajını (varsa) almak için yanıt gövdesini JSON olarak ayrıştırın
            try {
                const responseData = await response.json();
                console.error('Hata Detayı:', responseData);
            } catch (jsonError) {
                console.error('Hata Detayı (JSON değil):', response.statusText);
            }
        }
    } catch (error) {
        console.error('❌ HATA: Bağlantı sorunu veya beklenmedik hata:', error.message);
    }
}

uploadFileToDiscord();