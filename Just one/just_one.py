import asyncio
import discord
import random
from discord import activity
from discord.abc import User
from discord.enums import Status
from discord.ext import commands

token = "ODYxODMyMTY3NDk0NTE2NzM3.YOPhwA.1b1RDdH9v6lcyeC47CeUcrgtptA"
game = discord.Game("현재 대기")
bot = commands.Bot(command_prefix='!',
                   status=discord.Status.online, activity=game)
members = []
round = 13
hints = {}
words = open("C:/Users/byukim/Documents/python/discord_bot/Just one/word_list.txt",
             'r', encoding='UTF-8').read().split('\n')
already = []
guesser = None
main_channel = None
guess = None
start = False

async def start_round(num):
	global hints
	hints = {}
	word = random.choice(words)
	while word in already:
		word = random.choice(words)
	if num >= round:
		return
	guesser = random.choice(members)
	for member in members:
		if member == guesser:
			embed = discord.Embed(title="당신은 이번 라운드의 정답자입니다.",
			                      description="힌트 제공자들이 힌트를 줄 동안 잠시만 기다려주세요~")
		else:
			embed = discord.Embed(title="당신은 이번 라운드의 힌트 제공자입니다.",
			                      description=f"정답자가 제시어를 맞출 수 있도록 힌트 단어를 주세요. 제시어는 {word} 입니다.")
		await member.dm_channel.send(embed=embed)
	while len(hints) < len(members) - 1:
		pass
	embed = discord.Embed(title="모든 힌트가 제시되었습니다.", desciption="정답자는 너도나도 DM으로 정답을 입력해주세요!")
	await main_channel.send(embed=embed)
	start_round(num + 1)
	
async def start_game():
	global start
	start = True
	embed = discord.Embed(title="Just One 게임이 시작되었습니다!",
                       description="사용 방법을 설명드릴게요~")
	embed.add_field(name="힌트 제공자라면,",
	                value="제시어가 주어질 거에요! 정답자가 제시어를 맞출 수 있도록 한 단어짜리 힌트를 주시면 됩니다. 결정적이어도 되지만, 겹친다면 힌트를 보여줄 수 없으니 최대한 겹치지 않도록 주세요!")
	embed.add_field(
		name="정답자라면,", value="힌트 제공자들이 힌트를 비교한 후, 제가 힌트를 전해줄 거에요! 그 때 DM으로 정답으로 생각되는 단어를 적어주시면 됩니다!")
	for member in members:
		if member.dm_channel:
			channel = member.dm_channel
		elif member.dm_channel is None:
			channel = await member.create_dm()
		await channel.send(embed=embed)
	await start_round(0)


@bot.command()
async def 시작(ctx):
    global main_channel
    global can_join
    global start

    main_channel = ctx
    game.name = "게임 진행"
    player = ctx.message.author
    members.append(player)
    start = True
    can_join = True
    embed = discord.Embed(title="Just One에 오신 것을 환영합니다!",
                          desciption="Just One은 정답자에게 겹치지 않는 힌트를 줘야하는 협력 게임입니다. 제시어를 보고 다른 사람들이 적지 않을만한 힌트를 적어주세요!")
    embed.add_field(
        name="참가 방법", value="게임에 참가하고 싶다면 !참가를 입력해주세요.", inline=False)
    await ctx.send(embed=embed)


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
	global round
	# if len(members) < 3:
	# 	await ctx.send("플레이어 수가 2명 이하입니다. 게임을 시작할 수 없습니다.")
	# 	return
	if not round:
		await ctx.send("문제의 개수가 0개입니다. 단어 개수를 설정해주세요.")
		return
	if can_join == True:
		can_join = False
		await ctx.send("참가가 마감되었습니다.")
		await start_game()
	else:
		await ctx.send("현재 진행중인 게임이 없습니다.")


@bot.command()
async def 개수(ctx, number):
    global can_join
    global round
    if can_join:
        round = int(number)
    await ctx.send(f'문제 개수가 {round}로 설정되었습니다.')


@bot.event
async def on_message(message):
	global guesser
	global guess
	global start

	await bot.process_commands(message)
	if message.author.bot:
		return
	if start == True:
		if message.channel.type.name == "private":
			if guesser == message.author:
				guess = message.content
			else:
				hints[message.author] = message.content
				print(hints)
bot.run(token)
