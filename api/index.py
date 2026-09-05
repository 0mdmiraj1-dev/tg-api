from fastapi import FastAPI, HTTPException
import requests
from bs4 import BeautifulSoup

app = FastAPI()

@app.get("/api/tg-lookup/{username}")
def lookup_telegram_user(username: str):
    clean_username = username.lstrip("@").strip()

    if not clean_username:
        raise HTTPException(400, "Username is required")

    url = f"https://t.me/{clean_username}"

    try:
        response = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=10
        )

        if response.status_code != 200:
            raise HTTPException(404, "User not found")

        soup = BeautifulSoup(response.text, "html.parser")

        name_element = soup.find("div", class_="tgme_page_title")

        if not name_element:
            raise HTTPException(404, "Telegram username unavailable")

        img_element = soup.find(
            "img",
            class_="tgme_page_photo_image"
        )

        return {
            "username": clean_username,
            "profile_name": name_element.get_text(" ", strip=True),
            "photo_url": (
                img_element.get("src")
                if img_element else None
            )
        }

    except HTTPException:
        raise

    except requests.RequestException as e:
        raise HTTPException(502, str(e))
