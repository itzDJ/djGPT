"""
ABOUT ME
I am an AI chatbot powered by OpenAI.
- DM me or preface your server message with "djGPT" to chat.
- Preface your message with "djGPT3" for access to the engine that bypasses restrictions.
"""

import discord
from dotenv import load_dotenv
import os
import openai


class Bot(discord.Client):
    async def on_ready(self):
        """ Called when the bot is online """
        print(f"{self.user} is online")

    async def on_message(self, message):
        """ Called when a message is received -- private or public"""
        if message.author == self.user:
            # Prevents the bot from responding to itself
            return

        if message.content.startswith("djGPT3 "):
            # Runs the engine that bypasses restrictions (Ex: Allows malware generation).
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=message.content[7:],
                max_tokens=1000,
                temperature=0.0,
            )
            await message.channel.send(response['choices'][0]['text'])
            return
        elif message.content.startswith("djGPT "):
            prompt = message.content[6:]
        elif message.channel.type == discord.ChannelType.private:
            # Runs if the received message is private (a DM).
            prompt = message.content
        else:
            return

        # Runs the latest engine.
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}],
            max_tokens=1000,
            temperature=0.0,
        )
        await message.channel.send(response['choices'][0]['message']['content'])


if __name__ == "__main__":
    load_dotenv()
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    openai.api_key = OPENAI_API_KEY

    # Intents were added for security reasons
    intents = discord.Intents.default()
    intents.message_content = True
    Bot(intents=intents).run(DISCORD_TOKEN)
