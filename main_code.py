import discord, random, os, requests
from discord.ext import commands
description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', description=description, intents=intents)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'We have logged in as {bot.user} (ID: {self.user.id})')
        print("------")
        async def on_member_join(self, member):
            guild = member.guild
            if guild.system_channel is not None:
                to_send = f'Welcome {member.mention} to {guild.name}!'
                await guild.system_channel.send(to_send)

@bot.command()
async def add(ctx, left: int, right: int):
    await ctx.send(left + right)

@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    for i in range(times):
        await ctx.send(content)

@bot.group()
async def cool(ctx):
    """Says if a user is cool.

    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await ctx.send(f'No, {ctx.subcommand_passed} is not cool')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Привет! Я бот {bot.user}!', mention_author=True)

@bot.command()
async def adding(ctx, left: int, right: int):
    await ctx.send(left + right)

@bot.command()
async def help_nature(ctx):
    await ctx.send("Привет! Хочешь помочь сохранить природу? Вот базовые знания о материалах, которые ты используешь в быту!")
    await ctx.send("- Пластик - ты знаком с этим - бутылки, пакеты и т.д., но разлагаеться эта вещь 400-700 лет! Представь, что будет, если 1к людей выкинет пластик в природу!")
    await ctx.send("- Стекло - вторая вещь, которой пользуются многие, окна, например. Разлагается оно больше тысячи лет! Да, стекло вернётся обратно в песок, но всё же..")
    await ctx.send("- Алюминий - банки из под Колы состоят из него, а разлагается - 500 лет. Тоже неприятно ходить по банках спустя 200 лет, не так ли?")
    await ctx.send("- Жесть - нет, это не 18+ сцены с кровью и трупами, это жестянки - консервы и т.д., разложение - до 90 лет")

@bot.command()
async def roll(ctx, dice: str):
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return
    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

@bot.command()
async def HELP(ctx):
    await ctx.send(f"Я умею\r\nadd = считывать два числа\r\nheh = напишу (хех) пять раза, если не задашь другое число\r\nchoose = напиши варианты, между которыми выбрать через запятую, и я рандомно выберу из них\r\nroll = Пока что не реализовано")

@bot.command()
async def heh(ctx, count_heh = 5):
    await ctx.send("he" * count_heh)

@bot.command()
async def choose(ctx, *choices: str):
    await ctx.send(random.choice(choices))

@bot.command()
async def mems(ctx):
    # Список файлов
    img_name = random.choice(os.listdir('images'))
    with open(f'images/{img_name}', 'rb') as f:
        picture = discord.File(f)
    # Отправка файла
    await ctx.send(file=picture)

def get_duck_image_url():    
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']

@bot.command('duck')
async def duck(ctx):
    '''По команде duck вызывает функцию get_duck_image_url'''
    image_url = get_duck_image_url()
    await ctx.send(image_url)

@bot.command()
async def bye(ctx):
    await ctx.send(f'Пока. Приятно было с тобой поговорить', mention_author=True)

intents = discord.Intents.default()
intents.members = True
client = MyClient(intents=intents)
bot.run("key")
