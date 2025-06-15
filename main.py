import time
import smbus2 as smbus
from datetime import datetime
from alarm import alarm_cal
from aydinlatma import led_yak
from yonlendirme import yurut_json
from posta import deprem_mail_gonder
import os


# ADXL345 ayarları
DEVICE_ADDRESS = 0x53
bus = smbus.SMBus(1)

# Ayarlar
SAMPLE_INTERVAL = 0.1  # saniye
REQUIRED_DURATION = 2.0
REQUIRED_COUNT = int(REQUIRED_DURATION / SAMPLE_INTERVAL)

# Sayaçlar
hareket_sayaci = 0
ALARM_TETIKLENDI = False

# Global kalibrasyon ofsetleri (başlangıçta 0, sonra ölçülür)
x0, y0, z0 = 0, 0, 0

# Email bilgileri
SENDER_EMAIL = "b.pekalp@gmail.com"
GMAIL_SIFRE = os.getenv("GMAIL_SIFRE")
TARGET_EMAIL = "zzehrakr48@gmail.com"


def adxl345_init():
    bus.write_byte_data(DEVICE_ADDRESS, 0x2D, 0x08)


def read_axes():
    data = bus.read_i2c_block_data(DEVICE_ADDRESS, 0x32, 6)
    x = (data[1] << 8) | data[0]
    y = (data[3] << 8) | data[2]
    z = (data[5] << 8) | data[4]
    x = x - 65536 if x > 32767 else x
    y = y - 65536 if y > 32767 else y
    z = z - 65536 if z > 32767 else z
    return x, y, z


def otomatik_kalibrasyon(num_samples=50):
    print("📏 Kalibrasyon başlatılıyor... Lütfen sensörü sabit tutun.")
    toplam_x = toplam_y = toplam_z = 0
    for _ in range(num_samples):
        x, y, z = read_axes()
        toplam_x += x
        toplam_y += y
        toplam_z += z
        time.sleep(0.05)
    x0 = toplam_x / num_samples
    y0 = toplam_y / num_samples
    z0 = toplam_z / num_samples
    print(f"✅ Kalibrasyon tamamlandı ➤ x0={round(x0)}, y0={round(y0)}, z0={round(z0)}")
    return round(x0), round(y0), round(z0)


def pga_hesapla(x, y, z):
    delta_x = x - x0
    delta_y = y - y0
    delta_z = z - z0

    toplam_ivme_lsb = (delta_x**2 + delta_y**2 + delta_z**2) ** 0.5
    toplam_ivme_g = toplam_ivme_lsb * 0.0039
    return round(toplam_ivme_g, 6)


def mmi_seviyesi(pga):
    if pga < 0.028:
        return None
    elif pga < 0.062:
        return "V"
    elif pga < 0.12:
        return "VI"
    elif pga < 0.22:
        return "VII"
    else:
        return "VIII+"


def main():
    global hareket_sayaci, ALARM_TETIKLENDI, x0, y0, z0
    adxl345_init()
    x0, y0, z0 = otomatik_kalibrasyon()
    print("📡 Sistem başlatıldı...\n")

    while True:
        x, y, z = read_axes()
        pga = pga_hesapla(x, y, z)
        seviye = mmi_seviyesi(pga)
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]

        print(
            f"[{timestamp}] X:{x} | Y:{y} | Z:{z} | PGA: {pga}g | Seviye: {seviye or 'YOK'}"
        )

        if seviye:
            hareket_sayaci += 1
            print(f"⏳ {hareket_sayaci}/{REQUIRED_COUNT} eşik üstü hareket")
        else:
            if hareket_sayaci >= 2:
                hareket_sayaci -= 2
            else:
                hareket_sayaci = 0

        if hareket_sayaci >= REQUIRED_COUNT and not ALARM_TETIKLENDI:
            print(f"\n🚨 [{timestamp}] DEPREM ALGILANDI ➤ Şiddet (MMI): {seviye}")

            # 1. Alarm çal
            print("🔊 Alarm çalıyor...")
            alarm_cal(5)

            # 2. Aydınlatmayı yak
            print("💡 Aydınlatma açılıyor...")
            led_yak(10)

            # 3. Yönlendirme mesajlarını seslendir
            if seviye:
                print("🗣️ Yönlendirme mesajları seslendiriliyor...")
                yurut_json(seviye)
            else:
                print("⚠️ Deprem şiddeti belirlenemediği için yönlendirme yapılamıyor.")

            # 4. E-posta gönder
            if GMAIL_SIFRE:
                try:
                    print("📧 E-posta gönderiliyor...")
                    deprem_mail_gonder(SENDER_EMAIL, GMAIL_SIFRE, TARGET_EMAIL)
                    print("✅ E-posta başarıyla gönderildi.")
                except Exception as e:
                    print(f"❌ E-posta gönderimi başarısız: {e}")
            else:
                print(
                    "⚠️ GMAIL_SIFRE ortam değişkeni ayarlanmadığı için e-posta gönderilemedi."
                )

            ALARM_TETIKLENDI = True
            hareket_sayaci = 0
            time.sleep(10)
            ALARM_TETIKLENDI = False

        time.sleep(SAMPLE_INTERVAL)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Sistem manuel durduruldu.")
    except Exception as e:
        print(f"🚫 Hata oluştu: {e}")
