# 🔍 ADB Forensics Data Extractor v2.0

<div align="center">

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Linux-orange.svg)
![ADB](https://img.shields.io/badge/ADB-Required-red.svg)
![Stars](https://img.shields.io/github/stars/VIPOS-testuser/adb_tool?style=social)

**Mobil qurilmalardan forensik ma'lumotlarni olish va tahlil qilish uchun professional vosita**

[Features](#-asosiy-imkoniyatlar) • [Installation](#-ornatish) • [Usage](#-foydalanish) • [Legal](#-qonuniy-ogohlantirish) • [Contact](#-muallif)

</div>

---

## 📋 Tavsif

ADB Forensics Data Extractor - Android qurilmalardan forensik ma'lumotlarni olish, tahlil qilish va hisobot yaratish uchun mo'ljallangan professional Python vositasi. Pentesting, xavfsizlik tekshiruvi va forensik tahlil uchun ishlatiladi.

### ⚡ Asosiy Imkoniyatlar

#### 📱 Asosiy Ma'lumotlar
- ✅ Qurilma to'liq ma'lumotlari (model, versiya, IMEI, RAM, CPU)
- ✅ Kontaktlar bazasi + avtomatik tahlil
- ✅ SMS/MMS xabarlari + avtomatik tahlil
- ✅ Qo'ng'iroqlar tarixi
- ✅ O'rnatilgan ilovalar ro'yxati (tizim + foydalanuvchi)

#### 🖼️ Multimedia
- ✅ Ekran surati olish
- ✅ Video yozish
- ✅ Barcha rasmlarni zaxiralash (DCIM, Pictures)
- ✅ Barcha videolarni zaxiralash
- ✅ Barcha hujjatlarni zaxiralash (Documents, Downloads)

#### 💬 Messenger va Ijtimoiy Tarmoqlar
- ✅ WhatsApp to'liq zaxirasi
- ✅ Telegram to'liq zaxirasi

#### 🔐 Tarmoq va Xavfsizlik
- ✅ WiFi parollar ekstraktsiyasi (ROOT talab qiladi)
- ✅ Brauzer tarixi + avtomatik tahlil
- ✅ Tarmoq sozlamalari va ulanishlar
- ✅ Tizim loglari (Logcat)

#### 📦 Ilovalar
- ✅ Bitta ilova APK ini olish
- ✅ Barcha foydalanuvchi APK larini eksport qilish

#### 📊 Tahlil va Hisobot
- ✅ Xotira va tizim ma'lumotlari
- ✅ SHA256 hash hisoblash (fayl integrity)
- ✅ To'liq forensik hisobot yaratish
- ✅ JSON va TEXT formatda export

#### ⚡ Maxsus Funksiya
- ✅ **HAMMA NARSANI BIR VAQTDA OLISH** - To'liq avtomatik ekstraktsiya

---

## 🛠️ Ornatish

### Talablar

```bash
# OS: Linux (Kali Linux, Ubuntu, Debian, Arch)
# Python: 3.7 yoki yuqori
# ADB: Android Debug Bridge
```

### ADB O'rnatish

#### Debian/Ubuntu/Kali Linux
```bash
sudo apt update
sudo apt install adb -y
```

#### Arch Linux
```bash
sudo pacman -S android-tools
```

#### Fedora
```bash
sudo dnf install android-tools
```

### Tool O'rnatish

```bash
# Repository ni clone qilish
git clone https://github.com/VIPOS-testuser/adb_tool.git
cd adb_tool

# Executable qilish
chmod +x adb_tool.py

# Ishga tushirish
python3 adb_tool.py
```

---

## 🚀 Foydalanish

### 1. Qurilmani Tayyorlash

Android qurilmada USB Debugging ni yoqing:

```
Sozlamalar → Telefon haqida → Build Number (7 marta bosing)
Sozlamalar → Dasturchi parametrlari → USB Debugging ✓
```

### 2. Qurilmani Ulash

```bash
# USB orqali qurilmani ulang
# Qurilmada "Allow USB debugging" ni tasdiqlang

# Ulanishni tekshirish
adb devices
```

### 3. Toolni Ishga Tushirish

```bash
# Root huquqida ishga tushirish (tavsiya etiladi)
sudo python3 adb_tool.py

# Yoki oddiy foydalanuvchi sifatida
python3 adb_tool.py
```

### 4. Interaktiv Menyu

Tool ishga tushganda interaktiv menyu ko'rsatiladi:

```
═══════════════════════════════════════════════════════════
           FORENSIK EKSTRAKTSIYA MENYUSI
═══════════════════════════════════════════════════════════

ASOSIY MA'LUMOTLAR:
[1]  Qurilma ma'lumotlarini olish
[2]  Kontaktlar bazasini olish
[3]  SMS/MMS xabarlarini olish
[4]  Qo'ng'iroqlar tarixini olish
[5]  O'rnatilgan ilovalar ro'yxati

MULTIMEDIA:
[6]  Ekran surati olish
[7]  Ekrandan video yozish (10 soniya)
[8]  Barcha rasmlarni zaxiralash
[9]  Barcha videolarni zaxiralash
[10] Barcha hujjatlarni zaxiralash

MESSENGER VA IJTIMOIY TARMOQLAR:
[11] WhatsApp zaxirasi
[12] Telegram zaxirasi

TARMOQ VA XAVFSIZLIK:
[13] WiFi parollarni olish (ROOT)
[14] Brauzer tarixini olish
[15] Tarmoq ma'lumotlarini olish
[16] Tizim loglarini olish (Logcat)

ILOVALAR:
[17] Bitta ilova APK sini olish
[18] Barcha foydalanuvchi APK larini olish

TAHLIL VA HISOBOT:
[19] Xotira va tizim ma'lumotlari
[20] Fayllar uchun hash hisoblash
[21] To'liq forensik hisobot

MAXSUS:
[99] HAMMA NARSANI OLISH (To'liq dump)
[0]  Chiqish
```

---

## 📂 Natija Strukturasi

Barcha olingan ma'lumotlar timestamped papkada saqlanadi:

```
forensik_malumot_20241030_145623/
│
├── qurilma_malumoti.json           # Qurilma ma'lumotlari (JSON)
├── qurilma_malumoti.txt            # Qurilma ma'lumotlari (TEXT)
│
├── contacts2.db                    # Kontaktlar bazasi
├── kontaktlar_royxati.txt          # Tahlil qilingan kontaktlar
│
├── mmssms.db                       # SMS/MMS bazasi
├── sms_xabarlar.txt               # Tahlil qilingan xabarlar
│
├── qongiroqlar_tarixi.txt         # Qo'ng'iroqlar tarixi
├── barcha_ilovalar.txt            # Barcha ilovalar
├── foydalanuvchi_ilovalari.txt    # Foydalanuvchi ilovalari
│
├── screenshot_20241030_145630.png  # Ekran surati
├── screenrecord_20241030_145645.mp4 # Video
│
├── WhatsApp_Zaxira/               # WhatsApp backup
├── Telegram_Zaxira/               # Telegram backup
│
├── Rasmlar_Zaxira/                # Barcha rasmlar
│   ├── DCIM/
│   └── Pictures/
│
├── Videolar_Zaxira/               # Barcha videolar
├── Hujjatlar_Zaxira/              # Barcha hujjatlar
│   ├── Documents/
│   └── Downloads/
│
├── wifi_parollar.txt              # WiFi parollar (ROOT)
├── chrome_history.db              # Brauzer tarixi bazasi
├── brauzer_tarixi.txt             # Tahlil qilingan tarix
│
├── tarmoq_malumoti.txt            # Tarmoq ma'lumotlari
├── tizim_loglari.txt              # Logcat
├── xotira_malumoti.txt            # RAM, CPU, Disk
│
├── APK_Fayllar/                   # Eksport qilingan APK lar
│   ├── com.whatsapp.apk
│   ├── org.telegram.messenger.apk
│   └── ...
│
├── fayl_hashlari.json             # SHA256 hashlar (JSON)
├── fayl_hashlari.txt              # SHA256 hashlar (TEXT)
│
└── FORENSIK_HISOBOT.txt           # To'liq hisobot
```

---

## 🔬 Tahlil Qilish

### SQLite Bazalarni Ochish

```bash
# Kontaktlar bazasi
sqlite3 contacts2.db
sqlite> .tables
sqlite> SELECT * FROM view_contacts LIMIT 10;

# SMS bazasi
sqlite3 mmssms.db
sqlite> SELECT address, body, date FROM sms LIMIT 10;

# Brauzer tarixi
sqlite3 chrome_history.db
sqlite> SELECT url, title FROM urls LIMIT 10;
```

### GUI Tool bilan (DB Browser)

```bash
# O'rnatish
sudo apt install sqlitebrowser

# Ochish
sqlitebrowser contacts2.db
```

---

## ⚠️ ROOT Talab Qilinadigan Funksiyalar

Ba'zi funksiyalar qurilmada ROOT huquqi talab qiladi:

- 🔐 WiFi parollar ekstraktsiyasi
- 📱 Kontaktlar bazasi (ba'zi qurilmalarda)
- 💬 SMS/MMS bazasi (ba'zi qurilmalarda)
- 🌐 Brauzer tarixi (ba'zi qurilmalarda)

### ROOT Tekshirish

Tool avtomatik ravishda ROOT huquqini tekshiradi:

```
[+] Qurilma ROOT qilingan - To'liq kirish mavjud
```

yoki

```
[!] Qurilma ROOT qilinmagan - Cheklangan kirish
```

---

## 🛡️ Xavfsizlik va Maxfiylik

### Muhim Nuqtalar

- ✅ Barcha ma'lumotlar **faqat mahalliy** saqlanadi
- ✅ Hech qanday ma'lumot internetga yuborilmaydi
- ✅ Fayllar SHA256 hash bilan himoyalangan
- ✅ Olingan ma'lumotlar **shifrlash tavsiya etiladi**

### Fayllarni Shifrlash

```bash
# ZIP bilan shifrlash
zip -e -r forensic_data.zip forensik_malumot_*/

# 7z bilan shifrlash (kuchliroq)
7z a -p -mhe=on forensic_data.7z forensik_malumot_*/
```

---

## 📝 Qonuniy Ogohlantirish

### ⚖️ MUHIM: Qonuniy Foydalanish

Bu tool **faqat quyidagi maqsadlar** uchun ishlatilishi mumkin:

✅ **Ruxsat etilgan holatlarda:**
- O'z qurilmangizni tekshirish
- Yozma ruxsat olgan qurilmalarni tekshirish
- Professional pentesting va xavfsizlik auditi
- Forensic tahlil (sud buyrug'i asosida)
- Ta'lim va tadqiqot maqsadlari

❌ **Taqiqlangan holatlarda:**
- Ruxsatsiz qurilmalarga kirish
- Boshqa odamlarning shaxsiy ma'lumotlarini o'g'irlash
- Qonunga xilof harakatlar
- Maxfiylikni buzish

### Javobgarlik

- 🔴 Toolni noto'g'ri ishlatish **jinoiy javobgarlikka** olib keladi
- 🔴 Foydalanuvchi barcha harakatlari uchun **to'liq javobgar**
- 🔴 Muallif noto'g'ri foydalanish uchun javobgar emas

### Qonunlar

Quyidagi qonunlarga rioya qiling:
- Computer Fraud and Abuse Act (CFAA) - USA
- General Data Protection Regulation (GDPR) - EU
- O'zbekiston Respublikasi qonunlari

---

## 🤝 Hissa Qo'shish

Hissa qo'shishni xohlaysizmi? Ajoyib!

```bash
# Fork qiling
# Branch yarating
git checkout -b feature/yangi-funksiya

# Commit qiling
git commit -m "Yangi funksiya qo'shildi"

# Push qiling
git push origin feature/yangi-funksiya

# Pull Request yarating
```

---

## 🐛 Xatolar va Muammolar

Xato topsangiz yoki taklif bo'lsa:

1. [Issues](https://github.com/VIPOS-testuser/adb_tool/issues) bo'limida yangi issue oching
2. Xatoni batafsil tasvirlang
3. Screenshot qo'shing (agar mumkin bo'lsa)
4. Yoki Telegram orqali bog'laning: [@Xorazmlik_2004](https://t.me/Xorazmlik_2004)

---

## 📚 Qo'shimcha Resurslar

### ADB Qo'llanma
- [Official ADB Documentation](https://developer.android.com/studio/command-line/adb)
- [ADB Commands List](https://gist.github.com/Pulimet/5013acf2cd5b28e55036c82c91bd56d8)

### Forensics
- [Android Forensics Guide](https://source.android.com/security/overview/forensics)
- [Mobile Forensics Tools](https://www.sans.org/mobile-device-security/)

### SQLite
- [SQLite Tutorial](https://www.sqlitetutorial.net/)
- [DB Browser for SQLite](https://sqlitebrowser.org/)

---

## 📜 Litsenziya

MIT License - batafsil ma'lumot uchun [LICENSE](LICENSE) faylini ko'ring.

```
MIT License

Copyright (c) 2024 VIPOS-testuser

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 👨‍💻 Muallif

**VIPOS-testuser**
- 🌐 GitHub: [@VIPOS-testuser](https://github.com/VIPOS-testuser)
- 📱 Telegram: [@Xorazmlik_2004](https://t.me/Xorazmlik_2004)
- 🔗 Repository: [adb_tool](https://github.com/VIPOS-testuser/adb_tool.git)

---

## 💬 Aloqa

Savollar, takliflar yoki muammolar bo'lsa, bog'laning:

- 📧 GitHub Issues: [Yangi issue ochish](https://github.com/VIPOS-testuser/adb_tool/issues/new)
- 💬 Telegram: [@Xorazmlik_2004](https://t.me/Xorazmlik_2004)

---

## 🌟 Qo'llab-quvvatlash

Agar loyiha foydali bo'lsa, ⭐ (star) bering!

Qo'llab-quvvatlash:
- ⭐ GitHub da star qo'ying
- 🔄 Share qiling
- 🐛 Xatolar haqida xabar bering
- 💡 Yangi funksiyalar taklif qiling
- 📢 Do'stlaringizga ulashing

---

## 📊 Statistika

![GitHub Stars](https://img.shields.io/github/stars/VIPOS-testuser/adb_tool?style=social)
![GitHub Forks](https://img.shields.io/github/forks/VIPOS-testuser/adb_tool?style=social)
![GitHub Watchers](https://img.shields.io/github/watchers/VIPOS-testuser/adb_tool?style=social)
![GitHub Issues](https://img.shields.io/github/issues/VIPOS-testuser/adb_tool)
![GitHub Pull Requests](https://img.shields.io/github/issues-pr/VIPOS-testuser/adb_tool)
![GitHub Last Commit](https://img.shields.io/github/last-commit/VIPOS-testuser/adb_tool)
![GitHub Repo Size](https://img.shields.io/github/repo-size/VIPOS-testuser/adb_tool)
![GitHub Language](https://img.shields.io/github/languages/top/VIPOS-testuser/adb_tool)

---

## 🔄 Changelog

### Version 2.0 (2025-10-31)
- ✨ To'liq o'zbek tiliga tarjima qilindi
- ✨ 21+ yangi funksiya qo'shildi
- ✨ Avtomatik tahlil qo'shildi
- ✨ Hash hisoblash funksiyasi
- ✨ To'liq forensik hisobot
- ✨ WhatsApp va Telegram zaxirasi
- ✨ Multimedia zaxira funksiyalari
- 🐛 Barcha xatolar tuzatildi
- 🎨 Rangli va interaktiv interfeys

### Version 1.0 (2025-10-30)
- 🎉 Birinchi versiya chiqarildi
- ✅ Asosiy funksiyalar

---

## 🎯 Kelajak Rejalar

- [ ] GUI interfeys qo'shish (Tkinter/PyQt)
- [ ] Instagram va Facebook zaxirasi
- [ ] Avtomatik malware detection
- [ ] Cloud backup integratsiyasi
- [ ] Multi-device parallel ekstraktsiya
- [ ] HTML hisobot generatori
- [ ] Ko'proq tillar qo'shish (rus, ingliz)

---

## 🙏 Minnatdorchilik

Ushbu loyihani yaratishda yordam bergan barcha open-source jamoalarga rahmat:

- Python Community
- Android Debug Bridge (ADB) Developers
- SQLite Developers
- Kali Linux Team
- Cybersecurity Community

---

## ⚡ Tezkor Yo'riqnoma

```bash
# 1. Clone
git clone https://github.com/VIPOS-testuser/adb_tool.git

# 2. Kirish
cd adb_tool

# 3. Ruxsat
chmod +x adb_tool.py

# 4. Ishga tushirish
sudo python3 adb_tool.py

# 5. To'liq dump (99 tanlov)
# Barcha ma'lumotlarni bir vaqtda olish uchun
```

---

<div align="center">

### 🔥 Made with ❤️ for Cybersecurity Community 🔥

**⚠️ Faqat qonuniy maqsadlarda foydalaning! ⚠️**

[![GitHub](https://img.shields.io/badge/GitHub-VIPOS--testuser-181717?style=for-the-badge&logo=github)](https://github.com/VIPOS-testuser)
[![Telegram](https://img.shields.io/badge/Telegram-Xorazmlik__2004-26A5E4?style=for-the-badge&logo=telegram)](https://t.me/Xorazmlik_2004)

[⬆ Yuqoriga qaytish](#-adb-forensics-data-extractor-v20)

</div>
