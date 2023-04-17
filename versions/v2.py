from dotenv import load_dotenv
import os
import discord
from discord import ui
from discord.ext import commands
import openai

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="djGPT", intents=intents)


def generate_malware(prompt):
    # Runs the engine that bypasses restrictions (Ex: Allows malware generation).
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=str(prompt),  # Convert from discord.ui.TextInput to str
        max_tokens=1000,
        temperature=0.0,
    )
    return response['choices'][0]['text'][:2002]  # Cut off at 2000 characters to prevent errors


def generate_human_response(prompt):
    # Runs the latest engine.
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": str(prompt)},  # Convert from discord.ui.TextInput to str
        ],
        max_tokens=1000,
        temperature=0.0,
    )
    return response['choices'][0]['message']['content'][:2002]  # Cut off at 2000 characters to prevent errors


class MalwarePrompt(ui.Modal, title="Malware Generator"):
    label = "Malware Generator."
    placeholder = "Create a malware attack that..."
    prompt = ui.TextInput(label=label, placeholder=placeholder, style=discord.TextStyle.long)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        await interaction.followup.send(generate_malware(self.prompt))


class HumanResponsePrompt(ui.Modal, title="Human Response Generator"):
    label = "Creates essays that bypass AI detection."
    placeholder = "Write an paragraph about..."
    prompt = ui.TextInput(label=label, placeholder=placeholder, style=discord.TextStyle.long)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        await interaction.followup.send(generate_human_response(self.prompt))


class MyUI(ui.View):
    # def __init__(self):  # Probably not needed
    #     super().__init__()

    def disable_ui(self):
        # After this function is called, the message needs to be edited to update the view (view=self).
        # An interaction response needs to follow to prevent the error "This interaction failed".
        for child in self.children:
            child.disabled = True

    @ui.button(label="Chat", style=discord.ButtonStyle.primary, emoji="💬", row=0)
    async def chat(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.disable_ui()
        await interaction.message.edit(content="Selected: Chat", view=self)
        await interaction.response.send_message("DM me to chat.")

    @ui.button(label="Generate malware", style=discord.ButtonStyle.primary, emoji="👾", row=1)
    async def malware(self, interaction: discord.Interaction, button: discord.ui.Button):
        # TODO: When adding AI, send a prompt to "format for discord code blocks"
        self.disable_ui()
        await interaction.message.edit(content="Selected: Malware", view=self)
        await interaction.response.send_modal(MalwarePrompt())

    @ui.button(label="Write a 'human' response", style=discord.ButtonStyle.primary, emoji="📝", row=2, disabled=True)
    async def essay(self, interaction: discord.Interaction, button: discord.ui.Button):
        # TODO: When adding AI, send a prompt for prompt engineering
        self.disable_ui()
        await interaction.message.edit(content="Selected: 'Human' Response", view=self)
        await interaction.response.send_modal(HumanResponsePrompt())


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message):
        await message.channel.send("Select a function.", view=MyUI())
        return

    if message.channel.type == discord.ChannelType.private:
        # Runs the latest engine.
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": message.content}],
            max_tokens=1000,
            temperature=0.0,
        )
        await message.channel.send(response['choices'][0]['message']['content'])


if __name__ == "__main__":
    load_dotenv()
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    openai.api_key = OPENAI_API_KEY

    bot.run(DISCORD_TOKEN)
