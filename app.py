import eel,json,logging,os

from gevent import config
from pytube import YouTube
from tkinter import messagebox

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
def say_hello_py(x):
    print('Hello from %s' % x)

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


eel.start("index.html",size=(380,620),port=0)
config.close()