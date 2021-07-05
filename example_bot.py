import asyncio, discord
from discord import activity
from discord.abc import User
from discord.enums import Status
from discord.ext import commands

token = "ODYxNDc3NDM3NDkyODIyMDU3.YOKXYg.kN4FyB9Pbw42B694MO9jezDdJ2c"
game = discord.Game("현재 대기")
bot = commands.Bot(command_prefix='!', status=discord.Status.online, activity=game)

start = False
can_join = False
members = []
count = 0
words = {}
async def start_game():
    embed=discord.Embed(title="너도나도 게임이 시작되었습니다!", description="답을 어떻게 제출하면 되는지 설명드릴게요~")
    embed.add_field(name="제출 방법", value=f"본인이 작성하고 싶은 단어를 저에게 DM으로 보내주세요! 단어는 각각 다른 메세지로 보내주셔야 합니다. 총 {count}개의 단어를 제출해주세요!")
    for member in members:
        words[member] = []
        if member.dm_channel:
            channel = member.dm_channel
        elif member.dm_channel is None:                
            channel = await member.create_dm()
        await channel.send(embed=embed)

@bot.command()
async def 시작(ctx):
    global can_join
    game.name = "게임 진행"
    player = ctx.message.author
    members.append(player)
    start = True
    can_join = True
    embed = discord.Embed(title="너도나도에 오신 것을 환영합니다!", desciption="너도나도는 다른 사람들과 비슷한 답을 적어야하는 게임입니다. 게임이 시작할 때 제시어가 주어지면, 남들이 적을법한 단어를 적어주세요! 남들과 똑같은 단어를 적을수록 점수가 높아집니다!")
    embed.add_field(name="참가 방법", value="게임에 참가하고 싶다면 !참가를 입력해주세요.", inline=False)
    await ctx.send(embed=embed)

# @bot.command()
# async def 개수(ctx, number):
#     global can_join
#     global count
#     if can_join:
#         count = number
@bot.command()
async def 참가(ctx):
    global can_join
    if can_join == True:
        player = ctx.message.author
        if player not in members:
            members.append(player)
            await ctx.send("{}님이 참가하셨습니다. 현재 플레이어 {}명".format(player.name, len(members)))
        else:
            await ctx.send("{}님은 이미 참가중입니다.".format(player.name))
    else:
        await ctx.send("참가가 이미 마감되었습니다.")

@bot.command()
async def 마감(ctx):
    global can_join
    if can_join == True:
        can_join = False
        await ctx.send("참가가 마감되었습니다.")
        await start_game()
    else:
        await ctx.send("현재 진행중인 게임이 없습니다.")

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author.bot:
        return
    await message.channel.send("hi!")

bot.run(token)