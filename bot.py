from telegram.ext import Application, CommandHandler, MessageHandler, filters
import json
from datetime import datetime

# Ma'lumotlar fayli
DATA_FILE = "database.json"

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"income": [], "expense": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

async def start(update, context):
    await update.message.reply_text(
        "Salom! Men sizning kirim va chiqimlaringizni boshqaruvchi botman. Kirim yoki chiqim qo'shish uchun:\n"
        "+ [miqdor] [kategoriya] - Kirim qo'shish\n"
        "- [miqdor] [kategoriya] - Chiqim qo'shish\n"
        "Balansni bilish uchun: /balans"
    )

async def add_transaction(update, context):
    text = update.message.text.strip()
    data = load_data()

    if text.startswith("+"):
        _, amount, category = text.split(maxsplit=2)
        data["income"].append({"amount": int(amount), "category": category, "date": str(datetime.now().date())})
        save_data(data)
        await update.message.reply_text(f"Kirim qo'shildi: {amount} so'm - {category}")

    elif text.startswith("-"):
        _, amount, category = text.split(maxsplit=2)
        data["expense"].append({"amount": int(amount), "category": category, "date": str(datetime.now().date())})
        save_data(data)
        await update.message.reply_text(f"Chiqim qo'shildi: {amount} so'm - {category}")

async def balans(update, context):
    data = load_data()
    income_total = sum(item["amount"] for item in data["income"])
    expense_total = sum(item["amount"] for item in data["expense"])
    balance = income_total - expense_total
    await update.message.reply_text(
        f"Umumiy kirim: {income_total} so'm\n"
        f"Umumiy chiqim: {expense_total} so'm\n"
        f"Balans: {balance} so'm"
    )

def main():
    app = Application.builder().token("7368885974:AAEDaLQ63aafT1HUM67eMyOgFPnsHkCnDVQ").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("balans", balans))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, add_transaction))

    print("Bot ishga tushdi!")
    app.run_polling()

if __name__ == "__main__":
    main()
