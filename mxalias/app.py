#!/bin/bash/env python

from flask import Flask
from flask import redirect, url_for, render_template

app = Flask(__name__, template_folder="templates")

@app.route('/')
@app.route('/alias')
def index():
    return redirect(url_for('showAlias'))

@app.route('/alias/showalias')
def showAlias():
    return render_template('newalias.html')

def main():
    portnum = 8082
    hostname = '0.0.0.0'
    print("Application running on port %d, host=%s" %(portnum, hostname))
    app.run(host=hostname, port=portnum, debug=True)

if __name__ == '__main__':
    main()
