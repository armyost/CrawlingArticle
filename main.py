import requests
import os
import telegram
from bs4 import BeautifulSoup
from collections import OrderedDict
from urllib import parse

def Site_ON():
    search = parse.urlparse('https://www.mk.co.kr/news/economy/')
    query=parse.parse_qs(search.query)
    S_query=parse.urlencode(query, encoding='euc-kr', doseq=True)
    url='https://www.mk.co.kr/news/economy/{}'.format(S_query)
    Article_Crawll(url)

def Article_Crawll(url):
    news_link=[]
    response=requests.get(url,verify=False)
    html=response.text
    soup=BeautifulSoup(html,'html.parser')

    for link in soup.find_all('a', href=True):
        notices_link=link['href']
        if '/news/economy/view/' in notices_link:
            news_link.append(notices_link.rstrip())
    news_link=list(OrderedDict.fromkeys(news_link))
    Compare(news_link)

def Compare(news_link):
    BASE_DIR=os.path.dirname(os.path.abspath(__file__))
    temp=[]
    cnt=0
    with open(os.path.join(BASE_DIR,'compare.txt'), 'r') as f_read:
        before=f_read.readlines()
        before=[line.rstrip() for line in before]

        f_read.close()
        for i in news_link:
            if i not in before:
                temp.append(i)
                cnt=cnt+1
                with open(os.path.join(BASE_DIR,'compare.txt'),'a') as f_write:
                    f_write.write(i+'\n')
                    f_write.close()
        if cnt > 0:
            Maintext_Crawll(temp,cnt)

def Maintext_Crawll(temp, cnt):
    bot=telegram.Bot(token='1412399588:AAHvqSrLUTdpwupVSAcFzlMUFKl1bPMBgpE')
    chat_id=bot.getUpdates()[-1].message.chat.id

    NEW = "[+]매일경제 새로운 뉴스는 {}개 입니다.".format(cnt)
    bot.sendMessage(chat_id=chat_id, text=NEW)
    for n in temp:
        Main_URL=n.strip()
        bot.sendMessage(chat_id=chat_id, text=Main_URL)

    response=requests.get(Main_URL)
    html=response.text
    soup=BeautifulSoup(html,'html.parser')
    title=soup.find_all("div",{"id":"news_title02"})
    contents =soup.find_all("div",{"id":"news_util01"})
    photos=soup.find_all("div",{"class":"news_image"})
    for n in contents:
        text=n.text.strip()

if __name__=="__main__":
    Site_ON()