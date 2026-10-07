import logging
import random
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8991610241:AAH_OkObKgfCIlIMQxQa6xRSv2Ea9ek3M5k"
BOT_OWNER_ID = 848578882

user_custom_ids = {}

def get_or_create_user_id(telegram_id: int) -> int:
    if telegram_id not in user_custom_ids:
        new_id = random.randint(1000, 9999)
        while new_id in user_custom_ids.values():
            new_id = random.randint(1000, 9999)
        user_custom_ids[telegram_id] = new_id
    return user_custom_ids[telegram_id]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    custom_id = get_or_create_user_id(user.id)
    
    keyboard = [
        [KeyboardButton("📍 Xitoy ombor manzili")],
        [KeyboardButton("📦 Tariflar"), KeyboardButton("🆔 ID olish")],
        [KeyboardButton("🔍 Trek-kodni tekshirish")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    welcome_text = (
        f"Assalomu alaykum! Cargo xizmatimizga xush kelibsiz 🤗🇨🇳\n\n"
        f"Sizning mijoz ID kodingiz: <b>MAY-{custom_id}</b>"
    )
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="HTML")
    
    # Adminga xabar yuborish (Xato bergan 46-qator soddalashtirildi)
    try:
        username = user.username
        if not username:
            username = "Mavjud emas"
            
        admin_notify = (
            f"🔔 Yangi mijoz botga kirdi!\n\n"
            f"👤 Ismi: {user.full_name}\n"
            f"Username: @{username}\n"
            f"Telegram ID: {user.id}\n"
            f"Berilgan Mijoz ID: MAY-{custom_id}"
        )
        await context.bot.send_message(chat_id=BOT_OWNER_ID, text=admin_notify)
    except Exception as e:
        logging.error(f"Xatolik: {e}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user
    custom_id = get_or_create_user_id(user.id)
    
    if text == "📍 Xitoy ombor manzili":
        address_text = (
            "🇨🇳 <b>Xitoy ombor manzili:</b>\n\n"
            "📋 <b>Ilovalar uchun manzil (ustiga bossangiz nusxalanadi):</b>\n"
            f"<code>广东省佛山市禅城区祖庙街道文华北路81号御东公寓325房间 MAY-{custom_id}</code>\n\n"
            f"<b>Tel / 电话:</b> 13411828151\n"
            f"<b>Mijoz ID / 唛头:</b> MAY-{custom_id}"
        )
        await update.message.reply_text(address_text, parse_mode="HTML")
        
    elif text == "📦 Tariflar":
        tariffs = (
            "📦 <b>Yetkazib berish tariflari:</b>\n\n"
            "✈️ <b>Avia:</b> 8$/kg\n"
            "🚛 <b>Avto:</b> 4.5$/kg"
        )
        await update.message.reply_text(tariffs, parse_mode="HTML")
        
    elif text == "🆔 ID olish":
        id_info = (
            f"Sizning Telegram ID raqamingiz: <code>{user.id}</code>\n"
            f"Sizning mijoz kodingiz: <b>MAY-{custom_id}</b>"
        )
        await update.message.reply_text(id_info, parse_mode="HTML")
        
    elif text == "🔍 Trek-kodni tekshirish":
        await update.message.reply_text("Trek-kodingizni kiriting:")
        
    else:
        reply_msg = (
            "Xabaringiz qabul qilindi! Murojaatingiz bo'yicha tez orada javob beramiz 😊\n"
            "Agarda menyu kerak bo'lsa, pastdagi tugmalardan foydalanishingiz mumkin."
        )
        await update.message.reply_text(reply_msg)

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
          
