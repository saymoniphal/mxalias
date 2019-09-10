#!/bin/bash/env python3

from flask import Flask
from flask import flash, redirect, request, url_for, render_template, jsonify
from os import urandom, path
import json
from flask_sqlalchemy import SQLAlchemy


def load_config(config_file, app):
    with open(config_file, 'r') as config:
        configs = json.load(config)

    app.config['SECRET_KEY'] = urandom(16) # app secret key in unicode
    # note: 'config' is an attribute of the Flask object, it's a subclass of Dictionary
    #app.config['SQLALCHEMY_DATABASE_URI'] = configs['db_uri_sqlite']
    app.config['SQLALCHEMY_DATABASE_URI'] = configs['db_uri']
    app.config['HOST'] = configs['host']
    app.config['PORT'] = configs['port']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
    return app


config_file = path.join(path.dirname(path.abspath(__file__)), 'mxalias.config')
app = Flask(__name__, template_folder='templates')
load_config(config_file, app)
sqldb = SQLAlchemy(app)
escapes = ['/', '\'', '\\', '\"', '&']

@app.route('/')
@app.route('/alias')
@app.route('/v1/alias')
def index():
    return redirect(url_for('show_alias')) # look for function show_alias()


@app.route('/v1/alias/show')
def show_alias():
    #return render_template('newalias.html', name='new alias')
    # list of alias in the database
    alias_list = Mxalias.query.all()
    count = len(alias_list)
    return render_template('showalias.html', alias_list=alias_list, count=count)


@app.route('/v1/alias/<string:alias_addr>/<string:forw_addr>/edit', methods=["GET", "POST"])
def edit_alias(alias_addr=None, forw_addr=None):
    mxalias_obj = Mxalias.query.filter_by(alias=alias_addr, forw_addr=forw_addr)
    if request.method == 'POST':
        if request.form['post_action'] == 'edit_alias':
            new_alias = request.form['alias']
            new_forw_addr = request.form['email1']
            if not _valid(new_alias) or not _valid(new_forw_addr):
                return render_template('newalias.html', name='edit_alias',
                                        invalid=True, alias_addr=new_alias, forw_addr=new_forw_addr), 400

            mxalias_obj = Mxalias.query.filter_by(alias=alias_addr, forw_addr=forw_addr).update({'alias': new_alias,
                                                                                                 'forw_addr': new_forw_addr})
            sqldb.session.commit()
        return redirect(url_for('show_alias'))
    else:
        return render_template('newalias.html', name='edit_alias',
                               alias_addr=alias_addr, forw_addr=forw_addr)


@app.route('/v1/alias/new', methods=["GET", "POST"])
def new_alias():
    if request.method == 'POST':
        req_form = request.form
        if req_form['post_action'] == 'save_alias':
            # get alias and all emails
            alias = req_form['alias']
            if not _valid(alias):
                return render_template('newalias.html', name='new_alias',
                                        invalid=True, alias_addr=alias), 400

            counter = req_form['forw_addr_cnt']
            forward_emails = []
            for i in range(1, int(counter)+1):
                email = 'email' + str(i)
                if email in req_form and req_form[email]:
                    forward_emails.append(req_form[email])
            # add to the database
            alias_list = []
            for forw_addr in forward_emails:
                # ensure alias does not exist
                exists = Mxalias.query.filter_by(alias=alias, forw_addr=forw_addr).scalar()
                if exists is not None:
                    return render_template('newalias.html', name='new_alias', exist=True,
                                            alias_addr=alias, forw_addr=forw_addr)

                if not _valid(forw_addr):
                    return render_template('newalias.html', name='new_alias', invalid=True,
                                            alias_addr=alias, forw_addr=forw_addr), 400
                else:
                    alias_obj = Mxalias(alias=alias, forw_addr=forw_addr)
                    alias_list.append(alias_obj)
            sqldb.session.add_all(alias_list)
            sqldb.session.commit()
        return redirect(url_for('show_alias'))
    else: # request.method == 'GET'
        return render_template('newalias.html', name='new_alias')


@app.route('/v1/alias/<string:alias_addr>/<string:forw_addr>/delete', methods=['GET', 'POST'])
def delete_alias(alias_addr=None, forw_addr=None):
    alias_obj = Mxalias.query.filter_by(alias=alias_addr, forw_addr=forw_addr).one()

    if request.method == 'POST':
        if request.form['post_action'] == 'delete_alias':
            sqldb.session.delete(alias_obj)
            sqldb.session.commit()
        return redirect(url_for('show_alias'))
    else:
        return render_template('delete_alias.html', name='delete_alias',
                            alias_addr=alias_addr, forw_addr=forw_addr)



@app.route('/api/v1/alias/<string:alias_addr>')
def alias(alias_addr):
    aliases = Mxalias.query.filter_by(alias=alias_addr)
    return jsonify([alias.serialize for alias in aliases])


def _valid(alias):
    for char in alias:
        if char in escapes:
            return False
    return True


class Mxalias(sqldb.Model):

    __tablename__ = 'mxaliases'
    alias = sqldb.Column(sqldb.String(50), nullable=False, primary_key=True)
    forw_addr = sqldb.Column(sqldb.String(50), nullable=False, primary_key=True)

    def __repr__(self):
        return '<Mxaliases: %s %s>' %(self.alias, self.forw_addr)

    @property
    def serialize(self):
        '''Return object data in easily serialize format'''
        return {
                'alias': self.alias,
                'forw_addr': self.forw_addr
               }
