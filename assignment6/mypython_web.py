from flask import Flask
from flask import render_template
from flask import request
from feedline import *
app = Flask(__name__)
history=list() 
namespace= vars().copy()
@app.route("/")
def startup(): 
    """
    Function that just renders the "homepage"
    """
    return render_template("post.html",buffer="")

@app.route("/handle_input", methods=['POST'])
def handle_input(): 
    """
    Handles input from user in the form.
    Uses the feedline function to execute the commands.
    """
    assert request.method == 'POST' # make sure it's the right method
    input = request.form["input"]   # get the form-input
    a=feedline(input,namespace)     # send to the feedline function
    history.append(input)              # put input into the history list
    if a:                           # if a is not an empty string, append that too.
        history.append(a)
    # render page again. 
    return render_template("post.html",buffer=history)    
if __name__=="__main__":
    app.run()
