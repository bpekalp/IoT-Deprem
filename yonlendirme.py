from gtts import gTTS
import pygame
import os
import time


def metni_seslendir(dosya_yolu):
    # Metni oku
    with open(dosya_yolu, "r", encoding="utf-8") as file:
        metin = file.read()

    # gTTS ile ses dosyası oluştur
    tts = gTTS(metin, lang="tr")
    ses_dosyasi = "gecici_ses.mp3"
    tts.save(ses_dosyasi)

    # pygame ile sesi çal
    pygame.mixer.init()
    pygame.mixer.music.load(ses_dosyasi)
    pygame.mixer.music.play()

    # Ses bitene kadar bekle
    while pygame.mixer.music.get_busy():
        time.sleep(0.5)

    # Temizlik
    pygame.mixer.quit()
    os.remove(ses_dosyasi)


def yurut(dosya_yolu):
    try:
        metni_seslendir(dosya_yolu)
    except Exception as e:
        return f"{dosya_yolu} seslendirilirken hata oluştu: {e}"


if __name__ == "__main__":
    dosya_yolu = "resources/uyari.txt"
    yurut(dosya_yolu)

    dosya_yolu = "resources/deprem_cantasi.txt"
    yurut(dosya_yolu)

    dosya_yolu = "resources/yonlendirme.txt"
    yurut(dosya_yolu)
