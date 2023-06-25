import scraping
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands, tasks

intents = discord.Intents.default()
intents.message_content = True
load_dotenv()
bot = commands.Bot(command_prefix='!', intents=intents)
prev = []
urls = []


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game("the notifying game!"))
    user = await bot.fetch_user(int(os.getenv('USER_ID')))
    scrape.start(user)
    print(f'We have logged in as {bot.user}')


@bot.command()
async def ping(ctx):
    await ctx.send(f'Here is the ping: {round(bot.latency * 1000)} ms')


@bot.command()
async def add(ctx, url):
    urls.append(url)
    prev.append("")
    await ctx.send(f'Added **{scraping.scrape_title(url)}** to the reading list')


@bot.command()
async def remove(ctx, index):
    i = int(index) - 1
    if i < 0 or i >= len(urls):
        await ctx.send(f'Index out of bounds')
        return
    prev.pop(i)
    url = urls.pop(i)
    await ctx.send(f'Removed **{scraping.scrape_title(url)}** from the reading list')


@bot.command()
async def novels(ctx):
    text = ""
    if len(urls) == 0:
        await ctx.send("No novels in the reading list.\nAdd one with !add <url>")
        return
    for i in range(len(urls)):
        index = i + 1
        text += "**" + str(index) + "** - " + scraping.scrape_title(urls[i]) + "\n"
    await ctx.send(f'Reading List:\n {text}')


@tasks.loop(hours=1)
async def scrape(user):
    await bot.wait_until_ready()
    if urls:
        for i in range(len(urls)):
            url = urls[i]
            con = scraping.scraper(url)
            if con != prev[i]:
                prev[i] = con
                await user.send(f'**:mega: NEW CHAPTER - {scraping.scrape_title(url)} :mega:**\n{user.mention}\n{con}')
            # else:
            #     await user.send(f'No new chapters for {scraping.scrape_title(url)}')


bot.run(os.getenv('BOT_ID'))
