import smtplib
import time
import os
from email.mime.text import MIMEText
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()  # .env dosyasındaki ortam değişkenlerini yükle


def deprem_mail_gonder(gonderen, sifre, hedef, retries=3, delay=5):
    """
    Deprem algılandığında e-posta gönderir. Hata durumunda tekrar deneme yapar.
    """
    now = datetime.now()
    konu = "IoT Deprem Uyarısı"
    mesaj = f"{now.strftime('%d.%m.%Y')} tarihi saat {now.strftime('%H:%M:%S')}'de IoT cihazı deprem algıladı."

    msg = MIMEText(mesaj)
    msg["Subject"] = konu
    msg["From"] = gonderen
    msg["To"] = hedef

    for i in range(retries):
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(gonderen, sifre)
                server.sendmail(gonderen, hedef, msg.as_string())
            return True  # Başarılı olursa döngüden çık
        except Exception as e:
            print(f"Mail gönderme hatası (Deneme {i+1}/{retries}): {e}")
            time.sleep(delay)  # Hata durumunda bekle
    print("❌ E-posta gönderme maksimum deneme sayısına ulaştı, başarısız oldu.")
    return False


if __name__ == "__main__":
    # Test için .env'den çekilen değerleri kullan
    gonderen_test = os.getenv("SENDER_EMAIL")
    sifre_test = os.getenv("GMAIL_SIFRE")
    hedef_test = os.getenv("TARGET_EMAIL")

    if gonderen_test and sifre_test and hedef_test:
        try:
            print("Mail gönderme testi başlatılıyor...")
            if deprem_mail_gonder(gonderen_test, sifre_test, hedef_test):
                print("✅ Test maili başarıyla gönderildi.")
            else:
                print("❌ Test maili gönderilemedi.")
        except Exception as e:
            print(f"Test maili gönderilemedi: {e}")
    else:
        print("Test için gerekli e-posta ortam değişkenleri ayarlanmamış.")
