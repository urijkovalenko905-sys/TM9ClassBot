"""
╔══════════════════════════════════════════════╗
║   Бот расписания 9 класс — School16 Krasnodar ║
╚══════════════════════════════════════════════╝

Установка зависимостей:
    pip install python-telegram-bot

Запуск:
    python bot.py
"""

import os
import logging
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    WebAppInfo,
    MenuButtonWebApp,
    BotCommand,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# ─── НАСТРОЙКИ ────────────────────────────────────────────────────────────────
TOKEN       = os.environ.get("TOKEN")   # берётся из переменной окружения Railway
WEB_APP_URL = "https://urijkovalenko905-sys.github.io/TM9ClassBot/TM9ClassBot.html"

# Классы, которые есть в приложении
CLASSES = ["9А", "9Б", "9В", "9Г", "9Д", "9Е"]

# ─── ЛОГИРОВАНИЕ ──────────────────────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# ─── /start ───────────────────────────────────────────────────────────────────
async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Главная команда — кнопка открытия Mini App."""
    keyboard = [[
        InlineKeyboardButton(
            text="📅 Открыть расписание",
            web_app=WebAppInfo(url=WEB_APP_URL),
        )
    ]]
    await update.message.reply_text(
        text=(
            "👋 Привет!\n\n"
            "Это бот расписания для 9-х классов школы №16.\n"
            "Нажми кнопку ниже — откроется приложение с расписанием, "
            "звонками и подготовкой к ОГЭ 📚"
        ),
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# ─── /class ───────────────────────────────────────────────────────────────────
async def cmd_class(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Открыть расписание конкретного класса."""
    # Кнопки для каждого класса — открывают Mini App с параметром ?class=9А
    buttons = [
        InlineKeyboardButton(
            text=cls,
            web_app=WebAppInfo(url=f"{WEB_APP_URL}?class={cls}"),
        )
        for cls in CLASSES
    ]
    # Раскладываем по 3 в ряд
    keyboard = [buttons[i:i+3] for i in range(0, len(buttons), 3)]
    await update.message.reply_text(
        text="Выбери свой класс 👇",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# ─── /help ────────────────────────────────────────────────────────────────────
async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 *Команды бота:*\n\n"
        "/start — открыть расписание\n"
        "/class — выбрать класс и открыть его расписание\n"
        "/help  — список команд\n\n"
        "В приложении можно:\n"
        "• смотреть расписание уроков 📅\n"
        "• видеть текущий/следующий урок ⏱\n"
        "• записывать домашние задания 📝\n"
        "• смотреть расписание звонков 🔔\n"
        "• следить за датами ОГЭ и ресурсами 🎓",
        parse_mode="Markdown",
    )


# ─── Неизвестные сообщения ────────────────────────────────────────────────────
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
        InlineKeyboardButton(
            text="📅 Открыть расписание",
            web_app=WebAppInfo(url=WEB_APP_URL),
        )
    ]]
    await update.message.reply_text(
        "Не понял 🤔 Используй /help или просто открой расписание:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# ─── SETUP: команды и кнопка меню ────────────────────────────────────────────
async def post_init(application):
    """Выполняется один раз при запуске — регистрирует команды и кнопку меню."""
    await application.bot.set_my_commands([
        BotCommand("start", "Открыть расписание"),
        BotCommand("class", "Выбрать класс"),
        BotCommand("help",  "Список команд"),
    ])
    # Кнопка «Меню» прямо в поле ввода — открывает Mini App
    await application.bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(
            text="📅 Расписание",
            web_app=WebAppInfo(url=WEB_APP_URL),
        )
    )
    logger.info("✅ Бот запущен и готов к работе!")


# ─── MAIN ─────────────────────────────────────────────────────────────────────
def main():
    if not TOKEN:
        raise ValueError("❌ Переменная TOKEN не задана! Добавь её в Railway → Variables")

    app = (
        ApplicationBuilder()
        .token(TOKEN)
        .post_init(post_init)
        .build()
    )

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("class", cmd_class))
    app.add_handler(CommandHandler("help",  cmd_help))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown))

    logger.info("Запускаю polling...")
    app.run_polling()


if __name__ == "__main__":
    main()
