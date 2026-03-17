# 🤖 Huh Bot

Discord'un en kapsamlı botu! 750+ komut, web panel, müzik, ekonomi, seviye sistemi ve daha fazlası.

## 🌟 Özellikler

- **Moderasyon**: Kick, ban, mute, warn, temizleme
- **Ekonomi**: Para sistemi, market, slot, çalışma
- **Seviye**: Otomatik seviye, XP, ödüller
- **Eğlence**: 100+ eğlence komutu
- **Müzik**: YouTube, Spotify destekli müzik
- **Web Panel**: Sunucu yönetimi paneli
- **Yapay Zeka**: Sohbet botu

## 🚀 Render.com'da Deploy

### 1. GitHub'a Yükle
Bu kodları GitHub'a at.

### 2. Render.com'da Oluştur
1. https://render.com adresine git
2. **New** → **Web Service**
3. GitHub repo'nu seç
4. Ayarlar:
   - **Name**: `huh`
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
   - **Instance Type**: `Free`

### 3. Environment Variables
**Advanced** → **Environment Variables**:
```
BOT_TOKEN = [BOT_TOKEN]
CLIENT_ID = 1452460095085744238
CLIENT_SECRET = [CLIENT_SECRET]
WEB_URL = https://web-3-tdo1.onrender.com
```

### 4. Deploy
- **Deploy Web Service** tıkla
- 2-3 dakika bekle
- Hazır!

## 📊 Komutlar

Prefix: `h!`

### Genel
- `h!yardim` - Yardım menüsü
- `h!ping` - Ping
- `h!bot` - Bot bilgi
- `h!istatistik` - İstatistikler
- `h!site` - Web panel linki

### Profil
- `h!profil` - Profil görüntüle
- `h!avatar` - Avatar göster
- `h!kullanıcıbilgi` - Kullanıcı bilgi
- `h!sunucubilgi` - Sunucu bilgi
- `h!roller` - Rol listesi

### Eğlence
- `h!8ball` - Sihirli top
- `h!yazitura` - Yazı tura
- `h!zar` - Zar at
- `h!aşkölçer` - Aşk ölçer
- `h!şaka` - Şaka

### Ekonomi
- `h!para` - Bakiye gör
- `h!günlük` - Günlük para
- `h!çalış` - Çalış para kazan
- `h!bahis` - Bahis yap
- `h!market` - Market

## 🌐 Web Panel

- Web Panel: `https://web-3-tdo1.onrender.com`
- Discord ile giriş yap
- Sunucu seç
- Ayarları yap

## 📝 Lisans

MIT License
