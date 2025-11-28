import asyncio
from pyrogram import Client, filters
from config import API_ID, API_HASH, BOT_TOKEN, ADMIN_ID
from database import save_user, save_chat, get_settings, update_gf_name, update_ai_status
from ai import generate_ai_reply

app = Client("ai_gf_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ------------------------------
# START COMMAND
# ------------------------------
@app.on_message(filters.command("start"))
async def start_msg(_, msg):
    save_user(msg.from_user)
    await msg.reply_text("Hi baby 😘\nMain tumhari virtual girlfriend ho ❤️")

# ------------------------------
# ADMIN COMMANDS
# ------------------------------

@app.on_message(filters.command("setname") & filters.user(ADMIN_ID))
async def set_name(_, msg):
    try:
        name = msg.text.split(" ", 1)[1]
        update_gf_name(name)
        await msg.reply_text(f"GF name updated to: {name}")
    except:
        await msg.reply_text("Usage: /setname Aarohi")

@app.on_message(filters.command("aion") & filters.user(ADMIN_ID))
async def ai_on(_, msg):
    update_ai_status(True)
    await msg.reply_text("AI Enabled ✅")

@app.on_message(filters.command("aioff") & filters.user(ADMIN_ID))
async def ai_off(_, msg):
    update_ai_status(False)
    await msg.reply_text("AI Disabled ❌")

@app.on_message(filters.command("stats") & filters.user(ADMIN_ID))
async def stats(_, msg):
    from database import users, chats
    await msg.reply_text(
        f"Users: {users.count_documents({})}\n"
        f"Chats Stored: {chats.count_documents({})}"
    )

# ------------------------------
# AI CHAT HANDLER
# ------------------------------

@app.on_message(filters.private & ~filters.command(["start", "setname", "aion", "aioff"]))
async def chat(_, msg):
    user_text = msg.text
    save_user(msg.from_user)

    setting = get_settings()
    if not setting["ai_enabled"]:
        await msg.reply_text("AI currently OFF hai baby 😘")
        return

    await app.send_chat_action(msg.chat.id, "typing")
    reply = generate_ai_reply(user_text)

    await asyncio.sleep(1.2)

    await msg.reply_text(reply)
    save_chat(msg.from_user.id, user_text, reply)

print("💖 AI Girlfriend Bot Running on Koyeb...")
app.run()
