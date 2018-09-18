#!/bin/bash/env python

from flask import Flask
from flask import redirect, url_for, render_template

from mxalias import app

@app.route('/newalias')
def newAlias():
    return redirect(url_for('showAlias'))

@app.route('/mxalias/showalias')
def showAlias():
    return render_template('newalias.html')

def main():
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':
    main()
