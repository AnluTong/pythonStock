# coding=utf-8
import os
from flask import request, g
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from passlib.apps import custom_app_context as pwd_context

from global_var import app, db, expire_time, generate_resp, user_db_name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(64))

    # 加密密码
    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    # 验证密码
    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    # 生成token，并设置过期时间
    def generate_auth_token(self, expiration=expire_time):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    # 验证token的方法
    # 返回 1: token过期或失效  2: token对应用户与global不同   0: 找到用户
    def verify_token(self, token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return 1  # token过期
        except BadSignature:
            return 1  # token无效
        if self.id == data['id']:
            return 0
        else:
            return 2

    # 静态的验证token的方法, 返回对象
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # token过期
        except BadSignature:
            return None  # token无效
        user = User.query.get(data['id'])
        return user


# 创建账号
@app.route('/api/user/register', methods=['POST'])
def register():
    if not request.form:
        return generate_resp('invalid_params')  # 没有参数
    username = request.form.get('name')
    password = request.form.get('psw')
    if username is None or password is None:
        return generate_resp('invalid_params')  # 用户名或者密码为空
    if User.query.filter_by(username=username).first() is not None:
        return generate_resp('already_exist')  # 用户已经存在
    user = User(username=username)
    # 加密密码
    user.hash_password(password)
    # 保存进数据库
    db.session.add(user)
    db.session.commit()

    # 设置token过期时间
    token = user.generate_auth_token()
    # 成功注册后返回用户名和token
    return generate_resp('success', {'name': user.username, 'token': token.decode('ascii')})


# 登录账号
@app.route('/api/user/login', methods=['POST'])
def login():
    if not request.form:
        return generate_resp('invalid_params')  # 没有参数
    username = request.form.get('name')
    password = request.form.get('psw')
    if username is None or password is None:
        return generate_resp('invalid_params')  # 用户名或者密码为空
    user = User.query.filter_by(username=username).first()
    if not user:
        return generate_resp('not_found')  # 用户不存在
    if not user.verify_password(password):
        return generate_resp('failed')  # 密码错误

    # 设置token过期时间
    token = user.generate_auth_token()
    # 成功登录后返回用户名和token
    return generate_resp('success', {'name': user.username, 'token': token.decode('ascii')})


# 登录后（header带token）刷新token
@app.route('/api/user/token', methods=['POST'])
def refresh_token():
    user = verify_token()
    if user:
        # 设置token过期时间
        token = user.generate_auth_token()
        return generate_resp('success', {'token': token.decode('ascii')})
    else:
        return generate_resp('invalid_token')


# 登录后（header带token）获取用户信息
@app.route('/api/user/query', methods=['GET'])
def get_user_info():
    user = verify_token()
    if user:
        # 如果token有效的话就返回username
        return generate_resp('success', {'name': user.username})
    else:
        return generate_resp('invalid_token')


def verify_token():
    if not request.headers or not request.headers.get('token'):
        return None
    token = request.headers.get('token')
    # 验证token
    if hasattr(g, 'user') and g.user:
        res = g.user.verify_token(token)
        if res == 1:
            # token无效
            return None
        elif res == 0:
            # 与缓存的user匹配
            return g.user
    # 从数据库查询
    user = User.verify_auth_token(token)
    if not user:
        return None
    g.user = user
    return user


def init():
    if not os.path.exists(user_db_name):
        db.create_all()
