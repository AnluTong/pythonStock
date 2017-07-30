# coding=utf-8
import time

from flask import Flask, jsonify
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# 设置密钥
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
# 数据库的配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 数据库初始化
db = SQLAlchemy(app)
# 验证的初始化
auth = HTTPBasicAuth()
expire_time = 24 * 60 * 60
user_db_name = 'user.db'


def generate_resp(code, data=None, message=None):
    res = {'server_time': int(round(time.time() * 1000))}
    if code:
        res['result_code'] = code
    if message:
        res['message'] = message
    if data:
        res['data'] = data
    return jsonify(res)


def run():
    # 如果这个数据库不存在就创建
    app.run(debug=True)
