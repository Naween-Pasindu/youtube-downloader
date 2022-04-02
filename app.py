
import eel

from random import randint
  
eel.init("web")  

@eel.expose    
def say_hello_py(x):
    print('Hello from %s' % x)

say_hello_py('Python World!')
eel.say_hello_js('Python World!')
  
# Start the index.html file
eel.start("index.html",size=(350,600),port=0)