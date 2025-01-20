import os
import telebot
from cryptography.fernet import Fernet
import requests

# Replace with your actual bot token
BOT_TOKEN = "YOUR_BOT_TOKEN"

# Generate a key (keep this secret!)
key = Fernet.generate_key()

# Create a Fernet cipher object
cipher_suite = Fernet(key)

# Initialize the bot
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Hello! Send me the encrypted video URL link.")

@bot.message_handler(func=lambda message: True) 
def handle_message(message):
    try:
        # Extract the encrypted URL from the message
        encrypted_url = message.text

        # Decrypt the URL
        decrypted_url = cipher_suite.decrypt(encrypted_url.encode()).decode()

        # Download the video
        response = requests.get(decrypted_url, stream=True)
        response.raise_for_status()

        # Save the video to a temporary file
        with open('temp_video.mp4', 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192): 
                f.write(chunk)

        # Send the video to the user
        with open('temp_video.mp4', 'rb') as f:
            bot.send_video(message.chat.id, f)

        # Clean up (remove the temporary file)
        os.remove('temp_video.mp4')

        bot.reply_to(message, "Video decrypted and sent successfully!")

    except Exception as e:
        bot.reply_to(message, f"An error occurred: {str(e)}")

# Start the bot
bot.polling()

