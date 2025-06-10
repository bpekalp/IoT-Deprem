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


def metni_seslendir(metin, retries=3, delay=1):
    """
    Belirtilen metni seslendirir. Hata durumunda tekrar deneme yapar.
    """
    dosya = "gecici_ses.mp3"
    for i in range(retries):
        try:
            # Pygame mixer'ı her çağrıda başlat ve durdur
            pygame.mixer.init()
            pygame.mixer.music.set_volume(
                1.0
            )  # Ses seviyesini ayarla, gerekirse düşürebilirsin

            tts = gTTS(metin, lang="tr")
            tts.save(dosya)

            pygame.mixer.music.load(dosya)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                time.sleep(1)  # Ses bitene kadar bekle

            pygame.mixer.quit()  # Kullanım sonrası mixer'ı kapat

            if os.path.exists(dosya):
                os.remove(dosya)
            return True  # Başarılı olursa döngüden çık
        except Exception as e:
            print(f"Seslendirme hatası (Deneme {i+1}/{retries}): {e}")
            if os.path.exists(dosya):  # Hata oluşursa kalan dosyayı temizle
                os.remove(dosya)
            # Hata durumunda mixer'ı kapatmaya çalış, aksi halde bir sonraki deneme başarısız olabilir
            try:
                pygame.mixer.quit()
            except:
                pass
            time.sleep(delay)
    print("❌ Seslendirme maksimum deneme sayısına ulaştı, başarısız oldu.")
    return False


def yurut_json(seviye):
    """
    JSON dosyasından mesajları alıp seslendirir.
    Her mesaj kendi içinde retry mekanizmasına sahiptir.
    """
    for tur in ["uyari", "canta", "yonlendirme"]:
        try:
            metin = jsondan_mesaj_getir(seviye, tur)
            print(f"🔊 {tur.upper()} ➤ {metin}")
            metni_seslendir(metin)  # metni_seslendir kendi retry mantığına sahip
        except Exception as e:
            print(f"{tur} seslendirilirken hata oluştu: {e}")


if __name__ == "__main__":
    print("Yönlendirme testi başlatılıyor (VII seviyesi için)...")
    yurut_json("VII")
    # Ana blokta mixer'ı kapatmaya gerek yok, çünkü metni_seslendir içinde kapanıyor.
