import RPi.GPIO as GPIO
import time

LED_PIN = 16  # Kullandığın GPIO pin numarasını gir


def led_yak(sure=5):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)

    GPIO.output(LED_PIN, GPIO.HIGH)  # LED'i yak
    time.sleep(sure)
    GPIO.output(LED_PIN, GPIO.LOW)  # LED'i söndür

    GPIO.cleanup()


if __name__ == "__main__":
    try:
        led_yak()  # 5 saniye süreyle LED'i yak
    except KeyboardInterrupt:
        GPIO.cleanup()  # Program durdurulduğunda GPIO pinlerini temizle
    except Exception as e:
        print(f"Hata: {e}")
        GPIO.cleanup()  # Hata durumunda GPIO pinlerini temizle
