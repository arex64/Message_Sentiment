from datetime import datetime
import discord
from discord.ext import commands
from Controller import BotController


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)  # prefix used for using bot


@bot.event
async def on_ready():  # check bot is online
    print('Bot is ready')


@bot.command()
async def message_sentiment(ctx):
    owner = await bot.fetch_user(189091030874718209)
    await owner.send("Please input after and before dates seperated by a / (YYYY-MM-DD):")

    try:
        message = await bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout=70)
        dates = message.content.split('/')
        date_range = dates
        if len(dates) != 2:
            await owner.send("Invalid input. Please enter both inputs separated by a /.")
            return
        start_date = datetime.strptime(dates[0], '%Y-%m-%d')
        end_date = datetime.strptime(dates[1], '%Y-%m-%d')
        messages = []
        async for message in ctx.channel.history(limit=None):
            messages.append(message)

        if start_date > datetime.now() and end_date > datetime.now():
            await owner.send('Both dates are invalid.')
            return
        elif start_date > datetime.now():
            filtered_messages = [msg for msg in messages if msg.created_at.date() <= end_date.date()]
        elif end_date > datetime.now():
            filtered_messages = [msg for msg in messages if msg.created_at.date() >= start_date.date()]
        else:
            filtered_messages = [msg for msg in messages if
                                 start_date.date() <= msg.created_at.date() <= end_date.date()]
        if len(filtered_messages) == 0:
            await owner.send('No messages found between the specified dates.')
        else:
            messages_content = BotController.get_specific_attributes(filtered_messages)
            msg_sentiment = BotController.gpt_response(messages_content)
            elastic = BotController.messages_elastic(date_range, messages_content,
                                                     msg_sentiment)  # create new elastic index
            print(elastic)
            print('done')
            emojie = "\U0001F44B"
            await owner.send(f"{emojie} Message sentiment: {msg_sentiment}")
            await bot.close()
    except ValueError:
        await ctx.send('Invalid date format. Please use the format YYYY-MM-DD.')


# @bot.event
# async def on_command_error(ctx, error):
#     if isinstance(error, commands.MissingRole):
#         await ctx.send("You do not have the required role to use this command.")


bot.run('MTExNzM5MDc4NjQzOTQyMTk1Mg.Gcom0X.enZZBizILgbUto1WBq7u2RSc0lSZ71hgRDh8P4')  # Bot ID
