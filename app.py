import eel,json,logging,os,time

from bs4 import BeautifulSoup
from gevent import config
from pytube import YouTube,Playlist
from tkinter import messagebox
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

url=""

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
def search(link):
    global url
    url=link
    print(url)
    displayVideoLinks()

@eel.expose    
def displayVideoLinks():
    if("list" in url):
        p = Playlist(url)
        print('Number Of Videos In playlist: %s' % len(p.video_urls))
    else:
        p = YouTube(url)
    print(2) 
    print(p)
    return
    for video in p.videos:
        print(video)

def getMyMixUrls():
    data=[]
    result = messagebox.askquestion("Allow to open Chrome Window", "New Chrome Window will open on test mode?", icon='warning')
    if result == 'yes':
        #https://stackoverflow.com/questions/63192583/get-youtube-playlist-urls-with-python
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.set_window_size(1024, 600)
        driver.maximize_window()
        driver.get(url)
        time.sleep(2)
        soup=BeautifulSoup(driver.page_source,'html.parser')
        res=soup.find_all('a',{'class':'yt-simple-endpoint style-scope ytd-playlist-panel-video-renderer'})
        for i in res:
            data.append(i.get("href"))
        return data
    else:
        return 0

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