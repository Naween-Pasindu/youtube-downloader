import eel,json,logging
import libraries.GUID
from gevent import config
from pytube import YouTube
from tkinter import messagebox

eel.init("web")  

logging.basicConfig(filename='error.log', level=logging.DEBUG,format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)

@eel.expose    
def say_hello_py(x):
    print('Hello from %s' % x)

#say_hello_py('Python World!')
#eel.say_hello_js('Python World!')
try:
    config = open('config.json','r')
except FileNotFoundError:
    config = open('config.json','w+')

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
eel.start("index.html",size=(350,600),port=0)