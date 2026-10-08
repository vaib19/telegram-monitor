import asyncio
import threading
from flask import Flask, render_template_string
from telethon import TelegramClient, events

app = Flask(__name__)

API_ID = 32847306       #[cite: 2]
API_HASH = '34a9690c15f05b9fba0bb0a0abf47ff3'  #[cite: 2]

messages_db = []

# --- 1. Frontend Web Dashboard ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Live Telegram Monitor</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <meta http-equiv="refresh" content="5">
</head>
<body class="bg-gray-900 text-white font-sans p-6">
    <div class="max-w-4xl mx-auto">
        <h1 class="text-3xl font-bold mb-6 text-emerald-400">⚡ Live Telegram Feed</h1>
        <div id="feed" class="space-y-4">
            {% for msg in messages %}
            <div class="bg-gray-800 p-4 rounded-lg border border-gray-700 shadow-md">
                <div class="text-xs text-gray-400 mb-1">From: <span class="text-indigo-300 font-semibold">{{ msg.channel }}</span> | Time: {{ msg.time }}</div>
                <p class="text-lg whitespace-pre-wrap">{{ msg.text }}</p>
            </div>
            {% else %}
            <p class="text-gray-500">Waiting for incoming messages...</p>
            {% endfor %}
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, messages=reversed(messages_db))


# --- 2. Telegram Listener (All Incoming Messages) ---
def run_telegram_client():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    client = TelegramClient('stock_session', API_ID, API_HASH)

    # Yahan koi channel list nahi hai, yeh saare incoming messages sunega
    @client.on(events.NewMessage) 
    async def my_event_handler(event):
        from datetime import datetime
        
        chat = await event.get_chat()
        chat_title = getattr(chat, 'title', getattr(chat, 'first_name', str(event.chat_id)))

        message_data = {
            'channel': chat_title,
            'text': event.raw_text,
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        messages_db.append(message_data)
        print(f"[{chat_title}] New message captured!")

    print("Starting Telegram listener for all messages...")
    client.start()
    client.run_until_disconnected()

if __name__ == '__main__':
    t = threading.Thread(target=run_telegram_client, daemon=True)
    t.start()
    
    app.run(debug=False, port=5000, use_reloader=False)
















