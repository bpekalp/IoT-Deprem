from gtts import gTTS
import pygame
import os
import time
import json


def jsondan_mesaj_getir(seviye, tur):
    try:
        with open("resources/uyarilar.json", "r", encoding="utf-8") as file:
            veri = json.load(file)
        return veri.get(seviye, {}).get(
            tur, f"{seviye} için '{tur}' bilgisi bulunamadı."
        )
    except Exception as e:
        return f"{seviye} seviyesi için veri okunamadı: {e}"


def metni_seslendir(metin):
    try:
        tts = gTTS(metin, lang="tr")
        dosya = "gecici_ses.mp3"
        tts.save(dosya)

        pygame.mixer.init()
        pygame.mixer.music.load(dosya)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(1)

        pygame.mixer.quit()
        os.remove(dosya)
    except Exception as e:
        print(f"Seslendirme hatası: {e}")


def yurut_json(seviye):
    for tur in ["uyari", "canta", "yonlendirme"]:
        try:
            metin = jsondan_mesaj_getir(seviye, tur)
            print(f"🔊 {tur.upper()} ➤ {metin}")
            metni_seslendir(metin)
        except Exception as e:
            print(f"{tur} seslendirilirken hata oluştu: {e}")


if __name__ == "__main__":
    yurut_json("VII")  # test için
