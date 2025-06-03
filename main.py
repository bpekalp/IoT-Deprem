import time
import smbus2 as smbus  # smbus yerine smbus2 kullanıyoruz

# I2C adresi (ADXL345 için)
DEVICE_ADDRESS = 0x53
bus = smbus.SMBus(1)  # I2C bus 1 genellikle Raspberry Pi'de kullanılır


def adxl345_init():
    # Güç kontrol register'ı (0x2D) -> Ölçüm moduna geç (0x08)
    bus.write_byte_data(DEVICE_ADDRESS, 0x2D, 0x08)


def read_axes():
    data = bus.read_i2c_block_data(DEVICE_ADDRESS, 0x32, 6)
    x = (data[1] << 8) | data[0]
    y = (data[3] << 8) | data[2]
    z = (data[5] << 8) | data[4]

    # 2’s complement dönüşümü (negatif değer desteği)
    x = x - 65536 if x > 32767 else x
    y = y - 65536 if y > 32767 else y
    z = z - 65536 if z > 32767 else z

    return x, y, z


def main():
    adxl345_init()
    print("📡 ADXL345 sensörü başlatıldı. Veriler okunuyor...\n")

    while True:
        x, y, z = read_axes()
        print(f"X: {x} | Y: {y} | Z: {z}")
        time.sleep(0.2)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Program sonlandırıldı.")
    except Exception as e:
        print(f"🚫 Hata oluştu: {e}")
