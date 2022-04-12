from cgi import test
from dataclasses import dataclass
from re import I
import eel,json,logging,os,time

from bs4 import BeautifulSoup
from gevent import config
from pytube import YouTube,Playlist
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
            for video in data.videos:
                print(video)
    else:
        check="video"
        #data = [YouTube(url),]
        # for video in data:
        #     streams = set()
        #     for stream in video.streams.filter(type="video"):  # Only look for video streams to avoid None values
        #         streams.add(stream.resolution)
        #     print(streams)
    return check
    
@eel.expose    
def displayVideoLinks(url,check):
    output=""
    if(check=="myMix"):
        data=getMyMixUrls(url)
        for video in data:
            output+="<div class='card mb-2'><div class='card-body'><table style='width: 100%;'><tr><td style='width:30%;'><iframe class='embed-responsive-item'  src='https://www.youtube.com/embed/"+video+"' title='YouTube video player' frameborder='0' allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture' allowfullscreen></iframe></td><td  style='width:40%;'><h5 class='card-title'>Card title</h5></td><td  style='width:30%;'><h6 class='card-subtitle mb-2 text-muted'>Card subtitle</h6></td></tr></table></div></div>"
    elif(check=="playList"):
        pass
    print(output)
    return output
@eel.expose    
def displayVideoDefault():
    pass

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

#say_hello_py('Python World!')
#eel.say_hello_js('Python World!')
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