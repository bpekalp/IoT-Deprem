import smtplib
import os
from email.mime.text import MIMEText
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


def deprem_mail_gonder(gonderen, sifre, hedef):
    now = datetime.now()
    konu = "IoT Deprem Uyarısı"
    mesaj = f"{now.strftime('%d.%m.%Y')} tarihi saat {now.strftime('%H:%M:%S')}'de IoT cihazı deprem algıladı."

    msg = MIMEText(mesaj)
    msg["Subject"] = konu
    msg["From"] = gonderen
    msg["To"] = hedef

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(gonderen, sifre)
        server.sendmail(gonderen, hedef, msg.as_string())


if __name__ == "__main__":
    gonderen = "b.pekalp@gmail.com"
    sifre = os.getenv("GMAIL_SIFRE")
    hedef = "zzehrakr48@gmail.com"
    try:
        deprem_mail_gonder(gonderen, sifre, hedef)
        print("Mail gönderildi.")
    except Exception as e:
        print(f"Mail gönderilemedi: {e}")
