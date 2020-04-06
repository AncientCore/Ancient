import random
from itertools import cycle

from bs4 import BeautifulSoup
import discord
import requests
from discord.ext import tasks

client = discord.Client()
status = cycle(['내전', '롤 전적 검색', ';도움말'])


@client.event
async def on_ready():
    change_status.start()
    print("Bot is ready")


@tasks.loop(seconds=5)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


@client.event
async def on_message(message):
    if message.content.startswith(";팀나누기"):
        if message.author.voice and message.author.voice.channel:  # 채널에 들어가 있는지 파악
            channel = message.author.voice.channel.members  # 유저 정보 가져오기
            embed = discord.Embed(title="팀을 나눕니다!", color=0xFF99FF)
            embed.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/695953490010439704/696205751206543450/Y2iXpRRkNSnseh3NuL6KUBitJTXrc5K39n9mdWWaLEmad.gif")
            team = message.content[6:]
            teamname = team.split(" ")
            random.shuffle(teamname)
            ch = client.get_channel(690163365837799429)
            ch2 = client.get_channel(690163315657408645)
            for i in range(0, len(channel)):  # 인원수 체크
                embed.add_field(name=channel[i], value=teamname[i], inline=True)  # 팀을 뽑는다.
                if teamname[i] == '1':
                    await channel[i].move_to(ch)
                else:
                    await channel[i].move_to(ch2)
            await message.channel.send(embed=embed)  # 출력
        else:  # 유저가 채널에 없으면
            await message.channel.send("대기실에 있어야 합니다.")  # 출력

    if message.content.startswith(";도움말"):
        embed = discord.Embed(title='명령어', colour=0xFF99FF)
        embed.add_field(name=';전적 [닉넴]', value="[닉넴]님의 롤 전적을 가져옵니다.", inline=False)
        embed.add_field(name=';참가 1', value='수동으로 1팀에 참여합니다.', inline=False)
        embed.add_field(name=';참가 2', value='수동으로 2팀에 참여합니다.', inline=False)
        await message.channel.send(embed=embed)

    if message.content.startswith(";참가 1"):
        ch = client.get_channel(690163365837799429)
        user = message.author
        await user.move_to(ch)

    if message.content.startswith(";참가 2"):
        ch = client.get_channel(690163315657408645)
        user = message.author
        await user.move_to(ch)

    if message.content.startswith(";전적"):
        name = message.content[4:len(message.content)]
        req = requests.get('http://www.op.gg/summoner/userName=' + name)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')

        rank2 = soup.find_all("div", {"class": "TierRank unranked"})  # 랭크 있을시 [] , 랭크 없을시 unranked
        rank3 = soup.find_all("div", {"class": "TierRank"})  # 랭크 있을시 표시 , 없을시 unranked
        if rank2 == rank3:
            rank4 = str(rank2[0])[str(rank2[0]).find('ed">') + 4:str(rank2[0]).find('</div>')]
            rank5 = rank4.strip()
            print(rank5)
        else:
            rank5 = str(rank3[0])[str(rank3[0]).find('nk">') + 4:str(rank3[0]).find('</div>')]

        if rank5 != 'Unranked':
            lp1 = soup.find_all('span', {'class': 'LeaguePoints'})
            lp2 = str(lp1[0])[str(lp1[0]).find('">') + 2:str(lp1[0]).find('</sp')]
            lp3 = lp2.strip()

        lv1 = soup.find_all('span', {'class': 'Level tip'})
        lv2 = str(lv1[0])[str(lv1[0]).find('">') + 2:str(lv1[0]).find('</sp')]
        lv3 = lv2.strip()

        if rank5 != 'Unranked':
            ra1 = soup.find_all('span', {'class': 'ranking'})
            ra2 = str(ra1[0])[str(ra1[0]).find('">') + 2:str(ra1[0]).find('</span>')]

            win1 = soup.find_all('span', {'class': 'WinLose'})
            win2 = str(win1[0])[str(win1[0]).find('ns">') + 4:str(win1[0]).find('</sp')]
            win3 = win2.replace('W', '승')

            lose1 = soup.find_all('span', {'class': 'losses'})
            lose2 = str(lose1[0])[str(lose1[0]).find('es">') + 4:str(lose1[0]).find('</sp')]
            lose3 = lose2.replace('L', '패')

            ratio1 = soup.find_all('span', {'class': 'winratio'})
            ratio2 = str(ratio1[0])[str(ratio1[0]).find('io">') + 4:str(ratio1[0]).find('</sp')]
            ratio3 = ratio2.replace('Win Ratio', '승률')

        embed = discord.Embed(
            title='전적을 검색합니다..',
            description=name,
            colour=0xFF99FF
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/695953490010439704/696218048016678972/R800x0.png")
        if rank5 == 'Unranked':
            embed.add_field(name=name + '의 레벨', value=lv3 + "LV", inline=False)
            embed.add_field(name=name + '의 티어', value=rank5, inline=False)
            embed.add_field(name=name + '님은 언랭-', value="언랭은 더이상의 정보는 제공하지 않습니다.", inline=False)
            await message.channel.send(embed=embed)
        else:
            embed.add_field(name=name + '의 레벨', value=lv3 + "LV (" + ra2 + "등)", inline=False)
            embed.add_field(name=name + '의 티어', value=rank5, inline=False)
            embed.add_field(name=name + '의 LP(점수)', value=lp3, inline=False)
            embed.add_field(name=name + '의 승,패 정보', value=win3 + " " + lose3, inline=False)
            embed.add_field(name=name + '의 승률', value=ratio3, inline=False)
            await message.channel.send(embed=embed)


client.run("NTI2MjU5NDQ0MDI0MzQ0NTc3.Xohalw.FniAZQTIHMnikCgCztYJbuxgfn4")
