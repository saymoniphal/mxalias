#!/bin/bash/env python3

from flask import Flask
from flask import flash, redirect, request, url_for, render_template
from os import urandom, path
import json
from flask_sqlalchemy import SQLAlchemy


def load_config(config_file, app):
    with open(config_file, 'r') as config:
        configs = json.load(config)

    app.config['SECRET_KEY'] = urandom(16) # app secret key in unicode
    # note: 'config' is an attribute of the Flask object, it's a subclass of Dictionary
    app.config['SQLALCHEMY_DATABASE_URI'] = configs['db_uri_sqlite']
    app.config['HOST'] = configs['host']
    app.config['PORT'] = configs['port']
    return app 


config_file = path.join(path.dirname(path.abspath(__file__)), 'mxalias.config')
app = Flask(__name__, template_folder='templates')
load_config(config_file, app)
sqldb = SQLAlchemy(app)


@app.route('/')
@app.route('/v1/alias')
def index():
    return redirect(url_for('show_alias')) # look for function show_alias()


@app.route('/v1/alias/show')
def show_alias():
    #return render_template('newalias.html', name='new alias')
    # list of alias in the database
    alias_list = Mxalias.query.all()
    print("Inside show_alias, alias_list: %s" %(alias_list))
    if not alias_list or len(alias_list) == 0:
        return redirect(url_for('new_alias'))
    else:
        return render_template('showalias.html', alias_list=alias_list)


@app.route('/v1/alias/<string:alias_addr>/<string:forw_addr>/edit', methods=["GET", "POST"])
def edit_alias(alias_addr=None, forw_addr=None):
    sess = sqldb.session
    mxalias = Mxalias.query.filter_by(alias=alias_addr, forw_addr=forw_addr)
    if request.method == 'POST':
        flash("Under construction!") 
    else:
        return render_template('newalias.html', name='Edit alias',
                               alias_addr=alias_addr, forw_addr=forw_addr)


@app.route('/v1/alias/new', methods=["GET", "POST"])
def new_alias():
    if request.method == 'POST':
        req_form = request.form
        print(req_form)
        if request.form['post_action'] == 'save_alias':
            # get alias and all emails
            alias = req_form['alias']
            counter = req_form['forw_addr_cnt']
            # emails = request.form['input_emails'].getlist() can't get list of emails
            # print(emails)
            forward_emails = []
            for i in range(1, int(counter)+1):
                email = 'email' + str(i)
                if email in req_form and req_form[email]:
                    forward_emails.append(req_form[email])
            print(forward_emails)
            # add to the database
            for forw_addr in forward_emails:
                alias_obj = Mxalias(alias=alias, forw_addr=forw_addr)
                sqldb.session.add(alias_obj)
                print("Inside for loop: alias: %s, forw_addr: %s" %(alias, forw_addr))
            sqldb.session.commit()
            alias_list = Mxalias.query.all()
            print(alias_list)
            return redirect(url_for('show_alias'))
    else: # request.method == 'GET'
        return render_template('newalias.html', name='New alias')


class Mxalias(sqldb.Model):

    __tablename__ = 'mxaliases'
    alias = sqldb.Column(sqldb.String(50), nullable=False, primary_key=True)
    forw_addr = sqldb.Column(sqldb.String(50), nullable=False, primary_key=True)

    def __repr__(self):
        return '<Mxaliases: %s %s>' %(self.alias, self.forw_addr)

