#!/bin/bash/env python

from flask import Flask
from flask import redirect, url_for, render_template

app = Flask(__name__, template_folder="templates")


@app.route('/')
@app.route('/v1/alias')
def index():
    return redirect(url_for('show_alias')) # looking for a function show_alias() in alias module


def main():
    port_num = 8082
    hostname = '0.0.0.0'
    print("Application running on port %d, host=%s" % (port_num, hostname))
    app.run(host=hostname, port=port_num, debug=True)


if __name__ == '__main__':
    main()
