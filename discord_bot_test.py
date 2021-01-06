# -*- coding:utf-8 -*- 

import discord, asyncio
from discord.ext import commands
from stopwatch import Stopwatch
from datetime import date

token = "토큰"
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
     !ssh - 서버 연결 방법

     날짜 변경시 자동으로 시간은 초기화 됩니다.

     그럼 모두 즐공!

     깃 저장소는 여기로 -> : https://github.com/vinnyshin/Panopticon.git
     누구나 마음껏 수정하세요!

     gcp기반 서버 오픈했습니다.
     ssh 퍼블릭키 만들어서 주시면 접속할 수 있게 권한 부여하겠습니다.
     ''', color=0x62c1cc)
    
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

@app.command()
async def ssh(ctx):
    strTemp = '''
    __ssh 연결 방법__

    1. 키 값 생성
    윈도우면 cmd, 리눅스, 맥이면 터미널에
    
    ssh-keygen -t rsa -f ~/.ssh/[KEY_FILE_NAME] -C "[USERNAME]"
    Ex) ssh-keygen -t rsa -f ~/.ssh/gcp_key -C "noname@gmail.com"
    
    2. 생성된 [KEY_FILE_NAME].pub 파일을 텍스트 에디터 등을 활용해 내용물을 기록합니다.

    3. 내용물을 관리자에게 전송!

    4. 설정이 완료 되었다면

    ***주의***
    - [KEY_FILE_NAME].pub이 아닌 [KEY_FILE_NAME] 입니다!
    - 35.216.91.122 는 서버 고정 아이피 주소입니다.
    **********

    ssh -i ~/.ssh/[KEY_FILE_NAME] [USERNAME]@35.216.91.122

    를 입력하시고 접속하시면 됩니다!
    '''
    await ctx.send(strTemp)


app.run(token)
