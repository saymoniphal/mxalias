#!/bin/bash/env python

from flask import Flask
from flask import request, redirect, url_for, render_template


@app.route("/v1/alias/<int:alias_id>/edit", method=["GET", "POST"])
def edit_alias():
    if request.method == 'POST':
        pass
    else:
        return render_template('newalias.html')


@app.route('/v1/alias/new', method=["POST"])
def new_alias():
    if request.method == 'POST':
        req_form = request.form
        print(req_form)
        if request.form['post_action'] == 'save_alias':
            # get alias and all emails
            alias = request.form['alias']
            # emails = request.form.getlist()['input_emails']
    else: # request.method == 'GET'
        return render_template('newalias.html')


@app.route('/v1/alias/show')
def show_alias():
    # list all email alias
    # add a new a alias for now <-- to be removed -->
    return render_template('newalias.html')