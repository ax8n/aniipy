import requests
import asyncio
from telethon import TelegramClient, events, functions, types, Button

# 🔥 Telegram Bot Credentials
BOT_TOKEN = "7757976352:AAFFxLpZc1m5TPKXxT6ot5jWf5DMksi8g3o"
BOT_USERNAME = "Enclvebot"

client = TelegramClient("bot_sesn", api_id=6, api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e").start(bot_token=BOT_TOKEN)

# 🔥 Required Channels for Membership Check
REQUIRED_CHANNELS = [-1002628372650, "@Raremiddelman"]

# 🔥 Pending Requests Dictionary
pending_requests = {}

# 📌 Auto Delete After 30 Seconds
async def auto_delete(event, message):
    await asyncio.sleep(30)
    await message.delete()

async def check_membership(event):
    user = await event.get_sender()
    if user.id in pending_requests:
        return True  

    for channel in REQUIRED_CHANNELS:
        try:
            chat = await client.get_entity(channel)
            participant = await client(functions.channels.GetParticipantRequest(chat.id, user.id))
            if isinstance(participant.participant, (types.ChannelParticipantAdmin, types.ChannelParticipantCreator, types.ChannelParticipant)):
                return True  
        except:
            pass

    msg = await event.reply(
        "❌ **You must join required channels to use this bot!**",
        buttons=[Button.url("Join Here", "https://t.me/addlist/gs2GsRFkMrY4MzBl")]
    )
    await auto_delete(event, msg)
    return False

@client.on(events.NewMessage(pattern=r'^/start(@Enclvebot)?$'))
async def start_handler(event):
    if not await check_membership(event):
        return
    msg = await event.reply(
        "🎉 **Welcome!**\n"
        "- `/rest <gmail/username>` → Get Instagram reset link\n"
        "- `/insta <username>` → Fetch full Instagram profile\n"
        "- `/admin` → View admin details\n"
        "- `/leader` → View leader details\n"
    )
    await auto_delete(event, msg)

@client.on(events.NewMessage(pattern=r'^/admin(@Enclvebot)?$'))
async def admin_handler(event):
    if not await check_membership(event):
        return

    channel_username = "@ashuportal"
    message_id = 16  

    forwarded_msg = await client.get_messages(channel_username, ids=message_id)

    caption_text = (
        "<b>👑 Admin Details</b>\n"
        "<b>👤 Owner:</b> @Dick4y\n"
        "<b>📌 Channels:</b> <a href='https://t.me/+oymqjG5tY0M3NmJl'>𝐓𝐄𝐀𝐌 𝐄𝐍𝐂𝐋𝐕𝐄</a>\n"
        "<b>📅 Joined:</b> 8th August 2020\n"
        "<b>💰 Middleman:</b> Available ✅\n"
        "<b>🔹 Vouches:</b> @Raremiddelman"
    )

    msg = await client.send_file(event.chat_id, forwarded_msg.media, caption=caption_text, parse_mode='html')
    await auto_delete(event, msg)

@client.on(events.NewMessage(pattern=r'^/leader(@Enclvebot)?$'))
async def leader_handler(event):
    if not await check_membership(event):
        return

    channel_username = "@ashuportal"
    message_id = 17  

    forwarded_msg = await client.get_messages(channel_username, ids=message_id)

    caption_text = (
        "<b>👑 Leader Details</b>\n"
        "<b>👤 Username:</b> @AniiRo\n"
        "<b>📌 Channel:</b> <a href='https://t.me/+5hQSRZg96VY2MmFl'>𝐀𝐍𝐈𝐈 𝐏𝐎𝐑𝐓𝐀𝐋</a>\n"
        "<b>📌 Hobby:</b> File Maker 💋🔥\n"
        "<b>📞 Contact:</b> <a href='tg://user?id=5300575173'>𝐀𝐍𝐈𝐈</a>"
    )

    msg = await client.send_file(event.chat_id, forwarded_msg.media, caption=caption_text, parse_mode='html')
    await auto_delete(event, msg)

@client.on(events.NewMessage(pattern=r'^/rest(@Enclvebot)?(?:\s+(.+))?$'))
async def rest_handler(event):
    user = await event.get_sender()
    username_or_email = event.pattern_match.group(2)

    if not username_or_email:
        pending_requests[user.id] = "/rest"
        msg = await event.reply("📌 **Please reply with the Instagram username or email.**")
        await auto_delete(event, msg)
        return

    await send_reset_link(event, username_or_email)

async def send_reset_link(event, username_or_email):
    msg = await event.reply(f"🔍 Sending password reset link for `{username_or_email}`...")
    
    try:
        url = "https://www.instagram.com/accounts/account_recovery_send_ajax/"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "X-CSRFToken": "fjpGbVKIVyVXMaLCwQMGVP",
            "Cookie": "sessionid=16829956593%3AAb35PnGyCyyuca%3A24%3AAYdZ5xMFraWXM_4iP-r5ScRO9DRht8yLV2hc5E0rzQ",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {"email_or_username": username_or_email}

        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200 and response.json().get("status") == "ok":
            result_msg = await msg.edit(f"✅ Reset link sent to `{username_or_email}`.")
        else:
            result_msg = await msg.edit("❌ Failed to send reset link. Check the username/email.")
    except Exception as e:
        result_msg = await msg.edit(f"🛑 Error: `{str(e)}`")

    await auto_delete(event, result_msg)

@client.on(events.NewMessage(pattern=r'^/insta(@Enclvebot)?(?:\s+(.+))?$'))
async def insta_handler(event):
    user = await event.get_sender()
    username = event.pattern_match.group(2)

    if not username:
        pending_requests[user.id] = "/insta"
        msg = await event.reply("📌 **Please reply with the Instagram username.**")
        await auto_delete(event, msg)
        return

    await fetch_instagram_profile(event, username)

async def fetch_instagram_profile(event, username):
    msg = await event.reply(f"🔍 Fetching details for `{username}`...")

    try:
        url = f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}"
        headers = {
            "User-Agent": "Instagram 123.0.0.0 Android",
            "Referer": "https://www.instagram.com/",
            "Origin": "https://www.instagram.com/",
            "X-CSRFToken": "fjpGbVKIVyVXMaLCwQMGVP",
            "Cookie": "sessionid=16829956593%3AAb35PnGyCyyuca%3A24%3AAYdZ5xMFraWXM_4iP-r5ScRO9DRht8yLV2hc5E0rzQ"
        }
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            await msg.edit("🛑 Profile could be banned or doesn't exist.")
            await auto_delete(event, msg)
            return

        user_data = response.json().get("data", {}).get("user", {})
        if not user_data:
            await msg.edit("🛑 Profile could be banned or doesn't exist.")
            await auto_delete(event, msg)
            return

        profile_pic = user_data.get("profile_pic_url_hd", None)
        bio = user_data.get("biography", "N/A")
        full_name = user_data.get("full_name", "N/A")
        followers = user_data.get("edge_followed_by", {}).get("count", 0)
        following = user_data.get("edge_follow", {}).get("count", 0)
        posts = user_data.get("edge_owner_to_timeline_media", {}).get("count", 0)
        is_private = user_data.get("is_private", False)
        is_verified = user_data.get("is_verified", False)
        is_business = user_data.get("is_professional", False)
        business_category = user_data.get("business_category_name", "N/A")
        external_url = user_data.get("external_url", "N/A")

        result = (
            f"<b>📸 Instagram Profile Info</b><br>"
            f"<blockquote>"
            f"<b>👤 Name:</b> {full_name}<br>\n"
            f"<b>🔗 Username:</b> @{username}<br>\n"
            f"<b>📜 Bio:</b> {bio}<br>\n"
            f"<b>🔗 Website:</b> {external_url}<br>\n"
            f"<b>👥 Followers:</b> {followers}<br>\n"
            f"<b>👥 Following:</b> {following}<br>\n"
            f"<b>📮 Posts:</b> {posts}<br>\n"
            f"<b>🔒 Private:</b> {is_private}<br>\n"
            f"<b>✅ Verified:</b> {is_verified}<br>\n"
            f"<b>🏢 Business Account:</b> {is_business}<br>\n"
            f"<b>📂 Business Category:</b> {business_category}</blockquote>"
        )

        if profile_pic:
            sent_msg = await client.send_file(event.chat_id, profile_pic, caption=result, parse_mode='html')
            await msg.delete()
            await auto_delete(event, sent_msg)
        else:
            sent_msg = await msg.edit(result, parse_mode='html')
            await auto_delete(event, sent_msg)
    except Exception as e:
        error_msg = await msg.edit(f"🛑 Error: {str(e)}")
        await auto_delete(event, error_msg)

@client.on(events.NewMessage)
async def handle_pending_requests(event):
    user = await event.get_sender()

    if user.id in pending_requests:
        command = pending_requests.pop(user.id)

        if command == "/rest":
            await send_reset_link(event, event.raw_text.strip())
        elif command == "/insta":
            await fetch_instagram_profile(event, event.raw_text.strip())

print("🚀 Bot is running...")
client.run_until_disconnected()