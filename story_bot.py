import os
import time
import base64
from instaloader import Instaloader, Profile
from telegram import Bot

# === Конфигурация ===
IG_USERNAME = os.getenv("IG_USERNAME")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Список пользователей, чьи сторис нужно скачать
TARGETS = [
    "ishka.ii", "sofityshchenko", "darya_gree", "_rybina_juliua_",
    "battinaaa", "lil_froggggg", "mary.sushko_", "didididiana",
    "zdorova_anya", "tmrvtlv", "yuliya_karpaeva", "k.u.r.u.n.t.u",
    "betty_tsoy", "d.a.s.h.a.v.s"
]

# === Восстановление session-файла из IG_SESSION ===
def restore_session_file(username: str):
    session_b64 = os.getenv("IG_SESSION")
    if session_b64:
        with open(f"{username}.session", "wb") as f:
            f.write(base64.b64decode(session_b64))

# === Скачивание и пересылка сторис ===
def main():
    restore_session_file(IG_USERNAME)

    loader = Instaloader(sleep=True)
    loader.load_session_from_file(IG_USERNAME)

    bot = Bot(token=TELEGRAM_BOT_TOKEN)

    for username in TARGETS:
        try:
            profile = Profile.from_username(loader.context, username)
            stories = loader.get_stories(userids=[profile.userid])
            count = 0

            for story in stories:
                for item in story.get_items():
                    filepath = loader.download_storyitem(item, target=f"{username}_temp")
                    count += 1

                    # Отправка файла в Telegram
                    if filepath.endswith(".mp4"):
                        with open(filepath, "rb") as f:
                            bot.send_video(chat_id=TELEGRAM_CHAT_ID, video=f)
                    elif filepath.endswith(".jpg"):
                        with open(filepath, "rb") as f:
                            bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=f)

            print(f"{username}: отправлено {count} сторис")
        except Exception as e:
            print(f"Ошибка при обработке {username}: {e}")

if name == "main":
    main()
    input("\nГотово. Нажмите Enter для выхода...")