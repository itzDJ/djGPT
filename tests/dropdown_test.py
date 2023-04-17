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
    def __init__(self):
        super().__init__()
        # self.add_item(Dropdown())

    def disable_ui(self):
        # After this function is called, the message needs to be edited to update the view (view=self).
        # An interaction response needs to follow to prevent the error "This interaction failed".
        for child in self.children:
            child.disabled = True

    @ui.select(
        placeholder="Select a function.",
        options=[
            discord.SelectOption(label="Chat", description="Similar functionality to ChatGPT"),
            discord.SelectOption(label="Generate malware", description="Generate malware"),
            discord.SelectOption(label="Write a 'human' essay", description="Writes an essay bypassing AI detection"),
        ],
    )
    async def select_option(self, interaction: discord.Interaction, select: discord.ui.Select):
        match select.values[0]:
            case "Chat":
                await interaction.response.send_message("DM me to chat.")
            case "Generate malware":
                await interaction.response.send_modal(MalwarePrompt())
            case "Write a 'human' essay":
                await interaction.response.send_modal(EssayPrompt())

        self.disable_ui()  # TODO: Though dropdown disables, make the selected option freeze
        await interaction.message.edit(content=select.values[0], view=self)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message):
        # TODO: Possibly add the defer() function to show the bot is thinking
        await message.channel.send("testing", view=MyUI())


if __name__ == "__main__":
    load_dotenv()
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    bot.run(DISCORD_TOKEN)
