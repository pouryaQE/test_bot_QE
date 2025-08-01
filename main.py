import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, MenuButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from web_server import start_web_server

# فعال کردن لاگ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

# توکن ربات از environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    logging.error(
        "❌ توکن ربات پیدا نشد! برو به Tools > Secrets و BOT_TOKEN رو اضافه کن")
    exit(1)

# بررسی اعتبار توکن (باید شامل : باشه)
if ":" not in BOT_TOKEN:
    logging.error("❌ فرمت توکن اشتباهه!")
    exit(1)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """تابع مدیریت دستور /start"""
    if update.message:
        # منوی ثابت در پایین صفحه
        keyboard = [
            # دکمه خرید اشتراک کل عرض را می‌گیرد
            [KeyboardButton("🛒 خرید اشتراک")],
            # دکمه اشتراک تست رایگان کل عرض را می‌گیرد
            [KeyboardButton("🛡️ اشتراک تست رایگان")],
            # دکمه‌های اشتراک‌های من و کیف پول در یک ردیف
            [KeyboardButton("🎁 اشتراک‌های من"),
             KeyboardButton("💎 کیف پول")],
            # دکمه‌های پشتیبانی و درخواست نمایندگی در یک ردیف
            [
                KeyboardButton("🔥 پشتیبانی"),
                KeyboardButton("🤝 درخواست نمایندگی")
            ]
        ]

        reply_markup = ReplyKeyboardMarkup(keyboard,
                                           resize_keyboard=True,
                                           one_time_keyboard=False)

        welcome_text = """
🤖 سلام! به ربات من خوش آمدید

از منوی پایین گزینه مورد نظرتان را انتخاب کنید:
        """

        await update.message.reply_text(text=welcome_text,
                                        reply_markup=reply_markup)


async def help_command(update: Update,
                       context: ContextTypes.DEFAULT_TYPE) -> None:
    """تابع مدیریت دستور /help"""
    if update.message:
        help_text = """
دستورات موجود:
/start - شروع ربات و نمایش منو
/help - نمایش این راهنما
        """
        await update.message.reply_text(help_text)


async def handle_message(update: Update,
                         context: ContextTypes.DEFAULT_TYPE) -> None:
    """مدیریت پیام‌های متنی از منوی ثابت"""
    if update.message and update.message.text:
        text = update.message.text

        if text == "🛒 خرید اشتراک":
            await update.message.reply_text(
                "🛒 بخش خرید اشتراک\n\nلطفاً نوع اشتراک مورد نظر خود را انتخاب کنید..."
            )

        elif text == "🎁 اشتراک‌های من":
            await update.message.reply_text(
                "🎁 اشتراک‌های شما\n\nدر حال حاضر هیچ اشتراک فعالی ندارید.")

        elif text == "🔥 پشتیبانی":
            await update.message.reply_text(
                "🔥 پشتیبانی\n\nبرای دریافت پشتیبانی با ما در ارتباط باشید:\n@support_username"
            )

        elif text == "💎 کیف پول":
            await update.message.reply_text(
                "💎 کیف پول شما\n\nموجودی فعلی: 0 تومان")

        elif text == "🔥 اعتبار رایگان":
            await update.message.reply_text(
                "🔥 اعتبار رایگان\n\nشما می‌تونید روزانه اعتبار رایگان دریافت کنید!"
            )

        elif text == "🛡️ اشتراک تست رایگان":
            await update.message.reply_text(
                "🛡️ اشتراک تست رایگان\n\nاشتراک تست 24 ساعته رایگان دریافت کنید!"
            )

        # مدیریت دکمه جدید
        elif text == "🤝 درخواست نمایندگی":
            await update.message.reply_text(
                "🤝 درخواست نمایندگی\n\nبرای اطلاعات بیشتر در مورد نمایندگی با پشتیبانی تماس بگیرید."
            )

        else:
            await update.message.reply_text(
                "❓ گزینه‌ای که انتخاب کردید شناخته نشد. لطفاً از منوی پایین استفاده کنید."
            )


async def button_callback(update: Update,
                          context: ContextTypes.DEFAULT_TYPE) -> None:
    """مدیریت کلیک روی دکمه‌های inline (در صورت نیاز)"""
    query = update.callback_query
    await query.answer()


async def setup_menu_button(application):
    """تنظیم دکمه منو"""
    try:
        # تنظیم دکمه منو برای نمایش کیبورد
        await application.bot.set_chat_menu_button(menu_button=MenuButton(
            type="commands"))
        print("✅ دکمه منو تنظیم شد")
    except Exception as e:
        print(f"❌ خطا در تنظیم دکمه منو: {e}")


def main() -> None:
    """تابع اصلی ربات"""
    # شروع وب سرور
    start_web_server()

    # ساخت اپلیکیشن
    application = Application.builder().token(BOT_TOKEN).build()

    # اضافه کردن هندلرها
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(button_callback))

    # تنظیم دکمه منو بعد از شروع
    async def post_init(application):
        await setup_menu_button(application)

    application.post_init = post_init

    # شروع ربات
    print("ربات شروع شد...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
