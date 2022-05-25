



#import dependencies
from flask import Flask

#create a new flask instance
app = Flask(__name__)

#create flask route
@app.route('/')

#create a function called hello_world()
@app.route('/')
def hello_world():
    return 'Hello world'

    