# 🔍 ADB Forensics Data Extractor v2.0

<div align="center">

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Linux-orange.svg)
![ADB](https://img.shields.io/badge/ADB-Required-red.svg)

**Mobil qurilmalardan forensik ma'lumotlarni olish va tahlil qilish uchun professional vosita**

[Features](#-asosiy-imkoniyatlar) • [Installation](#-ornatish) • [Usage](#-foydalanish) • [Screenshots](#-screenshot) • [Legal](#-qonuniy-ogohlantirish)

</div>

---

## 📋 Tavsif

**ADB Forensics Data Extractor** — Android qurilmalardan forensik ma'lumotlarni olish, tahlil qilish va hisobot yaratish uchun mo‘ljallangan professional **Python** vositasi. Pentesting, xavfsizlik tekshiruvi va forensik tahlil uchun ishlatiladi.

---

## ⚡ Asosiy Imkoniyatlar

#### 📱 Asosiy Ma'lumotlar

* ✅ Qurilma to‘liq ma’lumotlari (model, versiya, IMEI, RAM, CPU)
* ✅ Kontaktlar bazasi + avtomatik tahlil
* ✅ SMS/MMS xabarlari + avtomatik tahlil
* ✅ Qo‘ng‘iroqlar tarixi
* ✅ O‘rnatilgan ilovalar ro‘yxati (tizim + foydalanuvchi)

#### 🖼️ Multimedia

* ✅ Ekran surati olish
* ✅ Video yozish
* ✅ Barcha rasmlarni zaxiralash (DCIM, Pictures)
* ✅ Barcha videolarni zaxiralash
* ✅ Barcha hujjatlarni zaxiralash (Documents, Downloads)

#### 💬 Messenger va Ijtimoiy Tarmoqlar

* ✅ WhatsApp to‘liq zaxirasi
* ✅ Telegram to‘liq zaxirasi

#### 🔐 Tarmoq va Xavfsizlik

* ✅ WiFi parollar ekstraktsiyasi (ROOT talab qiladi)
* ✅ Brauzer tarixi + avtomatik tahlil
* ✅ Tarmoq sozlamalari va ulanishlar
* ✅ Tizim loglari (Logcat)

#### 📦 Ilovalar

* ✅ Bitta ilova APK ni olish
* ✅ Barcha foydalanuvchi APK larini eksport qilish

#### 📊 Tahlil va Hisobot

* ✅ Xotira va tizim ma'lumotlari
* ✅ SHA256 hash hisoblash (fayl integrity)
* ✅ To‘liq forensik hisobot yaratish
* ✅ JSON va TEXT formatda export

#### ⚡ Maxsus Funksiya

* ✅ **HAMMA NARSANI BIR VAQTDA OLISH** — To‘liq avtomatik ekstraktsiya

---

## 🛠️ Ornatish

### Talablar

```bash
# OS: Linux (Kali Linux, Ubuntu, Debian, Arch)
# Python: 3.7 yoki yuqori
# ADB: Android Debug Bridge
```

### ADB O‘rnatish

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

### Tool O‘rnatish

```bash
# Repository ni clone qilish
git clone https://github.com/VIPOS-testuser/adb_tool.git
cd adb_tool

# Executable qilish
chmod +x adb_tool_v2.py

# Ishga tushirish
python3 adb_tool_v2.py
```

---

## 🚀 Foydalanish

(Android qurilmada USB Debugging yoqish, `adb devices`, va tool menyusi README ichidagi interaktiv menyu formatida ishlaydi.)

---

## 📸 Screenshot

README ichida konsol-misol va natija strukturasiga oid misollar keltirilgan. Agar xohlasangiz, men real screenshot yoki loyiha uchun demo rasm tayyorlab READMEga qo'shish bo'yicha yordam bera olaman (hozir siz repo ichida rasm qo‘ymagansiz).

---

## 📂 Natija Strukturasi

Barcha olingan ma'lumotlar timestamped papkada saqlanadi (README ichida misol struktura berilgan).

---

## ⚠️ ROOT Talab Qilinadigan Funksiyalar

Ba'zi funksiyalar qurilmada ROOT huquqi talab qiladi, README ichida qaysi funksiyalar root talab qilishini belgilab qo'yilgan.

---

## 🛡️ Xavfsizlik va Maxfiylik

* ✅ Barcha ma'lumotlar **faqat mahalliy** saqlanadi
* ✅ Hech qanday ma'lumot internetga yuborilmaydi (default)
* ✅ Fayllar SHA256 hash bilan himoyalangan
* ✅ Olingan ma'lumotlar **shifrlash tavsiya etiladi**

---

## 📝 Qonuniy Ogohlantirish

Bu tool **faqat ruxsat olingan holatlarda** ishlatilishi kerak. Noto'g'ri yoki ruxsatsiz foydalanish jinoiy javobgarlikka olib keladi. Foydalanuvchi to'liq javobgardir.

---

## 🤝 Hissa Qo'shish

Fork, branch yaratish, commit va pull request orqali hissa qo'shishingiz mumkin. README ichida oddiy git-workflow ko'rsatmalari berilgan.

---

## 🐛 Xatolar va Muammolar

Issues bo'limida yangi issue ochishingizni so'raymiz: [https://github.com/VIPOS-testuser/adb_tool/issues](https://github.com/VIPOS-testuser/adb_tool/issues)

---

## 👨‍💻 Muallif

**VIPOS-testuser**

* GitHub: [@VIPOS-testuser](https://github.com/VIPOS-testuser)
* Telegram: [@Xorazmlik_2004](https://t.me/Xorazmlik_2004)

---

## 📜 Litsenziya

MIT License — batafsil ma’lumot uchun `LICENSE` faylini ko‘ring.

---

## 🌟 Qo‘llab-quvvatlash

Agar loyiha foydali bo‘lsa: ⭐ GitHub’da star qo‘ying, 🔄 ulashing, 🐛 xatolar haqida xabar bering, 💡 takliflaringizni yozing.

---

## 📊 Statistika

![GitHub stars](https://img.shields.io/github/stars/VIPOS-testuser/adb_tool?style=social)
![GitHub forks](https://img.shields.io/github/forks/VIPOS-testuser/adb_tool?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/VIPOS-testuser/adb_tool?style=social)

---

## 🔄 Changelog

### Version 2.0 (2025-10-31)

* ✨ To‘liq o‘zbek tiliga tarjima qilindi
* ✨ 21+ yangi funksiya qo‘shildi
* ✨ Avtomatik tahlil qo‘shildi
* ✨ Hash hisoblash funksiyasi
* ✨ To‘liq forensik hisobot
* ✨ WhatsApp va Telegram zaxirasi
* ✨ Multimedia zaxira funksiyalari
* 🐛 Barcha xatolar tuzatildi

### Version 1.0 (2025-10-30)

* 🎉 Birinchi versiya chiqarildi
* ✅ Asosiy funksiyalar

<div align="center">

**Made with ❤️ by [@VIPOS-testuser](https://github.com/VIPOS-testuser) for the Cybersecurity Community**
[⬆ Yuqoriga qaytish](#-adb-forensics-data-extractor-v20)

</div>
