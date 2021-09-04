import os
from urllib.request import urlopen
from urllib import parse
from bs4 import BeautifulSoup
from bs4.element import SoupStrainer
import re

print("######################################################")
print("#                                                    #")
print("#          로스트아크 채팅방 닉네임 검사기           #")
print("#                                                    #")
print("#   Copyright 2021. 행복관NPC all rights reserved.   #")
print("######################################################\n")
if not os.path.exists("./out"):
    os.makedirs("./out")

server = ["루페온", "카제로스", "카마인", "카단", "아브렐슈드", "실리안", "아만", "니나브", "카제", "루페", "실리", "아브", "아브렐"]
ex = re.compile("[a-zA-Z0-9가-힣ㄱ-ㅎㅏ-ㅣ/]")
prod = SoupStrainer("span", {"class": ["profile-character-info__name", "profile-character-info__server"]})

print("채팅 내역으로부터 닉네임 추출중")
raw = open("KakaoTalkChats.txt", "rt", encoding="UTF-8")
nick = raw.readlines()
out = open("./out/nick.txt", "wt", encoding="UTF-8")
nick = nick[5:]
nick[0] = nick[0][1:]
nickname = []
for i in nick:
    if i[0] == "[" and ":" in i:
        i = i[1:i.find("]")]
        if not i in nickname:
            nickname.append(i)
    else: 
        if "님이 들어왔습니다." in i:
            i = i[:-11]
            nickname.append(i)
        elif "님이 나갔습니다." in i:
            i = i[:-10]
            if i in nickname:
                nickname.remove(i)
        elif "님을 내보냈습니다.":
            i = i[:-11]
            if i in nickname:
                nickname.remove(i)
for i in nickname:
    out.write(i)
    out.write("\n")
raw.close()
out.close()

print("닉네임 양식 파싱중")
nick = []
extra = []
for i in nickname:
    i = ''.join(ex.findall(i))
    l = len(nick)
    for j in server:
        if "/"+j in i:
            name = i[:i.find('/')]
            nick.append([i,name,j])
            break
        elif j+"/" in i and not '/' in i[len(j)+1:]:
            idx = i.find('/')
            sv = i[:idx]
            name = i[idx+1:]
            nick.append([i,name,sv])
            break
    if l == len(nick):
        extra.append(i)
out = open("./out/extra.txt", "wt", encoding="UTF-8")
for i in extra:
    out.write(i)
    out.write("\n")
out.close()
for i in range(len(nick)):
    for j in server[:8]:
        if nick[i][2] in j:
            nick[i][2] = j
print("프로그램에서 인식하지 못한 형식의 닉네임의 리스트가 extra.exe로 저장됨.")

print("닉네임 검사중")
ban = []
for i in nick:
    raw_page = urlopen(f"https://lostark.game.onstove.com/Profile/Character/{parse.quote(i[1])}")
    data = str(BeautifulSoup(raw_page, "html.parser", parse_only=prod))
    sv = data[data.find("@")+1:data.find(">@")-1]
    if sv == '':
        ban.append(i[0]+"    :닉네임이 검색되지 않음.")
        print(i[0]+"    :닉네임이 검색되지 않음.")
    else:
        if i[2] != sv:
            ban.append(i[0]+": "+i[1]+"@"+sv+" - 서버 불일치.")
            print(i[0]+": "+i[1]+"@"+sv+" - 서버 불일치.")
out = open("./out/ban.txt", "wt", encoding="UTF-8")
for i in ban:
    out.write(i)
    out.write("\n")
out.close()