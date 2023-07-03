from datetime import datetime
import discord
from discord.ext import commands
from Controller import BotController

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='.', intents=intents)  # prefix used for using bot


@bot.event
async def on_ready():  # check bot is online
    print('Bot is ready')


@bot.command()
async def message_history(ctx):
    await ctx.send("Please input after and before dates seperated by a / (YYYY-MM-DD):")
    channel_id = ctx.channel.id  # use the current channel's ID
    try:
        message = await bot.wait_for('message', check=lambda message: message.author == ctx.author, timeout=70)
        dates = message.content.split('/')
        if len(dates) != 2:
            await ctx.send("Invalid input. Please enter both inputs separated by a /.")
            return

        timestamp1 = int(datetime.fromisoformat(dates[0]).timestamp()) // 1000
        timestamp2 = int(datetime.fromisoformat(dates[1]).timestamp()) // 1000
        date_range = dates

        msg = BotController.retrieve_messages(channel_id)  # get messages from discord
        filtered_messages = BotController.get_specific_attributes(msg, timestamp1,
                                                                  timestamp2)  # filter messages with given timestamps
        # msg_sentiment = BotController.gpt_response(filtered_messages)  # get sentiment for messages
        msg_sentiment = 'neutral'
        elastic = BotController.messages_elastic(date_range, filtered_messages,
                                                 msg_sentiment)  # create new elastic index
        print(elastic)

        await ctx.reply('Done')
    except ValueError:
        await ctx.send("Invalid date format. Please try again")


bot.run('MTExNzM5MDc4NjQzOTQyMTk1Mg.GIsF7Y.WYiztlz-NGgNq0_Qifl6zXKC9YHoYX6StGS_-s')  # Bot ID
