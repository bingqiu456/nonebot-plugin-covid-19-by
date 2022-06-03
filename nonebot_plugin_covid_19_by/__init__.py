from ast import Not
import random
from loguru import logger
from nonebot.adapters.onebot.v11 import Message,MessageSegment,GroupMessageEvent
from nonebot import on_command
from nonebot.params import CommandArg,ArgPlainText
import httpx,os,aiofiles
from . import config_covid_19
from PIL import Image, ImageFont, ImageDraw
from time import strftime
import os,datetime
config_covid_19


async def json_ge(p):
    return str(str(p).replace("[","").replace("]","").replace("','","").replace(' ',""))

def max(p):
    a = []
    for  i in range(len(p)):
        a.append(len(p[i]))

    a.sort()
    b = int(len(a)-1)
    return a[b]
 
async def CreateImg(text,colour,size):
    if colour is None:
        colour = "#000000"

    if size is None:
        size = 30

    text = str(text)+str("\n\n——————Created By Bingyue——————")
    text = str(text).replace('\n',"\n")
    fontSize = size
    liens = text.split('\n')
    im = Image.new("RGB", ((fontSize *  max(liens)), len(liens) * (fontSize + 3)), (255, 255, 255))
    dr = ImageDraw.Draw(im)
    fontPath = os.path.join(os.path.dirname(__file__),"123.ttf")
    font = ImageFont.truetype(fontPath, fontSize)
    dr.text((0, 0), text, font=font, fill=colour)
    image_time =datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    if os.path.exists("covid_by_19") ==False:
        os.mkdir("covid_by_19")
        im.save('./covid_by_19/'+str(image_time)+'.png')
        return str(image_time)
    else:
        im.save("./covid_by_19/"+str(image_time)+".png")
        return str(image_time)




searchcovid =  on_command('by_covid_19_search')
covid_news = on_command('by_covid_19_news')
covid_19_mulu = on_command("by_covid_19")
ranking_list_jwsr = on_command("by_covid_19_list_jwsr")
details_covid = on_command("by_covid_19_details")
cha_covid = on_command("by_covid_19_cha")

@cha_covid.handle()
async def cha(event:GroupMessageEvent,foo:Message = CommandArg()):
    if  str (event.group_id) in config_covid_19.group_covid:
        try:
            a = str(foo).split(",")
            b = await httpx.AsyncClient().get(f"https://interface.sina.cn/news/ncp/data.d.json?mod=risk_level&areaname={a[0]}|{a[1]}|%E5%85%A8%E9%83%A8",headers={"user-agent":"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36"})
            b = b.json()
            c = [f"————{a[0]}{a[1]}的风险地区————\n"]
            if b["data"]["middleNum"]!=0:
                for i in range(len(b["data"]["middle"])):
                    c.append( str("🍁")+ str(i+1) + str(f',地址:{b["data"]["middle"][i]["area_name"]},具体位置:{b["data"]["middle"][i]["communitys"]}')+"\n" )

            if b["data"]["highNum"] != 0:
                c.append("\n以下是高风险地区\n")
                for i in range(len(b["data"]["high"])):
                    c.append( str("🍁")+ str(i+1) + str(f',地址:{b["data"]["high"][i]["area_name"]},具体位置:{b["data"]["high"][i]["communitys"]}')+"\n" )
        except(httpx.ConnectError,httpx.NetworkError):
            logger.error("covid_19:网络错误")
            await cha_covid.finish()
        except(KeyError):
            d = f"————{a[0]}{a[1]}的风险地区————\n🍁该地区低风险（也有可能是查询错误）"
            logger.success(f"covid_19:获取{a[0]}{a[1]}地区成功")
            if str (event.group_id) in config_covid_19.group_image_covid:
                b =  await CreateImg(text=d,colour=config_covid_19.colour,size=config_covid_19.size)
                a = os.path.join('./',os.getcwd(),'covid_by_19',b+".png")
                print(c)
                await cha_covid.finish(MessageSegment.image(file=str("file:///")+a))
            else:
                print(c)
                await cha_covid.finish(d)
        else:
            logger.success(f"covid_19:获取{a[0]}{a[1]}地区成功")
            if str (event.group_id) in config_covid_19.group_image_covid:
                for i in c:
                    with open("./covid_by_19/3.txt","a",encoding="utf_8") as f:
                        f.write(i)
                        f.close()
        
                with open("./covid_by_19/3.txt","r",encoding="utf_8")as g:
                    l = g.read()                        
                    b = await CreateImg(text=l,colour=config_covid_19.colour,size=config_covid_19.size)
                    a = os.path.join('./',os.getcwd(),'covid_by_19',b+".png")
                    g.close()
                    os.remove("./covid_by_19/3.txt")
                    await cha_covid.finish(MessageSegment.image(file=str("file:///")+a))
            else:
                await cha_covid.finish(c)



@details_covid.handle()
async def details(event:GroupMessageEvent):
    if  str (event.group_id) in config_covid_19.group_covid:
        try:
            a = await httpx.AsyncClient().get(url="https://interface.sina.cn/news/wap/fymap2020_data.d.json",headers={"user-agent":"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36"})
            a = a.json()
            gntotal = a["data"]["gntotal"]
            deathtotal = a["data"]["deathtotal"]
            jwsrNum = a["data"]["jwsrNum"]
            econNum = a["data"]["econNum"]
            time_covid = a["data"]["mtime"]
            curetotal = a["data"]["curetotal"]
        except(httpx.ConnectError,httpx.HTTPError,httpx.NetworkError):
            logger.error("covid_19:网络请求错误")
            await details_covid.finish()
        except(KeyError):
            logger.error("covid_19:获取数据错误 请检查json")
            await details_covid.finish()
        else:
            logger.success("covid_19:获取疫情详情成功")
            if str (event.group_id) in config_covid_19.group_image_covid:
                l = f"——本国疫情详情——\n🍁时间:{time_covid}\n🍁累计确诊:{gntotal}\n🍁累计死亡:{deathtotal}\n🍁境外输入:{jwsrNum}\n🍁现存确诊:{econNum}\n🍁治愈累计:{curetotal}\n【{await covid_txt()}】"
                b = await CreateImg(text=l,colour=config_covid_19.colour,size=config_covid_19.size)
                a = os.path.join('./',os.getcwd(),'covid_by_19',b+".png")
                await details_covid.finish(MessageSegment.image(file=str("file:///")+a))
            else:
                await details_covid.finish(f"——本国疫情详情——\n🍁时间:{time_covid}\n🍁累计确诊:{gntotal}\n🍁累计死亡:{deathtotal}\n🍁境外输入:{jwsrNum}\n🍁现存确诊:{econNum}\n🍁治愈累计:{curetotal}\n【{await covid_txt()}】")
        


async def covid_txt():
    try:
        async with  aiofiles.open(str(os.path.dirname(__file__))+'/covid_19.txt','r',encoding='utf-8') as f:
            o = await f.readlines()
            p = random.randint(0,len(o))
    except (FileNotFoundError):
        pass
    else:
        return o[p].strip("\n")
    

@ranking_list_jwsr.handle()
async def phb(event:GroupMessageEvent):
    if  str (event.group_id) in config_covid_19.group_covid:
        try:
            a = await httpx.AsyncClient().get(url="https://interface.sina.cn/news/wap/fymap2020_data.d.json",headers={"user-agent":"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36"})
            b = a.json()
            c = ["—境外输入排行榜—"]
            for i in range(len(b["data"]["jwsrTop"])):
                c.append("\n"+str(f"🍁{i+1}")+str(b["data"]["jwsrTop"][i]["name"])+str("  ")+str("输入人数:"+b["data"]['jwsrTop'][i]["jwsrNum"]))
        
            c.append(f"\n【{await covid_txt()}】")
        except(httpx.ConnectError,httpx.HTTPError,httpx.NetworkError):
            logger.error("covid_19:网络错误")
            await ranking_list_jwsr.finish()
        except(KeyError):
            logger.error("covid_19:数据解析失败")
            await ranking_list_jwsr.finish()
        else:
            logger.success("covid_19:获取排行榜成功")
            if str (event.group_id) in config_covid_19.group_image_covid:
                for i in c:
                    with open("./covid_by_19/2.txt","a",encoding="utf_8") as f:
                        f.write(i)
                        f.close()
        
                with open("./covid_by_19/2.txt","r",encoding="utf_8")as g:
                    l = g.read()
                    b = await CreateImg(text=l,colour=config_covid_19.colour,size=config_covid_19.size)
                    a = os.path.join('./',os.getcwd(),'covid_by_19',b+".png")
                    g.close()
                    os.remove("./covid_by_19/2.txt")
                    await ranking_list_jwsr.finish(MessageSegment.image(file=str("file:///")+a))
            else:
                await ranking_list_jwsr.finish(c)
            
                
            

@covid_19_mulu.handle()
async def _(event:GroupMessageEvent):
    if  str (event.group_id) in config_covid_19.group_covid:
        l = f"——————疫情小助手——————\n/by_covid_19_search[地区]\n/by_covid_19_news\n/by_covid_19_list_jwsr\n/by_covid_19_details\n/by_covid_19_cha[地区] 如 /by_covid_19_cha广东省,广州市,全部\n/covid_19_by_group_turn_on\n/covid_19_by_group_turn_off\n/covid_19_by_image_turn_on\n/covid_19_by_image_turn_off\n【{await covid_txt()}】"
        if str (event.group_id) in config_covid_19.group_image_covid:
            b =  await CreateImg(text=l,colour=config_covid_19.colour,size=config_covid_19.size)
            a = os.path.join('./',os.getcwd(),'covid_by_19',b+".png")
            await covid_19_mulu.finish(MessageSegment.image(file=str("file:///")+a))
        else:
            await covid_19_mulu.finish(l)
        

@searchcovid.handle()
async def searchcovid_handle (event:GroupMessageEvent,foo: Message = CommandArg()):
    if  str (event.group_id) in config_covid_19.group_covid:
        if str (event.group_id) in config_covid_19.group_image_covid:
            b = await CreateImg(text=await httpx_covid_city(msg=foo),colour=config_covid_19.colour,size=config_covid_19.size)
            a = os.path.join('./',os.getcwd(),'covid_by_19',b+".png")
            await searchcovid.finish(MessageSegment.image(file=str("file:///")+a))
        else:
            await searchcovid.finish(await httpx_covid_city(msg=foo))
    

@covid_news.handle()
async def chachacha(event:GroupMessageEvent):
    if  str (event.group_id) in config_covid_19.group_covid:
        if str (event.group_id) not in config_covid_19.group_image_covid:    
            await covid_news.send(await httpx_covid_news(msg=None))
        else:
             await covid_news.send(MessageSegment.image(file=str("file:///"+await httpx_covid_news(msg=True))))



@covid_news.got("number")
async def news_data(event:GroupMessageEvent,a: str = ArgPlainText("number")):
    if str (event.group_id) not in config_covid_19.group_image_covid: 
        await covid_news.finish(await covid_news_n(number=int(a)))
    else:
        b = await CreateImg(text=await covid_news_n(number=int(a)),colour=config_covid_19.colour,size=config_covid_19.size)
        a = os.path.join('./',os.getcwd(),'covid_by_19',b+".png")
        await covid_news.finish(MessageSegment.image(file=str("file:///")+a))




async def httpx_covid_news(msg):
    try:
        header = {"User-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36"}
        r = await httpx.AsyncClient().get(url='https://interface.sina.cn/app.news/24hours_news.d.json?conf=page&page=1&pageType=kangYiNewsFlash',headers=header)
        r = r.json()
    except(httpx.ConnectError,httpx.HTTPError,httpx.NetworkError):
        return logger.error(f'covid_19:资讯获取失败 网络错误')
    else:
        o = []
        for i in range(len(r["data"]["components"][1]["data"])):
            a = i+1
            o.append(str(a)+","+str(r["data"]["components"][1]["data"][i]["item"]["info"]["showTimeText"])+str('  ')+str(r["data"]["components"][1]["data"][i]["item"]["info"]["title"])+"\n")

    o.append(f"一共查到了{len(o)}条新闻\n想查看请发送序号\n【{await covid_txt()}】")
    logger.success("covid_19:获取新闻成功")
    if msg == None:
        return o
    else:
            for i in o:
                with open("./covid_by_19/1.txt","a",encoding="utf_8") as f:
                    f.write(i)
                    f.close()
        
    with open("./covid_by_19/1.txt","r",encoding="utf_8")as g:
        l = g.read()
        b = await CreateImg(text=l,colour=config_covid_19.colour,size=config_covid_19.size)
        a = os.path.join('./',os.getcwd(),'covid_by_19',b+".png")
        g.close()
        os.remove("./covid_by_19/1.txt")
        return a
        
        

async def covid_news_n(number):
    try:
        header = {"User-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36"}
        r = await httpx.AsyncClient().get(url='https://interface.sina.cn/app.news/24hours_news.d.json?conf=page&page=1&pageType=kangYiNewsFlash',headers=header)
        r = r.json()
        oo =  MessageSegment.image(r["data"]["components"][1]["data"][number-1]["item"]["info"]["mediaInfo"]["avatar"])
        pp =  MessageSegment.text(r["data"]["components"][1]["data"][number-1]["item"]["base"]["base"]["url"])
        ll =  MessageSegment.text(r["data"]["components"][1]["data"][number-1]["item"]["info"]["title"])
    except(KeyError,httpx.NetworkError,httpx.HTTPError):
        return logger.error("covid_19:获取失败")
    else:
        logger.success("covid_19:获取成功")
        return oo+"\n"+ll+"\n"+pp+f"\n【{await covid_txt()}】"
        


async def httpx_covid_city(msg):
    try:
        header = {"User-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36"}
        r = await httpx.AsyncClient().get(url= "https://interface.sina.cn/news/wap/fymap2020_data.d.json",headers=header)
        r = r.json()
        x = r["data"]["list"]
    except(KeyError,httpx.ConnectError,httpx.HTTPError,httpx.NetworkError):
        return logger.error(f'查询{msg}地区出现错误 网络错误')
    else:
        for i in range(len(x)):
            if x[i]["name"] == str(msg):
                logger.success(f"covid_19:{msg}疫情数据成功")
                return f'—{msg}的疫情数据—\n🍁时间:{r["data"]["times"]}\n🍁新增确诊:{x[i]["conadd"]}\n🍁累计确诊:{x[i]["value"]}\n🍁现存确诊:{x[i]["econNum"]}\n🍁死亡人数:{x[i]["deathNum"]}\n🍁治愈人数:{x[i]["cureNum"]}\n🍁境外输入:{x[i]["jwsrNum"]}\n【{await covid_txt()}】'
            else: 
                for o in range(len(r["data"]["list"][i]["city"])-1):
                    if r["data"]["list"][i]["city"][o]["name"]==str(msg):
                        logger.success(f"covid_19:{msg}疫情数据成功")
                        return f'—{msg}的疫情数据—\n🍁时间:{r["data"]["times"]}\n🍁新增确诊:{x[i]["city"][o]["conadd"]}\n🍁累计确诊:{x[i]["city"][o]["conNum"]}\n🍁现存确诊:{x[i]["city"][o]["econNum"]}\n🍁死亡人数:{x[i]["city"][o]["deathNum"]}\n🍁治愈人数:{x[i]["city"][o]["cureNum"]}\n【{await covid_txt()}】'
        for i in range(len(r["data"]["worldlist"])-1):
            if r["data"]["worldlist"][i]["name"]==str(msg):
                logger.success(f"covid_19:{msg}疫情数据成功")
                return f'—{msg}的疫情数据—\n🍁时间:{r["data"]["times"]}\n🍁新增确诊:{r["data"]["worldlist"][i]["conadd"]}\n🍁累计确诊:{r["data"]["worldlist"][i]["value"]}\n🍁现存确诊:{r["data"]["worldlist"][i]["econNum"]}\n🍁死亡人数:{r["data"]["worldlist"][i]["deathNum"]}\n🍁治愈人数:{r["data"]["worldlist"][i]["cureNum"]}\n【{await covid_txt()}】'
        
        return logger.error(f'查询{msg}地区出现错误 数据解析错误')



