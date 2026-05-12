"""
Big Cheese Languages — Telegram Bot v3
Новое: двуязычный (RU/EN), выбор языка при /start
"""
import logging, sqlite3, asyncio, os
from datetime import datetime
import httpx
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Application, CommandHandler, CallbackQueryHandler,
                           MessageHandler, filters, ContextTypes)
import config, messages as msg

PDF_RU = os.path.join(os.path.dirname(os.path.abspath(__file__)), "30_phrases.pdf")
PDF_EN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "30_phrases_en.pdf")
DB_PATH  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "users.db")

logging.basicConfig(format="%(asctime)s | %(levelname)s | %(message)s", level=logging.INFO)
log = logging.getLogger(__name__)

# TEST MODE:
# True = scheduled funnel messages go out in minutes for QA testing.
# False = production schedule in hours/days.
# Railway Variable: TEST_MODE=1 for test, TEST_MODE=0 for production.
TEST_MODE = os.getenv("TEST_MODE", "0").lower() in ("1", "true", "yes", "on")
SCHEDULE = {
    "day2_sent": 2 if TEST_MODE else 24,
    "day4_sent": 4 if TEST_MODE else 48,
    "day6_sent": 6 if TEST_MODE else 72,
    "day7_sent": 7 if TEST_MODE else 96,
}
SCHEDULE_UNIT = "minutes" if TEST_MODE else "hours"
SCHEDULER_EVERY_MINUTES = 1 if TEST_MODE else 60

# ── БД ────────────────────────────────────────────────────────────
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS users (
        user_id     INTEGER PRIMARY KEY,
        username    TEXT,
        first_name  TEXT,
        lang        TEXT DEFAULT 'ru',
        segment     TEXT DEFAULT NULL,
        subscribed  TEXT DEFAULT CURRENT_TIMESTAMP,
        day2_sent   INTEGER DEFAULT 0,
        day4_sent   INTEGER DEFAULT 0,
        day6_sent   INTEGER DEFAULT 0,
        day7_sent   INTEGER DEFAULT 0,
        clicked_cta INTEGER DEFAULT 0
    )""")

    # Safe migrations for older users.db versions
    c.execute("PRAGMA table_info(users)")
    existing_columns = [row[1] for row in c.fetchall()]

    migrations = {
        "username": "ALTER TABLE users ADD COLUMN username TEXT",
        "first_name": "ALTER TABLE users ADD COLUMN first_name TEXT",
        "lang": "ALTER TABLE users ADD COLUMN lang TEXT DEFAULT 'ru'",
        "segment": "ALTER TABLE users ADD COLUMN segment TEXT DEFAULT NULL",
        "subscribed": "ALTER TABLE users ADD COLUMN subscribed TEXT DEFAULT CURRENT_TIMESTAMP",
        "day2_sent": "ALTER TABLE users ADD COLUMN day2_sent INTEGER DEFAULT 0",
        "day4_sent": "ALTER TABLE users ADD COLUMN day4_sent INTEGER DEFAULT 0",
        "day6_sent": "ALTER TABLE users ADD COLUMN day6_sent INTEGER DEFAULT 0",
        "day7_sent": "ALTER TABLE users ADD COLUMN day7_sent INTEGER DEFAULT 0",
        "clicked_cta": "ALTER TABLE users ADD COLUMN clicked_cta INTEGER DEFAULT 0",
    }

    for column, sql in migrations.items():
        if column not in existing_columns:
            c.execute(sql)

    conn.commit()
    conn.close()
    log.info("DB ready: %s", DB_PATH)

def save_user(uid, username, first_name):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (user_id,username,first_name) VALUES (?,?,?)",
              (uid, username, first_name))
    conn.commit(); conn.close()

def set_lang(uid, lang):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET lang=? WHERE user_id=?", (lang, uid))
    conn.commit(); conn.close()

def set_segment(uid, segment):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Segment selection starts/restarts the nurture chain.
    # This makes testing predictable and prevents old test data from blocking scheduled messages.
    c.execute("""UPDATE users
        SET segment=?, subscribed=CURRENT_TIMESTAMP,
            day2_sent=0, day4_sent=0, day6_sent=0, day7_sent=0, clicked_cta=0
        WHERE user_id=?""", (segment, uid))
    conn.commit(); conn.close()

def mark_cta(uid):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET clicked_cta=1 WHERE user_id=?", (uid,))
    conn.commit(); conn.close()

def now_str():
    return datetime.now().strftime("%d.%m.%Y %H:%M")


async def send_lead_to_sheet(user, lang, segment, action, message="", status="Новая заявка"):
    """Send bot lead to Google Sheets via Apps Script Web App."""
    webhook_url = getattr(config, "SHEET_WEBHOOK_URL", "")
    if not webhook_url:
        log.info("SHEET_WEBHOOK_URL is empty; skipping sheet lead sync")
        return

    row = get_user(user.id)
    subscribed_at = row[2][:10] if row and row[2] else ""

    payload = {
        "name": user.first_name or "",
        "username": f"@{user.username}" if user.username else "",
        "telegram_id": str(user.id),
        "timestamp": now_str(),
        "source": "Telegram Bot",
        "lang": (lang or "").upper(),
        "segment": segment or "",
        "action": action or "",
        "message": message or "",
        "status": status or "Новая заявка",
        "channel": "https://t.me/BigCheesemaster",
        "subscribed_at": subscribed_at,
    }
    try:
        async with httpx.AsyncClient(timeout=12) as client:
            r = await client.post(webhook_url, json=payload)
            log.info("Sheet sync %s: %s", r.status_code, r.text[:200])
    except Exception as e:
        log.warning("Sheet sync error: %s", e)


def get_user(uid):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT lang, segment, subscribed, username, first_name, clicked_cta FROM users WHERE user_id=?", (uid,))
    row = c.fetchone(); conn.close()
    return row  # (lang, segment, subscribed, username, first_name, clicked_cta)

def get_users_for_day(day_col, delay_value):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    modifier = f"+{delay_value} {SCHEDULE_UNIT}"
    c.execute(f"""SELECT user_id, lang, segment, clicked_cta FROM users
        WHERE {day_col}=0 AND segment IS NOT NULL
        AND datetime(subscribed, ?) <= datetime('now')""", (modifier,))
    rows = c.fetchall(); conn.close()
    return rows

def mark_day_sent(uid, day_col):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(f"UPDATE users SET {day_col}=1 WHERE user_id=?", (uid,))
    conn.commit(); conn.close()

def db_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM users")
    total = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM users WHERE segment IS NOT NULL")
    seg = c.fetchone()[0]
    conn.close()
    return total, seg

# ── КЛАВИАТУРЫ ────────────────────────────────────────────────────
def kb_lang():
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
        InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
    ]])

def kb_segment(lang):
    btns = msg.BTN_SEGMENT[lang]
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(btns[0], callback_data="seg_relocation")],
        [InlineKeyboardButton(btns[1], callback_data="seg_career")],
        [InlineKeyboardButton(btns[2], callback_data="seg_other")],
    ])

def kb_when(lang):
    btns = msg.BTN_WHEN[lang]
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(btns[0], callback_data="when_soon")],
        [InlineKeyboardButton(btns[1], callback_data="when_half")],
        [InlineKeyboardButton(btns[2], callback_data="when_thinking")],
    ])

def kb_career(lang):
    btns = msg.BTN_CAREER[lang]
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(btns[0], callback_data="goal_speak")],
        [InlineKeyboardButton(btns[1], callback_data="goal_write")],
        [InlineKeyboardButton(btns[2], callback_data="goal_interview")],
    ])

def kb_other(lang):
    btns = msg.BTN_OTHER[lang]
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(btns[0], callback_data="other_yes")],
        [InlineKeyboardButton(btns[1], callback_data="other_no")],
    ])

def kb_cta(lang):
    btns = msg.BTN_CTA[lang]
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(btns[0], callback_data="cta_book")],
        [InlineKeyboardButton(btns[1], callback_data="cta_question")],
    ])

# ── ХЭНДЛЕРЫ ──────────────────────────────────────────────────────
async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    save_user(user.id, user.username, user.first_name)
    log.info("START: %s @%s", user.id, user.username)
    await update.message.reply_text(
        "Выбери язык / Choose language:",
        reply_markup=kb_lang()
    )

async def handle_lang(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id
    lang = "ru" if query.data == "lang_ru" else "en"
    set_lang(uid, lang)

    name = f" {query.from_user.first_name}" if query.from_user.first_name else ""
    await query.edit_message_text(
        msg.DAY0_WELCOME[lang].format(name=name),
        parse_mode="HTML"
    )
    await asyncio.sleep(1)
    pdf_path = PDF_EN if lang == "en" else PDF_RU
    pdf_name = "BigCheese_30_phrases_EN.pdf" if lang == "en" else "BigCheese_30_фраз_RU.pdf"
    caption_ru = "📄 Сохрани — пригодится.\n30 фраз для аренды, банка, врача и соседей.\n\n🇪🇸 Испанский · 🇮🇹 Итальянский · 🇬🇧 Английский"
    caption_en = "📄 Save this — you'll need it.\n30 phrases for housing, bank, doctor & neighbours.\n\n🇪🇸 Spanish · 🇮🇹 Italian · 🇬🇧 English"
    try:
        with open(pdf_path,"rb") as f:
            await ctx.bot.send_document(
                chat_id=uid, document=f,
                filename=pdf_name,
                caption=caption_en if lang=="en" else caption_ru
            )
    except FileNotFoundError:
        log.warning("PDF not found: %s", pdf_path)
    await asyncio.sleep(1)
    await ctx.bot.send_message(uid, msg.DAY0_SEGMENT[lang],
                               reply_markup=kb_segment(lang), parse_mode="HTML")

async def handle_segment(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id
    row = get_user(uid)
    lang = row[0] if row else "ru"
    seg_map = {"seg_relocation":"relocation","seg_career":"career","seg_other":"other"}
    seg = seg_map.get(query.data)
    if seg:
        set_segment(uid, seg)
        confirm = msg.SEG_CONFIRM[lang][seg]
        await query.edit_message_text(confirm+"\n\n"+msg.DAY0_CONFIRM[lang], parse_mode="HTML")
        log.info("Segment: %s → %s [%s]", uid, seg, lang)

async def handle_answers(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id
    row = get_user(uid)
    lang = row[0] if row else "ru"
    ans = msg.ANSWERS[lang].get(query.data)
    if ans:
        await query.edit_message_text(ans)


async def send_admin_lead_card(ctx, user, lang, segment, action="Записаться на урок"):
    """Send a clean lead card to Darya in Telegram."""
    flag = "🇷🇺" if lang == "ru" else "🌍"
    seg_label = msg.SEGMENT_LABELS.get(lang, msg.SEGMENT_LABELS["ru"]).get(segment or "other", segment or "other")
    username_line = f"@{user.username}" if user.username else "—"
    mention = f"<a href='tg://user?id={user.id}'>{user.first_name or user.id}</a>"

    if lang == "ru":
        text = f"""{flag} <b>Новая заявка из бота!</b>

👤 Пользователь: {mention}
💬 Username: {username_line}
🆔 Telegram ID: <code>{user.id}</code>
🌐 Язык интерфейса: RU
🎯 Сегмент: {seg_label}
✅ Действие: {action}
📅 Дата заявки: {now_str()}

<i>Напиши ему первой — он ждёт 🙂</i>"""
    else:
        text = f"""{flag} <b>New lead from Telegram bot!</b>

👤 User: {mention}
💬 Username: {username_line}
🆔 Telegram ID: <code>{user.id}</code>
🌐 Interface language: EN
🎯 Segment: {seg_label}
✅ Action: {action}
📅 Request date: {now_str()}

<i>Message them first — they are waiting 🙂</i>"""

    try:
        await ctx.bot.send_message(config.ADMIN_CHAT_ID, text, parse_mode="HTML")
    except Exception as e:
        log.warning("Admin lead card error: %s", e)


async def send_admin_question(ctx, user, lang, segment, text):
    """Send user's free-text question to Darya."""
    flag = "🇷🇺" if lang == "ru" else "🌍"
    seg_label = msg.SEGMENT_LABELS.get(lang, msg.SEGMENT_LABELS["ru"]).get(segment or "other", segment or "other")
    username_line = f"@{user.username}" if user.username else "—"
    mention = f"<a href='tg://user?id={user.id}'>{user.first_name or user.id}</a>"

    admin_text = f"""{flag} <b>Вопрос из бота</b>

👤 Пользователь: {mention}
💬 Username: {username_line}
🆔 Telegram ID: <code>{user.id}</code>
🌐 Язык интерфейса: {lang.upper()}
🎯 Сегмент: {seg_label}

💭 Сообщение:
{text}

<i>Ответь лично в течение 24 часов 🙂</i>"""

    try:
        await ctx.bot.send_message(config.ADMIN_CHAT_ID, admin_text, parse_mode="HTML")
    except Exception as e:
        log.warning("Admin question notify error: %s", e)


async def handle_cta(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id
    row = get_user(uid)
    lang = row[0] if row else "ru"
    segment = row[1] if row and row[1] else "other"

    if query.data == "cta_book":
        mark_cta(uid)
        await query.edit_message_text(msg.CTA_BOOKED[lang], parse_mode="HTML")
        log.info("CTA booked: %s [%s]", uid, lang)

        await send_admin_lead_card(
            ctx,
            query.from_user,
            lang=lang,
            segment=segment,
            action="Записаться на урок" if lang == "ru" else "Book a lesson"
        )

        await send_lead_to_sheet(
            query.from_user,
            lang=lang,
            segment=segment,
            action="Записаться на урок" if lang == "ru" else "Book a lesson",
            message="Нажал кнопку записи" if lang == "ru" else "Clicked booking button",
            status="Новая заявка" if lang == "ru" else "New lead"
        )

    elif query.data == "cta_question":
        resp = "Напиши свой вопрос — Дарья ответит лично в течение 24 часов 🙂" if lang=="ru" \
               else "Write your question — Darya will reply personally within 24 hours 🙂"
        await query.edit_message_text(resp)

        await send_lead_to_sheet(
            query.from_user,
            lang=lang,
            segment=segment,
            action="Есть вопрос" if lang == "ru" else "Has a question",
            message="Нажал кнопку вопроса" if lang == "ru" else "Clicked question button",
            status="Вопрос" if lang == "ru" else "Question"
        )

async def handle_text(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text
    row = get_user(user.id)
    lang = row[0] if row else "ru"
    segment = row[1] if row and row[1] else "other"

    await send_admin_question(ctx, user, lang, segment, text)

    await send_lead_to_sheet(
        user,
        lang=lang,
        segment=segment,
        action="Свободное сообщение" if lang == "ru" else "Free message",
        message=text,
        status="Вопрос" if lang == "ru" else "Question"
    )

    await update.message.reply_text(msg.FREE_TEXT_REPLY[lang])

# ── ПЛАНИРОВЩИК ───────────────────────────────────────────────────
async def send_scheduled(bot):
    total, seg = db_stats()
    log.info("⏰ Tick | users:%d seg:%d", total, seg)

    for day_col, delay, get_content in [
        ("day2_sent", SCHEDULE["day2_sent"], lambda l,s,_: (msg.DAY2[l][s], kb_when(l) if s=="relocation" else kb_career(l) if s=="career" else kb_other(l))),
        ("day4_sent", SCHEDULE["day4_sent"], lambda l,s,_: (msg.DAY4[l][s], None)),
        ("day6_sent", SCHEDULE["day6_sent"], lambda l,s,_: (msg.DAY6[l], kb_cta(l))),
        ("day7_sent", SCHEDULE["day7_sent"], lambda l,s,clicked: (None,None) if clicked else (msg.DAY7[l], kb_cta(l))),
    ]:
        users = get_users_for_day(day_col, delay)
        log.info("%s delay: %s %s", day_col, delay, SCHEDULE_UNIT)
        log.info("%s queue: %d", day_col, len(users))
        for uid, lang, segment, clicked in users:
            if not segment: continue
            try:
                text, kb = get_content(lang, segment, clicked)
                if text is None:
                    mark_day_sent(uid, day_col); continue
                await bot.send_message(uid, text, reply_markup=kb, parse_mode="HTML")
                mark_day_sent(uid, day_col)
                log.info("%s → %d [%s/%s]", day_col, uid, lang, segment)
            except Exception as e:
                log.warning("%s error %d: %s", day_col, uid, e)

# ── MAIN ──────────────────────────────────────────────────────────
def main():
    init_db()
    app = Application.builder().token(config.BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_lang,    pattern="^lang_"))
    app.add_handler(CallbackQueryHandler(handle_segment, pattern="^seg_"))
    app.add_handler(CallbackQueryHandler(handle_answers, pattern="^(when_|goal_|other_)"))
    app.add_handler(CallbackQueryHandler(handle_cta,     pattern="^cta_"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    async def scheduler_loop(application):
        log.info("✅ Scheduler loop started")
        await send_scheduled(application.bot)
        while True:
            await asyncio.sleep(SCHEDULER_EVERY_MINUTES * 60)
            await send_scheduled(application.bot)

    async def on_startup(application):
        application.create_task(scheduler_loop(application))

    app.post_init = on_startup
    log.info("🤖 Bot v3 starting (RU/EN)... TEST_MODE=%s unit=%s schedule=%s", TEST_MODE, SCHEDULE_UNIT, SCHEDULE)
    app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)

if __name__ == "__main__":
    main()
