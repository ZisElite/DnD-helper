import discord

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run('NzUyNjM3NjU2NTUwMjExNzYw.X1aicA.BT6J_VcC2LxUV-6PwGXBEJBb-aY')
