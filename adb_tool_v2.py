#!/usr/bin/env python3
"""
ADB Forensics Ma'lumot Extraktori
Mobil qurilmalardan forensik ma'lumotlarni olish va tahlil qilish vositasi
Muallif: Kali Linux Tool Development
Versiya: 2.0 (O'zbek tili)
"""

import subprocess
import os
import sys
import json
import time
import sqlite3
import hashlib
from datetime import datetime
from pathlib import Path
import re
import threading

class Ranglar:
    HEADER = '\033[95m'
    KOK = '\033[94m'
    YASHIL = '\033[92m'
    SARIQ = '\033[93m'
    QIZIL = '\033[91m'
    OQRANG = '\033[96m'
    TUGATISH = '\033[0m'
    QALIN = '\033[1m'
    CHIZIQ = '\033[4m'

class ADBForensics:
    def __init__(self):
        self.chiqish_papka = f"forensik_malumot_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.qurilma_id = None
        self.root_bor = False
        self.qurilma_malumoti = {}
        
    def banner_chiqar(self):
        banner = f"""
{Ranglar.OQRANG}╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║     ADB FORENSIK MA'LUMOT EKSTRAKTORI v2.0                ║
║     Mobil Qurilmalarni To'liq Tahlil Qilish Vositasi      ║
║     O'zbek Tili - Professional Edition                    ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝{Ranglar.TUGATISH}
        """
        print(banner)
    
    def adb_buyruq(self, buyruq, shell=False, timeout=30):
        """ADB buyrug'ini bajarish"""
        try:
            if shell:
                toliq_buyruq = f"adb -s {self.qurilma_id} shell {buyruq}" if self.qurilma_id else f"adb shell {buyruq}"
            else:
                toliq_buyruq = f"adb -s {self.qurilma_id} {buyruq}" if self.qurilma_id else f"adb {buyruq}"
            
            natija = subprocess.run(toliq_buyruq, shell=True, capture_output=True, text=True, timeout=timeout)
            return natija.stdout.strip()
        except subprocess.TimeoutExpired:
            return "[XATO] Buyruq vaqti tugadi"
        except Exception as e:
            return f"[XATO] {str(e)}"
    
    def adb_tekshir(self):
        """ADB o'rnatilganligini tekshirish"""
        try:
            subprocess.run(['adb', 'version'], capture_output=True, check=True)
            return True
        except:
            print(f"{Ranglar.QIZIL}[!] ADB topilmadi! Android Debug Bridge o'rnating{Ranglar.TUGATISH}")
            print(f"{Ranglar.SARIQ}[*] Ubuntu/Debian: sudo apt install adb{Ranglar.TUGATISH}")
            print(f"{Ranglar.SARIQ}[*] Arch: sudo pacman -S android-tools{Ranglar.TUGATISH}")
            return False
    
    def qurilmalar_royxati(self):
        """Ulangan qurilmalar ro'yxati"""
        chiqish = self.adb_buyruq("devices")
        qatorlar = chiqish.split('\n')[1:]
        qurilmalar = []
        for qator in qatorlar:
            if qator.strip() and 'device' in qator:
                qurilma_id = qator.split()[0]
                qurilmalar.append(qurilma_id)
        return qurilmalar
    
    def qurilma_tanlash(self):
        """Maqsadli qurilmani tanlash"""
        qurilmalar = self.qurilmalar_royxati()
        
        if not qurilmalar:
            print(f"{Ranglar.QIZIL}[!] Hech qanday qurilma ulanmagan!{Ranglar.TUGATISH}")
            print(f"{Ranglar.SARIQ}[*] USB debugging yoqilganligiga ishonch hosil qiling{Ranglar.TUGATISH}")
            print(f"{Ranglar.SARIQ}[*] Sozlamalar > Dasturchi parametrlari > USB debugging{Ranglar.TUGATISH}")
            return False
        
        if len(qurilmalar) == 1:
            self.qurilma_id = qurilmalar[0]
            print(f"{Ranglar.YASHIL}[+] Tanlangan qurilma: {self.qurilma_id}{Ranglar.TUGATISH}")
            return True
        
        print(f"{Ranglar.OQRANG}[*] Bir nechta qurilma topildi:{Ranglar.TUGATISH}")
        for idx, qurilma in enumerate(qurilmalar, 1):
            print(f"    {idx}. {qurilma}")
        
        try:
            tanlov = int(input(f"{Ranglar.SARIQ}Qurilmani tanlang (1-{len(qurilmalar)}): {Ranglar.TUGATISH}"))
            if 1 <= tanlov <= len(qurilmalar):
                self.qurilma_id = qurilmalar[tanlov-1]
                print(f"{Ranglar.YASHIL}[+] Tanlangan qurilma: {self.qurilma_id}{Ranglar.TUGATISH}")
                return True
        except:
            pass
        
        print(f"{Ranglar.QIZIL}[!] Noto'g'ri tanlov{Ranglar.TUGATISH}")
        return False
    
    def root_tekshir(self):
        """Qurilmada root borligini tekshirish"""
        chiqish = self.adb_buyruq("su -c 'id'", shell=True)
        self.root_bor = 'uid=0' in chiqish
        if self.root_bor:
            print(f"{Ranglar.YASHIL}[+] Qurilma ROOT qilingan - To'liq kirish mavjud{Ranglar.TUGATISH}")
        else:
            print(f"{Ranglar.SARIQ}[!] Qurilma ROOT qilinmagan - Cheklangan kirish{Ranglar.TUGATISH}")
        return self.root_bor
    
    def qurilma_malumoti_olish(self):
        """Qurilma haqida to'liq ma'lumot"""
        print(f"\n{Ranglar.OQRANG}[*] Qurilma ma'lumotlarini yig'yapman...{Ranglar.TUGATISH}")
        
        malumot = {
            'ishlab_chiqaruvchi': self.adb_buyruq("getprop ro.product.manufacturer", shell=True),
            'model': self.adb_buyruq("getprop ro.product.model", shell=True),
            'android_versiya': self.adb_buyruq("getprop ro.build.version.release", shell=True),
            'sdk_versiya': self.adb_buyruq("getprop ro.build.version.sdk", shell=True),
            'seriya_raqam': self.adb_buyruq("getprop ro.serialno", shell=True),
            'imei': self.adb_buyruq("service call iphonesubinfo 1", shell=True),
            'wifi_mac': self.adb_buyruq("cat /sys/class/net/wlan0/address", shell=True),
            'batareya_quvvat': self.adb_buyruq("dumpsys battery | grep level", shell=True),
            'ekran_olchami': self.adb_buyruq("wm size", shell=True),
            'ram_malumoti': self.adb_buyruq("cat /proc/meminfo | grep MemTotal", shell=True),
            'cpu_malumoti': self.adb_buyruq("cat /proc/cpuinfo | grep 'model name'", shell=True),
            'xotira_hajmi': self.adb_buyruq("df -h /data", shell=True),
            'til_sozlama': self.adb_buyruq("getprop persist.sys.language", shell=True),
            'vaqt_mintaqasi': self.adb_buyruq("getprop persist.sys.timezone", shell=True),
            'build_raqam': self.adb_buyruq("getprop ro.build.display.id", shell=True),
        }
        
        self.qurilma_malumoti = malumot
        
        # Ma'lumotni saqlash
        os.makedirs(self.chiqish_papka, exist_ok=True)
        with open(f"{self.chiqish_papka}/qurilma_malumoti.json", 'w', encoding='utf-8') as f:
            json.dump(malumot, f, indent=4, ensure_ascii=False)
        
        # Inson o'qiy oladigan format
        with open(f"{self.chiqish_papka}/qurilma_malumoti.txt", 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write("QURILMA MA'LUMOTLARI\n")
            f.write("="*60 + "\n\n")
            for kalit, qiymat in malumot.items():
                f.write(f"{kalit.replace('_', ' ').title()}: {qiymat}\n")
        
        print(f"{Ranglar.YASHIL}[+] Qurilma ma'lumotlari saqlandi{Ranglar.TUGATISH}")
        return malumot
    
    def kontaktlar_olish(self):
        """Kontaktlar bazasini olish"""
        print(f"\n{Ranglar.OQRANG}[*] Kontaktlarni yig'yapman...{Ranglar.TUGATISH}")
        
        try:
            buyruq = "pull /data/data/com.android.providers.contacts/databases/contacts2.db"
            chiqish = self.adb_buyruq(buyruq)
            
            if "pulled" in chiqish.lower() or os.path.exists("contacts2.db"):
                manzil = f"{self.chiqish_papka}/contacts2.db"
                if os.path.exists("contacts2.db"):
                    os.rename("contacts2.db", manzil)
                    self.kontaktlar_tahlil(manzil)
                print(f"{Ranglar.YASHIL}[+] Kontaktlar bazasi olindi{Ranglar.TUGATISH}")
                return True
            else:
                print(f"{Ranglar.QIZIL}[!] Kontaktlarni olishda xatolik (root kerak bo'lishi mumkin){Ranglar.TUGATISH}")
                return False
        except Exception as e:
            print(f"{Ranglar.QIZIL}[!] Xatolik: {e}{Ranglar.TUGATISH}")
            return False
    
    def kontaktlar_tahlil(self, db_fayl):
        """Kontaktlar bazasini tahlil qilish"""
        try:
            ulanish = sqlite3.connect(db_fayl)
            cursor = ulanish.cursor()
            
            cursor.execute("SELECT name, data1 FROM view_contacts WHERE mimetype='vnd.android.cursor.item/phone_v2'")
            kontaktlar = cursor.fetchall()
            
            with open(f"{self.chiqish_papka}/kontaktlar_royxati.txt", 'w', encoding='utf-8') as f:
                f.write("="*60 + "\n")
                f.write("KONTAKTLAR RO'YXATI\n")
                f.write("="*60 + "\n\n")
                for ism, telefon in kontaktlar:
                    f.write(f"Ism: {ism}\nTelefon: {telefon}\n" + "-"*40 + "\n")
            
            ulanish.close()
            print(f"{Ranglar.YASHIL}[+] {len(kontaktlar)} ta kontakt tahlil qilindi{Ranglar.TUGATISH}")
        except:
            pass
    
    def sms_olish(self):
        """SMS/MMS xabarlarini olish"""
        print(f"\n{Ranglar.OQRANG}[*] SMS/MMS xabarlarini yig'yapman...{Ranglar.TUGATISH}")
        
        try:
            buyruq = "pull /data/data/com.android.providers.telephony/databases/mmssms.db"
            chiqish = self.adb_buyruq(buyruq)
            
            if "pulled" in chiqish.lower() or os.path.exists("mmssms.db"):
                manzil = f"{self.chiqish_papka}/mmssms.db"
                if os.path.exists("mmssms.db"):
                    os.rename("mmssms.db", manzil)
                    self.sms_tahlil(manzil)
                print(f"{Ranglar.YASHIL}[+] SMS/MMS bazasi olindi{Ranglar.TUGATISH}")
                return True
            else:
                print(f"{Ranglar.QIZIL}[!] SMS olishda xatolik (root kerak bo'lishi mumkin){Ranglar.TUGATISH}")
                return False
        except Exception as e:
            print(f"{Ranglar.QIZIL}[!] Xatolik: {e}{Ranglar.TUGATISH}")
            return False
    
    def sms_tahlil(self, db_fayl):
        """SMS bazasini tahlil qilish"""
        try:
            ulanish = sqlite3.connect(db_fayl)
            cursor = ulanish.cursor()
            
            cursor.execute("SELECT address, date, body, type FROM sms ORDER BY date DESC LIMIT 1000")
            xabarlar = cursor.fetchall()
            
            with open(f"{self.chiqish_papka}/sms_xabarlar.txt", 'w', encoding='utf-8') as f:
                f.write("="*60 + "\n")
                f.write("SMS XABARLAR RO'YXATI\n")
                f.write("="*60 + "\n\n")
                for raqam, vaqt, matn, tur in xabarlar:
                    vaqt_str = datetime.fromtimestamp(int(vaqt)/1000).strftime('%Y-%m-%d %H:%M:%S')
                    tur_str = "Kelgan" if tur == 1 else "Yuborilgan"
                    f.write(f"Raqam: {raqam}\n")
                    f.write(f"Vaqt: {vaqt_str}\n")
                    f.write(f"Tur: {tur_str}\n")
                    f.write(f"Matn: {matn}\n")
                    f.write("-"*60 + "\n")
            
            ulanish.close()
            print(f"{Ranglar.YASHIL}[+] {len(xabarlar)} ta xabar tahlil qilindi{Ranglar.TUGATISH}")
        except:
            pass
    
    def qongiroqlar_olish(self):
        """Qo'ng'iroqlar tarixini olish"""
        print(f"\n{Ranglar.OQRANG}[*] Qo'ng'iroqlar tarixini yig'yapman...{Ranglar.TUGATISH}")
        
        try:
            buyruq = "content query --uri content://call_log/calls"
            chiqish = self.adb_buyruq(buyruq, shell=True)
            
            if chiqish and "Row:" in chiqish:
                with open(f"{self.chiqish_papka}/qongiroqlar_tarixi.txt", 'w', encoding='utf-8') as f:
                    f.write("="*60 + "\n")
                    f.write("QO'NG'IROQLAR TARIXI\n")
                    f.write("="*60 + "\n\n")
                    f.write(chiqish)
                print(f"{Ranglar.YASHIL}[+] Qo'ng'iroqlar tarixi olindi{Ranglar.TUGATISH}")
                return True
            else:
                print(f"{Ranglar.QIZIL}[!] Qo'ng'iroqlar tarixini olishda xatolik{Ranglar.TUGATISH}")
                return False
        except Exception as e:
            print(f"{Ranglar.QIZIL}[!] Xatolik: {e}{Ranglar.TUGATISH}")
            return False
    
    def ilovalar_royxati(self):
        """O'rnatilgan ilovalar ro'yxati"""
        print(f"\n{Ranglar.OQRANG}[*] O'rnatilgan ilovalar ro'yxatini olaman...{Ranglar.TUGATISH}")
        
        try:
            # Barcha paketlar
            buyruq1 = "pm list packages -f"
            chiqish1 = self.adb_buyruq(buyruq1, shell=True)
            
            # Foydalanuvchi ilovalari
            buyruq2 = "pm list packages -3"
            chiqish2 = self.adb_buyruq(buyruq2, shell=True)
            
            ilovalar = []
            for qator in chiqish1.split('\n'):
                if qator.startswith('package:'):
                    ilovalar.append(qator.replace('package:', ''))
            
            foydalanuvchi_ilovalari = []
            for qator in chiqish2.split('\n'):
                if qator.startswith('package:'):
                    foydalanuvchi_ilovalari.append(qator.replace('package:', ''))
            
            with open(f"{self.chiqish_papka}/barcha_ilovalar.txt", 'w', encoding='utf-8') as f:
                f.write("="*60 + "\n")
                f.write("BARCHA O'RNATILGAN ILOVALAR\n")
                f.write("="*60 + "\n\n")
                for ilova in ilovalar:
                    f.write(f"{ilova}\n")
            
            with open(f"{self.chiqish_papka}/foydalanuvchi_ilovalari.txt", 'w', encoding='utf-8') as f:
                f.write("="*60 + "\n")
                f.write("FOYDALANUVCHI O'RNATGAN ILOVALAR\n")
                f.write("="*60 + "\n\n")
                for ilova in foydalanuvchi_ilovalari:
                    f.write(f"{ilova}\n")
            
            print(f"{Ranglar.YASHIL}[+] Jami {len(ilovalar)} ta ilova topildi{Ranglar.TUGATISH}")
            print(f"{Ranglar.YASHIL}[+] Foydalanuvchi ilovalari: {len(foydalanuvchi_ilovalari)} ta{Ranglar.TUGATISH}")
            return True
        except Exception as e:
            print(f"{Ranglar.QIZIL}[!] Xatolik: {e}{Ranglar.TUGATISH}")
            return False
    
    def skrinshot_olish(self):
        """Ekran suratini olish"""
        print(f"\n{Ranglar.OQRANG}[*] Ekran suratini olaman...{Ranglar.TUGATISH}")
        
        try:
            vaqt_tamgasi = datetime.now().strftime('%Y%m%d_%H%M%S')
            masofaviy_yol = f"/sdcard/screenshot_{vaqt_tamgasi}.png"
            mahalliy_yol = f"{self.chiqish_papka}/screenshot_{vaqt_tamgasi}.png"
            
            self.adb_buyruq(f"screencap -p {masofaviy_yol}", shell=True)
            time.sleep(1)
            self.adb_buyruq(f"pull {masofaviy_yol} {mahalliy_yol}")
            self.adb_buyruq(f"rm {masofaviy_yol}", shell=True)
            
            if os.path.exists(mahalliy_yol):
                print(f"{Ranglar.YASHIL}[+] Ekran surati saqlandi{Ranglar.TUGATISH}")
                return True
            else:
                print(f"{Ranglar.QIZIL}[!] Ekran suratini olishda xatolik{Ranglar.TUGATISH}")
                return False
        except Exception as e:
            print(f"{Ranglar.QIZIL}[!] Xatolik: {e}{Ranglar.TUGATISH}")
            return False
    
    def video_yozish(self, davomiyligi=10):
        """Ekrandan video yozish"""
        print(f"\n{Ranglar.OQRANG}[*] {davomiyligi} soniya video yozilmoqda...{Ranglar.TUGATISH}")
        
        try:
            vaqt_tamgasi = datetime.now().strftime('%Y%m%d_%H%M%S')
            masofaviy_yol = f"/sdcard/screenrecord_{vaqt_tamgasi}.mp4"
            mahalliy_yol = f"{self.chiqish_papka}/screenrecord_{vaqt_tamgasi}.mp4"
            
            print(f"{Ranglar.SARIQ}[*] Yozuv boshlandi... Kutib turing{Ranglar.TUGATISH}")
            buyruq = f"screenrecord --time-limit {davomiyligi} {masofaviy_yol}"
            self.adb_buyruq(buyruq, shell=True)
            
            self.adb_buyruq(f"pull {masofaviy_yol} {mahalliy_yol}")
            self.adb_buyruq(f"rm {masofaviy_yol}", shell=True)
            
            if os.path.exists(mahalliy_yol):
                print(f"{Ranglar.YASHIL}[+] Video yozuv saqlandi{Ranglar.TUGATISH}")
                return True
            else:
                print(f"{Ranglar.QIZIL}[!] Video yozishda xatolik{Ranglar.TUGATISH}")
                return False
        except Exception as e:
            print(f"{Ranglar.QIZIL}[!] Xatolik: {e}{Ranglar.TUGATISH}")
            return False
    
    def logcat_olish(self):
        """Tizim loglarini olish"""
        print(f"\n{Ranglar.OQRANG}[*] Tizim loglarini yig'yapman...{Ranglar.TUGATISH}")
        
        try:
            chiqish = self.adb_buyruq("logcat -d", shell=True)
            
            with open(f"{self.chiqish_papka}/tizim_loglari.txt", 'w', encoding='utf-8') as f:
                f.write(chiqish)
            
            print(f"{Ranglar.YASHIL}[+] Tizim loglari saqlandi{Ranglar.TUGATISH}")
            return True
        except Exception as e:
            print(f"{Ranglar.QIZIL}[!] Xatolik: {e}{Ranglar.TUGATISH}")
            return False
    
    def whatsapp_zaxira(self):
        """WhatsApp ma'lumotlarini zaxiralash"""
        print(f"\n{Ranglar.OQRANG}[*] WhatsApp zaxirasi olinmoqda...{Ranglar.TUGATISH}")
        
        try:
            wa_yol = "/sdcard/WhatsApp"
            mahalliy_wa = f"{self.chiqish_papka}/WhatsApp_Zaxira"
            
            tekshirish = self.adb_buyruq(f"ls {wa_yol}", shell=True)
            if "No such file" in tekshirish:
                print(f"{Ranglar.SARIQ}[!] WhatsApp qurilmada topilmadi{Ranglar.TUGATISH}")
                return False
            
            os.makedirs(mahalliy_wa, exist_ok=True)
            buyruq = f"pull {wa_yol} {mahalliy_wa}"
            self.adb_buyruq(buyruq)
            
            print(f"{Ranglar.YASHIL}[+] WhatsApp zaxirasi yakunlandi{Ranglar.TUGATISH}")
            return True
        except Exception as e:
            print(f"{Ranglar.QIZIL}[!] Xatolik: {e}{Ranglar.TUGATISH}")
            return False
    
    def telegram_zaxira(self):
        """Telegram ma'lumotlarini zaxiralash"""
        print(f"\n{Ranglar.OQRANG}[*] Telegram zaxirasi olinmoqda...{Ranglar.TUGATISH}")
        
        try:
            tg_yol = "/sdcard/Telegram"
            mahalliy_tg = f"{self.chiqish_papka}/Telegram_Zaxira"
            
            tekshirish = self.adb_buyruq(f"ls {tg_yol}", shell=True)
            if "No such file" in tekshirish:
                print(f"{Ranglar.SARIQ}[!] Telegram qurilmada topilmadi{Ranglar.TUGATISH}")
                return False
            
            os.makedirs(mahalliy_tg, exist_ok=True)
            buyruq = f"pull {tg_yol} {mahalliy_tg}"
            self.adb_buyruq(buyruq)
            
            print(f"{Ranglar.YASHIL}[+] Telegram zaxirasi yakunlandi{Ranglar.TUGATISH}")
            return True
        except Exception as e:
            print(f"{Ranglar.QIZIL}[!] Xatolik: {e}{Ranglar.TUGATISH}")
            return False
    
    def rasmlar_zaxira(self):
        """Barcha rasmlarni zaxiralash"""
        print(f"\n{Ranglar.OQRANG}[*] Rasmlar zaxiralanyapti...{Ranglar.TUGATISH}")
        
        try:
            dcim_yol = "/sdcard/DCIM"
            rasm_yol = "/sdcard/Pictures"
            mahalliy_rasm = f"{self.chiqish_papka}/Rasmlar_Zaxira"
            
            os.makedirs(mahalliy_rasm, exist_ok=True)
            
            self.adb_buyruq(f"pull {dcim_yol} {mahalliy_rasm}/DCIM")
            self.adb_buyruq(f"pull {rasm_yol} {mahalliy_rasm}/Pictures")
            
            print(f"{Ranglar.YASHIL}[+] Rasmlar zaxiralandi{Ranglar.TUGATISH}")
            return True
        except Exception as e:
            print(f"{Ranglar.QIZIL}[!] Xatolik: {e}{Ranglar.TUGATISH}")
            return False
    
    def videolar_zaxira(self):
        """Barcha videolarni zaxiralash"""
        print(f"\n{Ranglar.OQRANG}[*] Videolar zaxiralanyapti...{Ranglar.TUGATISH}")
        
        try:
            video_yol = "/sdcard/Movies"
            mahalliy_video = f"{self.chiqish_papka}/Videolar_Zaxira"
            
            os.makedirs(mahalliy_video, exist_ok=True)
            self.adb_buyruq(f"pull {video_yol} {mahalliy_video}")
            
            print(f"{Ranglar.YASHIL}[+] Videolar zaxiralandi{Ranglar.TUGATISH}")
            return True
        except Exception as e:
            print(f"{Ranglar.QIZIL}[!] Xatolik: {e}{Ranglar.TUGATISH}")
            return False
    
    def hujjatlar_zaxira(self):
        """Barcha hujjatlarni zaxiralash"""
        print(f"\n{Ranglar.OQRANG}[*] Hujjatlar zaxiralanyapti...{Ranglar.TUGATISH}")
        
        try:
            hujjat_yol = "/sdcard/Documents"
            yuklab_olish_yol = "/sdcard/Download"
            mahalliy_hujjat = f"{self.chiqish_papka}/Hujjatlar_Zaxira"
            
            os.makedirs(mahalliy_hujjat, exist_ok=True)
            
            self.adb_buyruq(f"pull {hujjat_yol} {mahalliy_hujjat}/Documents")
            self.adb_buyruq(f"pull {yuklab_olish_yol} {mahalliy_hujjat}/Downloads")
            
            print(f"{Ranglar.YASHIL}[+] Hujjatlar zaxiralandi{Ranglar.TUGATISH}")
            return True
        except Exception as e:
            print(f"{Ranglar.QIZIL}[!] Xatolik: {e}{Ranglar.TUGATISH}")
            return False
    
    def wifi_parollar_olish(self):
        """Saqlangan WiFi parollarni olish (ROOT kerak)"""
        print(f"\n{Ranglar.OQRANG}[*] WiFi parollarini olaman (ROOT kerak)...{Ranglar.TUGATISH}")
        
        if not self.root_bor:
            print(f"{Ranglar.SARIQ}[!] Bu funksiya ROOT huquqi talab qiladi{Ranglar.TUGATISH}")
            return False
        
        try:
            buyruq = "su -c 'cat /data/misc/wifi/wpa_supplicant.conf'"
            chiqish = self.adb_buyruq(buyruq, shell=True)
            
            if chiqish and "ssid" in chiqish.lower():
                with open(f"{self.chiqish_papka}/wifi_parollar.txt", 'w', encoding='utf-8') as f:
                    f.write("="*60 + "\n")
                    f.write("SAQLANGAN WiFi PAROLLAR\n")
                    f.write("="*60 + "\n\n")
                    f.write(chiqish)
                print(f"{Ranglar.YASHIL}[+] WiFi parollar olindi{Ranglar.TUGATISH}")
                return True
            else:
                print(f"{Ranglar.QIZIL}[!] WiFi ma'lumotlarini olishda xatolik{Ranglar.TUGATISH}")
                return False
        except Exception as e:
            print(f"{Ranglar.QIZIL}[!] Xatolik: {e}{Ranglar.TUGATISH}")
            return False
    
    def brauzer_tarixi(self):
        """Brauzer tarixini olish"""
        print(f"\n{Ranglar.OQRANG}[*] Brauzer tarixini yig'yapman...{Ranglar.TUGATISH}")
        
        try:
            # Chrome brauzer tarixi
            chrome_db = "/data/data/com.android.chrome/app_chrome/Default/History"
            buyruq = f"pull {chrome_db}"
            self.adb_buyruq(buyruq)
            
            if os.path.exists("History"):
                manzil = f"{self.chiqish_papka}/chrome_history.db"
                os.rename("History", manzil)
                self.brauzer_tahlil(manzil)
                print(f"{Ranglar.YASHIL}[+] Chrome brauzer tarixi olindi{Ranglar.TUGATISH}")
                return True
            else:
                print(f"{Ranglar.SARIQ}[!] Brauzer tarixi topilmadi (root kerak bo'lishi mumkin){Ranglar.TUGATISH}")
                return False
        except Exception as e:
            print(f"{Ranglar.QIZIL}[!] Xatolik: {e}{Ranglar.TUGATISH}")
            return False
    
    def brauzer_tahlil(self, db_fayl):
        """Brauzer tarixini tahlil qilish"""
        try:
            ulanish = sqlite3.connect(db_fayl)
            cursor = ulanish.cursor()
            
            cursor.execute("SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT 500")
            tarix = cursor.fetchall()
            
            with open(f"{self.chiqish_papka}/brauzer_tarixi.txt", 'w', encoding='utf-8') as f:
                f.write("="*60 + "\n")
                f.write("BRAUZER TARIXI\n")
                f.write("="*60 + "\n\n")
                for url, sarlavha, vaqt in tarix:
                    f.write(f"URL: {url}\n")
                    f.write(f"Sarlavha: {sarlavha}\n")
                    f.write(f"Vaqt: {vaqt}\n")
                    f.write("-"*60 + "\n")
            
            ulanish.close()
            print(f"{Ranglar.YASHIL}[+] {len(tarix)} ta brauzer yozuvi tahlil qilindi{Ranglar.TUGATISH}")
        except:
            pass
    
    def xotira_malumoti(self):
        """Xotira va fayl tizimi ma'lumotlari"""
        print(f"\n{Ranglar.OQRANG}[*] Xotira ma'lumotlarini yig'yapman...{Ranglar.TUGATISH}")
        
        try:
            with open(f"{self.chiqish_papka}/xotira_malumoti.txt", 'w', encoding='utf-8') as f:
                f.write("="*60 + "\n")
                f.write("XOTIRA VA FAYL TIZIMI MA'LUMOTLARI\n")
                f.write("="*60 + "\n\n")
                
                # Disk hajmi
                df_chiqish = self.adb_buyruq("df -h", shell=True)
                f.write("DISK HAJMI:\n")
                f.write(df_chiqish + "\n\n")
                
                # Xotira
                mem_chiqish = self.adb_buyruq("cat /proc/meminfo", shell=True)
                f.write("="*60 + "\nXOTIRA:\n")
                f.write(mem_chiqish + "\n\n")
                
                # CPU
                cpu_chiqish = self.adb_buyruq("cat /proc/cpuinfo", shell=True)
                f.write("="*60 + "\nCPU MA'LUMOTI:\n")
                f.write(cpu_chiqish + "\n\n")
            
            print(f"{Ranglar.YASHIL}[+] Xotira ma'lumotlari saqlandi{Ranglar.TUGATISH}")
            return True
        except Exception as e:
            print(f"{Ranglar.QIZIL}[!] Xatolik: {e}{Ranglar.TUGATISH}")
            return False
    
    def tarmoq_malumoti(self):
        """Tarmoq sozlamalari va ulanishlar"""
        print(f"\n{Ranglar.OQRANG}[*] Tarmoq ma'lumotlarini yig'yapman...{Ranglar.TUGATISH}")
        
        try:
            with open(f"{self.chiqish_papka}/tarmoq_malumoti.txt", 'w', encoding='utf-8') as f:
                f.write("="*60 + "\n")
                f.write("TARMOQ MA'LUMOTLARI\n")
                f.write("="*60 + "\n\n")
                
                # IP manzil
                ip_chiqish = self.adb_buyruq("ip addr show", shell=True)
                f.write("IP MANZILLAR:\n")
                f.write(ip_chiqish + "\n\n")
                
                # Tarmoq statistika
                netstat = self.adb_buyruq("netstat -a", shell=True)
                f.write("="*60 + "\nTARMOQ ULANISHLARI:\n")
                f.write(netstat + "\n\n")
                
                # WiFi ma'lumot
                wifi = self.adb_buyruq("dumpsys wifi", shell=True)
                f.write("="*60 + "\nWIFI MA'LUMOTI:\n")
                f.write(wifi[:5000] + "\n\n")  # Birinchi 5000 belgi
            
            print(f"{Ranglar.YASHIL}[+] Tarmoq ma'lumotlari saqlandi{Ranglar.TUGATISH}")
            return True
        except Exception as e:
            print(f"{Ranglar.QIZIL}[!] Xatolik: {e}{Ranglar.TUGATISH}")
            return False
    
    def apk_ekstract(self, paket_nomi):
        """Ilova APK faylini olish"""
        print(f"\n{Ranglar.OQRANG}[*] {paket_nomi} APK fayli olinmoqda...{Ranglar.TUGATISH}")
        
        try:
            # APK yo'lini topish
            yol_buyruq = f"pm path {paket_nomi}"
            yol = self.adb_buyruq(yol_buyruq, shell=True)
            
            if yol and yol.startswith("package:"):
                apk_yol = yol.replace("package:", "").strip()
                mahalliy_yol = f"{self.chiqish_papka}/APK_Fayllar/{paket_nomi}.apk"
                
                os.makedirs(f"{self.chiqish_papka}/APK_Fayllar", exist_ok=True)
                
                self.adb_buyruq(f"pull {apk_yol} {mahalliy_yol}")
                
                if os.path.exists(mahalliy_yol):
                    print(f"{Ranglar.YASHIL}[+] APK fayl olindi: {mahalliy_yol}{Ranglar.TUGATISH}")
                    return True
            
            print(f"{Ranglar.QIZIL}[!] APK faylni olishda xatolik{Ranglar.TUGATISH}")
            return False
        except Exception as e:
            print(f"{Ranglar.QIZIL}[!] Xatolik: {e}{Ranglar.TUGATISH}")
            return False
    
    def barcha_apk_olish(self):
        """Barcha foydalanuvchi APK larini olish"""
        print(f"\n{Ranglar.OQRANG}[*] Barcha foydalanuvchi APK lari olinmoqda...{Ranglar.TUGATISH}")
        
        try:
            buyruq = "pm list packages -3"
            chiqish = self.adb_buyruq(buyruq, shell=True)
            
            paketlar = []
            for qator in chiqish.split('\n'):
                if qator.startswith('package:'):
                    paket = qator.replace('package:', '').strip()
                    paketlar.append(paket)
            
            print(f"{Ranglar.SARIQ}[*] {len(paketlar)} ta foydalanuvchi ilovasi topildi{Ranglar.TUGATISH}")
            print(f"{Ranglar.SARIQ}[*] APK fayllar olinmoqda...{Ranglar.TUGATISH}")
            
            for paket in paketlar:
                self.apk_ekstract(paket)
            
            print(f"{Ranglar.YASHIL}[+] Barcha APK fayllar olindi{Ranglar.TUGATISH}")
            return True
        except Exception as e:
            print(f"{Ranglar.QIZIL}[!] Xatolik: {e}{Ranglar.TUGATISH}")
            return False
    
    def hash_hisoblash(self):
        """Olingan fayllar uchun hash hisoblash"""
        print(f"\n{Ranglar.OQRANG}[*] Fayllar uchun hash hisoblanmoqda...{Ranglar.TUGATISH}")
        
        try:
            hash_malumot = []
            
            for root, dirs, files in os.walk(self.chiqish_papka):
                for fayl in files:
                    fayl_yol = os.path.join(root, fayl)
                    if os.path.isfile(fayl_yol):
                        try:
                            with open(fayl_yol, 'rb') as f:
                                fayl_hash = hashlib.sha256(f.read()).hexdigest()
                                fayl_hajmi = os.path.getsize(fayl_yol)
                                hash_malumot.append({
                                    'fayl': fayl_yol,
                                    'sha256': fayl_hash,
                                    'hajm': fayl_hajmi
                                })
                        except:
                            pass
            
            with open(f"{self.chiqish_papka}/fayl_hashlari.json", 'w', encoding='utf-8') as f:
                json.dump(hash_malumot, f, indent=4, ensure_ascii=False)
            
            with open(f"{self.chiqish_papka}/fayl_hashlari.txt", 'w', encoding='utf-8') as f:
                f.write("="*60 + "\n")
                f.write("FAYL HASHLARI (SHA256)\n")
                f.write("="*60 + "\n\n")
                for item in hash_malumot:
                    f.write(f"Fayl: {item['fayl']}\n")
                    f.write(f"Hajm: {item['hajm']} bayt\n")
                    f.write(f"SHA256: {item['sha256']}\n")
                    f.write("-"*60 + "\n")
            
            print(f"{Ranglar.YASHIL}[+] {len(hash_malumot)} ta fayl uchun hash hisoblandi{Ranglar.TUGATISH}")
            return True
        except Exception as e:
            print(f"{Ranglar.QIZIL}[!] Xatolik: {e}{Ranglar.TUGATISH}")
            return False
    
    def hisobot_yaratish(self):
        """To'liq forensik hisobot yaratish"""
        print(f"\n{Ranglar.OQRANG}[*] Forensik hisobot yaratilmoqda...{Ranglar.TUGATISH}")
        
        hisobot = f"""
╔═══════════════════════════════════════════════════════════╗
║         MOBIL FORENSIK EKSTRAKTSIYA HISOBOTI              ║
╚═══════════════════════════════════════════════════════════╝

Ekstraktsiya sanasi: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Qurilma ID: {self.qurilma_id}
Root huquqi: {'Ha' if self.root_bor else "Yoq"}

QURILMA MALUMATLAR:
{'='*60}
"""
        
        for kalit, qiymat in self.qurilma_malumoti.items():
            hisobot += f"{kalit.replace('_', ' ').title()}: {qiymat}\n"
        
        hisobot += f"\n{'='*60}\n"
        hisobot += "OLINGAN FAYLLAR:\n"
        hisobot += f"{'='*60}\n\n"
        
        if os.path.exists(self.chiqish_papka):
            jami_hajm = 0
            fayl_soni = 0
            for root, dirs, files in os.walk(self.chiqish_papka):
                for fayl in files:
                    fayl_yol = os.path.join(root, fayl)
                    if os.path.isfile(fayl_yol):
                        hajm = os.path.getsize(fayl_yol)
                        jami_hajm += hajm
                        fayl_soni += 1
                        nisbiy_yol = os.path.relpath(fayl_yol, self.chiqish_papka)
                        hisobot += f"  - {nisbiy_yol} ({hajm} bayt)\n"
            
            hisobot += f"\n{'='*60}\n"
            hisobot += f"Jami fayllar: {fayl_soni}\n"
            hisobot += f"Jami hajm: {jami_hajm / (1024*1024):.2f} MB\n"
        
        hisobot += f"\n{'='*60}\n"
        hisobot += "MUHIM ESLATMALAR:\n"
        hisobot += f"{'='*60}\n"
        hisobot += "1. Bazi ekstraktsiyalar root huquqi talab qiladi\n"
        hisobot += "2. Bazalar SQLite brauzer bilan tahlil qilinishi mumkin\n"
        hisobot += "3. Hash qiymatlar fayl integriteti uchun ishlatiladi\n"
        hisobot += "4. Barcha malumotlar mahfiy va xavfsiz saqlanishi kerak\n"
        hisobot += "5. Forensik tahlil qonuniy maqsadlarda amalga oshirilishi kerak\n"
        
        hisobot_yol = f"{self.chiqish_papka}/FORENSIK_HISOBOT.txt"
        with open(hisobot_yol, 'w', encoding='utf-8') as f:
            f.write(hisobot)
        
        print(hisobot)
        print(f"{Ranglar.YASHIL}[+] Hisobot saqlandi: {hisobot_yol}{Ranglar.TUGATISH}")
    
    def menyu_chiqar(self):
        """Interaktiv menyu"""
        menyu = f"""
{Ranglar.QALIN}═══════════════════════════════════════════════════════════{Ranglar.TUGATISH}
{Ranglar.SARIQ}           FORENSIK EKSTRAKTSIYA MENYUSI{Ranglar.TUGATISH}
{Ranglar.QALIN}═══════════════════════════════════════════════════════════{Ranglar.TUGATISH}

{Ranglar.YASHIL}ASOSIY MA'LUMOTLAR:{Ranglar.TUGATISH}
{Ranglar.OQRANG}[1]{Ranglar.TUGATISH}  Qurilma ma'lumotlarini olish
{Ranglar.OQRANG}[2]{Ranglar.TUGATISH}  Kontaktlar bazasini olish
{Ranglar.OQRANG}[3]{Ranglar.TUGATISH}  SMS/MMS xabarlarini olish
{Ranglar.OQRANG}[4]{Ranglar.TUGATISH}  Qo'ng'iroqlar tarixini olish
{Ranglar.OQRANG}[5]{Ranglar.TUGATISH}  O'rnatilgan ilovalar ro'yxati

{Ranglar.YASHIL}MULTIMEDIA:{Ranglar.TUGATISH}
{Ranglar.OQRANG}[6]{Ranglar.TUGATISH}  Ekran surati olish
{Ranglar.OQRANG}[7]{Ranglar.TUGATISH}  Ekrandan video yozish (10 soniya)
{Ranglar.OQRANG}[8]{Ranglar.TUGATISH}  Barcha rasmlarni zaxiralash
{Ranglar.OQRANG}[9]{Ranglar.TUGATISH}  Barcha videolarni zaxiralash
{Ranglar.OQRANG}[10]{Ranglar.TUGATISH} Barcha hujjatlarni zaxiralash

{Ranglar.YASHIL}MESSENGER VA IJTIMOIY TARMOQLAR:{Ranglar.TUGATISH}
{Ranglar.OQRANG}[11]{Ranglar.TUGATISH} WhatsApp zaxirasi
{Ranglar.OQRANG}[12]{Ranglar.TUGATISH} Telegram zaxirasi

{Ranglar.YASHIL}TARMOQ VA XAVFSIZLIK:{Ranglar.TUGATISH}
{Ranglar.OQRANG}[13]{Ranglar.TUGATISH} WiFi parollarni olish (ROOT)
{Ranglar.OQRANG}[14]{Ranglar.TUGATISH} Brauzer tarixini olish
{Ranglar.OQRANG}[15]{Ranglar.TUGATISH} Tarmoq ma'lumotlarini olish
{Ranglar.OQRANG}[16]{Ranglar.TUGATISH} Tizim loglarini olish (Logcat)

{Ranglar.YASHIL}ILOVALAR:{Ranglar.TUGATISH}
{Ranglar.OQRANG}[17]{Ranglar.TUGATISH} Bitta ilova APK sini olish
{Ranglar.OQRANG}[18]{Ranglar.TUGATISH} Barcha foydalanuvchi APK larini olish

{Ranglar.YASHIL}TAHLIL VA HISOBOT:{Ranglar.TUGATISH}
{Ranglar.OQRANG}[19]{Ranglar.TUGATISH} Xotira va tizim ma'lumotlari
{Ranglar.OQRANG}[20]{Ranglar.TUGATISH} Fayllar uchun hash hisoblash
{Ranglar.OQRANG}[21]{Ranglar.TUGATISH} To'liq forensik hisobot

{Ranglar.YASHIL}MAXSUS:{Ranglar.TUGATISH}
{Ranglar.OQRANG}[99]{Ranglar.TUGATISH} HAMMA NARSANI OLISH (To'liq dump)
{Ranglar.QIZIL}[0]{Ranglar.TUGATISH}  Chiqish

{Ranglar.QALIN}═══════════════════════════════════════════════════════════{Ranglar.TUGATISH}
"""
        print(menyu)
    
    def hammasi_olish(self):
        """Barcha mavjud ma'lumotlarni olish"""
        print(f"\n{Ranglar.SARIQ}[*] Toliq forensik ekstraktsiya boshlanmoqda...{Ranglar.TUGATISH}")
        print(f"{Ranglar.SARIQ}[*] Bu biroz vaqt olishi mumkin. Iltimos, kutib turing...{Ranglar.TUGATISH}\n")
        
        # Asosiy ma'lumotlar
        self.qurilma_malumoti_olish()
        self.kontaktlar_olish()
        self.sms_olish()
        self.qongiroqlar_olish()
        self.ilovalar_royxati()
        
        # Multimedia
        self.skrinshot_olish()
        self.rasmlar_zaxira()
        self.videolar_zaxira()
        self.hujjatlar_zaxira()
        
        # Messengerlar
        self.whatsapp_zaxira()
        self.telegram_zaxira()
        
        # Tarmoq va xavfsizlik
        if self.root_bor:
            self.wifi_parollar_olish()
        self.brauzer_tarixi()
        self.tarmoq_malumoti()
        self.logcat_olish()
        
        # Tizim
        self.xotira_malumoti()
        
        # Tahlil
        self.hash_hisoblash()
        self.hisobot_yaratish()
        
        print(f"\n{Ranglar.YASHIL}{'='*60}{Ranglar.TUGATISH}")
        print(f"{Ranglar.YASHIL}[+] TOLIQ EKSTRAKTSIYA MUVAFFAQIYATLI YAKUNLANDI!{Ranglar.TUGATISH}")
        print(f"{Ranglar.YASHIL}{'='*60}{Ranglar.TUGATISH}")
    
    def ishga_tushirish(self):
        """Asosiy dastur sikli"""
        self.banner_chiqar()
        
        # ADB tekshirish
        if not self.adb_tekshir():
            return
        
        # Qurilmani tanlash
        if not self.qurilma_tanlash():
            return
        
        # Root tekshirish
        self.root_tekshir()
        
        # Chiqish papkasini yaratish
        os.makedirs(self.chiqish_papka, exist_ok=True)
        print(f"{Ranglar.YASHIL}[+] Chiqish papkasi: {self.chiqish_papka}{Ranglar.TUGATISH}")
        
        # Asosiy sikl
        while True:
            self.menyu_chiqar()
            try:
                tanlov = input(f"{Ranglar.OQRANG}Tanlovingizni kiriting: {Ranglar.TUGATISH}").strip()
                
                if tanlov == '1':
                    self.qurilma_malumoti_olish()
                elif tanlov == '2':
                    self.kontaktlar_olish()
                elif tanlov == '3':
                    self.sms_olish()
                elif tanlov == '4':
                    self.qongiroqlar_olish()
                elif tanlov == '5':
                    self.ilovalar_royxati()
                elif tanlov == '6':
                    self.skrinshot_olish()
                elif tanlov == '7':
                    self.video_yozish()
                elif tanlov == '8':
                    self.rasmlar_zaxira()
                elif tanlov == '9':
                    self.videolar_zaxira()
                elif tanlov == '10':
                    self.hujjatlar_zaxira()
                elif tanlov == '11':
                    self.whatsapp_zaxira()
                elif tanlov == '12':
                    self.telegram_zaxira()
                elif tanlov == '13':
                    self.wifi_parollar_olish()
                elif tanlov == '14':
                    self.brauzer_tarixi()
                elif tanlov == '15':
                    self.tarmoq_malumoti()
                elif tanlov == '16':
                    self.logcat_olish()
                elif tanlov == '17':
                    paket = input(f"{Ranglar.SARIQ}Paket nomini kiriting (masalan: com.whatsapp): {Ranglar.TUGATISH}")
                    self.apk_ekstract(paket.strip())
                elif tanlov == '18':
                    self.barcha_apk_olish()
                elif tanlov == '19':
                    self.xotira_malumoti()
                elif tanlov == '20':
                    self.hash_hisoblash()
                elif tanlov == '21':
                    self.hisobot_yaratish()
                elif tanlov == '99':
                    tasdiqlash = input(f"{Ranglar.SARIQ}Hamma narsani olasizmi? (ha/yoq): {Ranglar.TUGATISH}")
                    if tasdiqlash.lower() in ['ha', 'yes', 'y']:
                        self.hammasi_olish()
                elif tanlov == '0':
                    print(f"\n{Ranglar.SARIQ}[*] Dasturdan chiqilmoqda...{Ranglar.TUGATISH}")
                    print(f"{Ranglar.YASHIL}[+] Forensik ma'lumotlar saqlandi: {self.chiqish_papka}{Ranglar.TUGATISH}")
                    break
                else:
                    print(f"{Ranglar.QIZIL}[!] Noto'g'ri tanlov! Qaytadan urinib ko'ring.{Ranglar.TUGATISH}")
                
                input(f"\n{Ranglar.SARIQ}Davom etish uchun Enter tugmasini bosing...{Ranglar.TUGATISH}")
                os.system('clear' if os.name != 'nt' else 'cls')
                self.banner_chiqar()
                
            except KeyboardInterrupt:
                print(f"\n{Ranglar.SARIQ}[*] Foydalanuvchi tomonidan to'xtatildi{Ranglar.TUGATISH}")
                break
            except Exception as e:
                print(f"{Ranglar.QIZIL}[!] Xatolik yuz berdi: {e}{Ranglar.TUGATISH}")

if __name__ == "__main__":
    try:
        forensics = ADBForensics()
        forensics.ishga_tushirish()
    except KeyboardInterrupt:
        print(f"\n{Ranglar.SARIQ}[*] Dastur to'xtatildi{Ranglar.TUGATISH}")
    except Exception as e:
        print(f"{Ranglar.QIZIL}[!] Fatal xatolik: {e}{Ranglar.TUGATISH}")
        sys.exit(1)
