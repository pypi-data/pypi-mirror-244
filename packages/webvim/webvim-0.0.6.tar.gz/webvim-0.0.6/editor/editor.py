# -*- coding: utf-8 -*-
import argparse
import base64
import os.path
import sys
from urllib.parse import unquote

from flask import Flask, render_template, request, jsonify
from flask_basicauth import BasicAuth

import version

LOCAL_PORT = 8084
LOCAL_HOST = "0.0.0.0"

DEFAULT_FILE_LIST = [
    "/etc/hosts",
    "/etc/profile",
    os.path.join(os.path.expanduser("~"), ".zshrc"),
    os.path.join(os.path.expanduser("~"), ".ssh", "id_rsa.pub"),
    os.path.join(os.path.expanduser("~"), ".ssh", "authorized_keys"),
    "/opt/homebrew/etc/nginx/nginx.conf",
    "/usr/local/etc/nginx/nginx.conf"
]

file_to_edit = []

app = Flask(__name__)

# basic auth
basic_auth = BasicAuth(app=app)


@app.route('/', methods=["GET"])
def editor():
    """
    web editor online
    """
    key = request.args.get("key")
    path = base64.b64decode(key.encode("utf-8")).decode("utf-8") if key else file_to_edit[0]
    file_obj = get_file_obj(path=path)
    nav_obj = get_nav_obj(path=path)
    return render_template("editor.html", fobj=file_obj, nobj=nav_obj)


@app.route('/save', methods=["POST"])
def save_content():
    code = 1
    message = "Success"
    try:
        content_sec = request.form["content"]
        key = request.form["key"]
        path = base64.b64decode(key.encode("utf-8")).decode("utf-8")
        content = unquote(base64.b64decode(content_sec).decode("utf-8"))
        if path and os.path.exists(path) and os.path.isfile(path):
            with open(path, 'w') as f:
                f.write(content)
    except Exception as e:
        code = 0
        message = str(e)

    data = {
        "code": code,
        "message": message
    }
    return jsonify(data)


# ------------------------------------------------------------

def get_nav_obj(path):
    """
    get nav obj
    """
    navs = []
    for f in file_to_edit:
        file_obj = dict()
        file_obj["fileName"] = os.path.basename(f)
        file_obj["fileKey"] = base64.b64encode(f.encode("utf-8")).decode("utf-8")
        file_obj["fileStatus"] = "active" if path == f else ""
        navs.append(file_obj)
    return navs


def get_file_obj(path):
    """
    get file obj
    """
    file_obj = dict()
    file_obj["filePath"] = path
    file_obj["fileName"] = os.path.basename(path)
    file_obj["fileKey"] = base64.b64encode(path.encode("utf-8")).decode("utf-8")
    with open(path, 'r') as f:
        file_obj["fileContent"] = f.read()
    return file_obj


# ------------------------------------------------------------


def run_web(args):
    """
    run web
    """
    host = args.host
    port = args.port
    files = args.file
    init = args.init
    auth = args.auth
    username = args.username
    password = args.password
    try:
        file_to_edit.clear()
        if init:
            for f in DEFAULT_FILE_LIST:
                files.append(f)
        for f in files:
            if os.path.exists(f) and os.path.isfile(f):
                file_to_edit.append(f)
            else:
                raise FileNotFoundError("File not found")
        # ----------
        if len(file_to_edit) == 0:
            raise ValueError("No file to edit")
        # basic auth
        if auth:
            app.config['BASIC_AUTH_USERNAME'] = username
            app.config['BASIC_AUTH_PASSWORD'] = password
            app.config['BASIC_AUTH_FORCE'] = True
        # run server
        app.run(port=port, host=host, debug=False)
    except ValueError as e:
        print(e)
    except FileNotFoundError as e:
        print(e)


def execute():
    """
    execute
    """
    parser = argparse.ArgumentParser(description='Web Editor {0}'.format(version.VERSION), epilog='make it easy')
    parser.add_argument("--port", type=str, default=LOCAL_PORT,
                        help=u"Local Port [default:{0}]".format(LOCAL_PORT))
    parser.add_argument("--host", type=str, default=LOCAL_HOST,
                        help=u"Local Host [default:{0}]".format(LOCAL_HOST))
    parser.add_argument("--file", action='append', default=[], help='File To Edit')
    parser.add_argument('--init', help='Init Default Files', action='store_true', default=False)
    parser.add_argument('--auth', help='Use Basic Auth', action='store_true', default=False)
    parser.add_argument("--username", type=str, default="admin", help="Basic Auth Username")
    parser.add_argument("--password", type=str, default="admin", help="Basic Auth Password")
    parser.set_defaults(func=run_web)
    # parser args
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    sys.argv.append("--init")
    execute()
