#!/bin/bash/env python

from flask import Flask
from flask import redirect, url_for, render_template

from mxalias import app

@app.route('/v1/alias/edit', method=("GET", "POST"))
def newAlias():
    return render_template('newalias.html'))

@app.route('/v1/alias/mails')
def showAll():
    # list all email alias
    return redirect(url_for('showAll'))
