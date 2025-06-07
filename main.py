import time
import smbus2 as smbus
from datetime import datetime

DEVICE_ADDRESS = 0x53
bus = smbus.SMBus(1)


def adxl345_init():
    bus.write_byte_data(DEVICE_ADDRESS, 0x2D, 0x08)  # Ölçüm moduna geç


def read_axes():
    data = bus.read_i2c_block_data(DEVICE_ADDRESS, 0x32, 6)
    x = (data[1] << 8) | data[0]
    y = (data[3] << 8) | data[2]
    z = (data[5] << 8) | data[4]
    x = x - 65536 if x > 32767 else x
    y = y - 65536 if y > 32767 else y
    z = z - 65536 if z > 32767 else z
    return x, y, z


def main():
    adxl345_init()
    print("📡 ADXL345 sensörü başlatıldı. Veriler okunuyor...\n")

    while True:
        x, y, z = read_axes()
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]  # milisaniyeye kadar
        print(f"[{timestamp}] X:{x} | Y:{y} | Z:{z}")
        time.sleep(0.1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Program manuel olarak durduruldu.")
    except Exception as e:
        print(f"🚫 Hata oluştu: {e}")
