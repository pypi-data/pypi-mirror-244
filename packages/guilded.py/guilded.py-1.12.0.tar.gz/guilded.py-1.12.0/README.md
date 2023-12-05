Welcome to guilded.py, a discord.py-esque asynchronous Python wrapper for Guilded's bot API. If you know discord.py, you know guilded.py.

## Documentation

Documentation is available on [Read the Docs](https://guildedpy.readthedocs.io).

## Basic Example

```py
import guilded

client = guilded.Client()

@client.event
async def on_ready():
    print('Ready')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == 'ping':
        await message.channel.send('pong!')

client.run('token')
```

### Bot example

```py
import guilded
from guilded.ext import commands

bot = commands.Bot(command_prefix='!')

@bot.command()
async def ping(ctx):
    await ctx.send('pong!')

bot.run('token')
```

For more examples, see the examples directory in this repository.

## Support

Guilded.py has a support channel under its dedicated group for any questions you may have.

1. Join [this server](https://guilded.gg/guilded-api)
2. Click on the far-left plus sign

    ![](https://img.guildedcdn.com/ContentMedia/f4f92fa74bf1b6043b438046eebcf0f4-Full.webp?w=198&h=165)

3. Click the "Follow" button on the guilded.py group

    ![](https://img.guildedcdn.com/ContentMedia/ecfc6237dd2f401fbd356edfd50916fc-Full.webp?w=816&h=339)
