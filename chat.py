import os
from urllib.request import urlopen
from urllib import parse
from bs4 import BeautifulSoup
import re

server = ["루페온", "카제로스", "카마인", "카단", "아브렐슈드", "실리안", "아만", "니나브", "카제", "루페", "실리", "아브", "아브렐"]
ban_list = []
ex = re.compile("[/w/가-힣]")

def get_nick():
    print("채팅 내역으로부터 닉네임 추출중")
    raw = open("KakaoTalkChats.txt", "rt", encoding="UTF-8")
    nick = raw.readlines()
    out = open("./out/nick.txt", "wt", encoding="UTF-8")
    nick = nick[5:]
    nick[0] = nick[0][1:]
    nickname = []
    for i in nick:
        if i[0] == "[":
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
    for i in range(len(nickname)):
        out.write(nickname[i])
        out.write("\n")
        #print(f"{i/len(nickname)*100:.2f}%")
    raw.close()
    out.close()

def check_fow():
    print("닉네임 검사중")
    raw = open("./out/nick.txt", "rt", encoding="UTF-8")
    nick = raw.readlines()
    extra = []
    for i in range(len(nick)):
        nick[i] = ''.join(ex.findall(nick[i]))
        extra.append(nick[i])
    for i in nick:
        for j in server:
            if "/"+j in i:
                n = i[:i.find('/')]
                r = urlopen(f"https://lostark.game.onstove.com/Profile/Character/{parse.quote(n)}")
                p = BeautifulSoup(r, "html.parser")
                n = str(p.select("#lostark-wrapper > div > main > div > div.profile-character-info > span.profile-character-info__name"))[1:]
                if n == "]":
                    #print(f"{i}: 검색안됨")
                    ban_list.append(i + ": 검색안됨")
                    extra.remove(i)
                    break
                s = str(p.select("#lostark-wrapper > div > main > div > div.profile-character-info > span.profile-character-info__server"))[1:]
                d = n[50:n.find(">")-1]
                s = s[53:s.find(">")-1]
                if not j in s:
                    #print(f"{i}: {d}@{s} 불일치")
                    ban_list.append(i + ": 서버 불일치")
                    extra.remove(i)
                    break
                extra.remove(i)
                break
    out = open("./out/extra.txt", "wt", encoding="UTF-8")
    for i in extra:
        out.write(i+"\n")
    raw.close()
    out.close()

def check_back():
    raw = open("./out/extra.txt", "rt", encoding="UTF-8")
    nick = raw.readlines()
    extra = []
    for i in range(len(nick)):
        extra.append(nick[i])
        nick[i] = nick[i].replace(" ","")[:-1]
    for i in nick:
        for j in server:
            if j+"/" in i:
                n = i[i.find('/')+1:]
                t = n.find('/')
                if t != -1:
                    n = n[:t]
                r = urlopen(f"https://lostark.game.onstove.com/Profile/Character/{parse.quote(n)}")
                p = BeautifulSoup(r, "html.parser")
                n = str(p.select("#lostark-wrapper > div > main > div > div.profile-character-info > span.profile-character-info__name"))[1:]
                if n == "]":
                    #print(f"{i}: 검색안됨")
                    ban_list.append(i + ": 검색안됨")
                    extra.remove(i)
                    break
                s = str(p.select("#lostark-wrapper > div > main > div > div.profile-character-info > span.profile-character-info__server"))[1:]
                d = n[50:n.find(">")-1]
                s = s[53:s.find(">")-1]
                if not j in s:
                    #print(f"{i}: {d}@{s} 불일치")
                    ban_list.append(i + ": 서버 불일치")
                    extra.remove(i)
                    break
                extra.remove(i)
                break
    out = open("./out/nick.txt", "wt", encoding="UTF-8")
    ban = open("./out/ban_list.txt", "wt", encoding="UTF-8")
    for i in extra:
        out.write(i+"\n")
    for i in ban_list:
        ban.write(i+"\n")
    raw.close()
    out.close()
    ban.close()
    print("닉네임 양식에 어긋난 유저 리스트가 /out/nick.txt로 생성됨.")
    print("추방 예정자 리스트가 /out/ban_list.txt로 생성됨.")

if __name__ == "__main__":
    print("######################################################")
    print("#                                                    #")
    print("#          로스트아크 채팅방 닉네임 검사기           #")
    print("#                                                    #")
    print("#   Copyright 2021. 행복관NPC all rights reserved.   #")
    print("######################################################\n")
    if not os.path.exists("./out"):
        os.makedirs("./out")
    get_nick()
    check_fow()
    check_back()