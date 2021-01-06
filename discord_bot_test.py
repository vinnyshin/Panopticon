# -*- coding:utf-8 -*- 

import discord, asyncio
from discord.ext import commands
from stopwatch import Stopwatch
from datetime import date

token = "Nzk2MTkxMTQ1MjQzNzA1Mzg0.X_UUyQ.STt2hovf1_4FZM7iIsE_sAgzev4"
app = commands.Bot(command_prefix='!')
stopwatch_dic = {}
app.remove_command('help')
today = date.today()

def getStudyTime(usrName) :
    duration = stopwatch_dic[usrName].duration

    # 시, 분, 초 각각 얻기
    hour = int(duration / 3600)
    duration = duration - (hour * 3600)
    minute = int(duration / 60)
    duration = duration - (minute * 60)
    sec = int(duration)

    return "{} 님은 지금까지 {}시간 {}분 {}초 공부하셨습니다.".format(usrName, hour, minute, sec)

 # When the bot is ready, execute once.
@app.event
async def on_ready():
    await app.change_presence(status=discord.Status.online, activity=None)
    print('...Logging in...')
    print("name = " + str(app.user.name)) # 봇 이름
    print("id = " + str(app.user.id)) # 봇 고유 ID
    print('Connection was succesful')
     

#todo help 명령어 완성시키기, 돌릴서버 만들기, 날짜 지나면 초기화

@app.command()
async def help(ctx) :
    embed = discord.Embed(title = "Welcome! User :" + str(ctx.author.name))
    await ctx.send(embed = embed)
    embed = discord.Embed(title="순공시간 Documentation",
     description = ''' 
     !빡공시작 - 타이머 시작
     !휴식 - 일시정지 # 따로 정지기능은 구현하지 않았습니다.
     !빡공시간 - 지금까지 공부한 시간 출력
     !시간대결 - 누가 더 열심히 공부했나 대결
     
     날짜 변경시 자동으로 시간은 초기화 됩니다.

     그럼 모두 즐공!
     ''', color=0x62c1cc)
    
    embed.set_footer(text="하단 설명")
    await ctx.send(embed = embed)

@app.command()
async def 빡공시작(ctx):
    # ctx.author.name 은 현재 메세지를 보내고 있는 유저 네임을
    global today
    usrName = ctx.author.name
    embed = discord.Embed(title = usrName + " 빡공시작...." , description = "다른거 하지말고 공부만 열심히! \n" + usrName + " 오늘도 파이팅!")
    
    # 날짜가 변경될 경우
    if(today != date.today()) :
        #초기화
        today = date.today()
        for key in stopwatch_dic :
            stopwatch_dic[key].reset()

    # 유저 네임을 키값으로 하여 Stopwatch 객체 저장..
    if usrName in stopwatch_dic :
        stopwatch_dic[usrName].start()
    else :
        stopwatch_dic[usrName] = Stopwatch()
        stopwatch_dic[usrName].start()    
    
    # discord에 출력..
    await ctx.send(embed = embed)

@app.command()
async def 휴식(ctx):
    usrName = ctx.author.name
    stopwatch_dic[usrName].stop()
    await ctx.send(usrName + " 님 고생하셨습니다.")
    await 빡공시간(ctx)

@app.command()
async def 빡공시간(ctx):
    usrName = ctx.author.name
    await ctx.send(getStudyTime(usrName))

@app.command()
async def 시간대결(ctx):
    temp_string = ""
    for key in stopwatch_dic :
        temp_string += getStudyTime(key) + "\n"
    await ctx.send(temp_string)

app.run(token)
