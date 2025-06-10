import time
import smbus2 as smbus
from datetime import datetime

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

# Seviye Aralıkları
DEPREM_SINIFLARI = [
    ("0", {"x": (-999, 16), "y": (-999, 6), "z": (249, 252)}),
    ("4", {"x": (16, 50), "y": (6, 40), "z": (231, 260)}),
    ("5", {"x": (50, 80), "y": (40, 60), "z": (211, 270)}),
    ("6", {"x": (80, 100), "y": (60, 80), "z": (206, 275)}),
    ("7<", {"x": (100, 999), "y": (80, 999), "z": (-999, 999)}),
]


# Sensör başlat
def adxl345_init():
    bus.write_byte_data(DEVICE_ADDRESS, 0x2D, 0x08)


# Sensör verisi oku
def read_axes():
    data = bus.read_i2c_block_data(DEVICE_ADDRESS, 0x32, 6)
    x = (data[1] << 8) | data[0]
    y = (data[3] << 8) | data[2]
    z = (data[5] << 8) | data[4]
    x = x - 65536 if x > 32767 else x
    y = y - 65536 if y > 32767 else y
    z = z - 65536 if z > 32767 else z
    return x, y, z


# Şiddet sınıflandırması
def deprem_seviyesi(x, y, z):
    for seviye, aralik in DEPREM_SINIFLARI:
        if (
            aralik["x"][0] <= x < aralik["x"][1]
            and aralik["y"][0] <= y < aralik["y"][1]
            and aralik["z"][0] <= z < aralik["z"][1]
        ):
            return seviye
    return "?"


# Alarm fonksiyonu (örnek simülasyon)
def alarm_cal(sure=5):
    print("🔔 ALARM ÇALIYOR! Süre:", sure, "saniye")
    time.sleep(sure)


# Ana döngü
def main():
    global hareket_sayaci, ALARM_TETIKLENDI
    adxl345_init()
    print("📡 Sistem başlatıldı...\n")

    while True:
        x, y, z = read_axes()
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"[{timestamp}] X:{x} | Y:{y} | Z:{z}")

        seviye = deprem_seviyesi(x, y, z)

        if seviye != "0" and seviye != "?":
            hareket_sayaci += 1
            print(
                f"⏳ {hareket_sayaci}/{REQUIRED_COUNT} eşik üstü sınıflama (Seviye: {seviye})"
            )
        else:
            hareket_sayaci = 0

        if hareket_sayaci >= REQUIRED_COUNT and not ALARM_TETIKLENDI:
            print(f"\n🚨 [{timestamp}] DEPREM ALGILANDI ➤ Şiddet: {seviye}")
            alarm_cal(5)
            ALARM_TETIKLENDI = True
            hareket_sayaci = 0
            time.sleep(10)  # alarm sonrası bekleme süresi
            ALARM_TETIKLENDI = False

        time.sleep(SAMPLE_INTERVAL)


# Çalıştır
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Sistem manuel durduruldu.")
    except Exception as e:
        print(f"🚫 Hata oluştu: {e}")
