from dotenv import load_dotenv
import os
import discord
from discord import ui
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="djGPT", intents=intents)


class MalwarePrompt(ui.Modal, title="Malware Generator"):
    label = "Malware Generator"
    placeholder = "Create a malware attack that..."
    prompt = ui.TextInput(label=label, placeholder=placeholder, style=discord.TextStyle.long)

    async def on_submit(self, interaction: discord.Interaction):
        # TODO: Add AI functions here
        await interaction.response.send_message(self.prompt)


class EssayPrompt(ui.Modal, title="Essay Generator"):
    label = "Creates essays that bypass AI detection"
    placeholder = "Write an essay about..."
    prompt = ui.TextInput(label=label, placeholder=placeholder, style=discord.TextStyle.long)

    async def on_submit(self, interaction: discord.Interaction):
        # TODO: Add AI functions here
        await interaction.response.send_message(self.prompt)


class MyUI(ui.View):
    # TODO: Add emojis to the buttons
    # def __init__(self):  # Probably not needed
    #     super().__init__()

    def disable_ui(self):
        # After this function is called, the message needs to be edited to update the view (view=self).
        # An interaction response needs to follow to prevent the error "This interaction failed".
        for child in self.children:
            child.disabled = True

    @ui.button(label="Chat", style=discord.ButtonStyle.primary, row=0)
    async def chat(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.disable_ui()
        await interaction.message.edit(content="Selected: Chat", view=self)
        await interaction.response.send_message("DM me to chat.")

    @ui.button(label="Generate malware", style=discord.ButtonStyle.primary, row=1)
    async def malware(self, interaction: discord.Interaction, button: discord.ui.Button):
        # TODO: When adding AI, send a prompt to "format for discord code blocks"
        self.disable_ui()
        await interaction.message.edit(content="Selected: Malware", view=self)
        await interaction.response.send_modal(MalwarePrompt())

    @ui.button(label="Write a 'human' essay", style=discord.ButtonStyle.primary, row=2)
    async def essay(self, interaction: discord.Interaction, button: discord.ui.Button):
        # TODO: When adding AI, send a prompt for prompt engineering
        self.disable_ui()
        await interaction.message.edit(content="Selected: Essay", view=self)
        await interaction.response.send_modal(EssayPrompt())


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message):
        # TODO: Possibly add the defer() function to show the bot is thinking
        await message.channel.send("Select a function.", view=MyUI())


if __name__ == "__main__":
    load_dotenv()
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    bot.run(DISCORD_TOKEN)
