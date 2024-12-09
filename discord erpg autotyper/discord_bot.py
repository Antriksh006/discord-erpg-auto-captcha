import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')


@bot.event
async def on_message(message):
    if 'is now in the jail!' in message.content.lower():
        channel = message.channel
        overwrite = channel.overwrites_for(message.guild.default_role) 
        overwrite.send_messages = False 
        await channel.set_permissions(message.guild.default_role, overwrite=overwrite)
        await channel.send("This channel has been locked. No one can send messages now.")

    elif 'stop there' in message.content and message.attachments:
        for attachment in message.attachments:
            if attachment.filename.lower().endswith(('png', 'jpg', 'jpeg', 'gif')):
                folder_path = os.path.join(os.getcwd(), 'images') 
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                
                file_path = os.path.join(folder_path, attachment.filename)
                await attachment.save(file_path)
                await message.channel.send(f'Image saved to {file_path}')

    await bot.process_commands(message)


DISCORD_BOT_TOKEN = "" # Add your Discord bot token here
bot.run(DISCORD_BOT_TOKEN)
