# Importing the required packages
from flask import Flask, request, render_template
import telegram
import os
from nltk.chat.eliza import eliza_chatbot

# Bot credentials
from botcontroller.credentials import BOT_TOKEN, BOT_USERNAME, URL

# Initialize flask app
app = Flask(__name__)

# Initialize telegram bot
bot = telegram.Bot(token = BOT_TOKEN)

@app.route("/")
def index():
    return render_template("index.html")
@app.route(f"/{BOT_TOKEN}", methods = ["POST"])
def respond():
    """
        Desc : This function defines the logic that controls how the telegram bot responds when a message is sent
    """

    # When a user sends a message in Telegram, we can receive the message as a JSON object and convert it to a Telegram object using the telegram module
    new_message = telegram.Update.de_json(request.get_json(force = True), bot)

    chat_id = new_message.message.chat_id
    message_id = new_message.message.message_id

    # Encoding text for unicode compatibility
    text = new_message.message.text.encode("utf-8").decode()
    print(f"[RECEIVED TEXT] : {text}")

    # For a welcome message
    if text == "/start":
        welcome_msg = f"Hi {new_message.message.from_user.first_name}, I'm Toyosi - The favourite mental health bot. Let's talk about your issues, Be free with me"
        bot.sendMessage(chat_id = chat_id, reply_to_message_id = message_id, text = welcome_msg)

    else:
        bot.sendMessage(chat_id = chat_id, reply_to_message_id = message_id, text = eliza_chatbot.respond(text))

    return ""

@app.route("/set_webhook")
def setWebhook():
    """
        Desc : This webhook enables the bot to run once the server is invoked
    """

    hook = bot.setWebhook(os.path.join(URL, BOT_TOKEN))
    if hook:
        return "Webhook successfully set."
    return "Webhook configuration failed."

if __name__ == "__main__":
    app.run(debug = True, threaded = True)