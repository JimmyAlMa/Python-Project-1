from dotenv import load_dotenv
import os
import json
import logging
from datetime import datetime

from google import genai
import gspread
from google.oauth2.service_account import Credentials
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

load_dotenv()

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GOOGLE_SHEET_NAME = "Jimmy's expense log"
SERVICE_ACCOUNT_FILE = "service_account.json"  

logging.basicConfig(
    level=logging.INFO,
    filename="app.log",
    filemode="a",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
logger = logging.getLogger(__name__)

client = genai.Client(api_key=GEMINI_API_KEY)
MODEL_NAME = "gemini-3.1-flash-lite"

SYSTEM_PROMPT = """Kamu parser pencatat keuangan. Ubah pesan berikut menjadi JSON
dengan format persis: {{"kategori": string, "nominal": number, "deskripsi": string}}.
Balas HANYA JSON, tanpa penjelasan apapun, tanpa markdown code block.

Pesan: {message_text}"""

def call_gemini(message_text: str) -> dict:
    prompt = SYSTEM_PROMPT.format(message_text=message_text)
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )
    raw_text = response.text.strip()
    if raw_text is None:
        raise ValueError("Gemini returns an empty response")

    if raw_text.startswith("```"):
        raw_text = raw_text.strip("`").replace("json", "", 1).strip()

    return json.loads(raw_text)



def get_sheet():
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scopes)
    client = gspread.authorize(creds)
    return client.open(GOOGLE_SHEET_NAME).sheet1

def save_to_sheet(data: dict):
    sheet = get_sheet()
    sheet.append_row([
        datetime.now().strftime("%Y-%m-%d %H:%M"),
        data.get("kategori", ""),
        data.get("nominal", 0),
        data.get("deskripsi", "")
    ])



async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_message = update.message.text

    try:
        data = call_gemini(text_message)

        save_to_sheet(data)

        reply = (
            f"Tercatat\n"
            f"Kategori: {data['kategori']}\n"
            f"Nominal: {data['nominal']}\n"
            f"Deskripsi: {data['deskripsi']}"
        )
        await update.message.reply_text(reply)

    except json.JSONDecodeError:
        await update.message.reply_text(
            "Maaf, aku nggak berhasil paham pesan itu sebagai catatan keuangan. "
            "Coba tulis ulang, misalnya: 'makan siang 25rb'"
        )
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text("Ups, ada masalah teknis. Coba lagi ya.")



def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info('Bot Running... Press Ctrl+C to stop.')
    app.run_polling()

if __name__ == "__main__":
    main()