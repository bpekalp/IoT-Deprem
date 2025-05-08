import pygame
import time


def alarm_cal(sure=5):
    pygame.mixer.init()
    pygame.mixer.music.load("resources/alarm.wav")
    pygame.mixer.music.play()

    time.sleep(sure)
    pygame.mixer.music.stop()
    pygame.mixer.quit()


if __name__ == "__main__":
    try:
        alarm_cal()
    except Exception as e:
        print(f"Alarm çalarken hata oluştu: {e}")
