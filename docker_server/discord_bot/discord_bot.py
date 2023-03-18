# bot.py
import os

import discord
from dotenv import load_dotenv
from send_udp import send_udp

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == "LED on":
        response = "I turned the LED on"
        send_udp("LED on")
        await message.channel.send(response)

    elif message.content == "LED off":
        response = "I turned the LED off"
        send_udp("LED off")
        await message.channel.send(response)
    
    else:
        response = "I dont know this command"
        send_udp("Wrong input!")
        await message.channel.send(response)
    

client.run(TOKEN)