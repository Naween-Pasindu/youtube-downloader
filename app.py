from cgi import test
from dataclasses import dataclass
from re import I
import eel,json,logging,os,time

from bs4 import BeautifulSoup
from gevent import config
from pytube import YouTube,Playlist
from pytube.cli import on_progress
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

eel.init("web") 
logging.basicConfig(filename='error.log', level=logging.DEBUG,format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)

#https://stackoverflow.com/questions/35851281/python-finding-the-users-downloads-folder
def get_download_path():
    """Returns the default downloads path for linux or windows"""
    if os.name == 'nt':
        import winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        return location
    else:
        return os.path.join(os.path.expanduser('~'), 'downloads')

@eel.expose    
def search(url):
    if("list" in url):
        data = Playlist(url)
        if(len(data)==0):
            check="myMix"
            eel.onModel()
        else:
            check="playList"
    else:
        check="video"
    return check
    
@eel.expose    
def displayVideoLinks(url,check):
    output=""
    print(check)
    print(url)
    if(check=="myMix"):
        dataMix=getMyMixUrls(url)
        for video in dataMix:
            data = YouTube("https://www.youtube.com/watch?v="+video)
            qualityList=[]
            output+="<h3>There are "+str(len(dataMix))+" videos.</h3>"
            a=0
            for stream in data.streams.filter(type="video",progressive=True):
                text = stream.mime_type + " " + stream.resolution
                qualityList.append(text)
            for stream in data.streams.filter(only_audio=True):
                text = stream.mime_type + " " + stream.abr
                qualityList.append(text)
            str1 = '-'.join(str(e) for e in qualityList)
            output+="<div class='card mb-2'><div class='card-body'><table style='width: 100%;'><tr><td style='width:30%;'><iframe class='embed-responsive-item'  src='https://www.youtube.com/embed/"+video+"' title='YouTube video player' frameborder='0' allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture' allowfullscreen></iframe></td><td  style='width:50%;'><h5 class='card-title'>"+data.title+"</h5><p><h6>"+data.author+"</h6></p></td><td  style='width:20%;text-align:center;'><h6 class='card-subtitle mb-2 text-muted'><input class='form-check-input' style='height:40px;width:40px' type='checkbox' value='"+video+"' data-quality='"+str1+"' id='flexCheckDefault"+str(a)+"'></h6></td></tr></table></div></div>"
            a+=1
    elif(check=="playList"):
        data = Playlist(url)
        output="<h3>There are "+str(len(data))+" videos.</h3>"
        for video in data.videos:
            a=0
            qualityList=[]
            for stream in video.streams.filter(type="video",progressive=True):
                text = stream.mime_type + " " + stream.resolution
                qualityList.append(text)
            for stream in video.streams.filter(only_audio=True):
                text = stream.mime_type + " " + stream.abr
                qualityList.append(text)
            str1 = '-'.join(str(e) for e in qualityList)
            output+="<div class='card mb-2'><div class='card-body'><table style='width: 100%;'><tr><td style='width:30%;'><iframe class='embed-responsive-item'  src='https://www.youtube.com/embed/"+video.video_id+"' title='YouTube video player' frameborder='0' allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture' allowfullscreen></iframe></td><td  style='width:50%;'><h5 class='card-title'>"+video.title+"</h5><p><h6>"+video.author+"</h6></p></td><td  style='width:20%;text-align:center;'><h6 class='card-subtitle mb-2 text-muted'><input class='form-check-input' style='height:40px;width:40px' type='checkbox' value='"+video.video_id+"' data-quality='"+str1+"' id='flexCheckDefault"+str(a)+"'></h6></td></tr></table></div></div>"
            a+=1
    print(output)
    return output
@eel.expose    
def displayVideoDefault(url,check):
    if(check=="video"):
        data = YouTube(url)
        video= url.strip().split("/")[-1].split("=")[-1]
        output ="<div class='card mb-2'><div class='card-body'><table style='width: 100%;'><tr><td style='width:30%;'><iframe class='embed-responsive-item'  src='https://www.youtube.com/embed/"+video+"' title='YouTube video player' frameborder='0' allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture' allowfullscreen></iframe></td><td  style='width:50%;'><h5 class='card-title'>"+data.title+"</h5><p><h6>"+data.author+"</h6></p></td><td  style='width:20%;'><select id='qualityList' class='form-select form-select-lg mb-3'>"
        qualityList=[]
        for stream in data.streams.filter(type="video",progressive=True):
            text = stream.mime_type + " " + stream.resolution
            size= str(round(stream.filesize/1024/1024,2))+"MB"
            output += "<option value='"+text+"'>"+text+" "+size+"</option>"
        for stream in data.streams.filter(only_audio=True):
            text = stream.mime_type + " " + stream.abr
            size= str(round(stream.filesize/1024/1024,2))+"MB"
            output += "<option value='"+text+"'>"+text+" "+size+"</option>"
        output+="</select><br><button type='button' id='download' class='btn btn-primary btn-download'>Download</button>"
        output +="</td></tr></table></div></div>"
        return output

@eel.expose    
def download(url,quality):
    temp = quality.split(" ")
    mime_type=temp[0]
    resolution=temp[1]
    path=get_download_path()
    for i in url:
        data = YouTube("https://www.youtube.com/watch?v="+i)
        if("audio" in mime_type):
            stream = data.streams.filter(mime_type=mime_type,only_audio=True)
            stream.order_by('abr').desc().first().download(path)
        else:
            stream = data.streams.filter(resolution=resolution,mime_type=mime_type,progressive=True)
            stream.order_by('resolution').desc().first().download(path)
        eel.sendAlert(data.title)

def getMyMixUrls(url):
    data=[]
    #https://stackoverflow.com/questions/63192583/get-youtube-playlist-urls-with-python
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.set_window_size(1024, 600)
    driver.maximize_window()
    driver.get(url)
    time.sleep(2)
    soup=BeautifulSoup(driver.page_source,'html.parser')
    res=soup.find_all('a',{'class':'yt-simple-endpoint style-scope ytd-playlist-panel-video-renderer'})
    for i in res:
        data.append(i.get("href").split("/watch?v=")[1].split("&list=")[0])
    return data

try:
    config = open('config.json','r')
except FileNotFoundError:
    config = open('config.json','w+')
    path = get_download_path()
    path = path.replace("\\","/")
    config.write(json.dumps({'save_dir':path}, sort_keys=False, indent=4))
    config.seek(0)

except Exception  as err:
    logger.error(err)
    messagebox.showwarning("Error", "Program terminating")
    quit()
try:
    jsonData = json.load(config)
except Exception  as err:
    logger.error(err)
    messagebox.showwarning("Error", "database error")
    quit()  

eel.start("index.html",port=0)
config.close()